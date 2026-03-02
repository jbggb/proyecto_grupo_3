# Guía de Uso del CSS Unificado

## 📁 Archivo Principal
`app/static/css/styles.css` - Este es el único archivo CSS que necesitas cargar en tus templates.

## 🎨 Cómo Usar en Templates

### 1. Cargar el CSS en cualquier template

```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Tu Página</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
```

## 📦 Componentes Disponibles

### Badges (Etiquetas)

```html
<!-- Estados de producto -->
<span class="badge badge-ok">Disponible</span>
<span class="badge badge-low">Stock Bajo</span>
<span class="badge badge-out">Agotado</span>

<!-- Estados de venta -->
<span class="badge badge-paid">Pagado</span>
<span class="badge badge-pend">Pendiente</span>
<span class="badge badge-cancel">Cancelado</span>

<!-- Tipos de cliente -->
<span class="badge badge-vip">VIP</span>
<span class="badge badge-reg">Regular</span>

<!-- Módulos -->
<span class="badge badge-venta">Ventas</span>
<span class="badge badge-prod">Productos</span>
```

### Botones

```html
<button class="btn btn-primary">Guardar</button>
<button class="btn btn-success">Confirmar</button>
<button class="btn btn-danger">Eliminar</button>
<button class="btn btn-warning">Advertencia</button>
<button class="btn btn-info">Información</button>
<button class="btn btn-sm btn-primary">Botón Pequeño</button>
```

### Tablas

```html
<div class="table-wrap">
    <table class="table">
        <thead>
            <tr>
                <th>Producto</th>
                <th>Precio</th>
                <th>Stock</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Laptop HP</td>
                <td class="price">$850.00</td>
                <td>15</td>
            </tr>
        </tbody>
    </table>
</div>
```

### KPIs (Indicadores)

```html
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">Total Ventas</div>
        <div class="kpi-value">$12,450</div>
        <div class="kpi-sub">Este mes</div>
    </div>
    
    <div class="kpi-card">
        <div class="kpi-label">Productos</div>
        <div class="kpi-value">156</div>
        <div class="kpi-sub">En inventario</div>
    </div>
</div>
```

### Barra de Stock

```html
<div class="stock-bar-wrap">
    <div class="stock-bar">
        <div class="stock-fill fill-ok" style="width: 75%"></div>
    </div>
    <span class="stock-num">75</span>
</div>

<!-- Clases disponibles: fill-ok, fill-low, fill-out -->
```

### Pestañas (Tabs)

```html
<div class="tabs-wrap">
    <div class="tabs-header">
        <button class="tab-btn active" onclick="showTab('tab1')">
            <i class="fa-solid fa-box"></i> Productos
        </button>
        <button class="tab-btn" onclick="showTab('tab2')">
            <i class="fa-solid fa-users"></i> Clientes
        </button>
    </div>
    
    <div class="tab-panel active" id="tab1">
        Contenido de productos...
    </div>
    
    <div class="tab-panel" id="tab2">
        Contenido de clientes...
    </div>
</div>

<script>
function showTab(tabId) {
    // Ocultar todos los paneles
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    // Mostrar el panel seleccionado
    document.getElementById(tabId).classList.add('active');
    event.target.closest('.tab-btn').classList.add('active');
}
</script>
```

### Tarjetas (Cards)

```html
<div class="card">
    <div class="card-header">
        <i class="fa-solid fa-box me-2"></i>Productos
    </div>
    <div class="card-body">
        Contenido de la tarjeta...
    </div>
</div>
```

### Encabezado de Sección

```html
<div class="section-header">
    <h2 class="section-title">
        <i class="fa-solid fa-box me-2"></i>Gestión de Productos
    </h2>
    <div>
        <button class="btn btn-primary">
            <i class="fa-solid fa-plus me-2"></i>Nuevo Producto
        </button>
    </div>
</div>
```

### Barra de Filtros

```html
<div class="filter-bar">
    <div class="search-box">
        <input type="text" class="form-control" placeholder="Buscar...">
    </div>
    <select class="form-control" style="width: auto;">
        <option>Todos</option>
        <option>Disponible</option>
        <option>Agotado</option>
    </select>
    <button class="btn btn-primary">Filtrar</button>
</div>
```

### Alertas

```html
<div class="alert alert-success">Operación exitosa</div>
<div class="alert alert-warning">Advertencia importante</div>
<div class="alert alert-danger">Error en la operación</div>
<div class="alert alert-info">Información adicional</div>
```

### Estado Vacío

```html
<div class="empty-state">
    <i class="fa-solid fa-box-open"></i>
    <h3>No hay productos</h3>
    <p>Comienza agregando tu primer producto</p>
    <button class="btn btn-primary mt-3">
        <i class="fa-solid fa-plus me-2"></i>Agregar Producto
    </button>
</div>
```

## 🎨 Variables CSS Personalizables

Si necesitas cambiar colores, puedes modificar las variables en `:root` al inicio del archivo `styles.css`:

```css
:root {
  --primary: #667eea;        /* Color principal */
  --success: #22c55e;        /* Color de éxito */
  --warning: #f59e0b;        /* Color de advertencia */
  --danger: #ef4444;         /* Color de peligro */
  --text-primary: #1e293b;   /* Color de texto principal */
  /* ... más variables */
}
```

## 📱 Responsive

Todos los componentes son responsive automáticamente. Los breakpoints son:
- Móvil: < 576px
- Tablet: < 768px
- Desktop: > 768px

## ✅ Archivos Actualizados

Los siguientes templates ya están usando el CSS unificado:
- ✅ `base.html`
- ✅ `login.html`
- ✅ `registro.html`

## 🗑️ Archivos CSS Antiguos (Puedes eliminarlos)

- `app/static/css/login.css` (ya no se usa)
- `app/static/css/reporte.css` (ya no se usa)
- `app/templates/css/reporte.css` (ya no se usa)

## 💡 Consejos

1. Siempre carga Bootstrap ANTES de `styles.css`
2. Usa las clases de Bootstrap cuando sea posible
3. Las clases personalizadas del `styles.css` complementan Bootstrap
4. Para iconos, usa Font Awesome 6.5.1
