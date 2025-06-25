"""
Módulo para la generación de código HTML a partir del AST
"""

import html


class HTMLGenerator:
    """
    Generador de código HTML a partir del AST
    
    Transforma un árbol de sintaxis abstracta en código HTML.
    """
    
    def __init__(self, nivel_complejidad=3):
        """
        Inicializa el generador con un nivel de complejidad específico
        
        Args:
            nivel_complejidad: Entero del 1 al 3 que determina la complejidad de la generación
                1 - Básico: Solo títulos y texto plano
                2 - Intermedio: Básico + formateo (negrita, cursiva) y listas
                3 - Avanzado: Intermedio + enlaces y bloques de código
        """
        self.nivel_complejidad = min(max(nivel_complejidad, 1), 3)
    
    def generar(self, ast):
        """
        Genera código HTML a partir del AST
        
        Args:
            ast: Árbol de sintaxis abstracta
            
        Returns:
            Código HTML generado
        """
        return self._generar_nodo(ast)
    
    def _generar_nodo(self, nodo, dentro_de_parrafo=False):
        """
        Genera código HTML para un nodo específico del AST
        
        Args:
            nodo: Nodo a procesar
            dentro_de_parrafo: Indica si el nodo está dentro de un párrafo
            
        Returns:
            Código HTML para el nodo
        """
        if nodo.tipo == "DOCUMENTO":
            return self._generar_documento(nodo)
        
        elif nodo.tipo == "TEXTO":
            return html.escape(nodo.valor)
        
        elif nodo.tipo == "SALTO_LINEA":
            return "\n"
        
        # Nivel de complejidad 1
        elif nodo.tipo == "TITULO1":
            return f"<h1>{html.escape(nodo.valor)}</h1>\n"
        
        elif nodo.tipo == "TITULO2":
            return f"<h2>{html.escape(nodo.valor)}</h2>\n"
        
        elif nodo.tipo == "TITULO3":
            return f"<h3>{html.escape(nodo.valor)}</h3>\n"
        
        # Nivel de complejidad 2
        elif self.nivel_complejidad >= 2:
            if nodo.tipo == "NEGRITA":
                contenido = self._generar_hijos(nodo, True)
                return f"<strong>{contenido}</strong>"
            
            elif nodo.tipo == "CURSIVA":
                contenido = self._generar_hijos(nodo, True)
                return f"<em>{contenido}</em>"
            
            elif nodo.tipo == "LISTA_ITEM":
                return f"<li>{html.escape(nodo.valor)}</li>\n"
            
            elif nodo.tipo == "LISTA_NUM_ITEM":
                return f'<li value="{nodo.numero}">{html.escape(nodo.valor)}</li>\n'
        
        # Nivel de complejidad 3
        elif self.nivel_complejidad >= 3:
            if nodo.tipo == "CODIGO_BLOQUE":
                return f'<pre><code>{html.escape(nodo.valor)}</code></pre>\n'
            
            elif nodo.tipo == "ENLACE":
                url = html.escape(nodo.url)
                texto = html.escape(nodo.valor)
                return f'<a href="{url}">{texto}</a>'
            
            elif nodo.tipo == "IMAGEN":
                url = html.escape(nodo.url)
                alt = html.escape(nodo.valor)
                return f'<img src="{url}" alt="{alt}">'
        
        # Tipo de nodo no reconocido
        return ""
    
    def _generar_documento(self, nodo):
        """
        Genera código HTML para el documento completo
        
        Args:
            nodo: Nodo raíz del AST
            
        Returns:
            Código HTML para el documento
        """
        html_partes = ['<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<title>Documento SimpleDoc</title>\n</head>\n<body>\n']
        
        # Procesar cada hijo del documento
        i = 0
        while i < len(nodo.hijos):
            hijo = nodo.hijos[i]
            
            # Manejar elementos de bloque (títulos, listas, código)
            if hijo.tipo in ["TITULO1", "TITULO2", "TITULO3", "CODIGO_BLOQUE"]:
                html_partes.append(self._generar_nodo(hijo))
            
            # Manejar listas
            elif hijo.tipo == "LISTA_ITEM" and self.nivel_complejidad >= 2:
                html_partes.append("<ul>\n")
                
                # Añadir todos los elementos de lista contiguos
                while i < len(nodo.hijos) and nodo.hijos[i].tipo == "LISTA_ITEM":
                    html_partes.append(self._generar_nodo(nodo.hijos[i]))
                    i += 1
                
                html_partes.append("</ul>\n")
                i -= 1  # Compensar el incremento extra en el bucle principal
            
            elif hijo.tipo == "LISTA_NUM_ITEM" and self.nivel_complejidad >= 2:
                html_partes.append("<ol>\n")
                
                # Añadir todos los elementos de lista numerada contiguos
                while i < len(nodo.hijos) and nodo.hijos[i].tipo == "LISTA_NUM_ITEM":
                    html_partes.append(self._generar_nodo(nodo.hijos[i]))
                    i += 1
                
                html_partes.append("</ol>\n")
                i -= 1  # Compensar el incremento extra en el bucle principal
            
            # Manejar elementos de línea (texto, formateo, enlaces, imágenes)
            else:
                # Agrupar elementos de línea en párrafos
                en_parrafo = False
                parrafo_partes = []
                
                while i < len(nodo.hijos):
                    hijo_actual = nodo.hijos[i]
                    
                    # Si encontramos un elemento de bloque, terminamos el párrafo
                    if hijo_actual.tipo in ["TITULO1", "TITULO2", "TITULO3", "LISTA_ITEM", "LISTA_NUM_ITEM", "CODIGO_BLOQUE"]:
                        break
                    
                    # Si encontramos varios saltos de línea consecutivos, terminamos el párrafo
                    if hijo_actual.tipo == "SALTO_LINEA":
                        if i + 1 < len(nodo.hijos) and nodo.hijos[i + 1].tipo == "SALTO_LINEA":
                            i += 1  # Consumimos un salto de línea
                            break
                    
                    # Añadir elemento al párrafo
                    contenido = self._generar_nodo(hijo_actual, True)
                    if contenido.strip():
                        parrafo_partes.append(contenido)
                        en_parrafo = True
                    
                    i += 1
                
                # Cerrar el párrafo si hay contenido
                if en_parrafo:
                    parrafo = "".join(parrafo_partes).strip()
                    html_partes.append(f"<p>{parrafo}</p>\n")
                
                i -= 1  # Compensar el incremento extra en el bucle principal
            
            i += 1
        
        html_partes.append('</body>\n</html>')
        return "".join(html_partes)
    
    def _generar_hijos(self, nodo, dentro_de_parrafo=False):
        """
        Genera código HTML para los hijos de un nodo
        
        Args:
            nodo: Nodo cuyos hijos se procesarán
            dentro_de_parrafo: Indica si los hijos están dentro de un párrafo
            
        Returns:
            Código HTML para los hijos
        """
        resultado = []
        for hijo in nodo.hijos:
            resultado.append(self._generar_nodo(hijo, dentro_de_parrafo))
        return "".join(resultado)
