#!/usr/bin/env python3
"""
Punto de entrada principal para el compilador SimpleDoc

Este script proporciona una interfaz de línea de comandos para el compilador,
permitiendo compilar archivos SimpleDoc a HTML directamente desde la terminal.
También inicia una interfaz web para usar el compilador de manera interactiva.
"""

import argparse
import logging
import os
import sys
from simpledoc.compiler import Compiler
from simpledoc.exceptions import SimpleDocError

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger('simpledoc')

# Importar la aplicación Flask para que Gunicorn pueda encontrarla
from web_interface import app

def compilar_archivo(archivo_entrada, archivo_salida=None, nivel_complejidad=3, modo_debug=False):
    """
    Compila un archivo SimpleDoc a HTML
    
    Args:
        archivo_entrada: Ruta del archivo de entrada
        archivo_salida: Ruta del archivo de salida (opcional)
        nivel_complejidad: Nivel de complejidad del compilador (1-3)
        modo_debug: Activa el modo de depuración
        
    Returns:
        True si la compilación fue exitosa, False en caso contrario
    """
    try:
        # Crear compilador
        compiler = Compiler(nivel_complejidad, modo_debug)
        
        # Compilar archivo
        ruta_salida = compiler.compilar_archivo(archivo_entrada, archivo_salida)
        
        logger.info(f"Archivo compilado exitosamente: {ruta_salida}")
        return True
        
    except SimpleDocError as e:
        logger.error(f"Error al compilar: {e}")
        return False
    except IOError as e:
        logger.error(f"Error de E/S: {e}")
        return False


def main():
    """Función principal del script"""
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(
        description='Compilador de SimpleDoc a HTML',
        epilog='Ejemplo: python main.py archivo.sd -o archivo.html -c 2'
    )
    
    # Agregar argumentos
    parser.add_argument('archivo', nargs='?', help='Archivo de entrada SimpleDoc a compilar')
    parser.add_argument('-o', '--output', help='Archivo de salida HTML')
    parser.add_argument('-c', '--complejidad', type=int, choices=[1, 2, 3], default=3,
                        help='Nivel de complejidad (1: básico, 2: intermedio, 3: avanzado)')
    parser.add_argument('-d', '--debug', action='store_true', help='Activa el modo de depuración')
    parser.add_argument('-w', '--web', action='store_true', help='Inicia la interfaz web')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Configurar nivel de logging según modo debug
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    # Iniciar interfaz web si se especifica
    if args.web:
        try:
            # Ejecutar la aplicación Flask directamente
            logger.info("Iniciando interfaz web en http://0.0.0.0:5000")
            app.run(host='0.0.0.0', port=5000)
            return 0
        except ImportError:
            logger.error("No se pudo iniciar la interfaz web. Asegúrate de tener Flask instalado.")
            return 1
    
    # Verificar si se especificó un archivo
    if not args.archivo:
        parser.print_help()
        return 1
    
    # Verificar si el archivo existe
    if not os.path.isfile(args.archivo):
        logger.error(f"El archivo {args.archivo} no existe")
        return 1
    
    # Compilar archivo
    exito = compilar_archivo(
        args.archivo,
        args.output,
        args.complejidad,
        args.debug
    )
    
    return 0 if exito else 1


if __name__ == "__main__":
    sys.exit(main())
