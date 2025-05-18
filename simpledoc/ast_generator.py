"""
Módulo para la generación del árbol de sintaxis abstracta (AST)
"""

from .lexer import Lexer, TokenType
from .parser import Parser


class ASTGenerator:
    """
    Generador de AST para el lenguaje SimpleDoc
    
    Coordina el lexer y el parser para generar el árbol de sintaxis abstracta.
    """
    
    def __init__(self, nivel_complejidad=3):
        """
        Inicializa el generador con un nivel de complejidad específico
        
        Args:
            nivel_complejidad: Entero del 1 al 3 que determina la complejidad del análisis
                1 - Básico: Solo títulos y texto plano
                2 - Intermedio: Básico + formateo (negrita, cursiva) y listas
                3 - Avanzado: Intermedio + enlaces, imágenes y bloques de código
        """
        self.lexer = Lexer(nivel_complejidad)
        self.parser = Parser(nivel_complejidad)
        self.nivel_complejidad = nivel_complejidad
    
    def generar_ast(self, texto):
        """
        Genera el AST a partir del texto de entrada
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Nodo raíz del AST
        """
        tokens = self.lexer.tokenizar(texto)
        ast = self.parser.parsear(tokens)
        return ast
    
    def imprimir_ast(self, nodo, nivel=0):
        """
        Imprime el AST con formato legible
        
        Args:
            nodo: Nodo a imprimir
            nivel: Nivel de indentación
        """
        indent = "  " * nivel
        
        # Imprimir información del nodo
        if hasattr(nodo, 'url'):
            print(f"{indent}- {nodo.tipo}: {nodo.valor} (URL: {nodo.url})")
        elif hasattr(nodo, 'numero'):
            print(f"{indent}- {nodo.tipo}: {nodo.valor} (Número: {nodo.numero})")
        elif nodo.valor:
            print(f"{indent}- {nodo.tipo}: {nodo.valor}")
        else:
            print(f"{indent}- {nodo.tipo}")
        
        # Imprimir hijos recursivamente
        for hijo in nodo.hijos:
            self.imprimir_ast(hijo, nivel + 1)
