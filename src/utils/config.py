import os
from typing import Dict, Any


class Config:
    """Clase de configuración centralizada"""

    def __init__(self):
        self.config_data = self._load_default_config()

    def _load_default_config(self) -> Dict[str, Any]:
        """Cargar configuración por defecto"""
        return {
            # Base de datos
            'database': {
                'name': 'siat_lite.db',
                'path': 'data',
                'backup_enabled': True,
                'backup_interval_hours': 24
            },

            # Interfaz
            'ui': {
                'theme': 'superhero',
                'window_size': '1200x800',
                'font_family': 'Arial',
                'font_size': 10
            },

            # Archivos
            'files': {
                'max_size_mb': 10,
                'allowed_image_formats': ['.jpg', '.jpeg', '.png', '.gif'],
                'allowed_doc_formats': ['.pdf', '.doc', '.docx', '.txt'],
                'upload_path': 'data/uploads'
            },

            # Notificaciones
            'notifications': {
                'email_enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': '',
                'sender_password': ''
            },

            # Seguridad
            'security': {
                'session_timeout_minutes': 120,
                'password_min_length': 6,
                'max_login_attempts': 3,
                'require_password_change': False
            }
        }

    def get(self, key_path: str, default=None):
        """Obtener valor usando notación de punto"""
        keys = key_path.split('.')
        value = self.config_data

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value):
        """Establecer valor de configuración"""
        keys = key_path.split('.')
        config = self.config_data

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value


# Instancia global
config = Config()
