# =====================================
# controllers/persona_controller.py
# =====================================
from models.persona_model import PersonaModel
from services.validation_service import ValidationService
from ttkbootstrap.dialogs import Messagebox


class PersonaController:
    def __init__(self):
        self.persona_model = PersonaModel()
        self.validation_service = ValidationService()

    def registrar_persona(self, datos_persona):
        """Registrar nueva persona en accidente"""
        try:
            # Validar datos
            errores = self.validation_service.validar_persona(datos_persona)
            if errores:
                return {'success': False, 'errores': errores}

            # Registrar persona
            id_persona = self.persona_model.crear_persona(datos_persona)

            return {
                'success': True,
                'id_persona': id_persona,
                'mensaje': f'Persona registrada con ID: {id_persona}'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'mensaje': 'Error al registrar persona'
            }

    def obtener_personas_accidente(self, id_accidente):
        """Obtener personas de un accidente"""
        try:
            return self.persona_model.obtener_personas_por_accidente(id_accidente)
        except Exception as e:
            print(f"Error al obtener personas: {str(e)}")
            return []

    def buscar_por_dni(self, dni):
        """Buscar persona por DNI"""
        try:
            return self.persona_model.buscar_por_dni(dni)
        except Exception as e:
            print(f"Error en búsqueda por DNI: {str(e)}")
            return []

    def obtener_heridos_fallecidos(self, id_accidente):
        """Obtener solo heridos y fallecidos de un accidente"""
        try:
            heridos = self.persona_model.obtener_personas_por_tipo(id_accidente, 'herido')
            fallecidos = self.persona_model.obtener_personas_por_tipo(id_accidente, 'fallecido')
            return {'heridos': heridos, 'fallecidos': fallecidos}
        except Exception as e:
            print(f"Error al obtener heridos/fallecidos: {str(e)}")
            return {'heridos': [], 'fallecidos': []}


# =====================================
# services/export_service.py
# =====================================
import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


class ExportService:
    def __init__(self):
        self.export_path = "exports"
        self._ensure_export_directory()

    def _ensure_export_directory(self):
        """Crear directorio de exportaciones"""
        os.makedirs(self.export_path, exist_ok=True)

    def exportar_excel(self, datos, nombre_archivo, titulo_hoja="Datos"):
        """Exportar datos a Excel"""
        try:
            # Generar nombre único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_completo = f"{nombre_archivo}_{timestamp}.xlsx"
            ruta_archivo = os.path.join(self.export_path, nombre_completo)

            # Crear DataFrame
            df = pd.DataFrame(datos)

            # Exportar a Excel con formato
            with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=titulo_hoja, index=False)

                # Obtener workbook y worksheet para formato
                workbook = writer.book
                worksheet = writer.sheets[titulo_hoja]

                # Ajustar ancho de columnas
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2) * 1.2
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

            return ruta_archivo

        except Exception as e:
            raise Exception(f"Error al exportar Excel: {str(e)}")

    def exportar_csv(self, datos, nombre_archivo):
        """Exportar datos a CSV"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_completo = f"{nombre_archivo}_{timestamp}.csv"
            ruta_archivo = os.path.join(self.export_path, nombre_completo)

            df = pd.DataFrame(datos)
            df.to_csv(ruta_archivo, index=False, encoding='utf-8')

            return ruta_archivo

        except Exception as e:
            raise Exception(f"Error al exportar CSV: {str(e)}")

    def generar_reporte_pdf(self, nombre_archivo, titulo):
        """Generar reporte en PDF"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_completo = f"{nombre_archivo}_{timestamp}.pdf"
            ruta_archivo = os.path.join(self.export_path, nombre_completo)

            # Crear documento PDF
            doc = SimpleDocTemplate(ruta_archivo, pagesize=A4)
            story = []

            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Centrado
            )

            # Título
            story.append(Paragraph(titulo, title_style))
            story.append(Spacer(1, 12))

            # Fecha de generación
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            story.append(Paragraph(f"Generado el: {fecha_actual}", styles['Normal']))
            story.append(Spacer(1, 20))

            # Construir PDF
            doc.build(story)

            return ruta_archivo

        except Exception as e:
            raise Exception(f"Error al generar PDF: {str(e)}")


# =====================================
# services/file_service.py
# =====================================
import os
import shutil
from datetime import datetime
from PIL import Image
import hashlib


