"""
Pruebas unitarias para el parser de SimpleDoc
"""

import unittest
from simpledoc.lexer import Lexer
from simpledoc.parser import Parser
from simpledoc.exceptions import ParserError


class TestParser(unittest.TestCase):
    """Pruebas para el analizador sintáctico"""
    
    def setUp(self):
        """Configuración para las pruebas"""
        self.lexer = Lexer(nivel_complejidad=3)
        self.parser = Parser(nivel_complejidad=3)
    
    def test_parsear_titulo(self):
        """Prueba el parseo de títulos"""
        texto = "# Título de prueba"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "TITULO1")
        self.assertEqual(ast.hijos[0].valor, "Título de prueba")
    
    def test_parsear_texto(self):
        """Prueba el parseo de texto simple"""
        texto = "Este es un texto de prueba"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "TEXTO")
        self.assertEqual(ast.hijos[0].valor, "Este es un texto de prueba")
    
    def test_parsear_negrita(self):
        """Prueba el parseo de texto en negrita"""
        texto = "**texto en negrita**"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "NEGRITA")
        self.assertEqual(len(ast.hijos[0].hijos), 1)
        self.assertEqual(ast.hijos[0].hijos[0].tipo, "TEXTO")
        self.assertEqual(ast.hijos[0].hijos[0].valor, "texto en negrita")
    
    def test_parsear_cursiva(self):
        """Prueba el parseo de texto en cursiva"""
        texto = "*texto en cursiva*"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "CURSIVA")
        self.assertEqual(len(ast.hijos[0].hijos), 1)
        self.assertEqual(ast.hijos[0].hijos[0].tipo, "TEXTO")
        self.assertEqual(ast.hijos[0].hijos[0].valor, "texto en cursiva")
    
    def test_parsear_lista(self):
        """Prueba el parseo de elementos de lista"""
        texto = "- Elemento de lista"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "LISTA_ITEM")
        self.assertEqual(ast.hijos[0].valor, "Elemento de lista")
    
    def test_parsear_lista_numerada(self):
        """Prueba el parseo de elementos de lista numerada"""
        texto = "1. Elemento numerado"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "LISTA_NUM_ITEM")
        self.assertEqual(ast.hijos[0].valor, "Elemento numerado")
        self.assertEqual(ast.hijos[0].numero, 1)
    
    def test_parsear_enlace(self):
        """Prueba el parseo de enlaces"""
        texto = "[texto](https://ejemplo.com)"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "ENLACE")
        self.assertEqual(ast.hijos[0].valor, "texto")
        self.assertEqual(ast.hijos[0].url, "https://ejemplo.com")
    
    def test_parsear_imagen(self):
        """Prueba el parseo de imágenes"""
        texto = "![alt](https://ejemplo.com/imagen.jpg)"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "IMAGEN")
        self.assertEqual(ast.hijos[0].valor, "alt")
        self.assertEqual(ast.hijos[0].url, "https://ejemplo.com/imagen.jpg")
    
    def test_parsear_codigo(self):
        """Prueba el parseo de bloques de código"""
        texto = "```codigo```"
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        
        self.assertEqual(len(ast.hijos), 1)
        self.assertEqual(ast.hijos[0].tipo, "CODIGO_BLOQUE")
        self.assertEqual(ast.hijos[0].valor, "codigo")
    
    def test_parsear_documento_completo(self):
        """Prueba el parseo de un documento completo"""
        texto = """# Título
        
Este es un **párrafo** con *formato*.

- Lista
- Elementos

```código