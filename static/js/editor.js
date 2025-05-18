/**
 * Script para la funcionalidad del editor de SimpleDoc
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const editor = document.getElementById('editor');
    const resultado = document.getElementById('resultado');
    const previewContainer = document.getElementById('preview-container');
    const preview = document.getElementById('preview');
    const toggleVista = document.getElementById('toggle-vista');
    const btnCompilar = document.getElementById('btn-compilar');
    const btnEjemplo = document.getElementById('btn-ejemplo');
    const btnLimpiar = document.getElementById('btn-limpiar');
    const nivelComplejidad = document.getElementById('nivel-complejidad');
    const alertaContainer = document.getElementById('alerta-container');
    
    // Ejemplo según nivel de complejidad
    const ejemplos = {
        1: `# Mi primer documento SimpleDoc

Este es un ejemplo básico que solo incluye títulos y texto plano.

## Sección 1

Este es un párrafo de texto normal.

### Subsección

Otro párrafo con texto simple.`,

        2: `# Mi documento SimpleDoc (Nivel intermedio)

Este ejemplo incluye **texto en negrita** y *texto en cursiva*.

## Listas

- Elemento 1 de lista no ordenada
- Elemento 2
- Elemento 3

## Lista numerada

1. Primer elemento numerado
2. Segundo elemento
3. Tercer elemento`,

        3: `# SimpleDoc Avanzado

Este ejemplo incluye todas las características de SimpleDoc.

## Formato de texto

Texto normal con **negrita** y *cursiva*.

## Enlaces e imágenes

[Enlace a Google](https://www.google.com)

![Logo de ejemplo](https://via.placeholder.com/150)

## Listas

- Elemento 1
- Elemento 2
  
1. Elemento numerado
2. Otro elemento

## Código

\`\`\`
function hola() {
    console.log("Hola mundo");
}
\`\`\``
    };
    
    // Función para mostrar alertas
    function mostrarAlerta(mensaje, tipo = 'danger', duracion = 5000) {
        const alerta = document.createElement('div');
        alerta.className = `alert alert-${tipo} alert-dismissible fade show`;
        alerta.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        `;
        alertaContainer.appendChild(alerta);
        
        // Eliminar automáticamente después de la duración especificada
        if (duracion > 0) {
            setTimeout(() => {
                alerta.classList.remove('show');
                setTimeout(() => alerta.remove(), 300);
            }, duracion);
        }
    }
    
    // Función para compilar el código
    function compilar() {
        const codigo = editor.value;
        const nivel = nivelComplejidad.value;
        
        if (!codigo.trim()) {
            mostrarAlerta('El editor está vacío. Escribe algo para compilar.');
            return;
        }
        
        // Enviar el código al servidor para compilar
        const formData = new FormData();
        formData.append('codigo', codigo);
        formData.append('nivel_complejidad', nivel);
        
        fetch('/compilar', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar el resultado
                resultado.value = data.html;
                preview.innerHTML = data.html;
                mostrarAlerta('Compilación exitosa', 'success');
            } else {
                // Mostrar error
                mostrarAlerta(`Error: ${data.error}`);
                console.error(data.error);
            }
        })
        .catch(error => {
            mostrarAlerta(`Error al comunicarse con el servidor: ${error}`);
            console.error('Error:', error);
        });
    }
    
    // Event listeners
    btnCompilar.addEventListener('click', compilar);
    
    btnEjemplo.addEventListener('click', function() {
        const nivel = nivelComplejidad.value;
        editor.value = ejemplos[nivel];
        compilar();
    });
    
    btnLimpiar.addEventListener('click', function() {
        editor.value = '';
        resultado.value = '';
        preview.innerHTML = '<div class="alert alert-info"><i class="fas fa-info-circle me-2"></i>Editor limpiado.</div>';
    });
    
    toggleVista.addEventListener('change', function() {
        if (this.checked) {
            // Mostrar vista previa
            previewContainer.classList.remove('d-none');
            resultado.classList.add('d-none');
        } else {
            // Mostrar código HTML
            previewContainer.classList.add('d-none');
            resultado.classList.remove('d-none');
        }
    });
    
    nivelComplejidad.addEventListener('change', function() {
        // Actualizar el ejemplo si el editor está vacío o tiene un ejemplo
        if (!editor.value.trim() || Object.values(ejemplos).some(ej => editor.value === ej)) {
            const nivel = nivelComplejidad.value;
            editor.value = ejemplos[nivel];
        }
    });
    
    // Auto-compilar cuando se presiona Ctrl+Enter
    editor.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            compilar();
            e.preventDefault();
        }
    });
    
    // Cargar un ejemplo al inicio
    nivelComplejidad.value = '3'; // Establecer nivel avanzado por defecto
    editor.value = ejemplos[3];
    compilar();
});