class FileService:
    def __init__(self):
        self.base_path = "data/archivos"
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt'],
            'spreadsheets': ['.xls', '.xlsx', '.csv']
        }
        self._ensure_directories()

    def _ensure_directories(self):
        """Crear directorios necesarios"""
        directories = ['images', 'documents', 'spreadsheets', 'temp']
        for directory in directories:
            path = os.path.join(self.base_path, directory)
            os.makedirs(path, exist_ok=True)

    def subir_archivo(self, archivo_origen, tipo_archivo, id_accidente=None):
        """Subir archivo al sistema"""
        try:
            # Validar archivo
            if not self._validar_archivo(archivo_origen, tipo_archivo):
                raise Exception("Archivo no válido")

            # Generar nombre único
            nombre_unico = self._generar_nombre_unico(archivo_origen, id_accidente)

            # Determinar ruta destino
            ruta_destino = os.path.join(self.base_path, tipo_archivo, nombre_unico)

            # Copiar archivo
            shutil.copy2(archivo_origen, ruta_destino)

            # Optimizar si es imagen
            if tipo_archivo == 'images':
                self._optimizar_imagen(ruta_destino)

            return {
                'success': True,
                'ruta_archivo': ruta_destino,
                'nombre_archivo': nombre_unico,
                'tamaño_bytes': os.path.getsize(ruta_destino)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _validar_archivo(self, archivo, tipo_archivo):
        """Validar archivo antes de subir"""
        # Verificar que existe
        if not os.path.exists(archivo):
            return False

        # Verificar tamaño
        if os.path.getsize(archivo) > self.max_file_size:
            return False

        # Verificar extensión
        extension = os.path.splitext(archivo)[1].lower()
        if extension not in self.allowed_extensions.get(tipo_archivo, []):
            return False

        return True

    def _generar_nombre_unico(self, archivo_origen, id_accidente=None):
        """Generar nombre único para archivo"""
        nombre_base = os.path.basename(archivo_origen)
        nombre, extension = os.path.splitext(nombre_base)

        # Crear hash único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        contenido = f"{nombre}{timestamp}{id_accidente or ''}"
        hash_unico = hashlib.md5(contenido.encode()).hexdigest()[:8]

        return f"{nombre}_{timestamp}_{hash_unico}{extension}"

    def _optimizar_imagen(self, ruta_imagen):
        """Optimizar imagen para reducir tamaño"""
        try:
            with Image.open(ruta_imagen) as img:
                # Redimensionar si es muy grande
                if img.width > 1920 or img.height > 1080:
                    img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)

                # Guardar optimizada
                img.save(ruta_imagen, optimize=True, quality=85)

        except Exception as e:
            print(f"Error optimizando imagen: {str(e)}")


# =====================================
# services/notification_service.py
# =====================================
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class NotificationService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_usuario = ""  # Configurar
        self.email_password = ""  # Configurar

    def enviar_notificacion_accidente_grave(self, datos_accidente, destinatarios):
        """Enviar notificación de accidente grave"""
        try:
            if datos_accidente.get('gravedad') in ['Muy Grave', 'Fatal']:
                mensaje = self._crear_mensaje_accidente_grave(datos_accidente)
                self._enviar_email(destinatarios, "ALERTA: Accidente Grave Registrado", mensaje)

        except Exception as e:
            print(f"Error al enviar notificación: {str(e)}")

    def _crear_mensaje_accidente_grave(self, datos):
        """Crear mensaje para accidente grave"""
        mensaje = f"""
        ALERTA DE ACCIDENTE GRAVE

        Número de Caso: {datos.get('numero_caso', 'N/A')}
        Fecha: {datos.get('fecha', 'N/A')} {datos.get('hora', 'N/A')}
        Lugar: {datos.get('lugar', 'N/A')}
        Tipo: {datos.get('tipo_accidente', 'N/A')}
        Gravedad: {datos.get('gravedad', 'N/A')}

        Heridos: {datos.get('heridos', 0)}
        Fallecidos: {datos.get('fallecidos', 0)}

        Este es un mensaje automático del sistema SIAT-Lite.
        """
        return mensaje

    def _enviar_email(self, destinatarios, asunto, mensaje):
        """Enviar email"""
        if not self.email_usuario or not self.email_password:
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_usuario
            msg['To'] = ', '.join(destinatarios)
            msg['Subject'] = asunto

            msg.attach(MIMEText(mensaje, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_usuario, self.email_password)
            server.sendmail(self.email_usuario, destinatarios, msg.as_string())
            server.quit()

        except Exception as e:
            print(f"Error enviando email: {str(e)}")


# =====================================
# utils/config.py
# =====================================
import os
from typing import Dict, Any


class Config:
    """Clase de configuración centralizada"""

    def __init__(self):
        self.config_data = self._load_default_config()

    def _load_default_config(self) -> Dict[str, Any]:
        """Cargar configuración por defecto"""
        return {
            # Base de datos
            'database': {
                'name': 'siat_lite.db',
                'path': 'data',
                'backup_enabled': True,
                'backup_interval_hours': 24
            },

            # Interfaz
            'ui': {
                'theme': 'superhero',
                'window_size': '1200x800',
                'font_family': 'Arial',
                'font_size': 10
            },

            # Archivos
            'files': {
                'max_size_mb': 10,
                'allowed_image_formats': ['.jpg', '.jpeg', '.png', '.gif'],
                'allowed_doc_formats': ['.pdf', '.doc', '.docx', '.txt'],
                'upload_path': 'data/uploads'
            },

            # Notificaciones
            'notifications': {
                'email_enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': '',
                'sender_password': ''
            },

            # Seguridad
            'security': {
                'session_timeout_minutes': 120,
                'password_min_length': 6,
                'max_login_attempts': 3,
                'require_password_change': False
            }
        }

    def get(self, key_path: str, default=None):
        """Obtener valor usando notación de punto"""
        keys = key_path.split('.')
        value = self.config_data

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value):
        """Establecer valor de configuración"""
        keys = key_path.split('.')
        config = self.config_data

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value


