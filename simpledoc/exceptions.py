"""
Excepciones personalizadas para el compilador SimpleDoc
"""


class SimpleDocError(Exception):
    """Clase base para todas las excepciones de SimpleDoc"""
    pass


class LexerError(SimpleDocError):
    """Error durante el análisis léxico"""
    def __init__(self, message, line_number=None, column=None):
        self.line_number = line_number
        self.column = column
        
        if line_number is not None and column is not None:
            message = f"Error en línea {line_number}, columna {column}: {message}"
        elif line_number is not None:
            message = f"Error en línea {line_number}: {message}"
        
        super().__init__(message)


class ParserError(SimpleDocError):
    """Error durante el análisis sintáctico"""
    def __init__(self, message, line_number=None, token=None):
        self.line_number = line_number
        self.token = token
        
        if line_number is not None and token is not None:
            message = f"Error en línea {line_number}, token '{token}': {message}"
        elif line_number is not None:
            message = f"Error en línea {line_number}: {message}"
        
        super().__init__(message)


class ValidationError(SimpleDocError):
    """Error durante la validación del documento"""
    def __init__(self, message, element=None, line_number=None):
        self.element = element
        self.line_number = line_number
        
        if element is not None and line_number is not None:
            message = f"Error de validación en línea {line_number}, elemento '{element}': {message}"
        elif line_number is not None:
            message = f"Error de validación en línea {line_number}: {message}"
        elif element is not None:
            message = f"Error de validación en elemento '{element}': {message}"
            
        super().__init__(message)


class GenerationError(SimpleDocError):
    """Error durante la generación de código"""
    pass
