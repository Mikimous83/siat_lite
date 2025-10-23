# src/utils/email_service.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    """Servicio de envío de correos con modo seguro de pruebas"""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.user = os.getenv("SMTP_USER")          # ej: tu_correo@gmail.com
        self.password = os.getenv("SMTP_PASSWORD")  # clave o token de aplicación

    def enviar_correo(self, destinatario: str, asunto: str, html_body: str, plain_fallback: str = ""):
        """Envía un correo real o simulado (según configuración)."""

        # 🧩 Si no hay credenciales, modo "simulación"
        if not self.user or not self.password:
            print("⚠️ [EmailService] SMTP_USER o SMTP_PASSWORD no configurados.")
            print("Simulando envío de correo a:", destinatario)
            print("Asunto:", asunto)
            print("Contenido HTML:\n", html_body)
            return True  # simula éxito para no romper la app

        msg = MIMEMultipart("alternative")
        msg["From"] = self.user
        msg["To"] = destinatario
        msg["Subject"] = asunto

        if plain_fallback:
            msg.attach(MIMEText(plain_fallback, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=15) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
            print(f"✅ Correo enviado correctamente a {destinatario}")
            return True
        except smtplib.SMTPAuthenticationError:
            print("❌ Error de autenticación SMTP: revisa usuario o contraseña.")
        except Exception as e:
            print(f"❌ Error al enviar correo: {e}")
        return False
