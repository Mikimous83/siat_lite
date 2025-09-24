import re
from datetime import datetime


class ValidationService:
    def validar_accidente(self, datos):
        """Validar datos de accidente"""
        errores = []

        # ✅ Validar fecha
        if not datos.get('fecha'):
            errores.append("La fecha es obligatoria")
        else:
            try:
                datetime.strptime(datos['fecha'], "%Y-%m-%d")
            except ValueError:
                errores.append("La fecha no tiene el formato válido (YYYY-MM-DD)")

        # ✅ Validar lugar
        if not datos.get('lugar') or len(datos['lugar'].strip()) < 3:
            errores.append("El lugar debe tener al menos 3 caracteres")

        # ✅ Validar tipo de accidente
        tipos_validos = ["Colisión", "Atropello", "Volcadura", "Choque"]
        if datos.get('tipo_accidente') not in tipos_validos:
            errores.append("Tipo de accidente no válido")

        return errores

    def validar_vehiculo(self, datos):
        """Validar datos de vehículo"""
        errores = []

        if datos.get('placa'):
            if not self._validar_formato_placa(datos['placa']):
                errores.append("Formato de placa inválido (ejemplo: ABC-123 o ABC-1234)")

        return errores

    def validar_persona(self, datos):
        """Validar datos de persona involucrada en accidente"""
        errores = []

        # ✅ Validar nombre
        if not datos.get('nombre') or len(datos['nombre'].strip()) < 2:
            errores.append("El nombre debe tener al menos 2 caracteres")

        # ✅ Validar DNI (opcional, pero si se ingresa debe tener 8 dígitos en Perú)
        if datos.get('dni'):
            if not re.match(r'^\d{8}$', datos['dni']):
                errores.append("El DNI debe tener exactamente 8 dígitos")

        # ✅ Validar edad
        if datos.get('edad') is not None:
            try:
                edad = int(datos['edad'])
                if edad < 0 or edad > 120:
                    errores.append("La edad debe estar entre 0 y 120")
            except ValueError:
                errores.append("La edad debe ser un número válido")

        # ✅ Validar rol en el accidente
        roles_validos = ["Conductor", "Pasajero", "Peatón"]
        if datos.get('rol') not in roles_validos:
            errores.append("El rol debe ser Conductor, Pasajero o Peatón")

        return errores

    def _validar_formato_placa(self, placa):
        """Validar formato de placa peruana"""
        # Formato: ABC-123 o ABC-1234
        patron = r'^[A-Z]{3}-\d{3,4}$'
        return re.match(patron, placa.upper()) is not None
