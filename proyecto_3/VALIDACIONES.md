# Guía de Validaciones del Sistema

## 📋 Resumen

El sistema ahora utiliza **formularios HTML tradicionales** sin JSON/AJAX, con validaciones tanto en el **frontend (HTML5)** como en el **backend (Django)**.

## ✅ Validaciones Implementadas

### 1. PRODUCTOS

#### Frontend (HTML5)
- **Nombre**: 
  - Solo letras, números y espacios
  - Mínimo 3 caracteres, máximo 100
  - Pattern: `[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]+`
  
- **Precio**: 
  - Solo números enteros
  - Mínimo: 1, Máximo: 99,999,999
  - Type: `number` con `step="1"`
  
- **Stock**: 
  - Solo números enteros
  - Mínimo: 0, Máximo: 999,999
  - Type: `number` con `step="1"`
  
- **Marca, Tipo, Unidad**: 
  - Selección obligatoria (required)

#### Backend (Django)
```python
# Validaciones en views/Productos/views.py
- Nombre: strip(), longitud mínima 3
- Precio: isdigit(), rango 1-99999999
- Stock: isdigit(), rango 0-999999
- Marca/Tipo/Unidad: verificación de existencia
```

### 2. CLIENTES

#### Frontend (HTML5)
- **Nombre**: 
  - Solo letras y espacios
  - Mínimo 3 caracteres, máximo 100
  - Pattern: `[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+`
  
- **Documento**: 
  - Solo números
  - Mínimo 6 dígitos, máximo 15
  - Pattern: `[0-9]+`
  
- **Teléfono**: 
  - Solo números
  - Mínimo 7 dígitos, máximo 15
  - Type: `tel` con pattern `[0-9]+`
  
- **Email**: 
  - Formato de email válido
  - Type: `email`
  - Máximo 100 caracteres
  
- **Dirección**: 
  - Mínimo 5 caracteres, máximo 200
  
- **Estado**: 
  - Selección obligatoria (Activo/Inactivo)

#### Backend (Django)
```python
# Validaciones en views/Clientes/views.py
- Nombre: regex [a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+, longitud 3+
- Documento: isdigit(), longitud 6-15, único
- Teléfono: isdigit(), longitud 7-15
- Email: contiene '@', único
- Dirección: longitud mínima 5
- Estado: debe ser 'Activo' o 'Inactivo'
- Duplicados: verifica documento y email únicos
```

## 🔒 Tipos de Validación

### Validación Frontend (HTML5)

**Ventajas:**
- Respuesta inmediata al usuario
- No requiere envío al servidor
- Mejor experiencia de usuario

**Atributos HTML5 utilizados:**
```html
<!-- Campos de texto -->
<input type="text" 
       required 
       minlength="3" 
       maxlength="100"
       pattern="[a-zA-Z\s]+"
       title="Mensaje de ayuda">

<!-- Campos numéricos -->
<input type="number" 
       required 
       min="0" 
       max="999999"
       step="1">

<!-- Email -->
<input type="email" required>

<!-- Teléfono -->
<input type="tel" 
       pattern="[0-9]+"
       minlength="7"
       maxlength="15">

<!-- Select -->
<select required>
    <option value="">Seleccione...</option>
</select>
```

### Validación Backend (Django)

**Ventajas:**
- Seguridad (no se puede saltear)
- Validaciones complejas
- Verificación de duplicados en BD

**Patrón utilizado:**
```python
@login_required
def crear_entidad(request):
    if request.method == 'POST':
        try:
            # 1. Obtener datos
            campo = request.POST.get('campo', '').strip()
            
            # 2. Validar formato
            if not campo or len(campo) < 3:
                messages.error(request, 'Error de validación')
                return redirect('vista')
            
            # 3. Validar con regex si es necesario
            if not re.match(r'^[a-zA-Z\s]+$', campo):
                messages.error(request, 'Solo letras')
                return redirect('vista')
            
            # 4. Verificar duplicados
            if Modelo.objects.filter(campo=campo).exists():
                messages.error(request, 'Ya existe')
                return redirect('vista')
            
            # 5. Crear registro
            Modelo.objects.create(campo=campo)
            messages.success(request, 'Creado exitosamente')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('vista')
```

## 🎨 Mensajes de Usuario

### Sistema de Mensajes Django
```python
from django.contrib import messages

# Tipos de mensajes
messages.success(request, 'Operación exitosa')
messages.error(request, 'Error en la operación')
messages.warning(request, 'Advertencia')
messages.info(request, 'Información')
```

### Mostrar en Template
```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    {% endfor %}
{% endif %}
```

## 📝 Patterns Regex Comunes

```regex
# Solo letras y espacios
[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+

# Solo letras, números y espacios
[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]+

# Solo números
[0-9]+

# Email (básico)
.+@.+\..+

# Teléfono colombiano
[3][0-9]{9}

# Documento (6-15 dígitos)
[0-9]{6,15}
```

## 🚫 Restricciones de Entrada

### Bloquear Caracteres Especiales
```html
<!-- Solo letras -->
<input type="text" pattern="[a-zA-Z\s]+" 
       title="Solo se permiten letras">

<!-- Solo números -->
<input type="number" step="1" 
       title="Solo números enteros">

<!-- Sin espacios -->
<input type="text" pattern="[^\s]+" 
       title="No se permiten espacios">
```

### JavaScript Adicional (Opcional)
```javascript
// Bloquear teclas no numéricas
document.getElementById('campo').addEventListener('keypress', function(e) {
    if (!/[0-9]/.test(e.key)) {
        e.preventDefault();
    }
});

// Bloquear teclas no alfabéticas
document.getElementById('campo').addEventListener('keypress', function(e) {
    if (!/[a-zA-Z\s]/.test(e.key)) {
        e.preventDefault();
    }
});
```

## ✨ Mejores Prácticas

1. **Siempre validar en backend**: El frontend puede ser manipulado
2. **Mensajes claros**: Indicar exactamente qué está mal
3. **Usar `strip()`**: Eliminar espacios al inicio/final
4. **Verificar duplicados**: Antes de crear/actualizar
5. **Try-except**: Capturar errores inesperados
6. **Usar `required`**: En todos los campos obligatorios
7. **Indicar campos requeridos**: Con asterisco rojo (*)
8. **Placeholders útiles**: Mostrar ejemplos de formato

## 🔄 Flujo de Validación

```
Usuario llena formulario
        ↓
Validación HTML5 (Frontend)
        ↓
    ¿Válido?
    ↙     ↘
  NO      SÍ
   ↓       ↓
Mensaje  Envío POST
Error     ↓
      Validación Django (Backend)
            ↓
        ¿Válido?
        ↙     ↘
      NO      SÍ
       ↓       ↓
    Mensaje  Guardar en BD
    Error     ↓
          Mensaje Éxito
              ↓
          Redirect
```

## 📚 Módulos Completados

- ✅ **Productos**: Validaciones completas frontend + backend
- ✅ **Clientes**: Validaciones completas frontend + backend
- ⏳ **Compras**: Pendiente
- ⏳ **Ventas**: Pendiente
- ⏳ **Proveedores**: Pendiente

## 🎯 Próximos Pasos

1. Aplicar el mismo patrón a Compras
2. Aplicar el mismo patrón a Proveedores
3. Eliminar endpoints JSON innecesarios
4. Eliminar JavaScript de fetch/AJAX
5. Probar todas las validaciones en el navegador
