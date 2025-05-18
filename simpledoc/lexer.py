"""
Módulo para el análisis léxico de documentos SimpleDoc
"""

import re
from enum import Enum, auto
from .exceptions import LexerError


class TokenType(Enum):
    """Tipos de tokens reconocidos por el lexer"""
    TITULO1 = auto()       # # Título
    TITULO2 = auto()       # ## Título
    TITULO3 = auto()       # ### Título
    NEGRITA_INICIO = auto()  # **
    NEGRITA_FIN = auto()     # **
    CURSIVA_INICIO = auto()  # *
    CURSIVA_FIN = auto()     # *
    LISTA_ITEM = auto()    # - Item
    LISTA_NUM_ITEM = auto()  # 1. Item
    CODIGO_BLOQUE = auto() # ```
    ENLACE = auto()        # [texto](url)
    IMAGEN = auto()        # ![alt](url)
    TEXTO = auto()         # Texto normal
    SALTO_LINEA = auto()   # \n
    EOF = auto()           # Fin de archivo


class Token:
    """Representa un token identificado en el documento"""
    
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def __repr__(self):
        return f"Token(tipo={self.tipo}, valor='{self.valor}', linea={self.linea}, columna={self.columna})"


class Lexer:
    """
    Analizador léxico para el lenguaje SimpleDoc
    
    Convierte un texto de entrada en una secuencia de tokens.
    """
    
    def __init__(self, nivel_complejidad=3):
        """
        Inicializa el lexer con un nivel de complejidad específico
        
        Args:
            nivel_complejidad: Entero del 1 al 3 que determina la complejidad del análisis
                1 - Básico: Solo títulos y texto plano
                2 - Intermedio: Básico + formateo (negrita, cursiva) y listas
                3 - Avanzado: Intermedio + enlaces, imágenes y bloques de código
        """
        self.texto = ""
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.nivel_complejidad = min(max(nivel_complejidad, 1), 3)
        
        # Definir patrones según nivel de complejidad
        self.patrones = [
            # Patrones básicos (nivel 1)
            (r'^# (.+)$', self._procesar_titulo1),
            (r'^## (.+)$', self._procesar_titulo2),
            (r'^### (.+)$', self._procesar_titulo3),
        ]
        
        if self.nivel_complejidad >= 2:
            # Patrones intermedios (nivel 2)
            self.patrones.extend([
                (r'\*\*([^*]+)\*\*', self._procesar_negrita),
                (r'\*([^*]+)\*', self._procesar_cursiva),
                (r'^- (.+)$', self._procesar_lista_item),
                (r'^(\d+)\. (.+)$', self._procesar_lista_num_item),
            ])
            
        if self.nivel_complejidad >= 3:
            # Patrones avanzados (nivel 3)
            self.patrones.extend([
                (r'```([^`]*)```', self._procesar_codigo_bloque),
                (r'\[([^\]]+)\]\(([^)]+)\)', self._procesar_enlace),
                (r'!\[([^\]]*)\]\(([^)]+)\)', self._procesar_imagen),
            ])
    
    def tokenizar(self, texto):
        """
        Convierte el texto de entrada en una lista de tokens
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Lista de tokens
        """
        self.texto = texto
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        
        # Procesar línea por línea
        lineas = self.texto.split('\n')
        for i, linea in enumerate(lineas):
            self.linea = i + 1
            self.columna = 1
            
            # Si la línea está vacía, añadir un salto de línea
            if not linea.strip():
                self.tokens.append(Token(TokenType.SALTO_LINEA, '\n', self.linea, self.columna))
                continue
            
            # Intentar aplicar patrones especiales primero
            linea_procesada = False
            for patron, procesador in self.patrones:
                if re.match(patron, linea):
                    procesador(linea)
                    linea_procesada = True
                    break
            
            # Si no se aplicó ningún patrón especial, procesar como texto normal
            if not linea_procesada:
                # Procesar la línea buscando patrones en medio del texto
                pos = 0
                while pos < len(linea):
                    match_encontrado = False
                    
                    # Patrones que pueden estar en medio del texto
                    for patron, procesador in self.patrones:
                        if not patron.startswith('^'):  # Solo patrones que no requieren inicio de línea
                            match = re.search(patron, linea[pos:])
                            if match and match.start() == 0:
                                nuevo_pos = pos + match.end()
                                procesador(linea[pos:nuevo_pos])
                                pos = nuevo_pos
                                match_encontrado = True
                                break
                    
                    if not match_encontrado:
                        # Extraer texto hasta el próximo patrón especial o fin de línea
                        siguiente_especial = float('inf')
                        for patron, _ in self.patrones:
                            if not patron.startswith('^'):
                                match = re.search(patron, linea[pos:])
                                if match:
                                    siguiente_especial = min(siguiente_especial, pos + match.start())
                        
                        if siguiente_especial == float('inf'):
                            texto_normal = linea[pos:]
                            pos = len(linea)
                        else:
                            texto_normal = linea[pos:siguiente_especial]
                            pos = siguiente_especial
                        
                        if texto_normal:
                            self.tokens.append(Token(TokenType.TEXTO, texto_normal, self.linea, self.columna))
                            self.columna += len(texto_normal)
            
            # Añadir salto de línea al final de cada línea a menos que sea la última
            if i < len(lineas) - 1:
                self.tokens.append(Token(TokenType.SALTO_LINEA, '\n', self.linea, self.columna))
        
        # Añadir token de fin de archivo
        self.tokens.append(Token(TokenType.EOF, '', self.linea, self.columna))
        
        return self.tokens
    
    def _procesar_titulo1(self, linea):
        """Procesa un título de nivel 1"""
        match = re.match(r'^# (.+)$', linea)
        if match:
            contenido = match.group(1)
            self.tokens.append(Token(TokenType.TITULO1, contenido, self.linea, self.columna))
            self.columna += len(linea)
    
    def _procesar_titulo2(self, linea):
        """Procesa un título de nivel 2"""
        match = re.match(r'^## (.+)$', linea)
        if match:
            contenido = match.group(1)
            self.tokens.append(Token(TokenType.TITULO2, contenido, self.linea, self.columna))
            self.columna += len(linea)
    
    def _procesar_titulo3(self, linea):
        """Procesa un título de nivel 3"""
        match = re.match(r'^### (.+)$', linea)
        if match:
            contenido = match.group(1)
            self.tokens.append(Token(TokenType.TITULO3, contenido, self.linea, self.columna))
            self.columna += len(linea)
    
    def _procesar_negrita(self, texto):
        """Procesa texto en negrita"""
        match = re.match(r'\*\*([^*]+)\*\*', texto)
        if match:
            contenido = match.group(1)
            self.tokens.append(Token(TokenType.NEGRITA_INICIO, '**', self.linea, self.columna))
            self.columna += 2
            self.tokens.append(Token(TokenType.TEXTO, contenido, self.linea, self.columna))
            self.columna += len(contenido)
            self.tokens.append(Token(TokenType.NEGRITA_FIN, '**', self.linea, self.columna))
            self.columna += 2
    
    def _procesar_cursiva(self, texto):
        """Procesa texto en cursiva"""
        match = re.match(r'\*([^*]+)\*', texto)
        if match:
            contenido = match.group(1)
            self.tokens.append(Token(TokenType.CURSIVA_INICIO, '*', self.linea, self.columna))
            self.columna += 1
            self.tokens.append(Token(TokenType.TEXTO, contenido, self.linea, self.columna))
            self.columna += len(contenido)
            self.tokens.append(Token(TokenType.CURSIVA_FIN, '*', self.linea, self.columna))
            self.columna += 1
    
    def _procesar_lista_item(self, linea):
        """Procesa un elemento de lista no ordenada"""
        match = re.match(r'^- (.+)$', linea)
        if match:
            contenido = match.group(1)
            self.tokens.append(Token(TokenType.LISTA_ITEM, contenido, self.linea, self.columna))
            self.columna += len(linea)
    
    def _procesar_lista_num_item(self, linea):
        """Procesa un elemento de lista ordenada"""
        match = re.match(r'^(\d+)\. (.+)$', linea)
        if match:
            numero = match.group(1)
            contenido = match.group(2)
            self.tokens.append(Token(TokenType.LISTA_NUM_ITEM, f"{numero}. {contenido}", self.linea, self.columna))
            self.columna += len(linea)
    
    def _procesar_codigo_bloque(self, texto):
        """Procesa un bloque de código"""
        match = re.match(r'```([^`]*)```', texto)
        if match:
            contenido = match.group(1)
            self.tokens.append(Token(TokenType.CODIGO_BLOQUE, contenido, self.linea, self.columna))
            self.columna += len(texto)
    
    def _procesar_enlace(self, texto):
        """Procesa un enlace"""
        match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', texto)
        if match:
            texto_enlace = match.group(1)
            url = match.group(2)
            self.tokens.append(Token(TokenType.ENLACE, f"{texto_enlace}|{url}", self.linea, self.columna))
            self.columna += len(texto)
    
    def _procesar_imagen(self, texto):
        """Procesa una imagen"""
        match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', texto)
        if match:
            alt_text = match.group(1)
            url = match.group(2)
            self.tokens.append(Token(TokenType.IMAGEN, f"{alt_text}|{url}", self.linea, self.columna))
            self.columna += len(texto)
