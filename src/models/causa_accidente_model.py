from typing import List, Dict

class CausaAccidenteModel:
    def __init__(self, db):
        self.db = db

    # =====================================================
    # 🔹 CREAR CAUSA (verifica existencia del accidente)
    # =====================================================
    def crear_causa(self, datos: Dict) -> int:
        """
        Registrar una causa asociada a un accidente.
        Verifica si el id_accidente existe antes de guardar.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # 1️⃣ Verificar si el accidente existe
            cursor.execute("SELECT COUNT(*) FROM accidentes WHERE id_accidente = ?", (datos["id_accidente"],))
            existe = cursor.fetchone()[0]

            if existe == 0:
                raise Exception(f"❌ No existe un accidente con ID {datos['id_accidente']}")

            # 2️⃣ Insertar la causa
            sql = """
            INSERT INTO causas (
                id_accidente, tipo_causa, descripcion_causa, factor_principal
            ) VALUES (?, ?, ?, ?)
            """

            cursor.execute(sql, (
                datos["id_accidente"],
                datos.get("tipo_causa"),
                datos.get("descripcion_causa"),
                1 if datos.get("factor_principal", False) else 0
            ))

            conn.commit()
            print(f"✅ Causa registrada para el accidente {datos['id_accidente']}")
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al registrar causa: {str(e)}")

    # =====================================================
    # 🔹 OBTENER CAUSAS POR ACCIDENTE
    # =====================================================
    def obtener_por_accidente(self, id_accidente: int) -> List[Dict]:
        """Obtiene todas las causas asociadas a un accidente."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM causas 
            WHERE id_accidente = ?
            ORDER BY factor_principal DESC, tipo_causa ASC
        """, (id_accidente,))

        causas = cursor.fetchall()
        return [self._dict_from_row(cursor, c) for c in causas]

    # =====================================================
    # 🔹 OBTENER POR ID
    # =====================================================
    def obtener_por_id(self, id_causa: int) -> Dict:
        """Obtiene los datos de una causa específica."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM causas WHERE id_causa = ?", (id_causa,))
        fila = cursor.fetchone()
        return self._dict_from_row(cursor, fila) if fila else {}

    # =====================================================
    # 🔹 ACTUALIZAR CAUSA
    # =====================================================
    def actualizar_causa(self, id_causa: int, datos: Dict) -> bool:
        """Actualizar los datos de una causa existente."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            UPDATE causas SET
                tipo_causa = ?, descripcion_causa = ?, factor_principal = ?
            WHERE id_causa = ?
            """

            cursor.execute(sql, (
                datos.get("tipo_causa"),
                datos.get("descripcion_causa"),
                1 if datos.get("factor_principal", False) else 0,
                id_causa
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar causa: {str(e)}")

    # =====================================================
    # 🔹 ELIMINAR CAUSA
    # =====================================================
    def eliminar_causa(self, id_causa: int) -> bool:
        """Eliminar una causa por su ID."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM causas WHERE id_causa = ?", (id_causa,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar causa: {str(e)}")

    # =====================================================
    # 🔹 UTILIDAD: convertir fila en diccionario
    # =====================================================
    def _dict_from_row(self, cursor, row) -> Dict:
        """Convierte una fila SQLite en un diccionario."""
        if not row:
            return {}
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
