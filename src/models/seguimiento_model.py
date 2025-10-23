from typing import List, Dict
from datetime import datetime


class SeguimientoModel:
    def __init__(self, db):
        self.db = db

    # =====================================================
    # 🔹 CREAR SEGUIMIENTO (con validación de accidente)
    # =====================================================
    def crear_seguimiento(self, datos: Dict) -> int:
        """
        Registrar un nuevo seguimiento de un accidente.
        Verifica que el accidente exista antes de guardar.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # 1️⃣ Verificar si el accidente existe
            cursor.execute("SELECT COUNT(*) FROM accidentes WHERE id_accidente = ?", (datos["id_accidente"],))
            existe = cursor.fetchone()[0]

            if existe == 0:
                raise Exception(f"❌ No existe un accidente con ID {datos['id_accidente']}")

            # 2️⃣ Insertar el seguimiento si existe
            sql = """
            INSERT INTO seguimientos (
                id_accidente, fecha_seguimiento, estado_anterior,
                estado_nuevo, observaciones, id_usuario
            ) VALUES (?, ?, ?, ?, ?, ?)
            """

            fecha = datos.get("fecha_seguimiento") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(sql, (
                datos["id_accidente"],
                fecha,
                datos.get("estado_anterior"),
                datos.get("estado_nuevo"),
                datos.get("observaciones"),
                datos.get("id_usuario")
            ))

            conn.commit()
            print(f"✅ Seguimiento registrado correctamente para el accidente {datos['id_accidente']}")
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear seguimiento: {str(e)}")

    # =====================================================
    # 🔹 OBTENER SEGUIMIENTOS POR ACCIDENTE
    # =====================================================
    def obtener_seguimientos_por_accidente(self, id_accidente: int) -> List[Dict]:
        """Obtiene todos los seguimientos registrados para un accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.*, u.nombre AS usuario_nombre, u.apellido AS usuario_apellido
            FROM seguimientos s
            LEFT JOIN usuarios u ON s.id_usuario = u.id_usuario
            WHERE s.id_accidente = ?
            ORDER BY s.fecha_seguimiento DESC
        """, (id_accidente,))

        registros = cursor.fetchall()
        return [self._dict_from_row(cursor, r) for r in registros]

    # =====================================================
    # 🔹 OBTENER ÚLTIMO ESTADO
    # =====================================================
    def obtener_ultimo_estado(self, id_accidente: int) -> Dict:
        """Obtiene el último estado registrado para un accidente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT estado_nuevo, fecha_seguimiento
            FROM seguimientos
            WHERE id_accidente = ?
            ORDER BY fecha_seguimiento DESC
            LIMIT 1
        """, (id_accidente,))

        fila = cursor.fetchone()
        return self._dict_from_row(cursor, fila) if fila else {}

    # =====================================================
    # 🔹 ELIMINAR SEGUIMIENTO
    # =====================================================
    def eliminar_seguimiento(self, id_seguimiento: int) -> bool:
        """Elimina un registro de seguimiento específico"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM seguimientos WHERE id_seguimiento = ?", (id_seguimiento,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar seguimiento: {str(e)}")

    # =====================================================
    # 🔹 UTILIDAD: convertir fila a diccionario
    # =====================================================
    def _dict_from_row(self, cursor, row) -> Dict:
        """Convierte una fila SQLite en un diccionario"""
        if not row:
            return {}
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, row))
