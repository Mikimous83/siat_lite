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