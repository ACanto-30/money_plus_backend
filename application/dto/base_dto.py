from pydantic import BaseModel, ConfigDict

class BaseDTO(BaseModel):
    """Clase base con configuración global de errores"""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        error_messages={
            'missing': 'Este campo es requerido',
            'string_too_short': 'Mínimo {min_length} caracteres',
            'string_too_long': 'Máximo {max_length} caracteres',
            'string_pattern_mismatch': 'Formato inválido',
            'email_syntax': 'Formato de email inválido',
            'greater_than': 'Debe ser mayor que {gt}',
            'value_error.any_str.min_length': 'Mínimo {min_length} caracteres',
            'value_error.any_str.max_length': 'Máximo {max_length} caracteres',
            'value_error.any_str.regex': 'Formato inválido',
            'value_error.number.not_gt': 'Debe ser mayor que {limit_value}',
        }
    )