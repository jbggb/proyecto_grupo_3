from django import forms
from django.core.exceptions import ValidationError


from .models import Administrador,Cliente,compra


class AdministradorRegistroForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label='Contraseña'
    )
    
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        }),
        label='Confirmar Contraseña'
    )
    
    class Meta:
        model = Administrador
        fields = ['nombre', 'usuario', 'email', 'contrasena']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'usuario': 'Usuario',
            'email': 'Correo Electrónico',
        }
    
    def clean_usuario(self):
        """Validar que el usuario no exista"""
        usuario = self.cleaned_data.get('usuario')
        
        if Administrador.objects.filter(usuario=usuario).exists():
            raise ValidationError('Este usuario ya está registrado.')
        
        return usuario
    
    def clean_email(self):
        """Validar que el email no exista"""
        email = self.cleaned_data.get('email')
        
        if Administrador.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        
        return email
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')
        
        if contrasena and confirmar_contrasena:
            if contrasena != confirmar_contrasena:
                raise ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data
    
    



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'documento', 'telefono', 'email', 'direccion', 'estado']
        widgets = {
            'nombre':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez'}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234567890', 'maxlength': '12'}),
            'telefono':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3001234567', 'maxlength': '10'}),
            'email':     forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: cliente@email.com'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calle 123 #45-67'}),
            'estado':    forms.Select(
                attrs={'class': 'form-select'},
                choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')]
            ),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')
        import re
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError('El nombre solo debe contener letras y espacios.')
        return nombre

    def clean_documento(self):
        documento = self.cleaned_data.get('documento', '').strip()
        if not documento:
            raise forms.ValidationError('El documento es obligatorio.')
        if not documento.isdigit():
            raise forms.ValidationError('El documento solo debe contener números.')
        if not (6 <= len(documento) <= 12):
            raise forms.ValidationError('El documento debe tener entre 6 y 12 dígitos.')
        qs = Cliente.objects.filter(documento=documento)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe un cliente con este número de documento.')
        return documento

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono:
            raise forms.ValidationError('El teléfono es obligatorio.')
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono solo debe contener números.')
        if len(telefono) != 10:
            raise forms.ValidationError('El teléfono debe tener exactamente 10 dígitos.')
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise forms.ValidationError('El email es obligatorio.')
        qs = Cliente.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe un cliente con este email.')
        return email

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if not direccion:
            raise forms.ValidationError('La dirección es obligatoria.')
        return direccion




def solo_letras(valor, nombre_campo):
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', str(valor).strip()):
        raise forms.ValidationError(
            f'El campo {nombre_campo} solo debe contener letras y espacios, '
            f'sin números ni caracteres especiales.'
        )
    return valor


class CompraForm(forms.ModelForm):
    class Meta:
        model = compra
        fields = ['Administrador', 'Proveedor', 'Producto', 'fecha_compra', 'totalcompra', 'estado']
        widgets = {
            'Administrador': forms.Select(attrs={'class': 'form-select'}),
            'Proveedor':     forms.Select(attrs={'class': 'form-select'}),
            'Producto':      forms.Select(attrs={'class': 'form-select'}),
            'fecha_compra':  forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'totalcompra':   forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 150000', 'min': '0', 'step': '0.01'}),
            'estado':        forms.Select(attrs={'class': 'form-select'}, choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }
        labels = {
            'Administrador': 'Administrador',
            'Proveedor':     'Proveedor',
            'Producto':      'Producto',
            'fecha_compra':  'Fecha de Compra',
            'totalcompra':   'Total Compra',
            'estado':        'Estado',
        }

    def clean_Administrador(self):
        administrador = self.cleaned_data.get('Administrador')
        if not administrador:
            raise forms.ValidationError('Debe seleccionar un administrador.')
        return administrador

    def clean_Proveedor(self):
        proveedor = self.cleaned_data.get('Proveedor')
        if not proveedor:
            raise forms.ValidationError('Debe seleccionar un proveedor.')
        # Valida el nombre del proveedor que viene de la BD
        solo_letras(proveedor.nombre, 'proveedor')
        return proveedor

    def clean_Producto(self):
        producto = self.cleaned_data.get('Producto')
        if not producto:
            raise forms.ValidationError('Debe seleccionar un producto.')
        # Valida nombre del producto
        solo_letras(producto.nombre, 'producto')
        # Valida el tipo de producto
        solo_letras(producto.idTipo.nombre_tipo, 'tipo de producto')
        # Valida la marca
        solo_letras(producto.idMarca.nombreMarca, 'marca')
        return producto

    def clean_fecha_compra(self):
        fecha = self.cleaned_data.get('fecha_compra')
        if not fecha:
            raise forms.ValidationError('La fecha de compra es obligatoria.')
        return fecha

    def clean_totalcompra(self):
        total = self.cleaned_data.get('totalcompra')
        if total is None or total == '':
            raise forms.ValidationError('El total de la compra es obligatorio.')
        if total <= 0:
            raise forms.ValidationError('El total debe ser mayor a 0.')
        return total

    def clean(self):
        cleaned_data = super().clean()
        campos_requeridos = {
            'Administrador': 'administrador',
            'Proveedor':     'proveedor',
            'Producto':      'producto',
            'fecha_compra':  'fecha de compra',
            'totalcompra':   'total de compra',
        }
        for campo, nombre in campos_requeridos.items():
            if not cleaned_data.get(campo):
                self.add_error(campo, f'El campo {nombre} es obligatorio.')
        return cleaned_data