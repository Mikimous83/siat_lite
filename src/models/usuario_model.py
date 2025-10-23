import sqlite3
from hashlib import sha256
from datetime import datetime, timedelta


class UsuarioModel:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    # =====================================================
    # 👤 USUARIOS
    # =====================================================
    def crear_usuario(self, nombre, apellido, email, password, id_rol=None):
        password_hash = sha256(password.encode()).hexdigest()
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO usuarios (nombre, apellido, email, password_hash, id_rol, activo)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (nombre, apellido, email.lower(), password_hash, id_rol))
            return cur.lastrowid

    def obtener_rol_usuario(self, id_usuario):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT r.nombre_rol
                FROM usuarios u
                LEFT JOIN roles r ON u.id_rol = r.id_rol
                WHERE u.id_usuario = ?
            """, (id_usuario,))
            row = cur.fetchone()
            return row[0] if row else None

    def activar_usuario(self, email: str):
        with self._conn() as conn:
            conn.execute("UPDATE usuarios SET activo = 1 WHERE LOWER(email) = ?", (email.lower(),))

    def verificar_credenciales(self, email: str, password: str):
        h = sha256(password.encode()).hexdigest()
        print("🧩 Verificando usuario:", email)
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_usuario, nombre, apellido, email, password_hash, activo
                FROM usuarios
                WHERE LOWER(email) = ?
            """, (email.lower(),))
            user = cur.fetchone()

            if not user:
                print("⚠️ Usuario no encontrado en la base de datos.")
                return None

            print("✅ Usuario encontrado:", user[1], user[3])

            if user[4] != h:
                print("❌ Contraseña incorrecta para:", email)
                return None

            if user[5] == 0:
                print("🚫 Usuario inactivo:", email)
                return None

            print("🎉 Credenciales válidas para:", email)
            return user

    def cambiar_password(self, email: str, new_password: str):
        h = sha256(new_password.encode()).hexdigest()
        with self._conn() as conn:
            conn.execute("UPDATE usuarios SET password_hash = ? WHERE LOWER(email) = ?", (h, email.lower(),))

    def existe_email(self, email: str) -> bool:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM usuarios WHERE LOWER(email) = ?", (email.lower(),))
            return cur.fetchone() is not None

    # =====================================================
    # 🔐 TOKENS
    # =====================================================
    def crear_token(self, email: str, token: str, tipo: str, minutos_validez: int = 60) -> None:
        exp = (datetime.utcnow() + timedelta(minutes=minutos_validez)).isoformat(timespec="seconds") + "Z"
        with self._conn() as conn:
            conn.execute("DELETE FROM auth_tokens WHERE email = ? AND tipo = ?", (email.lower(), tipo))
            conn.execute("""
                INSERT INTO auth_tokens (email, token, tipo, expiracion, usado)
                VALUES (?, ?, ?, ?, 0)
            """, (email.lower(), token, tipo, exp))

    def consumir_token(self, token: str, tipo: str):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT email, expiracion, usado FROM auth_tokens
                WHERE token = ? AND tipo = ?
            """, (token, tipo))
            row = cur.fetchone()
            if not row:
                return None  # token inválido

            email, expiracion, usado = row
            if usado:
                return None

            # ⏰ Validar expiración (UTC ISO)
            exp_dt = datetime.fromisoformat(expiracion.replace("Z", ""))
            if datetime.utcnow() > exp_dt:
                return None

            conn.execute("UPDATE auth_tokens SET usado = 1 WHERE token = ?", (token,))
            return email
