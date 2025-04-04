from rest_framework import serializers


def parse_boolean(value):
    value = value.strip()
    if isinstance(value, bool):
        return value
    if value in ['1', 'true', 'True']:
        return True
    if value in ['0', 'false', 'False']:
        return False
    raise serializers.ValidationError(f"Invalid boolean value: {value}")

def parse_integer(value):
    value = value.strip()
    try:
        parsed_value = float(value)        
        if parsed_value.is_integer():
            return int(parsed_value)
        raise ValueError(f'Invalid integer value: {value}')
    except ValueError:
        raise ValueError(f'Invalid integer value: {value}')
    
def parse_decimal(value):
    value = value.strip()
    try:
        parsed_value = float(value)
        return parsed_value
    except ValueError:
        raise ValueError(f'Invalid decimal value: {value}')
    
def parse_percentage(value):
    value = value.strip()
    try:
        if '%' in value:
            return float(value.replace('%', '').strip()) / 100
        return float(value) / 100
    except ValueError:
        raise ValueError(f'Invalid percentage value: {value}')
    