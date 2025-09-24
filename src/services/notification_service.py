import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class NotificationService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_usuario = ""  # Configurar
        self.email_password = ""  # Configurar

    def enviar_notificacion_accidente_grave(self, datos_accidente, destinatarios):
        """Enviar notificación de accidente grave"""
        try:
            if datos_accidente.get('gravedad') in ['Muy Grave', 'Fatal']:
                mensaje = self._crear_mensaje_accidente_grave(datos_accidente)
                self._enviar_email(destinatarios, "ALERTA: Accidente Grave Registrado", mensaje)

        except Exception as e:
            print(f"Error al enviar notificación: {str(e)}")

    def _crear_mensaje_accidente_grave(self, datos):
        """Crear mensaje para accidente grave"""
        mensaje = f"""
        ALERTA DE ACCIDENTE GRAVE

        Número de Caso: {datos.get('numero_caso', 'N/A')}
        Fecha: {datos.get('fecha', 'N/A')} {datos.get('hora', 'N/A')}
        Lugar: {datos.get('lugar', 'N/A')}
        Tipo: {datos.get('tipo_accidente', 'N/A')}
        Gravedad: {datos.get('gravedad', 'N/A')}

        Heridos: {datos.get('heridos', 0)}
        Fallecidos: {datos.get('fallecidos', 0)}

        Este es un mensaje automático del sistema SIAT-Lite.
        """
        return mensaje

    def _enviar_email(self, destinatarios, asunto, mensaje):
        """Enviar email"""
        if not self.email_usuario or not self.email_password:
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_usuario
            msg['To'] = ', '.join(destinatarios)
            msg['Subject'] = asunto

            msg.attach(MIMEText(mensaje, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_usuario, self.email_password)
            server.sendmail(self.email_usuario, destinatarios, msg.as_string())
            server.quit()

        except Exception as e:
            print(f"Error enviando email: {str(e)}")