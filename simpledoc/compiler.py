"""
Módulo principal que coordina todo el proceso de compilación
"""

from .lexer import Lexer
from .parser import Parser
from .validator import Validator
from .ast_generator import ASTGenerator
from .html_generator import HTMLGenerator
from .exceptions import SimpleDocError


class Compiler:
    """
    Compilador principal para el lenguaje SimpleDoc
    
    Coordina todo el proceso de compilación desde el texto de entrada
    hasta la generación del código HTML.
    """
    
    def __init__(self, nivel_complejidad=3, modo_debug=False):
        """
        Inicializa el compilador con un nivel de complejidad específico
        
        Args:
            nivel_complejidad: Entero del 1 al 3 que determina la complejidad del compilador
                1 - Básico: Solo títulos y texto plano
                2 - Intermedio: Básico + formateo (negrita, cursiva) y listas
                3 - Avanzado: Intermedio + enlaces, imágenes y bloques de código
            modo_debug: Indica si el compilador debe imprimir información de depuración
        """
        self.nivel_complejidad = min(max(nivel_complejidad, 1), 3)
        self.modo_debug = modo_debug
        
        # Inicializar componentes
        self.lexer = Lexer(nivel_complejidad)
        self.parser = Parser(nivel_complejidad)
        self.validator = Validator(nivel_complejidad)
        self.ast_generator = ASTGenerator(nivel_complejidad)
        self.html_generator = HTMLGenerator(nivel_complejidad)
    
    def compilar(self, texto_entrada):
        """
        Compila un texto de entrada en SimpleDoc a HTML
        
        Args:
            texto_entrada: Texto a compilar
            
        Returns:
            Código HTML generado
            
        Raises:
            SimpleDocError: Si ocurre algún error durante la compilación
        """
        try:
            # Paso 1: Análisis léxico
            tokens = self.lexer.tokenizar(texto_entrada)
            
            if self.modo_debug:
                print("--- Tokens generados ---")
                for token in tokens:
                    print(token)
            
            # Paso 2: Análisis sintáctico y generación del AST
            ast = self.parser.parsear(tokens)
            
            if self.modo_debug:
                print("\n--- AST generado ---")
                self.ast_generator.imprimir_ast(ast)
            
            # Paso 3: Validación del AST
            self.validator.validar(ast)
            
            if self.modo_debug:
                print("\n--- Validación exitosa ---")
            
            # Paso 4: Generación de HTML
            html = self.html_generator.generar(ast)
            
            if self.modo_debug:
                print("\n--- HTML generado ---")
                print(html[:200] + "..." if len(html) > 200 else html)
            
            return html
            
        except SimpleDocError as e:
            if self.modo_debug:
                print(f"\n--- Error de compilación ---\n{str(e)}")
            raise
    
    def compilar_archivo(self, ruta_entrada, ruta_salida=None):
        """
        Compila un archivo de entrada en SimpleDoc a HTML
        
        Args:
            ruta_entrada: Ruta del archivo de entrada
            ruta_salida: Ruta del archivo de salida. Si es None, se usa el nombre
                         del archivo de entrada con extensión .html
            
        Returns:
            Ruta del archivo de salida
            
        Raises:
            SimpleDocError: Si ocurre algún error durante la compilación
            IOError: Si ocurre un error de E/S al leer o escribir archivos
        """
        if not ruta_salida:
            # Cambiar la extensión a .html
            if ruta_entrada.endswith(('.sd', '.simpledoc')):
                ruta_salida = ruta_entrada.rsplit('.', 1)[0] + '.html'
            else:
                ruta_salida = ruta_entrada + '.html'
        
        try:
            # Leer archivo de entrada
            with open(ruta_entrada, 'r', encoding='utf-8') as f:
                texto_entrada = f.read()
            
            # Compilar
            html = self.compilar(texto_entrada)
            
            # Escribir archivo de salida
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(html)
            
            return ruta_salida
            
        except IOError as e:
            raise IOError(f"Error de E/S: {str(e)}")
        except SimpleDocError:
            raise
