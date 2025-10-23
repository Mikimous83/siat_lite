import os
import shutil
import sqlite3
from typing import List, Dict
from datetime import datetime


class DocumentoModel:
    """Modelo para la tabla documentos"""

    def __init__(self, conn: sqlite3.Connection):
        """Recibe una conexión SQLite (desde DataService)"""
        self.conn = conn

        # 📁 Carpeta base: docs/ (al mismo nivel que data/)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.base_path = os.path.join(base_dir, 'docs')
        self._ensure_directories()

    # ------------------------------------------------------
    # 🔧 UTILIDADES
    # ------------------------------------------------------

    def _ensure_directories(self):
        """Crea las subcarpetas dentro de /docs."""
        os.makedirs(self.base_path, exist_ok=True)
        for tipo in ['fotos', 'croquis', 'informes', 'otros']:
            os.makedirs(os.path.join(self.base_path, tipo), exist_ok=True)

    # ------------------------------------------------------
    # 📂 SUBIR DOCUMENTO
    # ------------------------------------------------------

    def subir(self, id_accidente: int, archivo_origen: str, tipo_documento: str, id_usuario: int) -> int:
        """Sube un archivo físico a /docs y lo registra en la base de datos."""
        cursor = self.conn.cursor()

        try:
            # ✅ Nombre único del archivo
            nombre_archivo = os.path.basename(archivo_origen)
            nombre_sin_ext, extension = os.path.splitext(nombre_archivo)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            nombre_unico = f"{id_accidente}_{tipo_documento}_{id_usuario}_{timestamp}{extension}"

            # ✅ Determinar carpeta destino
            carpeta_tipo = tipo_documento.lower()
            if carpeta_tipo not in ['fotos', 'croquis', 'informes']:
                carpeta_tipo = 'otros'

            ruta_destino = os.path.join(self.base_path, carpeta_tipo, nombre_unico)

            # ✅ Copiar archivo
            shutil.copy2(archivo_origen, ruta_destino)

            # ✅ Calcular tamaño y fecha
            tamaño_kb = os.path.getsize(ruta_destino) // 1024
            fecha_subida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # ✅ Insertar en la base de datos
            cursor.execute(
                """
                INSERT INTO documentos (
                    id_accidente, id_tipo_doc, nombre_archivo,
                    ruta_archivo, tamaño_kb, fecha_subida, subido_por
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (id_accidente, None, nombre_unico, ruta_destino, tamaño_kb, fecha_subida, id_usuario),
            )

            self.conn.commit()
            return cursor.lastrowid

        except Exception as e:
            self.conn.rollback()
            if 'ruta_destino' in locals() and os.path.exists(ruta_destino):
                os.remove(ruta_destino)
            raise Exception(f"Error al subir documento: {str(e)}")

    # ------------------------------------------------------
    # 📄 CONSULTAS
    # ------------------------------------------------------

    def listar(self, id_accidente: int | None = None) -> List[Dict]:
        """Obtiene los documentos asociados a un accidente (o todos)."""
        cursor = self.conn.cursor()
        if id_accidente:
            cursor.execute(
                """
                SELECT d.*, u.nombre AS usuario_nombre, u.apellido AS usuario_apellido
                FROM documentos d
                LEFT JOIN usuarios u ON d.subido_por = u.id_usuario
                WHERE d.id_accidente = ?
                ORDER BY d.fecha_subida DESC
                """,
                (id_accidente,),
            )
        else:
            cursor.execute(
                """
                SELECT d.*, u.nombre AS usuario_nombre, u.apellido AS usuario_apellido
                FROM documentos d
                LEFT JOIN usuarios u ON d.subido_por = u.id_usuario
                ORDER BY d.fecha_subida DESC
                """
            )

        filas = cursor.fetchall()
        return [self._dict_from_row(row, cursor) for row in filas]

    def obtener(self, id_documento: int) -> Dict:
        """Obtiene un documento por ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM documentos WHERE id_documento = ?", (id_documento,))
        row = cursor.fetchone()
        return self._dict_from_row(row, cursor) if row else {}

    # ------------------------------------------------------
    # ❌ ELIMINAR
    # ------------------------------------------------------

    def eliminar(self, id_documento: int) -> bool:
        """Elimina un documento físico y su registro."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT ruta_archivo FROM documentos WHERE id_documento = ?", (id_documento,))
        fila = cursor.fetchone()

        if not fila:
            return False

        ruta_archivo = fila[0]

        try:
            cursor.execute("DELETE FROM documentos WHERE id_documento = ?", (id_documento,))
            self.conn.commit()

            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)

            return True
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error al eliminar documento: {str(e)}")

    # ------------------------------------------------------
    # 🔧 Helper
    # ------------------------------------------------------

    def _dict_from_row(self, row, cursor) -> Dict:
        """Convierte una fila en diccionario."""
        if not row:
            return {}
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