# Instancia global
config = Config()

# =====================================
# utils/constants.py
# =====================================
"""
Constantes del sistema SIAT-Lite
"""

# Tipos de accidente
TIPOS_ACCIDENTE = [
    "Colisión frontal",
    "Colisión lateral",
    "Colisión trasera",
    "Atropello",
    "Volcadura",
    "Despiste",
    "Choque contra objeto fijo",
    "Caída de vehículo",
    "Incendio",
    "Otro"
]

# Niveles de gravedad
NIVELES_GRAVEDAD = [
    "Leve",
    "Grave",
    "Muy Grave",
    "Fatal"
]

# Tipos de vehículo
TIPOS_VEHICULO = [
    "Automóvil",
    "Camioneta",
    "Camión",
    "Ómnibus",
    "Microbus",
    "Motocicleta",
    "Mototaxi",
    "Bicicleta",
    "Vehículo de carga",
    "Vehículo especial",
    "Otro"
]

# Estados de vehículo
ESTADOS_VEHICULO = [
    "Sin daños",
    "Daños leves",
    "Daños graves",
    "Pérdida total",
    "Incendiado"
]

# Condiciones climáticas
CONDICIONES_CLIMATICAS = [
    "Despejado",
    "Nublado",
    "Lluvia ligera",
    "Lluvia intensa",
    "Neblina",
    "Viento fuerte",
    "Otro"
]

# Estados de vía
ESTADOS_VIA = [
    "Bueno",
    "Regular",
    "Malo",
    "Muy malo",
    "En construcción",
    "Mojado",
    "Con baches",
    "Otro"
]

# Tipos de persona
TIPOS_PERSONA = [
    "conductor",
    "pasajero",
    "peatón",
    "herido",
    "fallecido",
    "testigo"
]

# Distritos de Trujillo
DISTRITOS_TRUJILLO = [
    "Trujillo",
    "El Porvenir",
    "Florencia de Mora",
    "Huanchaco",
    "La Esperanza",
    "Laredo",
    "Moche",
    "Poroto",
    "Salaverry",
    "Simbal",
    "Víctor Larco Herrera"
]

# =====================================
# utils/helpers.py
# =====================================
import re
from datetime import datetime
from typing import Optional, Dict


def validar_dni(dni: str) -> bool:
    """Validar DNI peruano (8 dígitos)"""
    if not dni:
        return False
    return bool(re.match(r'^\d{8}$', dni))


def validar_placa_vehicular(placa: str) -> bool:
    """Validar placa vehicular peruana"""
    if not placa:
        return False

    # Formato antiguo: ABC-123
    formato_antiguo = r'^[A-Z]{3}-\d{3}$'
    # Formato nuevo: ABC-123A o ABC-1234
    formato_nuevo = r'^[A-Z]{3}-\d{3}[A-Z]$|^[A-Z]{3}-\d{4}$'

    placa_upper = placa.upper()
    return bool(re.match(formato_antiguo, placa_upper) or re.match(formato_nuevo, placa_upper))


