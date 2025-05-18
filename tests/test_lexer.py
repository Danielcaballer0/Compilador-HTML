"""
Pruebas unitarias para el lexer de SimpleDoc
"""

import unittest
from simpledoc.lexer import Lexer, TokenType


class TestLexer(unittest.TestCase):
    """Pruebas para el analizador léxico"""
    
    def setUp(self):
        """Configuración para las pruebas"""
        self.lexer = Lexer(nivel_complejidad=3)
    
    def test_tokenizar_titulo(self):
        """Prueba la tokenización de títulos"""
        texto = "# Título de prueba"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 2)  # Título + EOF
        self.assertEqual(tokens[0].tipo, TokenType.TITULO1)
        self.assertEqual(tokens[0].valor, "Título de prueba")
    
    def test_tokenizar_texto(self):
        """Prueba la tokenización de texto simple"""
        texto = "Este es un texto de prueba"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 2)  # Texto + EOF
        self.assertEqual(tokens[0].tipo, TokenType.TEXTO)
        self.assertEqual(tokens[0].valor, "Este es un texto de prueba")
    
    def test_tokenizar_negrita(self):
        """Prueba la tokenización de texto en negrita"""
        texto = "Texto con **negrita**"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 4)  # Texto + NegritaInicio + Texto + NegritaFin + EOF
        self.assertEqual(tokens[0].tipo, TokenType.TEXTO)
        self.assertEqual(tokens[1].tipo, TokenType.NEGRITA_INICIO)
        self.assertEqual(tokens[2].tipo, TokenType.TEXTO)
        self.assertEqual(tokens[2].valor, "negrita")
        self.assertEqual(tokens[3].tipo, TokenType.NEGRITA_FIN)
    
    def test_tokenizar_cursiva(self):
        """Prueba la tokenización de texto en cursiva"""
        texto = "Texto con *cursiva*"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 4)  # Texto + CursivaInicio + Texto + CursivaFin + EOF
        self.assertEqual(tokens[0].tipo, TokenType.TEXTO)
        self.assertEqual(tokens[1].tipo, TokenType.CURSIVA_INICIO)
        self.assertEqual(tokens[2].tipo, TokenType.TEXTO)
        self.assertEqual(tokens[2].valor, "cursiva")
        self.assertEqual(tokens[3].tipo, TokenType.CURSIVA_FIN)
    
    def test_tokenizar_lista(self):
        """Prueba la tokenización de elementos de lista"""
        texto = "- Elemento de lista"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 2)  # ListaItem + EOF
        self.assertEqual(tokens[0].tipo, TokenType.LISTA_ITEM)
        self.assertEqual(tokens[0].valor, "Elemento de lista")
    
    def test_tokenizar_lista_numerada(self):
        """Prueba la tokenización de elementos de lista numerada"""
        texto = "1. Elemento numerado"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 2)  # ListaNumItem + EOF
        self.assertEqual(tokens[0].tipo, TokenType.LISTA_NUM_ITEM)
        self.assertEqual(tokens[0].valor, "1. Elemento numerado")
    
    def test_tokenizar_enlace(self):
        """Prueba la tokenización de enlaces"""
        texto = "[texto](url)"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 2)  # Enlace + EOF
        self.assertEqual(tokens[0].tipo, TokenType.ENLACE)
        self.assertEqual(tokens[0].valor, "texto|url")
    
    def test_tokenizar_imagen(self):
        """Prueba la tokenización de imágenes"""
        texto = "![alt](url)"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 2)  # Imagen + EOF
        self.assertEqual(tokens[0].tipo, TokenType.IMAGEN)
        self.assertEqual(tokens[0].valor, "alt|url")
    
    def test_tokenizar_codigo(self):
        """Prueba la tokenización de bloques de código"""
        texto = "```codigo```"
        tokens = self.lexer.tokenizar(texto)
        
        self.assertEqual(len(tokens), 2)  # CodigoBloque + EOF
        self.assertEqual(tokens[0].tipo, TokenType.CODIGO_BLOQUE)
        self.assertEqual(tokens[0].valor, "codigo")
    
    def test_tokenizar_documento_completo(self):
        """Prueba la tokenización de un documento completo"""
        texto = """# Título
        
Este es un **párrafo** con *formato*.

- Lista
- Elementos

```código```
"""
        tokens = self.lexer.tokenizar(texto)
        
        # Verificar que se generan tokens correctamente
        self.assertGreater(len(tokens), 1)
        self.assertEqual(tokens[0].tipo, TokenType.TITULO1)
        self.assertEqual(tokens[-1].tipo, TokenType.EOF)


if __name__ == "__main__":
    unittest.main()
