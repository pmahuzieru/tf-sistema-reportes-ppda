import re

def calculate_dv(body):
    """Calcula el dígito verificador usando el algoritmo Módulo 11."""
    factors = [2, 3, 4, 5, 6, 7]
    reversed_digits = map(int, reversed(body))
    total = sum(d * factors[i % len(factors)] for i, d in enumerate(reversed_digits))
    
    remainder = 11 - (total % 11)
    return "K" if remainder == 10 else "0" if remainder == 11 else str(remainder)

def validate_rut(rut):
    """Valida un RUT chileno verificando su dígito verificador."""
    if not isinstance(rut, str):
        return False  # Asegura que sea un string antes de procesar

    rut = rut.upper().replace(".", "").replace("-", "").strip()
    
    # Validar formato: 7 u 8 dígitos seguidos de un DV (número o 'K')
    if not re.match(r"^\d{7,8}[0-9K]$", rut):
        return False

    body, dv = rut[:-1], rut[-1]  # Separar el número del dígito verificador

    return dv == calculate_dv(body)

def format_rut(rut: str) -> str:
    """Formats a Chilean RUT ID to 'XXXXXXXX-X' format."""
    rut = re.sub(r"[^\dkK]", "", rut).upper()
    return f"{rut[:-1]}-{rut[-1]}" if len(rut) > 1 else rut
