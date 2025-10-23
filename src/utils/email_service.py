# src/utils/email_service.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self):
        # Usa variables de entorno para no hardcodear secrets
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.user = os.getenv("SMTP_USER")          # ej: tu_correo@gmail.com
        self.password = os.getenv("SMTP_PASSWORD")  # clave de aplicación

    def enviar_correo(self, destinatario: str, asunto: str, html_body: str, plain_fallback: str = ""):
        if not self.user or not self.password:
            raise RuntimeError("SMTP_USER/SMTP_PASSWORD no configurados en variables de entorno.")

        msg = MIMEMultipart("alternative")
        msg["From"] = self.user
        msg["To"] = destinatario
        msg["Subject"] = asunto

        if plain_fallback:
            msg.attach(MIMEText(plain_fallback, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
