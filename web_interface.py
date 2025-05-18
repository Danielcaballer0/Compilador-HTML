"""
Interfaz web para el compilador SimpleDoc

Proporciona una interfaz gráfica para utilizar el compilador de manera interactiva.
"""

import os
from flask import Flask, render_template, request, flash, jsonify
from simpledoc.compiler import Compiler
from simpledoc.exceptions import SimpleDocError
from simpledoc.lexer import Lexer
from simpledoc.parser import Parser
from simpledoc.validator import Validator
from simpledoc.html_generator import HTMLGenerator
from simpledoc.ast_generator import ASTGenerator

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "simpledoc_secret_key")

# Compilador por defecto (nivel de complejidad 3)
default_compiler = Compiler(nivel_complejidad=3)


@app.route('/')
def index():
    """Página principal con editor y opciones de compilación"""
    return render_template('index.html')


@app.route('/compilar', methods=['POST'])
def compilar():
    """
    Compila el código SimpleDoc enviado y devuelve el HTML generado
    
    Returns:
        JSON con el resultado de la compilación
    """
    # Obtener datos del formulario
    codigo = request.form.get('codigo', '')
    nivel_complejidad = int(request.form.get('nivel_complejidad', 3))
    modo_detallado = request.form.get('modo_detallado', 'false') == 'true'
    
    try:
        if not modo_detallado:
            # Modo normal: usar el compilador directamente
            compiler = Compiler(nivel_complejidad=nivel_complejidad)
            html_generado = compiler.compilar(codigo)
            
            return jsonify({
                'success': True,
                'html': html_generado,
                'mensaje': 'Compilación exitosa',
                'detalles': None
            })
        else:
            # Modo detallado: mostrar cada etapa del proceso
            detalles = procesar_detallado(codigo, nivel_complejidad)
            
            return jsonify({
                'success': True,
                'html': detalles['html'],
                'mensaje': 'Compilación exitosa con detalles',
                'detalles': detalles
            })
        
    except SimpleDocError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'mensaje': 'Error de compilación',
            'detalles': None
        })


def procesar_detallado(codigo, nivel_complejidad):
    """
    Procesa el código SimpleDoc mostrando cada etapa del proceso de compilación
    
    Args:
        codigo: Texto SimpleDoc a compilar
        nivel_complejidad: Nivel de complejidad (1-3)
        
    Returns:
        Diccionario con detalles de cada etapa
    """
    # 1. Análisis léxico (tokenización)
    lexer = Lexer(nivel_complejidad)
    tokens = lexer.tokenizar(codigo)
    
    # Formatear tokens para mostrar
    tokens_formateados = []
    for i, token in enumerate(tokens[:30]):  # Mostrar solo los primeros 30 tokens
        tokens_formateados.append({
            'tipo': str(token.tipo),
            'valor': token.valor,
            'linea': token.linea,
            'columna': token.columna
        })
    tokens_info = {
        'tokens': tokens_formateados,
        'total': len(tokens),
        'mostrados': min(30, len(tokens))
    }
    
    # 2. Análisis sintáctico (generación del AST)
    parser = Parser(nivel_complejidad)
    ast = parser.parsear(tokens)
    
    # Formatear AST para mostrar (capturando la salida de imprimir_ast)
    import io
    import sys
    ast_generator = ASTGenerator(nivel_complejidad)
    
    # Capturar la salida de la función imprimir_ast
    stdout_original = sys.stdout
    string_io = io.StringIO()
    sys.stdout = string_io
    
    ast_generator.imprimir_ast(ast)
    
    # Restaurar stdout y obtener el texto capturado
    sys.stdout = stdout_original
    ast_texto = string_io.getvalue()
    
    # 3. Validación del documento
    validator = Validator(nivel_complejidad)
    try:
        validator.validar(ast)
        validacion_exitosa = True
        validacion_mensaje = "El documento es válido."
    except Exception as e:
        validacion_exitosa = False
        validacion_mensaje = str(e)
    
    # 4. Generación de código HTML
    generator = HTMLGenerator(nivel_complejidad)
    html = generator.generar(ast)
    
    # Devolver todos los detalles
    return {
        'tokens': tokens_info,
        'ast': ast_texto,
        'validacion': {
            'exitosa': validacion_exitosa,
            'mensaje': validacion_mensaje
        },
        'html': html
    }


@app.route('/ayuda')
def ayuda():
    """Página de ayuda con documentación del lenguaje"""
    return render_template('result.html', 
                          titulo='Ayuda de SimpleDoc',
                          contenido=obtener_documentacion_html())


@app.route('/demo')
def demo():
    """Página de demostración que muestra el proceso completo de compilación"""
    return render_template('demo.html')


def obtener_documentacion_html():
    """
    Genera HTML con la documentación del lenguaje SimpleDoc
    
    Returns:
        HTML con la documentación
    """
    # Documentación en SimpleDoc
    doc_simpledoc = """
# Guía de uso de SimpleDoc

## Introducción
SimpleDoc es un lenguaje de marcado simplificado que permite crear documentos HTML de manera sencilla.

## Sintaxis básica

### Títulos
# Título de nivel 1
## Título de nivel 2
### Título de nivel 3

### Texto
Texto normal sin formato.

## Sintaxis intermedia

### Formateo de texto
**Texto en negrita**
*Texto en cursiva*

### Listas
- Elemento de lista no ordenada
- Otro elemento

1. Elemento de lista ordenada
2. Segundo elemento

## Sintaxis avanzada

### Enlaces
[Texto del enlace](https://ejemplo.com)

### Imágenes
![Texto alternativo](https://ejemplo.com/imagen.jpg)

### Bloques de código
```
function ejemplo() {
  console.log("Este es un bloque de código");
}
```
"""
    
    # Compilar la documentación usando el compilador
    try:
        html = default_compiler.compilar(doc_simpledoc)
        return html
    except Exception as e:
        return f"<p>Error al generar la documentación: {str(e)}</p>"


# Función para iniciar la aplicación web
def iniciar_app():
    """Inicia la aplicación web Flask"""
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    iniciar_app()
