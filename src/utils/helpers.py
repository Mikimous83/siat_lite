from datetime import datetime, timedelta
import os


class Helpers:
    """Clase con funciones auxiliares"""

    @staticmethod
    def formatear_fecha(fecha_str, formato_entrada='%Y-%m-%d', formato_salida='%d/%m/%Y'):
        """Formatea una fecha de un formato a otro"""
        try:
            fecha = datetime.strptime(fecha_str, formato_entrada)
            return fecha.strftime(formato_salida)
        except:
            return fecha_str

    @staticmethod
    def formatear_hora(hora_str, formato_entrada='%H:%M:%S', formato_salida='%H:%M'):
        """Formatea una hora"""
        try:
            if len(hora_str) == 5:  # Ya está en formato HH:MM
                return hora_str
            hora = datetime.strptime(hora_str, formato_entrada)
            return hora.strftime(formato_salida)
        except:
            return hora_str

    @staticmethod
    def calcular_edad(fecha_nacimiento):
        """Calcula la edad a partir de la fecha de nacimiento"""
        try:
            nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            hoy = datetime.now()
            edad = hoy.year - nacimiento.year
            if hoy.month < nacimiento.month or (hoy.month == nacimiento.month and hoy.day < nacimiento.day):
                edad -= 1
            return edad
        except:
            return None

    @staticmethod
    def obtener_mes_nombre(mes_numero):
        """Obtiene el nombre del mes"""
        meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        return meses.get(mes_numero, '')

    @staticmethod
    def obtener_dia_semana(fecha_str):
        """Obtiene el día de la semana"""
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            return dias[fecha.weekday()]
        except:
            return ''

    @staticmethod
    def formatear_numero(numero, decimales=2):
        """Formatea un número con separadores de miles"""
        try:
            return f"{float(numero):,.{decimales}f}".replace(',', ' ')
        except:
            return str(numero)

    @staticmethod
    def truncar_texto(texto, longitud_maxima=50):
        """Trunca un texto si excede la longitud máxima"""
        if not texto:
            return ''
        if len(texto) <= longitud_maxima:
            return texto
        return texto[:longitud_maxima - 3] + '...'

    @staticmethod
    def generar_nombre_archivo(prefijo, extension):
        """Genera un nombre único para un archivo"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefijo}_{timestamp}.{extension}"

    @staticmethod
    def crear_directorio_si_no_existe(ruta):
        """Crea un directorio si no existe"""
        if not os.path.exists(ruta):
            os.makedirs(ruta)
            return True
        return False

    @staticmethod
    def calcular_porcentaje(parte, total):
        """Calcula el porcentaje de una parte respecto al total"""
        try:
            if total == 0:
                return 0
            return round((parte / total) * 100, 2)
        except:
            return 0

    @staticmethod
    def obtener_rango_fechas(tipo='mes'):
        """Obtiene un rango de fechas predefinido"""
        hoy = datetime.now()

        if tipo == 'hoy':
            return hoy.strftime('%Y-%m-%d'), hoy.strftime('%Y-%m-%d')

        elif tipo == 'semana':
            inicio = hoy - timedelta(days=hoy.weekday())
            fin = inicio + timedelta(days=6)
            return inicio.strftime('%Y-%m-%d'), fin.strftime('%Y-%m-%d')

        elif tipo == 'mes':
            inicio = hoy.replace(day=1)
            if hoy.month == 12:
                fin = hoy.replace(day=31)
            else:
                fin = (hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1))
            return inicio.strftime('%Y-%m-%d'), fin.strftime('%Y-%m-%d')

        elif tipo == 'año':
            inicio = hoy.replace(month=1, day=1)
            fin = hoy.replace(month=12, day=31)
            return inicio.strftime('%Y-%m-%d'), fin.strftime('%Y-%m-%d')

        return None, None

    @staticmethod
    def normalizar_texto(texto):
        """Normaliza un texto (mayúsculas, sin espacios extras)"""
        if not texto:
            return ''
        return ' '.join(texto.strip().upper().split())

    @staticmethod
    def es_numero(valor):
        """Verifica si un valor es numérico"""
        try:
            float(valor)
            return True
        except:
            return False

    @staticmethod
    def convertir_a_bool(valor):
        """Convierte un valor a booleano"""
        if isinstance(valor, bool):
            return valor
        if isinstance(valor, str):
            return valor.lower() in ['true', '1', 'si', 'sí', 'yes', 's']
        if isinstance(valor, int):
            return valor == 1
        return False

    @staticmethod
    def formatear_telefono(telefono):
        """Formatea un número de teléfono"""
        if not telefono:
            return ''
        # Eliminar espacios y caracteres no numéricos
        telefono = ''.join(filter(str.isdigit, telefono))

        # Formatear según longitud
        if len(telefono) == 9:  # Celular
            return f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}"
        elif len(telefono) == 7:  # Fijo
            return f"{telefono[:3]}-{telefono[3:]}"

        return telefono

    @staticmethod
    def obtener_iniciales(nombre_completo):
        """Obtiene las iniciales de un nombre"""
        if not nombre_completo:
            return ''
        palabras = nombre_completo.strip().split()
        return ''.join([p[0].upper() for p in palabras if p])

    @staticmethod
    def tiempo_transcurrido(fecha_str, hora_str=None):
        """Calcula el tiempo transcurrido desde una fecha"""
        try:
            if hora_str:
                fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", '%Y-%m-%d %H:%M')
            else:
                fecha_hora = datetime.strptime(fecha_str, '%Y-%m-%d')

            diferencia = datetime.now() - fecha_hora

            if diferencia.days > 365:
                años = diferencia.days // 365
                return f"Hace {años} año{'s' if años > 1 else ''}"
            elif diferencia.days > 30:
                meses = diferencia.days // 30
                return f"Hace {meses} mes{'es' if meses > 1 else ''}"
            elif diferencia.days > 0:
                return f"Hace {diferencia.days} día{'s' if diferencia.days > 1 else ''}"
            elif diferencia.seconds > 3600:
                horas = diferencia.seconds // 3600
                return f"Hace {horas} hora{'s' if horas > 1 else ''}"
            elif diferencia.seconds > 60:
                minutos = diferencia.seconds // 60
                return f"Hace {minutos} minuto{'s' if minutos > 1 else ''}"
            else:
                return "Hace un momento"
        except:
            return ''


"""
utils/constants.py - Constantes del sistema
"""

# Estados de caso
ESTADOS_CASO = [
    'Abierto',
    'En Proceso',
    'Cerrado',
    'Archivado'
]

# Tipos de persona
TIPOS_PERSONA = [
    'Conductor',
    'Pasajero',
    'Peatón',
    'Testigo',
    'Otro'
]

# Estados de salud
ESTADOS_SALUD = [
    'Ileso',
    'Herido Leve',
    'Herido Grave',
    'Crítico',
    'Fallecido'
]

# Condiciones climáticas
CONDICIONES_CLIMATICAS = [
    'Soleado',
    'Nublado',
    'Lluvioso',
    'Neblina',
    'Tormenta',
    'Viento Fuerte'
]

# Iluminación
NIVELES_ILUMINACION = [
    'Día',
    'Noche con iluminación',
    'Noche sin iluminación',
    'Amanecer/Atardecer'
]

# Señalización
ESTADOS_SEÑALIZACION = [
    'Adecuada',
    'Deficiente',
    'Inexistente',
    'En mal estado'
]

# Sexo
SEXOS = ['M', 'F', 'Otro']

# Roles de usuario
ROLES = [
    'Administrador',
    'Operador',
    'Consultor',
    'Inspector'
]

# Formatos de exportación
FORMATOS_EXPORTACION = [
    'PDF',
    'Excel',
    'CSV',
    'JSON'
]

# Colores para gráficos
COLORES_GRAFICOS = {
    'primary': '#2A82DA',
    'success': '#28A745',
    'danger': '#DC3545',
    'warning': '#FFC107',
    'info': '#17A2B8',
    'secondary': '#6C757D'
}

# Mensajes del sistema
MENSAJES = {
    'exito_crear': '✓ Registro creado exitosamente',
    'exito_actualizar': '✓ Registro actualizado exitosamente',
    'exito_eliminar': '✓ Registro eliminado exitosamente',
    'error_crear': '✗ Error al crear el registro',
    'error_actualizar': '✗ Error al actualizar el registro',
    'error_eliminar': '✗ Error al eliminar el registro',
    'confirmar_eliminar': '¿Está seguro de eliminar este registro?',
    'sin_seleccion': 'Debe seleccionar un registro',
    'campos_obligatorios': 'Complete todos los campos obligatorios',
}