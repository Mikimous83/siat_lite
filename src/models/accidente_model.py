import sqlite3
from datetime import datetime

class AccidenteModel:
    def __init__(self, db: sqlite3.Connection):
        # db es una conexión sqlite3.Connection ya activa
        self.db = db
        self.verificar_tabla()

    # =========================================================
    #  VERIFICACIÓN DE TABLA
    # =========================================================
    def verificar_tabla(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accidentes'")
        existe = cursor.fetchone()
        if not existe:
            print("❌ La tabla 'accidentes' no existe.")
        else:
            print("✅ Tabla 'accidentes' verificada.")

    # =========================================================
    #  CONSULTAS
    # =========================================================
    def obtener_todos(self):
        """Obtiene todos los accidentes con nombres de tipo y gravedad"""
        query = """
        SELECT 
            a.id_accidente,
            a.numero_caso,
            a.fecha,
            a.hora,
            a.lugar,
            IFNULL(t.descripcion, 'Sin tipo') AS tipo_accidente,
            IFNULL(g.nivel, 'Sin dato') AS nivel_gravedad,
            a.heridos,
            a.fallecidos,
            a.estado_caso
        FROM accidentes a
        LEFT JOIN tipos_accidente t ON t.id_tipo = a.id_tipo
        LEFT JOIN niveles_gravedad g ON g.id_gravedad = a.id_gravedad
        ORDER BY a.fecha DESC, a.hora DESC;
        """
        cursor = self.db.cursor()
        cursor.execute(query)
        columnas = [desc[0] for desc in cursor.description]
        registros = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        cursor.close()
        return registros
    # =========================================================
    #  INSERTAR NUEVO REGISTRO
    # =========================================================
    def insertar(self, data):
        """Inserta un nuevo accidente"""
        try:
            cursor = self.db.cursor()
            campos = ", ".join(data.keys())
            valores = tuple(data.values())
            placeholders = ", ".join(["?"] * len(data))
            sql = f"INSERT INTO accidentes ({campos}) VALUES ({placeholders})"
            cursor.execute(sql, valores)
            self.db.commit()
            print("✅ Registro insertado correctamente:", data)
        except Exception as e:
            print("❌ Error al insertar:", e)
            raise

    # =========================================================
    #  ACTUALIZAR REGISTRO
    # =========================================================
    def actualizar(self, id_accidente, data):
        """Actualiza un accidente existente"""
        try:
            cursor = self.db.cursor()
            campos = ", ".join([f"{k}=?" for k in data.keys()])
            valores = tuple(data.values()) + (id_accidente,)
            sql = f"UPDATE accidentes SET {campos} WHERE id_accidente=?"
            cursor.execute(sql, valores)
            self.db.commit()
            print(f"✅ Accidente {id_accidente} actualizado correctamente.")
        except Exception as e:
            print("❌ Error al actualizar:", e)
            raise

    # =========================================================
    #  ELIMINAR REGISTRO
    # =========================================================
    def eliminar(self, id_accidente):
        """Elimina un accidente"""
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM accidentes WHERE id_accidente=?", (id_accidente,))
            self.db.commit()
            print(f"🗑️ Accidente {id_accidente} eliminado correctamente.")
        except Exception as e:
            print("❌ Error al eliminar:", e)
            raise

    # =========================================================
    #  GENERADOR DE NÚMERO DE CASO AUTOMÁTICO
    # =========================================================
    def generar_numero_caso(self):
        """Genera número automático como ACC-2025-001"""
        try:
            year = datetime.now().year
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT numero_caso FROM accidentes WHERE numero_caso LIKE ? ORDER BY id_accidente DESC LIMIT 1",
                (f"ACC-{year}-%",)
            )
            ultimo = cursor.fetchone()

            if ultimo and ultimo[0]:
                try:
                    ultimo_num = int(ultimo[0].split("-")[-1])
                except ValueError:
                    ultimo_num = 0
            else:
                ultimo_num = 0

            nuevo_num = ultimo_num + 1
            return f"ACC-{year}-{nuevo_num:03d}"
        except Exception as e:
            print("❌ Error al generar número de caso:", e)
            return f"ACC-{datetime.now().year}-000"
