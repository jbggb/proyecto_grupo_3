# 📁 Estructura del Proyecto - Sistema de Inventario

## 🎯 Organización Modular

Este proyecto sigue una estructura modular profesional para facilitar el mantenimiento y escalabilidad.

## 📂 Estructura de Carpetas

```
proyecto_3/
├── app/
│   ├── views/                    # 🔹 VISTAS MODULARES
│   │   ├── __init__.py          # Importaciones centralizadas
│   │   ├── index.py             # Vista principal/inicio
│   │   ├── auth.py              # Login, logout, registro
│   │   ├── productos.py         # Gestión de productos
│   │   ├── marcas.py            # AJAX marcas
│   │   ├── tipos.py             # AJAX tipos de productos
│   │   ├── unidades.py          # AJAX unidades de medida
│   │   ├── clientes.py          # Gestión de clientes
│   │   ├── ventas.py            # Gestión de ventas
│   │   ├── proveedores.py       # Gestión de proveedores
│   │   ├── compras.py           # Gestión de compras
│   │   ├── reportes.py          # Reportes y estadísticas
│   │   └── administradores.py   # Gestión de administradores
│   │
│   ├── static/                   # 🔹 ARCHIVOS ESTÁTICOS
│   │   ├── css/
│   │   │   ├── styles.css       # ✅ CSS ÚNICO UNIFICADO
│   │   │   ├── login.css        # ❌ (Obsoleto - eliminar)
│   │   │   └── reporte.css      # ❌ (Obsoleto - eliminar)
│   │   ├── js/                  # Scripts JavaScript
│   │   ├── img/                 # Imágenes
│   │   └── lib/                 # Librerías externas
│   │
│   ├── templates/                # 🔹 PLANTILLAS HTML
│   │   ├── base.html            # Template base con menú lateral
│   │   ├── index.html           # Página de inicio
│   │   ├── login.html           # Página de login
│   │   ├── registro.html        # Registro de usuarios
│   │   │
│   │   ├── Productos/           # Módulo de productos
│   │   │   └── productos.html
│   │   │
│   │   ├── cliente/             # Módulo de clientes
│   │   │   └── cliente.html
│   │   │
│   │   ├── Ventas/              # Módulo de ventas
│   │   │   └── Ventas.html
│   │   │
│   │   ├── proveedores/         # Módulo de proveedores
│   │   │   └── proveedores.html
│   │   │
│   │   ├── Compras/             # Módulo de compras
│   │   │   └── Compras.html
│   │   │
│   │   ├── Reportes/            # Módulo de reportes
│   │   │   └── reportes.html
│   │   │
│   │   └── Registros/           # Módulo de registros
│   │       ├── registro.html
│   │       └── productos.html
│   │
│   ├── templatetags/            # Filtros personalizados
│   │   ├── __init__.py
│   │   └── ventas_filters.py
│   │
│   ├── migrations/              # Migraciones de base de datos
│   ├── models.py                # Modelos de datos
│   ├── forms.py                 # Formularios
│   ├── urls.py                  # URLs de la aplicación
│   ├── admin.py                 # Configuración del admin
│   └── apps.py                  # Configuración de la app
│
├── config/                      # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3                   # Base de datos
├── manage.py                    # Script de gestión Django
├── GUIA_CSS.md                  # Guía de uso del CSS
└── ESTRUCTURA_PROYECTO.md       # Este archivo
```

## 🎨 Sistema de Estilos

### CSS Unificado
- **Archivo único:** `static/css/styles.css`
- Contiene todos los estilos del proyecto
- Variables CSS para fácil personalización
- Componentes reutilizables
- Responsive design

### Componentes Disponibles
- Login y autenticación
- Formularios y controles
- Botones con efectos
- Tablas responsivas
- Badges de estado
- KPIs y métricas
- Pestañas (tabs)
- Barras de progreso
- Alertas y modales

## 🔧 Vistas Modulares

### Ventajas de la Estructura Modular

1. **Mantenibilidad:** Cada módulo es independiente y fácil de mantener
2. **Escalabilidad:** Agregar nuevas funcionalidades es más sencillo
3. **Claridad:** El código está organizado por responsabilidad
4. **Reutilización:** Funciones comunes se pueden compartir entre módulos
5. **Testing:** Más fácil probar módulos individuales

### Módulos Principales

#### 🏠 index.py
- Vista principal del sistema
- Dashboard con estadísticas

#### 🔐 auth.py
- Login de usuarios
- Logout
- Registro de administradores

#### 📦 productos.py
- Listar productos
- Crear, editar, eliminar productos
- API JSON de productos

#### 👥 clientes.py
- Gestión completa de clientes
- CRUD con validaciones
- API JSON

#### 💰 ventas.py
- Sistema de ventas
- Carrito de compras
- Estadísticas de ventas
- Gestión de detalles

#### 🚚 proveedores.py
- Gestión de proveedores
- Validaciones de email único

#### 🛒 compras.py
- Registro de compras
- Relación con productos y proveedores

#### 📊 reportes.py
- Reportes del sistema
- Estadísticas generales

## 📝 Convenciones de Código

### Nombres de Archivos
- Módulos de vistas: `nombre_modulo.py` (snake_case)
- Templates: `NombreModulo/archivo.html` (PascalCase para carpetas)
- CSS: `nombre-archivo.css` (kebab-case)

### Estructura de Vistas
```python
"""Descripción del módulo"""
import ...

@login_required
def nombre_vista(request):
    """Docstring explicativo"""
    # Lógica de la vista
    return render(request, 'template.html', context)
```

### Importaciones
- Todas las vistas se importan en `views/__init__.py`
- Usar importaciones relativas: `from ..models import Modelo`

## 🚀 Próximos Pasos

### Tareas Pendientes
- [ ] Eliminar archivos CSS obsoletos
- [ ] Actualizar templates de Productos y Clientes para usar `base.html`
- [ ] Mover estilos inline de Ventas al CSS unificado
- [ ] Agregar JavaScript modular en `static/js/`
- [ ] Documentar APIs JSON
- [ ] Agregar tests unitarios por módulo

### Mejoras Sugeridas
- [ ] Implementar paginación en listados
- [ ] Agregar búsqueda avanzada
- [ ] Sistema de permisos por rol
- [ ] Exportación de reportes a PDF/Excel
- [ ] Notificaciones en tiempo real
- [ ] Historial de cambios (auditoría)

## 📚 Recursos

- **Guía de CSS:** Ver `GUIA_CSS.md`
- **Django Docs:** https://docs.djangoproject.com/
- **Bootstrap 5:** https://getbootstrap.com/docs/5.3/

## 👥 Equipo

- **Grupo 3** - Sistema de Inventario
- Proyecto Final - 2025

---

**Nota:** Esta estructura sigue las mejores prácticas de Django y facilita el trabajo en equipo.
