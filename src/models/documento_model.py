from .database_connection import DatabaseConnection
import os
import shutil
from typing import List, Dict, Optional


class DocumentoModel:
    def __init__(self):
        self.db = DatabaseConnection()
        self.base_path = "data/documentos"
        self._ensure_directories()

    def _ensure_directories(self):
        """Crear directorios necesarios"""
        os.makedirs(self.base_path, exist_ok=True)
        for tipo in ['fotos', 'croquis', 'informes', 'otros']:
            os.makedirs(os.path.join(self.base_path, tipo), exist_ok=True)

    def subir_documento(self, id_accidente: int, archivo_origen: str,
                        tipo_documento: str, id_usuario: int) -> int:
        """Subir documento y registrar en BD"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # Generar nombre único
            nombre_archivo = os.path.basename(archivo_origen)
            extension = os.path.splitext(nombre_archivo)[1]
            nombre_unico = f"{id_accidente}_{tipo_documento}_{id_usuario}_{nombre_archivo}"

            # Determinar ruta destino
            ruta_destino = os.path.join(self.base_path, tipo_documento, nombre_unico)

            # Copiar archivo
            shutil.copy2(archivo_origen, ruta_destino)

            # Obtener tamaño
            tamaño_kb = os.path.getsize(ruta_destino) // 1024

            # Registrar en BD
            sql = """
            INSERT INTO documentos (
                id_accidente, tipo_documento, nombre_archivo, 
                ruta_archivo, tamaño_kb, subido_por
            ) VALUES (?, ?, ?, ?, ?, ?)
            """

            cursor.execute(sql, (
                id_accidente, tipo_documento, nombre_unico,
                ruta_destino, tamaño_kb, id_usuario
            ))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            # Eliminar archivo si falló la BD
            if os.path.exists(ruta_destino):
                os.remove(ruta_destino)
            raise Exception(f"Error al subir documento: {str(e)}")

    def obtener_documentos_accidente(self, id_accidente: int) -> List[Dict]:
        """Obtener todos los documentos de un accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT d.*, u.nombre, u.apellido
            FROM documentos d
            LEFT JOIN usuarios u ON d.subido_por = u.id_usuario
            WHERE d.id_accidente = ?
            ORDER BY d.fecha_subida DESC
        """, (id_accidente,))

        documentos = cursor.fetchall()
        return [self._dict_from_row(doc) for doc in documentos]