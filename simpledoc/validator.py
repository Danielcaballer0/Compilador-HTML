"""
Módulo para la validación de documentos SimpleDoc
"""

from .exceptions import ValidationError


class Validator:
    """
    Validador de documentos SimpleDoc
    
    Verifica que la estructura del documento sea válida según las reglas del lenguaje.
    """
    
    def __init__(self, nivel_complejidad=3):
        """
        Inicializa el validador con un nivel de complejidad específico
        
        Args:
            nivel_complejidad: Entero del 1 al 3 que determina la complejidad de la validación
                1 - Básico: Solo títulos y texto plano
                2 - Intermedio: Básico + formateo (negrita, cursiva) y listas
                3 - Avanzado: Intermedio + enlaces, imágenes y bloques de código
        """
        self.nivel_complejidad = min(max(nivel_complejidad, 1), 3)
    
    def validar(self, ast):
        """
        Valida la estructura del AST
        
        Args:
            ast: Árbol de sintaxis abstracta a validar
            
        Returns:
            True si el documento es válido, False en caso contrario
            
        Raises:
            ValidationError: Si se encuentra un error en la estructura del documento
        """
        # Realizar validaciones específicas según el nivel de complejidad
        if self.nivel_complejidad >= 1:
            self._validar_estructura_basica(ast)
        
        if self.nivel_complejidad >= 2:
            self._validar_formato(ast)
            self._validar_listas(ast)
        
        if self.nivel_complejidad >= 3:
            self._validar_enlaces(ast)
            self._validar_imagenes(ast)
            self._validar_codigo(ast)
        
        return True
    
    def _validar_estructura_basica(self, nodo):
        """
        Valida la estructura básica del documento
        
        Args:
            nodo: Nodo AST a validar
            
        Raises:
            ValidationError: Si se encuentra un error en la estructura básica
        """
        # Validar que el documento no esté vacío
        if nodo.tipo == "DOCUMENTO" and not nodo.hijos:
            raise ValidationError("El documento está vacío")
        
        # Validar títulos
        for hijo in nodo.hijos:
            if hijo.tipo in ["TITULO1", "TITULO2", "TITULO3"]:
                if not hijo.valor or not hijo.valor.strip():
                    raise ValidationError(f"Título vacío", hijo.tipo, hijo.linea)
            
            # Validar recursivamente los hijos
            if hijo.hijos:
                self._validar_estructura_basica(hijo)
    
    def _validar_formato(self, nodo):
        """
        Valida el formato del texto (negrita, cursiva)
        
        Args:
            nodo: Nodo AST a validar
            
        Raises:
            ValidationError: Si se encuentra un error en el formato
        """
        # Validar que los elementos de formato no estén vacíos
        for hijo in nodo.hijos:
            if hijo.tipo in ["NEGRITA", "CURSIVA"]:
                if not hijo.hijos:
                    raise ValidationError(f"{hijo.tipo} sin contenido", hijo.tipo, hijo.linea)
            
            # Validar recursivamente los hijos
            if hijo.hijos:
                self._validar_formato(hijo)
    
    def _validar_listas(self, nodo):
        """
        Valida la estructura de las listas
        
        Args:
            nodo: Nodo AST a validar
            
        Raises:
            ValidationError: Si se encuentra un error en las listas
        """
        # Validar elementos de lista
        for i, hijo in enumerate(nodo.hijos):
            if hijo.tipo == "LISTA_NUM_ITEM":
                # Validar que los elementos de lista numerada tengan números consecutivos
                if i > 0 and nodo.hijos[i-1].tipo == "LISTA_NUM_ITEM":
                    if hijo.numero != nodo.hijos[i-1].numero + 1:
                        raise ValidationError(
                            f"Numeración de lista incorrecta: se esperaba {nodo.hijos[i-1].numero + 1}, se encontró {hijo.numero}", 
                            hijo.tipo, 
                            hijo.linea
                        )
            
            # Validar recursivamente los hijos
            if hijo.hijos:
                self._validar_listas(hijo)
    
    def _validar_enlaces(self, nodo):
        """
        Valida los enlaces
        
        Args:
            nodo: Nodo AST a validar
            
        Raises:
            ValidationError: Si se encuentra un error en los enlaces
        """
        for hijo in nodo.hijos:
            if hijo.tipo == "ENLACE":
                # Validar que el enlace tenga URL
                if not hasattr(hijo, 'url') or not hijo.url:
                    raise ValidationError(f"Enlace sin URL", hijo.tipo, hijo.linea)
                
                # Validar formato de URL básico
                if not hijo.url.startswith(('http://', 'https://', 'mailto:', 'tel:', '/')):
                    raise ValidationError(f"URL de enlace mal formada: {hijo.url}", hijo.tipo, hijo.linea)
            
            # Validar recursivamente los hijos
            if hijo.hijos:
                self._validar_enlaces(hijo)
    
    def _validar_imagenes(self, nodo):
        """
        Valida las imágenes
        
        Args:
            nodo: Nodo AST a validar
            
        Raises:
            ValidationError: Si se encuentra un error en las imágenes
        """
        for hijo in nodo.hijos:
            if hijo.tipo == "IMAGEN":
                # Validar que la imagen tenga URL
                if not hasattr(hijo, 'url') or not hijo.url:
                    raise ValidationError(f"Imagen sin URL", hijo.tipo, hijo.linea)
                
                # Validar formato de URL básico
                if not hijo.url.startswith(('http://', 'https://', '/')):
                    raise ValidationError(f"URL de imagen mal formada: {hijo.url}", hijo.tipo, hijo.linea)
            
            # Validar recursivamente los hijos
            if hijo.hijos:
                self._validar_imagenes(hijo)
    
    def _validar_codigo(self, nodo):
        """
        Valida los bloques de código
        
        Args:
            nodo: Nodo AST a validar
            
        Raises:
            ValidationError: Si se encuentra un error en los bloques de código
        """
        # No hay validaciones específicas para bloques de código por ahora
        for hijo in nodo.hijos:
            if hijo.hijos:
                self._validar_codigo(hijo)
