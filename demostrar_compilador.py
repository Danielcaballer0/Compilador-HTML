
import os
import sys
from simpledoc.lexer import Lexer
from simpledoc.parser import Parser
from simpledoc.validator import Validator
from simpledoc.html_generator import HTMLGenerator
from simpledoc.ast_generator import ASTGenerator

def mostrar_tokens(tokens):
    """Muestra los tokens generados por el lexer"""
    print("\n=== TOKENS GENERADOS (Análisis Léxico) ===")
    for token in tokens[:20]:  # Mostrar solo los primeros 20 tokens
        print(f"  {token}")
    if len(tokens) > 20:
        print(f"  ... y {len(tokens) - 20} tokens más")

def mostrar_ast(ast):
    """Muestra el AST generado por el parser"""
    print("\n=== ÁRBOL DE SINTAXIS ABSTRACTA (AST) ===")
    ast_generator = ASTGenerator()
    ast_generator.imprimir_ast(ast)

def validar_documento(validator, ast):
    """Valida el documento y muestra el resultado"""
    print("\n=== VALIDACIÓN DEL DOCUMENTO ===")
    try:
        validator.validar(ast)
        print("  El documento es válido.")
    except Exception as e:
        print(f"  Error de validación: {str(e)}")

def generar_html(generator, ast):
    """Genera el HTML final y muestra un fragmento"""
    print("\n=== GENERACIÓN DE CÓDIGO HTML ===")
    html = generator.generar(ast)
    
    # Mostrar una parte del HTML generado
    preview_length = 500
    if len(html) > preview_length:
        preview = html[:preview_length] + "..."
    else:
        preview = html
    
    print(preview)
    return html

def proceso_completo(archivo_entrada, nivel_complejidad=3):
    """Muestra el proceso completo de compilación"""
    
    print(f"\n*** COMPILANDO ARCHIVO: {archivo_entrada} (Nivel: {nivel_complejidad}) ***\n")
    
    try:
        # Leer el archivo de entrada
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            texto_entrada = f.read()
        
        print(f"Contenido del archivo ({len(texto_entrada)} caracteres):")
        preview_length = 200
        if len(texto_entrada) > preview_length:
            preview = texto_entrada[:preview_length] + "..."
        else:
            preview = texto_entrada
        print(preview)
        
        # 1. Análisis léxico (tokenización)
        lexer = Lexer(nivel_complejidad)
        tokens = lexer.tokenizar(texto_entrada)
        mostrar_tokens(tokens)
        
        # 2. Análisis sintáctico (generación del AST)
        parser = Parser(nivel_complejidad)
        ast = parser.parsear(tokens)
        mostrar_ast(ast)
        
        # 3. Validación del documento
        validator = Validator(nivel_complejidad)
        validar_documento(validator, ast)
        
        # 4. Generación de código HTML
        generator = HTMLGenerator(nivel_complejidad)
        html = generar_html(generator, ast)
        
        # Guardar el HTML generado
        archivo_salida = archivo_entrada.rsplit('.', 1)[0] + '.html'
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n*** COMPILACIÓN EXITOSA: {archivo_salida} ***")
        return True
        
    except Exception as e:
        print(f"\n*** ERROR DE COMPILACIÓN: {str(e)} ***")
        return False

if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <archivo.sd> [nivel_complejidad]")
        sys.exit(1)
    
    archivo = sys.argv[1]
    nivel = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    if not os.path.isfile(archivo):
        print(f"Error: El archivo {archivo} no existe")
        sys.exit(1)
    
    exito = proceso_completo(archivo, nivel)
    sys.exit(0 if exito else 1)