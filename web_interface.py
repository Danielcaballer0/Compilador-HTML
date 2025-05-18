"""
Interfaz web para el compilador SimpleDoc

Proporciona una interfaz gráfica para utilizar el compilador de manera interactiva.
"""

import os
from flask import Flask, render_template, request, flash, jsonify
from simpledoc.compiler import Compiler
from simpledoc.exceptions import SimpleDocError

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
    
    try:
        # Crear compilador con el nivel de complejidad especificado
        compiler = Compiler(nivel_complejidad=nivel_complejidad)
        
        # Compilar código
        html_generado = compiler.compilar(codigo)
        
        return jsonify({
            'success': True,
            'html': html_generado,
            'mensaje': 'Compilación exitosa'
        })
        
    except SimpleDocError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'mensaje': 'Error de compilación'
        })


@app.route('/ayuda')
def ayuda():
    """Página de ayuda con documentación del lenguaje"""
    return render_template('result.html', 
                          titulo='Ayuda de SimpleDoc',
                          contenido=obtener_documentacion_html())


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
