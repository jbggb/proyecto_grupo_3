from django import forms
from django.core.exceptions import ValidationError
from .models import Administrador
import re

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
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'usuario': 'Usuario',
            'email': 'Correo Electrónico',
        }

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if Administrador.objects.filter(usuario=usuario).exists():
            raise ValidationError('Este usuario ya está registrado.')
        return usuario

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Administrador.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')
        if contrasena and confirmar_contrasena:
            if contrasena != confirmar_contrasena:
                raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data


class ventaForm(forms.Form):
    cliente = forms.CharField(max_length=100)
    estado = forms.ChoiceField(choices=[
        ('completada', 'Completada'),
        ('pendiente', 'Pendiente'),
    ])

    def clean_cliente(self):       # ← ahora SÍ está dentro de la clase
        cliente = self.cleaned_data.get('cliente', '').strip()

        if not cliente:
            raise ValidationError('Por favor ingrese un nombre de cliente.')

        if re.search(r'\d', cliente):
            raise ValidationError('El nombre del cliente no puede contener números.')

        if len(cliente) < 3:
            raise ValidationError('El nombre debe tener al menos 5 caracteres.')

        return cliente