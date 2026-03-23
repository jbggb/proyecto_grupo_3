from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario


class AdminCrearForm(forms.ModelForm):
    """Formulario para crear un admin nuevo. Siempre crea is_superuser=False."""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres'
        }),
        label='Contraseña'
    )
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite la contraseña'
        }),
        label='Confirmar contraseña'
    )

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username':   'Usuario',
            'first_name': 'Nombre',
            'last_name':  'Apellido',
            'email':      'Correo electrónico',
        }
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirmar_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        if p1 and len(p1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return cleaned_data


class AdminEditarForm(forms.ModelForm):
    """Formulario para editar un admin. Contraseña opcional."""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dejar en blanco para no cambiar'
        }),
        label='Nueva contraseña',
        required=False
    )

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username':   'Usuario',
            'first_name': 'Nombre',
            'last_name':  'Apellido',
            'email':      'Correo electrónico',
        }
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model  = PerfilUsuario
        fields = ['cedula', 'telefono']
        labels = {
            'cedula':   'Cédula',
            'telefono': 'Teléfono',
        }
        widgets = {
            'cedula':   forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }