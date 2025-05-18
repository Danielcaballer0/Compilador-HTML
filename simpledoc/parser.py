"""
Módulo para el análisis sintáctico de documentos SimpleDoc
"""

from .lexer import TokenType
from .exceptions import ParserError


class ASTNode:
    """Nodo base para el árbol de sintaxis abstracta"""
    
    def __init__(self, tipo, valor=None, hijos=None, linea=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos or []
        self.linea = linea
    
    def __repr__(self):
        return f"ASTNode(tipo={self.tipo}, valor={self.valor}, hijos={len(self.hijos)}, linea={self.linea})"
    
    def add_hijo(self, hijo):
        """Añade un hijo al nodo"""
        self.hijos.append(hijo)


class Parser:
    """
    Analizador sintáctico para el lenguaje SimpleDoc
    
    Convierte una secuencia de tokens en un árbol de sintaxis abstracta (AST).
    """
    
    def __init__(self, nivel_complejidad=3):
        """
        Inicializa el parser con un nivel de complejidad específico
        
        Args:
            nivel_complejidad: Entero del 1 al 3 que determina la complejidad del análisis
                1 - Básico: Solo títulos y texto plano
                2 - Intermedio: Básico + formateo (negrita, cursiva) y listas
                3 - Avanzado: Intermedio + enlaces, imágenes y bloques de código
        """
        self.tokens = []
        self.posicion = 0
        self.nivel_complejidad = min(max(nivel_complejidad, 1), 3)
    
    def parsear(self, tokens):
        """
        Convierte una lista de tokens en un árbol de sintaxis abstracta
        
        Args:
            tokens: Lista de tokens generada por el lexer
            
        Returns:
            Nodo raíz del AST
        """
        self.tokens = tokens
        self.posicion = 0
        
        # Crear nodo raíz para el documento
        raiz = ASTNode("DOCUMENTO")
        
        # Procesar tokens mientras no lleguemos al final
        while not self._es_fin():
            nodo = self._parsear_elemento()
            if nodo:
                raiz.add_hijo(nodo)
        
        return raiz
    
    def _token_actual(self):
        """Devuelve el token actual sin avanzar"""
        return None if self._es_fin() else self.tokens[self.posicion]
    
    def _avanzar(self):
        """Avanza al siguiente token"""
        token = self._token_actual()
        self.posicion += 1
        return token
    
    def _es_fin(self):
        """Comprueba si hemos llegado al final de los tokens"""
        return self.posicion >= len(self.tokens) or self.tokens[self.posicion].tipo == TokenType.EOF
    
    def _consumir(self, tipo_token):
        """
        Consume un token del tipo específico y avanza
        
        Args:
            tipo_token: Tipo de token esperado
            
        Returns:
            El token consumido
            
        Raises:
            ParserError: Si el tipo de token no coincide con el esperado
        """
        token = self._token_actual()
        
        if not token or token.tipo != tipo_token:
            tipo_actual = token.tipo if token else "fin de archivo"
            raise ParserError(
                f"Se esperaba token de tipo {tipo_token}, pero se encontró {tipo_actual}",
                token.linea if token else None,
                token.valor if token else None
            )
        
        self._avanzar()
        return token
    
    def _parsear_elemento(self):
        """
        Parsea un elemento del documento
        
        Returns:
            Nodo AST correspondiente al elemento parseado
        """
        token = self._token_actual()
        
        if not token:
            return None
        
        # Manejar diferentes tipos de tokens
        if token.tipo == TokenType.SALTO_LINEA:
            self._avanzar()
            return ASTNode("SALTO_LINEA", linea=token.linea)
        
        elif token.tipo == TokenType.TITULO1:
            self._avanzar()
            return ASTNode("TITULO1", token.valor, linea=token.linea)
        
        elif token.tipo == TokenType.TITULO2:
            self._avanzar()
            return ASTNode("TITULO2", token.valor, linea=token.linea)
        
        elif token.tipo == TokenType.TITULO3:
            self._avanzar()
            return ASTNode("TITULO3", token.valor, linea=token.linea)
        
        elif token.tipo == TokenType.TEXTO:
            self._avanzar()
            return ASTNode("TEXTO", token.valor, linea=token.linea)
        
        # Nivel de complejidad 2 o superior
        elif self.nivel_complejidad >= 2:
            if token.tipo == TokenType.NEGRITA_INICIO:
                return self._parsear_negrita()
            
            elif token.tipo == TokenType.CURSIVA_INICIO:
                return self._parsear_cursiva()
            
            elif token.tipo == TokenType.LISTA_ITEM:
                self._avanzar()
                return ASTNode("LISTA_ITEM", token.valor, linea=token.linea)
            
            elif token.tipo == TokenType.LISTA_NUM_ITEM:
                self._avanzar()
                # Extraer el número y el contenido
                partes = token.valor.split('. ', 1)
                numero = int(partes[0])
                contenido = partes[1]
                nodo = ASTNode("LISTA_NUM_ITEM", contenido, linea=token.linea)
                nodo.numero = numero
                return nodo
        
        # Nivel de complejidad 3
        elif self.nivel_complejidad >= 3:
            if token.tipo == TokenType.CODIGO_BLOQUE:
                self._avanzar()
                return ASTNode("CODIGO_BLOQUE", token.valor, linea=token.linea)
            
            elif token.tipo == TokenType.ENLACE:
                self._avanzar()
                texto, url = token.valor.split('|', 1)
                nodo = ASTNode("ENLACE", texto, linea=token.linea)
                nodo.url = url
                return nodo
            
            elif token.tipo == TokenType.IMAGEN:
                self._avanzar()
                alt_text, url = token.valor.split('|', 1)
                nodo = ASTNode("IMAGEN", alt_text, linea=token.linea)
                nodo.url = url
                return nodo
        
        # Token no reconocido, lo saltamos
        self._avanzar()
        return None
    
    def _parsear_negrita(self):
        """
        Parsea un texto en negrita
        
        Returns:
            Nodo AST de tipo NEGRITA
        """
        inicio = self._consumir(TokenType.NEGRITA_INICIO)
        nodo = ASTNode("NEGRITA", linea=inicio.linea)
        
        # Parsear contenido de la negrita
        token = self._token_actual()
        while token and token.tipo != TokenType.NEGRITA_FIN:
            elemento = self._parsear_elemento()
            if elemento:
                nodo.add_hijo(elemento)
            else:
                # Si no se pudo parsear el elemento, avanzamos para evitar bucle infinito
                self._avanzar()
            token = self._token_actual()
        
        # Consumir el token de cierre
        try:
            self._consumir(TokenType.NEGRITA_FIN)
        except ParserError:
            raise ParserError("Falta el cierre de negrita (**)", inicio.linea, inicio.valor)
        
        return nodo
    
    def _parsear_cursiva(self):
        """
        Parsea un texto en cursiva
        
        Returns:
            Nodo AST de tipo CURSIVA
        """
        inicio = self._consumir(TokenType.CURSIVA_INICIO)
        nodo = ASTNode("CURSIVA", linea=inicio.linea)
        
        # Parsear contenido de la cursiva
        token = self._token_actual()
        while token and token.tipo != TokenType.CURSIVA_FIN:
            elemento = self._parsear_elemento()
            if elemento:
                nodo.add_hijo(elemento)
            else:
                # Si no se pudo parsear el elemento, avanzamos para evitar bucle infinito
                self._avanzar()
            token = self._token_actual()
        
        # Consumir el token de cierre
        try:
            self._consumir(TokenType.CURSIVA_FIN)
        except ParserError:
            raise ParserError("Falta el cierre de cursiva (*)", inicio.linea, inicio.valor)
        
        return nodo
