"""
Sistema de logging para SIATLITE
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class Logger:
    """Clase para gestionar logs del sistema"""

    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        """Configura el logger"""
        # Crear directorio de logs si no existe
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        # Nombre del archivo de log
        log_file = os.path.join(log_dir, f'siatlite_{datetime.now().strftime("%Y%m")}.log')

        # Configurar logger
        self._logger = logging.getLogger('SIATLITE')
        self._logger.setLevel(logging.DEBUG)

        # Evitar duplicación de handlers
        if not self._logger.handlers:
            # Handler para archivo (rotativo, max 10MB, 5 backups)
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)

            # Handler para consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Formato de los logs
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)

    def debug(self, mensaje):
        """Registra mensaje de debug"""
        self._logger.debug(mensaje)

    def info(self, mensaje):
        """Registra mensaje informativo"""
        self._logger.info(mensaje)

    def warning(self, mensaje):
        """Registra advertencia"""
        self._logger.warning(mensaje)

    def error(self, mensaje, exc_info=False):
        """Registra error"""
        self._logger.error(mensaje, exc_info=exc_info)

    def critical(self, mensaje, exc_info=False):
        """Registra error crítico"""
        self._logger.critical(mensaje, exc_info=exc_info)

    def log_operacion(self, usuario, operacion, tabla, detalles=''):
        """Registra una operación del sistema"""
        mensaje = f"Usuario: {usuario} | Operación: {operacion} | Tabla: {tabla}"
        if detalles:
            mensaje += f" | Detalles: {detalles}"
        self.info(mensaje)

    def log_error_db(self, operacion, tabla, error):
        """Registra error de base de datos"""
        mensaje = f"Error BD | Operación: {operacion} | Tabla: {tabla} | Error: {error}"
        self.error(mensaje, exc_info=True)

    def log_login(self, usuario, exitoso=True):
        """Registra intento de login"""
        if exitoso:
            self.info(f"Login exitoso - Usuario: {usuario}")
        else:
            self.warning(f"Login fallido - Usuario: {usuario}")

    def log_logout(self, usuario):
        """Registra cierre de sesión"""
        self.info(f"Logout - Usuario: {usuario}")


# Instancia global del logger
logger = Logger()


# Decorador para logging automático de funciones
def log_function(func):
    """Decorador para registrar llamadas a funciones"""

    def wrapper(*args, **kwargs):
        logger.debug(f"Llamando a función: {func.__name__}")
        try:
            resultado = func(*args, **kwargs)
            logger.debug(f"Función {func.__name__} ejecutada correctamente")
            return resultado
        except Exception as e:
            logger.error(f"Error en función {func.__name__}: {e}", exc_info=True)
            raise

    return wrapper


# Clase de contexto para operaciones
class OperacionContext:
    """Context manager para registrar operaciones"""

    def __init__(self, nombre_operacion, usuario='Sistema'):
        self.nombre = nombre_operacion
        self.usuario = usuario
        self.inicio = None

    def __enter__(self):
        self.inicio = datetime.now()
        logger.info(f"Iniciando operación: {self.nombre} (Usuario: {self.usuario})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duracion = (datetime.now() - self.inicio).total_seconds()

        if exc_type is None:
            logger.info(
                f"Operación completada: {self.nombre} "
                f"(Duración: {duracion:.2f}s)"
            )
        else:
            logger.error(
                f"Operación fallida: {self.nombre} "
                f"(Duración: {duracion:.2f}s) - Error: {exc_val}",
                exc_info=True
            )

        return False  # No suprimir excepciones


# Función auxiliar para limpiar logs antiguos
def limpiar_logs_antiguos(dias=30):
    """Elimina archivos de log más antiguos que X días"""
    import glob
    from pathlib import Path

    log_dir = 'logs'
    if not os.path.exists(log_dir):
        return

    limite = datetime.now().timestamp() - (dias * 24 * 60 * 60)

    for log_file in glob.glob(os.path.join(log_dir, '*.log*')):
        if os.path.getmtime(log_file) < limite:
            try:
                os.remove(log_file)
                logger.info(f"Log antiguo eliminado: {log_file}")
            except Exception as e:
                logger.error(f"Error al eliminar log: {log_file} - {e}")


# Ejemplo de uso:
if __name__ == '__main__':
    # Uso básico
    logger.info("Sistema iniciado")
    logger.debug("Mensaje de debug")
    logger.warning("Esto es una advertencia")
    logger.error("Esto es un error")


    # Uso con decorador
    @log_function
    def mi_funcion():
        print("Ejecutando función...")
        return "OK"


    resultado = mi_funcion()

    # Uso con context manager
    with OperacionContext("Operación de prueba", "admin"):
        # Código de la operación
        import time

        time.sleep(0.5)
        print("Operación completada")

    # Registrar operación específica
    logger.log_operacion("admin", "CREAR", "accidentes", "ACC-2025-001")

    # Registrar login
    logger.log_login("admin", exitoso=True)

    print("\nLogs guardados en: logs/")