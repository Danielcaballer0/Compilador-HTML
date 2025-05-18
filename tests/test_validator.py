"""
Pruebas unitarias para el validador de SimpleDoc
"""

import unittest
from simpledoc.lexer import Lexer
from simpledoc.parser import Parser
from simpledoc.validator import Validator
from simpledoc.exceptions import ValidationError


class TestValidator(unittest.TestCase):
    """Pruebas para el validador"""
    
    def setUp(self):
        """Configuración para las pruebas"""
        self.lexer = Lexer(nivel_complejidad=3)
        self.parser = Parser(nivel_complejidad=3)
        self.validator = Validator(nivel_complejidad=3)
    
    def test_validar_documento_valido(self):
        """Prueba la validación de un documento válido"""
        texto = """# Título de prueba

Este es un párrafo de prueba con **negrita** y *cursiva*.

## Lista

- Elemento 1
- Elemento 2

1. Elemento numerado 1
2. Elemento numerado 2

[Enlace](https://ejemplo.com)

![Imagen](https://ejemplo.com/imagen.jpg)

