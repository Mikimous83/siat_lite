from typing import List, Dict


class TipoAccidenteModel:
    def __init__(self, db):
        self.db = db

    # =====================================================
    # 🔹 CREAR NUEVO TIPO DE ACCIDENTE
    # =====================================================
    def crear_tipo(self, datos: Dict) -> int:
        """Crear un nuevo tipo de accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            INSERT INTO tipos_accidente (
                nombre_tipo, descripcion, gravedad_base, activo
            ) VALUES (?, ?, ?, ?)
            """

            cursor.execute(sql, (
                datos["nombre_tipo"],
                datos.get("descripcion"),
                datos.get("gravedad_base"),
                datos.get("activo", True)
            ))

            conn.commit()
            print(f"✅ Tipo de accidente '{datos['nombre_tipo']}' creado correctamente.")
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear tipo de accidente: {str(e)}")

    # =====================================================
    # 🔹 OBTENER TODOS LOS TIPOS
    # =====================================================
    def obtener_todos(self, incluir_inactivos: bool = False) -> List[Dict]:
        """Obtener todos los tipos de accidente (activos por defecto)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM tipos_accidente"
        if not incluir_inactivos:
            sql += " WHERE activo = 1"

        sql += " ORDER BY nombre_tipo ASC"

        cursor.execute(sql)
        tipos = cursor.fetchall()
        return [self._dict_from_row(cursor, t) for t in tipos]

    # =====================================================
    # 🔹 OBTENER POR ID
    # =====================================================
    def obtener_por_id(self, id_tipo: int) -> Dict:
        """Obtener un tipo de accidente por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tipos_accidente WHERE id_tipo = ?", (id_tipo,))
        tipo = cursor.fetchone()
        return self._dict_from_row(cursor, tipo) if tipo else {}

    # =====================================================
    # 🔹 ACTUALIZAR TIPO DE ACCIDENTE
    # =====================================================
    def actualizar_tipo(self, id_tipo: int, datos: Dict) -> bool:
        """Actualizar la información de un tipo de accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            UPDATE tipos_accidente SET
                nombre_tipo = ?, descripcion = ?, gravedad_base = ?, activo = ?
            WHERE id_tipo = ?
            """

            cursor.execute(sql, (
                datos["nombre_tipo"],
                datos.get("descripcion"),
                datos.get("gravedad_base"),
                datos.get("activo", True),
                id_tipo
            ))

            conn.commit()
            actualizado = cursor.rowcount > 0

            if actualizado:
                print(f"📝 Tipo de accidente {id_tipo} actualizado correctamente.")
            else:
                print(f"⚠️ No se encontró el tipo con ID {id_tipo}.")

            return actualizado

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar tipo de accidente: {str(e)}")

    # =====================================================
    # 🔹 CAMBIAR ESTADO (ACTIVO / INACTIVO)
    # =====================================================
    def cambiar_estado(self, id_tipo: int, activo: bool) -> bool:
        """Activar o desactivar un tipo de accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE tipos_accidente
                SET activo = ?
                WHERE id_tipo = ?
            """, (1 if activo else 0, id_tipo))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al cambiar estado: {str(e)}")

    # =====================================================
    # 🔹 ELIMINAR TIPO
    # =====================================================
    def eliminar_tipo(self, id_tipo: int) -> bool:
        """Eliminar un tipo de accidente del registro"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM tipos_accidente WHERE id_tipo = ?", (id_tipo,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar tipo: {str(e)}")

    # =====================================================
    # 🔹 UTILIDAD: convertir fila a diccionario
    # =====================================================
    def _dict_from_row(self, cursor, row) -> Dict:
        """Convierte una fila SQLite en un diccionario"""
        if not row:
            return {}
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
