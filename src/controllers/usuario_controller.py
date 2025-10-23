# src/controllers/usuario_controller.py
import secrets
from src.models.usuario_model import UsuarioModel
from src.utils.email_service import EmailService

class UsuarioController:
    def __init__(self, db_path: str, public_base_url: str = "http://localhost"):
        self.model = UsuarioModel(db_path)
        self.mailer = EmailService()
        self.public_base_url = public_base_url.rstrip("/")

    # ---------- Registro ----------
    def registrar(self, nombre, apellido, email, password, id_rol=None):
        if self.model.existe_email(email):
            return False, "El correo ya está registrado."
        user_id = self.model.crear_usuario(nombre, apellido, email, password, id_rol)
        token = secrets.token_urlsafe(24)
        self.model.crear_token(email, token, tipo="confirm", minutos_validez=60*24)  # 24h

        link = f"{self.public_base_url}/siatlite/php_server/confirmar.php?token={token}"
        html = f"""
        <h3>Confirma tu cuenta</h3>
        <p>Hola {nombre},</p>
        <p>Gracias por registrarte. Confirma tu cuenta dando clic en el siguiente enlace:</p>
        <p><a href="{link}" target="_blank">Confirmar cuenta</a></p>
        <p>Si no fuiste tú, ignora este correo.</p>
        """
        self.mailer.enviar_correo(email, "Confirma tu cuenta - SIATLITE", html, "Confirma tu cuenta: " + link)
        return True, "Registro exitoso. Revisa tu correo para confirmar tu cuenta."

    # ---------- Confirmación ----------
    def confirmar(self, token: str):
        email = self.model.consumir_token(token, tipo="confirm")
        if not email:
            return False, "Token inválido o expirado."
        self.model.activar_usuario(email)
        return True, f"Cuenta {email} confirmada."

    # ---------- Login ----------
    def login(self, email, password):
        user = self.model.verificar_credenciales(email, password)
        if not user:
            return False, "Credenciales inválidas."
        if user[4] == 0:
            return False, "Cuenta no confirmada. Revisa tu correo."
        return True, {"id_usuario": user[0], "nombre": user[1], "apellido": user[2], "email": user[3]}

    # ---------- Recuperación (envío de link) ----------
    def solicitar_reset(self, email: str):
        if not self.model.existe_email(email):
            return False, "Correo no registrado."

        token = secrets.token_urlsafe(24)
        self.model.crear_token(email, token, tipo="reset", minutos_validez=30)  # 30 minutos

        link = f"{self.public_base_url}/siatlite/php_server/restablecer.php?token={token}"
        html = f"""
        <h3>Restablecer contraseña</h3>
        <p>Solicitaste restablecer tu contraseña. Usa este enlace:</p>
        <p><a href="{link}" target="_blank">Restablecer contraseña</a></p>
        <p>Este enlace expira en 30 minutos. Si no fuiste tú, ignora este mensaje.</p>
        """
        self.mailer.enviar_correo(email, "Restablece tu contraseña - SIATLITE", html, "Restablece tu contraseña: " + link)
        return True, "Se envió un enlace de recuperación a tu correo."

    # ---------- Aplicar nueva contraseña (desde token) ----------
    def aplicar_reset(self, token: str, new_password: str):
        email = self.model.consumir_token(token, tipo="reset")
        if not email:
            return False, "Token inválido o expirado."
        self.model.cambiar_password(email, new_password)
        return True, "Contraseña actualizada correctamente."
