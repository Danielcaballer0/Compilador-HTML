"""
Pruebas unitarias para el compilador de SimpleDoc
"""

import unittest
import tempfile
import os
from simpledoc.compiler import Compiler
from simpledoc.exceptions import SimpleDocError


class TestCompiler(unittest.TestCase):
    """Pruebas para el compilador completo"""
    
    def setUp(self):
        """Configuración para las pruebas"""
        self.compiler = Compiler(nivel_complejidad=3)
    
    def test_compilar_documento_basico(self):
        """Prueba la compilación de un documento básico"""
        texto = """# Título de prueba

Este es un párrafo de prueba.
"""
        html = self.compiler.compilar(texto)
        
        # Verificar que el HTML contiene el título y el párrafo
        self.assertIn("<h1>Título de prueba</h1>", html)
        self.assertIn("<p>Este es un párrafo de prueba.</p>", html)
    
    def test_compilar_documento_intermedio(self):
        """Prueba la compilación de un documento con formato intermedio"""
        texto = """# Título de prueba

Este es un párrafo con **negrita** y *cursiva*.

- Lista 1
- Lista 2

1. Numerada 1
2. Numerada 2
"""
        html = self.compiler.compilar(texto)
        
        # Verificar elementos de formato y listas
        self.assertIn("<strong>", html)
        self.assertIn("<em>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<ol>", html)
    
    def test_compilar_documento_avanzado(self):
        """Prueba la compilación de un documento con formato avanzado"""
        texto = """# Título de prueba

Este es un [enlace](https://ejemplo.com) y una ![imagen](https://ejemplo.com/img.jpg).

