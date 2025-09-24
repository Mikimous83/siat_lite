import sqlite3

class AccidenteModel:
    def __init__(self, db):
        self.db = db

    def crear_tabla(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accidentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                hora TEXT,
                distrito TEXT,
                direccion TEXT,
                tipo_accidente TEXT,
                descripcion TEXT
            )
        ''')
        conn.commit()

    def insertar(self, fecha, hora, distrito, direccion, tipo_accidente, descripcion):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accidentes (fecha, hora, distrito, direccion, tipo_accidente, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (fecha, hora, distrito, direccion, tipo_accidente, descripcion))
        conn.commit()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accidentes")
        return cursor.fetchall()

    def eliminar(self, accidente_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accidentes WHERE id = ?", (accidente_id,))
        conn.commit()

    def actualizar(self, accidente_id, fecha, hora, distrito, direccion, tipo_accidente, descripcion):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE accidentes
            SET fecha = ?, hora = ?, distrito = ?, direccion = ?, tipo_accidente = ?, descripcion = ?
            WHERE id = ?
        ''', (fecha, hora, distrito, direccion, tipo_accidente, descripcion, accidente_id))
        conn.commit()

    # ========================
    # MÉTODOS DE REPORTES
    # ========================

    def obtener_accidentes(self, fecha_desde=None, fecha_hasta=None, distrito=None):
        """
        Devuelve todos los accidentes o filtra por fechas/distrito si se pasan parámetros.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM accidentes WHERE 1=1"
        params = []

        if fecha_desde:
            sql += " AND fecha >= ?"
            params.append(fecha_desde)
        if fecha_hasta:
            sql += " AND fecha <= ?"
            params.append(fecha_hasta)
        if distrito:
            sql += " AND distrito = ?"
            params.append(distrito)

        sql += " ORDER BY fecha ASC"

        cursor.execute(sql, params)
        return cursor.fetchall()

    def obtener_estadisticas_por_distrito(self, fecha_desde=None, fecha_hasta=None, distrito=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT distrito, COUNT(*) as total
        FROM accidentes
        WHERE 1=1
        """
        params = []

        if fecha_desde:
            sql += " AND fecha >= ?"
            params.append(fecha_desde)
        if fecha_hasta:
            sql += " AND fecha <= ?"
            params.append(fecha_hasta)
        if distrito:
            sql += " AND distrito = ?"
            params.append(distrito)

        sql += " GROUP BY distrito ORDER BY total DESC"

        cursor.execute(sql, params)
        return cursor.fetchall()

    def obtener_estadisticas_por_tipo(self, fecha_desde=None, fecha_hasta=None, distrito=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT tipo_accidente, COUNT(*) as total
        FROM accidentes
        WHERE 1=1
        """
        params = []

        if fecha_desde:
            sql += " AND fecha >= ?"
            params.append(fecha_desde)
        if fecha_hasta:
            sql += " AND fecha <= ?"
            params.append(fecha_hasta)
        if distrito:
            sql += " AND distrito = ?"
            params.append(distrito)

        sql += " GROUP BY tipo_accidente ORDER BY total DESC"

        cursor.execute(sql, params)
        return cursor.fetchall()

    def obtener_tendencias_temporales(self, fecha_desde=None, fecha_hasta=None, distrito=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT strftime('%Y-%m', fecha) as mes, COUNT(*) as total
        FROM accidentes
        WHERE 1=1
        """
        params = []

        if fecha_desde:
            sql += " AND fecha >= ?"
            params.append(fecha_desde)
        if fecha_hasta:
            sql += " AND fecha <= ?"
            params.append(fecha_hasta)
        if distrito:
            sql += " AND distrito = ?"
            params.append(distrito)

        sql += " GROUP BY mes ORDER BY mes ASC"

        cursor.execute(sql, params)
        return cursor.fetchall()
