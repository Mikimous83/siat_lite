import re
from datetime import datetime
from typing import Optional, Dict


def validar_dni(dni: str) -> bool:
    """Validar DNI peruano (8 dígitos)"""
    if not dni:
        return False
    return bool(re.match(r'^\d{8}$', dni))


def validar_placa_vehicular(placa: str) -> bool:
    """Validar placa vehicular peruana"""
    if not placa:
        return False

    # Formato antiguo: ABC-123
    formato_antiguo = r'^[A-Z]{3}-\d{3}$'
    # Formato nuevo: ABC-123A o ABC-1234
    formato_nuevo = r'^[A-Z]{3}-\d{3}[A-Z]$|^[A-Z]{3}-\d{4}$'

    placa_upper = placa.upper()
    return bool(re.match(formato_antiguo, placa_upper) or re.match(formato_nuevo, placa_upper))


def validar_email(email: str) -> bool:
    """Validar formato de email"""
    if not email:
        return False

    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))


def validar_telefono(telefono: str) -> bool:
    """Validar teléfono peruano"""
    if not telefono:
        return False

    # Celular: 9XXXXXXXX, Fijo: XXXXXXX
    patron = r'^(9\d{8}|\d{7})$'
    return bool(re.match(patron, telefono.replace(' ', '').replace('-', '')))


def formatear_numero_caso(id_accidente: int, año: Optional[int] = None) -> str:
    """Formatear número de caso"""
    if año is None:
        año = datetime.now().year

    return f"ACC-{año}-{id_accidente:06d}"


def limpiar_texto(texto: str) -> str:
    """Limpiar texto removiendo caracteres especiales"""
    if not texto:
        return ""

    # Remover espacios extra
    texto = ' '.join(texto.split())
    return texto.title()