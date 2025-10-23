"""
Validadores de datos para SIATLITE
"""
import re
from datetime import datetime
from src.utils.constants import PATRONES, RANGOS


class Validators:
    """Clase con métodos de validación de datos"""

    @staticmethod
    def validar_dni(dni):
        """
        Valida formato de DNI peruano (8 dígitos)

        Args:
            dni: String con el DNI

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not dni:
            return False, "El DNI es obligatorio"

        # Eliminar espacios
        dni = str(dni).strip()

        if not re.match(PATRONES['dni'], dni):
            return False, "El DNI debe tener exactamente 8 dígitos numéricos"

        return True, ""

    @staticmethod
    def validar_placa(placa):
        """
        Valida formato de placa vehicular peruana
        Formato antiguo: ABC-123
        Formato nuevo: ABC-1234

        Args:
            placa: String con la placa

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not placa:
            return False, "La placa es obligatoria"

        # Convertir a mayúsculas y eliminar espacios
        placa = str(placa).strip().upper()

        # Validar formato antiguo o nuevo
        if not (re.match(PATRONES['placa_antigua'], placa) or
                re.match(PATRONES['placa_nueva'], placa)):
            return False, "Formato de placa inválido. Use ABC-123 o ABC-1234"

        return True, ""

    @staticmethod
    def validar_telefono(telefono, tipo='celular'):
        """
        Valida formato de teléfono

        Args:
            telefono: String con el teléfono
            tipo: 'celular' (9 dígitos) o 'fijo' (7 dígitos)

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not telefono:
            return True, ""  # Es opcional

        # Eliminar espacios y caracteres no numéricos
        telefono = re.sub(r'[^\d]', '', str(telefono))

        if tipo == 'celular':
            if not re.match(PATRONES['telefono_celular'], telefono):
                return False, "El teléfono celular debe tener 9 dígitos"
        elif tipo == 'fijo':
            if not re.match(PATRONES['telefono_fijo'], telefono):
                return False, "El teléfono fijo debe tener 7 dígitos"
        else:
            # Aceptar cualquiera
            if not (re.match(PATRONES['telefono_celular'], telefono) or
                    re.match(PATRONES['telefono_fijo'], telefono)):
                return False, "El teléfono debe tener 7 o 9 dígitos"

        return True, ""

    @staticmethod
    def validar_email(email):
        """
        Valida formato de email

        Args:
            email: String con el email

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not email:
            return True, ""  # Es opcional

        email = str(email).strip()

        if not re.match(PATRONES['email'], email):
            return False, "Formato de email inválido"

        return True, ""

    @staticmethod
    def validar_fecha(fecha_str, fecha_maxima=None):
        """
        Valida formato de fecha YYYY-MM-DD

        Args:
            fecha_str: String con la fecha
            fecha_maxima: Fecha máxima permitida (datetime o None para hoy)

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not fecha_str:
            return False, "La fecha es obligatoria"

        fecha_str = str(fecha_str).strip()

        if not re.match(PATRONES['fecha'], fecha_str):
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

            # Validar que no sea futura
            max_fecha = fecha_maxima if fecha_maxima else datetime.now()
            if fecha > max_fecha:
                return False, "La fecha no puede ser futura"

            # Validar que no sea muy antigua (más de 50 años)
            fecha_minima = datetime.now().replace(year=datetime.now().year - 50)
            if fecha < fecha_minima:
                return False, "La fecha es demasiado antigua"

            return True, ""

        except ValueError:
            return False, "Fecha inválida"

    @staticmethod
    def validar_hora(hora_str):
        """
        Valida formato de hora HH:MM

        Args:
            hora_str: String con la hora

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not hora_str:
            return False, "La hora es obligatoria"

        hora_str = str(hora_str).strip()

        if not re.match(PATRONES['hora'], hora_str):
            return False, "Formato de hora inválido. Use HH:MM"

        try:
            datetime.strptime(hora_str, '%H:%M')
            return True, ""
        except ValueError:
            return False, "Hora inválida"

    @staticmethod
    def validar_rango_numerico(valor, minimo, maximo, nombre_campo):
        """
        Valida que un valor numérico esté en un rango

        Args:
            valor: Valor a validar
            minimo: Valor mínimo permitido
            maximo: Valor máximo permitido
            nombre_campo: Nombre del campo para el mensaje

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        try:
            val = float(valor)

            if val < minimo or val > maximo:
                return False, f"{nombre_campo} debe estar entre {minimo} y {maximo}"

            return True, ""

        except (ValueError, TypeError):
            return False, f"{nombre_campo} debe ser un número válido"

    @staticmethod
    def validar_coordenadas(latitud, longitud):
        """
        Valida coordenadas geográficas

        Args:
            latitud: Valor de latitud
            longitud: Valor de longitud

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if latitud is None or longitud is None:
            return True, ""  # Son opcionales

        try:
            lat = float(latitud)
            lon = float(longitud)

            lat_min, lat_max = RANGOS['latitud']
            if lat < lat_min or lat > lat_max:
                return False, f"Latitud debe estar entre {lat_min} y {lat_max}"

            lon_min, lon_max = RANGOS['longitud']
            if lon < lon_min or lon > lon_max:
                return False, f"Longitud debe estar entre {lon_min} y {lon_max}"

            return True, ""

        except (ValueError, TypeError):
            return False, "Coordenadas inválidas"

    @staticmethod
    def validar_edad(edad):
        """
        Valida la edad de una persona

        Args:
            edad: Edad en años

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if edad is None:
            return True, ""  # Es opcional

        min_edad, max_edad = RANGOS['edad']
        return Validators.validar_rango_numerico(edad, min_edad, max_edad, "Edad")

    @staticmethod
    def validar_año_vehiculo(año):
        """
        Valida el año de un vehículo

        Args:
            año: Año del vehículo

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not año:
            return True, ""  # Es opcional

        min_año, max_año = RANGOS['año_vehiculo']
        return Validators.validar_rango_numerico(año, min_año, max_año, "Año del vehículo")

    @staticmethod
    def validar_numero_motor(numero_motor):
        """
        Valida el número de motor

        Args:
            numero_motor: String con el número de motor

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not numero_motor:
            return True, ""  # Es opcional

        numero_motor = str(numero_motor).strip()

        if len(numero_motor) < 5:
            return False, "El número de motor debe tener al menos 5 caracteres"

        if len(numero_motor) > 30:
            return False, "El número de motor no puede exceder 30 caracteres"

        return True, ""

    @staticmethod
    def validar_numero_chasis(numero_chasis):
        """
        Valida el número de chasis (VIN)

        Args:
            numero_chasis: String con el número de chasis

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not numero_chasis:
            return True, ""  # Es opcional

        numero_chasis = str(numero_chasis).strip().upper()

        # VIN estándar tiene 17 caracteres
        if len(numero_chasis) != 17:
            return False, "El número de chasis (VIN) debe tener 17 caracteres"

        # No debe contener letras I, O, Q (confusión con números)
        if any(c in numero_chasis for c in ['I', 'O', 'Q']):
            return False, "El VIN no puede contener las letras I, O o Q"

        return True, ""

    @staticmethod
    def validar_campo_requerido(valor, nombre_campo):
        """
        Valida que un campo no esté vacío

        Args:
            valor: Valor a validar
            nombre_campo: Nombre del campo para el mensaje

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            return False, f"{nombre_campo} es obligatorio"

        return True, ""

    @staticmethod
    def validar_longitud_texto(texto, longitud_min, longitud_max, nombre_campo):
        """
        Valida la longitud de un texto

        Args:
            texto: Texto a validar
            longitud_min: Longitud mínima
            longitud_max: Longitud máxima
            nombre_campo: Nombre del campo

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not texto:
            return True, ""  # Si está vacío, usar validar_campo_requerido

        texto = str(texto).strip()
        longitud = len(texto)

        if longitud < longitud_min:
            return False, f"{nombre_campo} debe tener al menos {longitud_min} caracteres"

        if longitud > longitud_max:
            return False, f"{nombre_campo} no puede exceder {longitud_max} caracteres"

        return True, ""

    @staticmethod
    def validar_numero_positivo(valor, nombre_campo, permitir_cero=True):
        """
        Valida que un número sea positivo

        Args:
            valor: Valor a validar
            nombre_campo: Nombre del campo
            permitir_cero: Si se permite el valor 0

        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        try:
            val = float(valor)

            if permitir_cero:
                if val < 0:
                    return False, f"{nombre_campo} no puede ser negativo"
            else:
                if val <= 0:
                    return False, f"{nombre_campo} debe ser mayor a cero"

            return True, ""

        except (ValueError, TypeError):
            return False, f"{nombre_campo} debe ser un número válido"

    @staticmethod
    def validar_formulario(datos, reglas):
        """
        Valida múltiples campos de un formulario

        Args:
            datos: Diccionario con los datos del formulario
            reglas: Diccionario con las reglas de validación
                   Formato: {'campo': [('funcion_validacion', parametros)]}

        Returns:
            tuple: (bool, list) - (es_valido, lista_errores)
        """
        errores = []

        for campo, validaciones in reglas.items():
            valor = datos.get(campo)

            for validacion in validaciones:
                if isinstance(validacion, tuple):
                    funcion, *params = validacion
                else:
                    funcion = validacion
                    params = []

                # Ejecutar validación
                valido, mensaje = funcion(valor, *params)

                if not valido:
                    errores.append(f"{campo}: {mensaje}")

        return len(errores) == 0, errores


# ========== VALIDADORES ESPECÍFICOS ==========

class AccidenteValidator:
    """Validador específico para accidentes"""

    @staticmethod
    def validar(datos):
        """
        Valida todos los campos de un accidente

        Args:
            datos: Diccionario con los datos del accidente

        Returns:
            list: Lista de errores (vacía si es válido)
        """
        errores = []

        # Fecha
        valido, msg = Validators.validar_fecha(datos.get('fecha'))
        if not valido:
            errores.append(msg)

        # Hora
        valido, msg = Validators.validar_hora(datos.get('hora'))
        if not valido:
            errores.append(msg)

        # Lugar
        valido, msg = Validators.validar_campo_requerido(datos.get('lugar'), 'Lugar')
        if not valido:
            errores.append(msg)

        # Tipo de accidente
        valido, msg = Validators.validar_campo_requerido(datos.get('id_tipo'), 'Tipo de accidente')
        if not valido:
            errores.append(msg)

        # Gravedad
        valido, msg = Validators.validar_campo_requerido(datos.get('id_gravedad'), 'Gravedad')
        if not valido:
            errores.append(msg)

        # Coordenadas
        valido, msg = Validators.validar_coordenadas(
            datos.get('latitud'),
            datos.get('longitud')
        )
        if not valido:
            errores.append(msg)

        # Heridos
        valido, msg = Validators.validar_numero_positivo(
            datos.get('heridos', 0),
            'Número de heridos'
        )
        if not valido:
            errores.append(msg)

        # Fallecidos
        valido, msg = Validators.validar_numero_positivo(
            datos.get('fallecidos', 0),
            'Número de fallecidos'
        )
        if not valido:
            errores.append(msg)

        return errores


class PersonaValidator:
    """Validador específico para personas"""

    @staticmethod
    def validar(datos):
        """Valida los datos de una persona"""
        errores = []

        # Nombre
        valido, msg = Validators.validar_campo_requerido(datos.get('nombre'), 'Nombre')
        if not valido:
            errores.append(msg)

        # Apellido
        valido, msg = Validators.validar_campo_requerido(datos.get('apellido'), 'Apellido')
        if not valido:
            errores.append(msg)

        # DNI (opcional pero debe ser válido si se proporciona)
        if datos.get('dni'):
            valido, msg = Validators.validar_dni(datos.get('dni'))
            if not valido:
                errores.append(msg)

        # Edad
        if datos.get('edad'):
            valido, msg = Validators.validar_edad(datos.get('edad'))
            if not valido:
                errores.append(msg)

        # Teléfono
        if datos.get('telefono'):
            valido, msg = Validators.validar_telefono(datos.get('telefono'))
            if not valido:
                errores.append(msg)

        return errores


class VehiculoValidator:
    """Validador específico para vehículos"""

    @staticmethod
    def validar(datos):
        """Valida los datos de un vehículo"""
        errores = []

        # Placa
        if datos.get('placa'):
            valido, msg = Validators.validar_placa(datos.get('placa'))
            if not valido:
                errores.append(msg)

        # Año
        if datos.get('año'):
            valido, msg = Validators.validar_año_vehiculo(datos.get('año'))
            if not valido:
                errores.append(msg)

        # Número de motor
        if datos.get('numero_motor'):
            valido, msg = Validators.validar_numero_motor(datos.get('numero_motor'))
            if not valido:
                errores.append(msg)

        # Número de chasis
        if datos.get('numero_chasis'):
            valido, msg = Validators.validar_numero_chasis(datos.get('numero_chasis'))
            if not valido:
                errores.append(msg)

        return errores


# Exportar todo
__all__ = [
    'Validators',
    'AccidenteValidator',
    'PersonaValidator',
    'VehiculoValidator'
]