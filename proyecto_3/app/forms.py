from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Administrador, Producto, Marca, TipoProductos, unidad_medida

# Solo letras (con tildes y ñ) y espacios
REGEX_SOLO_LETRAS = re.compile(r'^[a-zA-Z\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da\u00fc\u00dc\u00f1\u00d1\s]+$')
# Solo letras, numeros y espacios (para abreviatura)
REGEX_ALFANUMERICO = re.compile(r'^[a-zA-Z0-9\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da\u00fc\u00dc\u00f1\u00d1\s]+$')
# Precio valido: no empieza con 0, permite decimales
REGEX_PRECIO = re.compile(r'^[1-9]\d*(\.\d{1,2})?$')
# Stock: solo enteros positivos
REGEX_ENTERO = re.compile(r'^\d+$')


def validar_solo_letras(valor, campo="Este campo"):
    if not REGEX_SOLO_LETRAS.match(valor):
        raise ValidationError(f"{campo} solo puede contener letras y espacios, sin numeros ni caracteres especiales.")


class AdministradorRegistroForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contrasena'}),
        label='Contrasena'
    )
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contrasena'}),
        label='Confirmar Contrasena'
    )
    class Meta:
        model = Administrador
        fields = ['nombre', 'usuario', 'email', 'contrasena']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }
        labels = {'nombre': 'Nombre Completo', 'usuario': 'Usuario', 'email': 'Correo Electronico'}

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if Administrador.objects.filter(usuario=usuario).exists():
            raise ValidationError('Este usuario ya esta registrado.')
        return usuario

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Administrador.objects.filter(email=email).exists():
            raise ValidationError('Este correo ya esta registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        c1 = cleaned_data.get('contrasena')
        c2 = cleaned_data.get('confirmar_contrasena')
        if c1 and c2 and c1 != c2:
            raise ValidationError('Las contrasenas no coinciden.')
        return cleaned_data


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombreMarca']
        widgets = {'nombreMarca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Alpina, Colombina...'})}
        labels = {'nombreMarca': 'Nombre de la Marca'}

    def clean_nombreMarca(self):
        valor = ' '.join(self.cleaned_data.get('nombreMarca', '').split())
        if not valor:
            raise ValidationError("El nombre de la marca es obligatorio.")
        validar_solo_letras(valor, "El nombre de la marca")
        if Marca.objects.filter(nombreMarca__iexact=valor).exists():
            raise ValidationError(f'Ya existe una marca con el nombre "{valor}".')
        return valor


class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProductos
        fields = ['nombre_tipo']
        widgets = {
            'nombre_tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Bebidas, Lacteos...'})
        }
        labels = {'nombre_tipo': 'Nombre del Tipo'}

    def clean_nombre_tipo(self):
        valor = ' '.join(self.cleaned_data.get('nombre_tipo', '').split())
        if not valor:
            raise ValidationError("El nombre del tipo es obligatorio.")
        validar_solo_letras(valor, "El nombre del tipo de producto")
        if TipoProductos.objects.filter(nombre_tipo__iexact=valor).exists():
            raise ValidationError(f'Ya existe un tipo con el nombre "{valor}".')
        return valor


class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = unidad_medida
        fields = ['nombre_unidad', 'abreviatura']
        widgets = {
            'nombre_unidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Kilogramo, Litro...'}),
            'abreviatura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: kg, L...'})
        }
        labels = {'nombre_unidad': 'Nombre de la Unidad', 'abreviatura': 'Abreviatura (opcional)'}

    def clean_nombre_unidad(self):
        valor = ' '.join(self.cleaned_data.get('nombre_unidad', '').split())
        if not valor:
            raise ValidationError("El nombre de la unidad es obligatorio.")
        validar_solo_letras(valor, "El nombre de la unidad")
        if unidad_medida.objects.filter(nombre_unidad__iexact=valor).exists():
            raise ValidationError(f'Ya existe una unidad con el nombre "{valor}".')
        return valor

    def clean_abreviatura(self):
        valor = self.cleaned_data.get('abreviatura', '').strip()
        if valor and not REGEX_ALFANUMERICO.match(valor):
            raise ValidationError("La abreviatura no puede contener caracteres especiales.")
        return valor if valor else '-'


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'idMarca', 'idTipo', 'idUnidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'idMarca': forms.Select(attrs={'class': 'form-select'}),
            'idTipo': forms.Select(attrs={'class': 'form-select'}),
            'idUnidad': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre del Producto', 'precio': 'Precio', 'stock': 'Stock',
            'idMarca': 'Marca', 'idTipo': 'Tipo de Producto', 'idUnidad': 'Unidad de Medida',
        }

    def clean_nombre(self):
        nombre = ' '.join(self.cleaned_data.get('nombre', '').split())
        if not nombre:
            raise ValidationError('El nombre del producto no puede estar vacio.')
        if len(nombre) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')
        if len(nombre) > 200:
            raise ValidationError('El nombre no puede exceder 200 caracteres.')
        validar_solo_letras(nombre, "El nombre del producto")
        qs = Producto.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(f'Ya existe un producto con el nombre "{nombre}".')
        return nombre

    def clean_precio(self):
        raw = self.data.get('precio', '').strip()
        if not raw:
            raise ValidationError('El precio es obligatorio.')
        # Si viene con decimales tipo "15000.0" o "15000.00" desde la BD, quitarlos si son solo ceros
        if '.' in raw:
            partes = raw.split('.')
            if all(c == '0' for c in partes[1]):
                raw = partes[0]
            else:
                raise ValidationError('El precio debe ser un numero entero, sin decimales (ej: 1500).')
        if ',' in raw:
            raise ValidationError('El precio debe ser un numero entero, sin decimales (ej: 1500).')
        if not re.match(r'^[1-9]\d*$', raw):
            raise ValidationError('El precio debe ser un numero entero mayor a 0, sin ceros al inicio.')
        precio = int(raw)
        if precio > 999999:
            raise ValidationError('El precio no puede exceder $999,999.')
        return precio

    def clean_stock(self):
        raw = self.data.get('stock', '').strip()
        if not raw:
            raise ValidationError('El stock es obligatorio.')
        # Si viene con decimales tipo "256.0" desde la BD, quitarlos si son solo ceros
        if '.' in raw:
            partes = raw.split('.')
            if all(c == '0' for c in partes[1]):
                raw = partes[0]
            else:
                raise ValidationError('El stock debe ser un numero entero, sin decimales.')
        if ',' in raw:
            raise ValidationError('El stock debe ser un numero entero, sin decimales.')
        if not re.match(r'^\d+$', raw):
            raise ValidationError('El stock solo puede contener numeros enteros positivos.')
        stock = int(raw)
        # Se permite stock 0 (producto agotado)
        if stock < 0:
            raise ValidationError('El stock no puede ser negativo.')
        if stock > 1000000:
            raise ValidationError('El stock no puede exceder 1,000,000 unidades.')
        return stock

    def clean_idMarca(self):
        marca = self.cleaned_data.get('idMarca')
        if not marca:
            raise ValidationError('Debe seleccionar una marca.')
        return marca

    def clean_idTipo(self):
        tipo = self.cleaned_data.get('idTipo')
        if not tipo:
            raise ValidationError('Debe seleccionar un tipo de producto.')
        return tipo

    def clean_idUnidad(self):
        unidad = self.cleaned_data.get('idUnidad')
        if not unidad:
            raise ValidationError('Debe seleccionar una unidad de medida.')
        return unidad