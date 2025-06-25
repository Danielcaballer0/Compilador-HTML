# Proyecto Compiladores - SimpleDoc Compiler

Este proyecto es un compilador para un subconjunto simplificado de un lenguaje llamado **SimpleDoc**. El compilador es capaz de analizar la estructura de un documento, validar la sintaxis, generar un árbol de sintaxis abstracta (AST) y transformar el AST en código HTML.

## Características

- Análisis léxico, sintáctico y semántico de documentos SimpleDoc.
- Generación de un árbol de sintaxis abstracta (AST).
- Validación de la estructura y semántica del documento.
- Generación de código HTML a partir del AST.
- Soporte para diferentes niveles de complejidad:
  - Nivel 1: Títulos y texto plano.
  - Nivel 2: Formateo (negrita, cursiva) y listas.
  - Nivel 3: Enlaces, imágenes y bloques de código.
- Modo de depuración para mostrar información detallada del proceso.
- Interfaz de línea de comandos (CLI) para compilar archivos SimpleDoc.
- Interfaz web para compilar documentos de forma interactiva.

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. (Opcional) Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Línea de comandos

Para compilar un archivo SimpleDoc a HTML desde la terminal:

```bash
python main.py archivo.sd -o archivo.html -c 3
```

Opciones:

- `archivo.sd`: Archivo de entrada en formato SimpleDoc.
- `-o archivo.html`: Archivo de salida HTML (opcional).
- `-c [1-3]`: Nivel de complejidad (1: básico, 2: intermedio, 3: avanzado).
- `-d`: Activar modo depuración.
- `-w`: Iniciar la interfaz web.

### Interfaz web

Para iniciar la interfaz web interactiva:

```bash
python main.py -w
```

Luego abrir en el navegador: `http://localhost:5000`

## Estructura del proyecto

- `main.py`: Punto de entrada principal, CLI y servidor web.
- `simpledoc/`: Código fuente del compilador.
  - `lexer.py`: Análisis léxico.
  - `parser.py`: Análisis sintáctico y definición del AST.
  - `validator.py`: Validación del AST.
  - `ast_generator.py`: Generación del AST.
  - `compiler.py`: Coordinación del proceso de compilación.
  - `html_generator.py`: Generación de código HTML.
  - `exceptions.py`: Definición de excepciones personalizadas.
- `web_interface.py`: Código de la interfaz web con Flask.
- `tests/`: Pruebas unitarias.
- `ejemplos/`: Archivos de ejemplo en formato SimpleDoc.
- `static/` y `templates/`: Archivos estáticos y plantillas para la interfaz web.

## Licencia

Este proyecto está bajo la licencia MIT. Consulte el archivo LICENSE para más detalles.
