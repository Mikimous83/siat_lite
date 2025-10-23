# src/models/usuario_model.py
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

    # -------------------- Usuarios --------------------
    def crear_usuario(self, nombre, apellido, email, password, id_rol=None):
        password_hash = sha256(password.encode()).hexdigest()
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO usuarios (nombre, apellido, email, password_hash, id_rol, activo)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (nombre, apellido, email.lower(), password_hash, id_rol))
            return cur.lastrowid

    def activar_usuario(self, email: str):
        with self._conn() as conn:
            conn.execute("UPDATE usuarios SET activo = 1 WHERE email = ?", (email.lower(),))

    def verificar_credenciales(self, email: str, password: str):
        h = sha256(password.encode()).hexdigest()
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_usuario, nombre, apellido, email, activo
                FROM usuarios
                WHERE email = ? AND password_hash = ?
            """, (email.lower(), h))
            return cur.fetchone()

    def cambiar_password(self, email: str, new_password: str):
        h = sha256(new_password.encode()).hexdigest()
        with self._conn() as conn:
            conn.execute("UPDATE usuarios SET password_hash = ? WHERE email = ?", (h, email.lower(),))

    def existe_email(self, email: str) -> bool:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM usuarios WHERE email = ?", (email.lower(),))
            return cur.fetchone() is not None

    # -------------------- Tokens --------------------
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

            # validar expiración (UTC ISO)
            exp_dt = datetime.fromisoformat(expiracion.replace("Z", ""))
            if datetime.utcnow() > exp_dt:
                return None

            conn.execute("UPDATE auth_tokens SET usado = 1 WHERE token = ?", (token,))
            return email
