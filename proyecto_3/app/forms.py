from django import forms
from django.core.exceptions import ValidationError


from .models import Administrador,Cliente


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
