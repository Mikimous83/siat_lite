import re
from datetime import datetime


class ValidationService:
    def validar_accidente(self, datos):
        """Validar datos de accidente"""
        errores = []

        # Validar fecha
        if not datos.get('fecha'):
            errores.append("La fecha es obligatoria")

        # Validar lugar
        if not datos.get('lugar') or len(datos['lugar']) < 3:
            errores.append("El lugar debe tener al menos 3 caracteres")

        # Validar tipo de accidente
        tipos_validos = ["Colisión", "Atropello", "Volcadura", "Choque"]
        if datos.get('tipo_accidente') not in tipos_validos:
            errores.append("Tipo de accidente no válido")

        return errores

    def validar_vehiculo(self, datos):
        """Validar datos de vehículo"""
        errores = []

        if datos.get('placa'):
            if not self._validar_formato_placa(datos['placa']):
                errores.append("Formato de placa inválido")

        return errores

    def _validar_formato_placa(self, placa):
        """Validar formato de placa peruana"""
        # Formato: ABC-123 o ABC-1234
        patron = r'^[A-Z]{3}-\\d{3,4}$'
        return re.match(patron, placa.upper()) is not None