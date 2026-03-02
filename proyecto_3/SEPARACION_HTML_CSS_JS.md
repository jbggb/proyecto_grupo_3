# 📋 Guía: Separación de HTML, CSS y JavaScript

## 🎯 Objetivo

Mantener los archivos HTML limpios, con solo HTML puro, y separar los estilos (CSS) y la lógica (JavaScript) en archivos independientes.

## ✅ Estructura Recomendada

```
app/
├── templates/
│   └── Ventas/
│       └── Ventas.html          # Solo HTML
│
├── static/
    ├── css/
    │   ├── styles.css           # CSS global
    │   └── ventas.css           # CSS específico de ventas
    │
    └── js/
        └── ventas.js            # JavaScript de ventas
```

## 📝 Ejemplo: Antes y Después

### ❌ ANTES (Todo mezclado)

```html
{% extends 'base.html' %}

{% block content %}
<style>
    .mi-clase {
        color: red;
    }
</style>

<div class="mi-clase">Contenido</div>

<script>
    function miFunction() {
        alert('Hola');
    }
</script>
{% endblock %}
```

### ✅ DESPUÉS (Separado)

**HTML (template.html)**
```html
{% extends 'base.html' %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/mi-modulo.css' %}">
{% endblock %}

{% block content %}
<div class="mi-clase">Contenido</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/mi-modulo.js' %}"></script>
{% endblock %}
```

**CSS (static/css/mi-modulo.css)**
```css
.mi-clase {
    color: red;
}
```

**JavaScript (static/js/mi-modulo.js)**
```javascript
function miFunction() {
    alert('Hola');
}
```

## 🔧 Pasos para Separar un Template

### 1. Extraer CSS

**Buscar en el HTML:**
```html
<style>
    /* Estilos aquí */
</style>
```

**Mover a:** `static/css/nombre-modulo.css`

**Cargar en el template:**
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/nombre-modulo.css' %}">
```

### 2. Extraer JavaScript

**Buscar en el HTML:**
```html
<script>
    // Código JavaScript aquí
</script>
```

**Mover a:** `static/js/nombre-modulo.js`

**Cargar en el template:**
```html
<script src="{% static 'js/nombre-modulo.js' %}"></script>
```

### 3. Limpiar HTML

- Eliminar etiquetas `<style>` y `<script>`
- Dejar solo estructura HTML
- Mantener atributos `onclick`, `onchange`, etc. (o mejor, usar event listeners en JS)

## 📦 Archivos Creados

### Módulo de Ventas

✅ **CSS separado:**
- `static/css/ventas.css` - Estilos del módulo de ventas

✅ **JavaScript separado:**
- `static/js/ventas.js` - Lógica del carrito y gestión de ventas

### Pendientes de Separar

Los siguientes templates aún tienen estilos/scripts inline:

- [ ] `Productos/productos.html`
- [ ] `cliente/cliente.html`
- [ ] `proveedores/proveedores.html`
- [ ] `Compras/Compras.html`

## 🎨 Actualizar base.html

Para facilitar la carga de CSS y JS específicos, actualiza `base.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Sistema de Inventario{% endblock %}</title>
    
    <!-- CSS Global -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    
    <!-- CSS Específico de cada página -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Contenido -->
    {% block content %}{% endblock %}
    
    <!-- JavaScript Global -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    
    <!-- JavaScript Específico de cada página -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## 💡 Mejores Prácticas

### 1. Nombres de Archivos
- CSS: `nombre-modulo.css` (kebab-case)
- JS: `nombre-modulo.js` (kebab-case)
- Coincidir con el nombre del módulo

### 2. Organización del CSS
```css
/* ═══════════════════════════════════════════════════════════════
   NOMBRE DEL MÓDULO - Estilos
   ═══════════════════════════════════════════════════════════════ */

/* Sección 1 */
.clase-1 {
    /* estilos */
}

/* Sección 2 */
.clase-2 {
    /* estilos */
}
```

### 3. Organización del JavaScript
```javascript
/**
 * ═══════════════════════════════════════════════════════════════
 * NOMBRE DEL MÓDULO - JavaScript
 * Descripción del módulo
 * ═══════════════════════════════════════════════════════════════
 */

// Variables globales
let miVariable = [];

/**
 * Descripción de la función
 */
function miFunction() {
    // código
}
```

### 4. Event Listeners vs onclick

**❌ Evitar (inline):**
```html
<button onclick="miFunction()">Click</button>
```

**✅ Preferir (event listener):**
```html
<button id="miBoton">Click</button>

<script>
document.getElementById('miBoton').addEventListener('click', miFunction);
</script>
```

### 5. Variables de Django en JavaScript

**Para pasar datos de Django a JavaScript:**

```html
<script>
    const CSRF_TOKEN = '{{ csrf_token }}';
    const API_URL = "{% url 'mi_api' %}";
</script>
<script src="{% static 'js/mi-modulo.js' %}"></script>
```

O mejor, usar atributos `data-*`:

```html
<div id="app" 
     data-csrf="{{ csrf_token }}"
     data-api-url="{% url 'mi_api' %}">
</div>

<script>
const app = document.getElementById('app');
const CSRF_TOKEN = app.dataset.csrf;
const API_URL = app.dataset.apiUrl;
</script>
```

## 🚀 Ventajas de la Separación

1. **Mantenibilidad:** Más fácil encontrar y modificar código
2. **Reutilización:** CSS y JS se pueden usar en múltiples páginas
3. **Caché:** Los archivos estáticos se cachean en el navegador
4. **Organización:** Código más limpio y profesional
5. **Colaboración:** Varios desarrolladores pueden trabajar sin conflictos
6. **Performance:** Mejor carga y optimización

## 📚 Recursos

- [Django Static Files](https://docs.djangoproject.com/en/stable/howto/static-files/)
- [MDN: Separación de Concerns](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)

---

**Nota:** Esta estructura sigue las mejores prácticas de desarrollo web moderno.
