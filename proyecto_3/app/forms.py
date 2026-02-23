from django import forms
from django.core.exceptions import ValidationError
from .models import Administrador, Producto, Marca, TipoProductos, unidad_medida


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


class ProductoForm(forms.ModelForm):
    """
    Formulario para crear y editar productos con validaciones
    """
    
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'idMarca', 'idTipo', 'idUnidad']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'idMarca': forms.Select(attrs={
                'class': 'form-select'
            }),
            'idTipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'idUnidad': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'precio': 'Precio',
            'stock': 'Stock',
            'idMarca': 'Marca',
            'idTipo': 'Tipo de Producto',
            'idUnidad': 'Unidad de Medida',
        }
    
    def clean_nombre(self):
        """
        Validar que el nombre del producto no exista (evitar duplicados)
        """
        nombre = self.cleaned_data.get('nombre', '').strip()
        
        # Validar que no esté vacío
        if not nombre:
            raise ValidationError('El nombre del producto no puede estar vacío.')
        
        # Validar longitud mínima
        if len(nombre) < 3:
            raise ValidationError('El nombre del producto debe tener al menos 3 caracteres.')
        
        # Validar longitud máxima
        if len(nombre) > 200:
            raise ValidationError('El nombre del producto no puede exceder 200 caracteres.')
        
        # Verificar duplicados (case-insensitive)
        productos_existentes = Producto.objects.filter(nombre__iexact=nombre)
        
        # Si estamos editando, excluir el producto actual
        if self.instance and self.instance.pk:
            productos_existentes = productos_existentes.exclude(pk=self.instance.pk)
        
        if productos_existentes.exists():
            raise ValidationError(f'Ya existe un producto con el nombre "{nombre}". Por favor, utilice un nombre diferente.')
        
        return nombre
    
    def clean_precio(self):
        """
        Validar que el precio sea mayor a 0
        """
        precio = self.cleaned_data.get('precio')
        
        if precio is None:
            raise ValidationError('El precio es obligatorio.')
        
        if precio <= 0:
            raise ValidationError('El precio debe ser mayor a 0.')
        
        if precio > 999999.99:
            raise ValidationError('El precio no puede exceder $999,999.99.')
        
        return precio
    
    def clean_stock(self):
        """
        Validar que el stock sea mayor o igual a 0
        """
        stock = self.cleaned_data.get('stock')
        
        if stock is None:
            raise ValidationError('El stock es obligatorio.')
        
        if stock < 0:
            raise ValidationError('El stock no puede ser negativo.')
        
        if stock > 1000000:
            raise ValidationError('El stock no puede exceder 1,000,000 unidades.')
        
        return stock
    
    def clean_idMarca(self):
        """
        Validar que la marca exista
        """
        marca = self.cleaned_data.get('idMarca')
        
        if not marca:
            raise ValidationError('Debe seleccionar una marca.')
        
        return marca
    
    def clean_idTipo(self):
        """
        Validar que el tipo de producto exista
        """
        tipo = self.cleaned_data.get('idTipo')
        
        if not tipo:
            raise ValidationError('Debe seleccionar un tipo de producto.')
        
        return tipo
    
    def clean_idUnidad(self):
        """
        Validar que la unidad de medida exista
        """
        unidad = self.cleaned_data.get('idUnidad')
        
        if not unidad:
            raise ValidationError('Debe seleccionar una unidad de medida.')
        
        return unidad