def validar_email(email: str) -> bool:
    """Validar formato de email"""
    if not email:
        return False

    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))


def validar_telefono(telefono: str) -> bool:
    """Validar teléfono peruano"""
    if not telefono:
        return False

    # Celular: 9XXXXXXXX, Fijo: XXXXXXX
    patron = r'^(9\d{8}|\d{7})$'
    return bool(re.match(patron, telefono.replace(' ', '').replace('-', '')))


def formatear_numero_caso(id_accidente: int, año: Optional[int] = None) -> str:
    """Formatear número de caso"""
    if año is None:
        año = datetime.now().year

    return f"ACC-{año}-{id_accidente:06d}"


def limpiar_texto(texto: str) -> str:
    """Limpiar texto removiendo caracteres especiales"""
    if not texto:
        return ""

    # Remover espacios extra
    texto = ' '.join(texto.split())
    return texto.title()


# =====================================
# views/persona_form_view.py
# =====================================
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from utils.constants import TIPOS_PERSONA


class PersonaFormView:
    def __init__(self, parent, controller, id_accidente):
        self.controller = controller
        self.id_accidente = id_accidente
        self.window = ttk.Toplevel(parent)
        self.window.title("Registro de Personas Involucradas")
        self.window.geometry("800x600")
        self.setup_ui()

    def setup_ui(self):
        """Configurar interfaz"""
        # Notebook para diferentes tipos
        self.notebook = ttk.Notebook(self.window, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Pestaña heridos
        self.setup_heridos()

        # Pestaña fallecidos
        self.setup_fallecidos()

        # Pestaña testigos
        self.setup_testigos()

        # Botones
        self.setup_botones()

    def setup_heridos(self):
        """Pestaña de heridos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🚑 Heridos")

        # Formulario herido
        form_frame = ttk.LabelFrame(frame, text="Datos del Herido")
        form_frame.pack(fill=X, padx=10, pady=10)

        # Nombre
        ttk.Label(form_frame, text="Nombre:").pack(anchor=W, padx=10, pady=5)
        self.herido_nombre = ttk.Entry(form_frame)
        self.herido_nombre.pack(fill=X, padx=10, pady=(0, 10))

        # Apellido
        ttk.Label(form_frame, text="Apellido:").pack(anchor=W, padx=10, pady=5)
        self.herido_apellido = ttk.Entry(form_frame)
        self.herido_apellido.pack(fill=X, padx=10, pady=(0, 10))

        # DNI
        ttk.Label(form_frame, text="DNI:").pack(anchor=W, padx=10, pady=5)
        self.herido_dni = ttk.Entry(form_frame)
        self.herido_dni.pack(fill=X, padx=10, pady=(0, 10))

        # Edad
        ttk.Label(form_frame, text="Edad:").pack(anchor=W, padx=10, pady=5)
        self.herido_edad = ttk.Spinbox(form_frame, from_=0, to=120)
        self.herido_edad.pack(fill=X, padx=10, pady=(0, 10))

        # Hospital
        ttk.Label(form_frame, text="Hospital de Traslado:").pack(anchor=W, padx=10, pady=5)
        self.herido_hospital = ttk.Entry(form_frame)
        self.herido_hospital.pack(fill=X, padx=10, pady=(0, 10))

        # Lesiones
        ttk.Label(form_frame, text="Descripción de Lesiones:").pack(anchor=W, padx=10, pady=5)
        self.herido_lesiones = ttk.Text(form_frame, height=4)
        self.herido_lesiones.pack(fill=X, padx=10, pady=(0, 10))

        # Botón agregar herido
        ttk.Button(form_frame, text="➕ Agregar Herido",
                   bootstyle="warning", command=self.agregar_herido).pack(pady=10)

    def setup_fallecidos(self):
        """Pestaña de fallecidos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💀 Fallecidos")

        # Similar estructura para fallecidos
        form_frame = ttk.LabelFrame(frame, text="Datos del Fallecido")
        form_frame.pack(fill=X, padx=10, pady=10)

        ttk.Label(form_frame, text="Nombre:").pack(anchor=W, padx=10, pady=5)
        self.fallecido_nombre = ttk.Entry(form_frame)
        self.fallecido_nombre.pack(fill=X, padx=10, pady=(0, 10))

        ttk.Label(form_frame, text="Apellido:").pack(anchor=W, padx=10, pady=5)
        self.fallecido_apellido = ttk.Entry(form_frame)
        self.fallecido_apellido.pack(fill=X, padx=10, pady=(0, 10))

        ttk.Label(form_frame, text="DNI:").pack(anchor=W, padx=10, pady=5)
        self.fallecido_dni = ttk.Entry(form_frame)
        self.fallecido_dni.pack(fill=X, padx=10, pady=(0, 10))

        ttk.Button(form_frame, text="➕ Agregar Fallecido",
                   bootstyle="danger", command=self.agregar_fallecido).pack(pady=10)

    def setup_testigos(self):
        """Pestaña de testigos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👁️ Testigos")

        form_frame = ttk.LabelFrame(frame, text="Datos del Testigo")
        form_frame.pack(fill=X, padx=10, pady=10)

        ttk.Label(form_frame, text="Nombre Completo:").pack(anchor=W, padx=10, pady=5)
        self.testigo_nombre = ttk.Entry(form_frame)
        self.testigo_nombre.pack(fill=X, padx=10, pady=(0, 10))

        ttk.Label(form_frame, text="Teléfono:").pack(anchor=W, padx=10, pady=5)
        self.testigo_telefono = ttk.Entry(form_frame)
        self.testigo_telefono.pack(fill=X, padx=10, pady=(0, 10))

        ttk.Button(form_frame, text="➕ Agregar Testigo",
                   bootstyle="info", command=self.agregar_testigo).pack(pady=10)

    def setup_botones(self):
        """Botones de acción"""
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=X, padx=10, pady=10)

        ttk.Button(button_frame, text="💾 Guardar Todo",
                   bootstyle="success", command=self.guardar_personas).pack(side=RIGHT, padx=5)
        ttk.Button(button_frame, text="❌ Cancelar",
                   bootstyle="danger-outline", command=self.window.destroy).pack(side=RIGHT, padx=5)

    def agregar_herido(self):
        """Agregar herido a la lista"""
        datos = {
            'id_accidente': self.id_accidente,
            'tipo_persona': 'herido',
            'nombre': self.herido_nombre.get(),
            'apellido': self.herido_apellido.get(),
            'dni': self.herido_dni.get(),
            'edad': self.herido_edad.get(),
            'hospital_traslado': self.herido_hospital.get(),
            'lesiones_descripcion': self.herido_lesiones.get("1.0", END)
        }

        resultado = self.controller.registrar_persona(datos)
        if resultado['success']:
            Messagebox.show_info("Éxito", "Herido registrado correctamente")
            self.limpiar_herido()
        else:
            Messagebox.show_error("Error", resultado['mensaje'])

    def agregar_fallecido(self):
        """Agregar fallecido"""
        datos = {
            'id_accidente': self.id_accidente,
            'tipo_persona': 'fallecido',
            'nombre': self.fallecido_nombre.get(),
            'apellido': self.fallecido_apellido.get(),
            'dni': self.fallecido_dni.get()
        }

        resultado = self.controller.registrar_persona(datos)
        if resultado['success']:
            Messagebox.show_info("Éxito", "Fallecido registrado correctamente")
            self.limpiar_fallecido()
        else:
            Messagebox.show_error("Error", resultado['mensaje'])

    def agregar_testigo(self):
        """Agregar testigo"""
        datos = {
            'id_accidente': self.id_accidente,
            'tipo_persona': 'testigo',
            'nombre': self.testigo_nombre.get(),
            'telefono': self.testigo_telefono.get()
        }

        resultado = self.controller.registrar_persona(datos)
        if resultado['success']:
            Messagebox.show_info("Éxito", "Testigo registrado correctamente")
            self.limpiar_testigo()
        else:
            Messagebox.show_error("Error", resultado['mensaje'])

    def limpiar_herido(self):
        """Limpiar campos de herido"""
        self.herido_nombre.delete(0, END)
        self.herido_apellido.delete(0, END)
        self.herido_dni.delete(0, END)
        self.herido_edad.delete(0, END)
        self.herido_hospital.delete(0, END)
        self.herido_lesiones.delete("1.0", END)

    def limpiar_fallecido(self):
        """Limpiar campos de fallecido"""
        self.fallecido_nombre.delete(0, END)
        self.fallecido_apellido.delete(0, END)
        self.fallecido_dni.delete(0, END)

    def limpiar_testigo(self):
        """Limpiar campos de testigo"""
        self.testigo_nombre.delete(0, END)
        self.testigo_telefono.delete(0, END)

    def guardar_personas(self):
        """Acción al guardar todo (placeholder para expansión futura)"""
        Messagebox.show_info("Guardar", "Se han guardado todas las personas registradas.")
        self.window.destroy()
