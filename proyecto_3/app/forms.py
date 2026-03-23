from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import Administrador
import re


class AdministradorRegistroForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres, una mayúscula y un número',
            'id': 'id_contrasena'
        }),
        label='Contraseña'
    )
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite la contraseña',
            'id': 'id_confirmar_contrasena'
        }),
        label='Confirmar Contraseña'
    )

    class Meta:
        model  = Administrador
        fields = ['nombre', 'usuario', 'email', 'contrasena']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'id': 'id_nombre'
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Solo letras, números y guión bajo',
                'id': 'id_usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'id': 'id_email'
            }),
        }
        labels = {
            'nombre':  'Nombre Completo',
            'usuario': 'Usuario',
            'email':   'Correo Electrónico',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError('El nombre es obligatorio.')
        if len(nombre) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario', '').strip()
        if not usuario:
            raise ValidationError('El usuario es obligatorio.')
        if len(usuario) < 3:
            raise ValidationError('El usuario debe tener al menos 3 caracteres.')
        if not re.match(r'^[a-zA-Z0-9_]+$', usuario):
            raise ValidationError('El usuario solo puede contener letras, números y guión bajo (_).')
        qs = Administrador.objects.filter(usuario=usuario)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Este usuario ya está registrado.')
        return usuario

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise ValidationError('El correo electrónico es obligatorio.')

        # Validar formato general de email
        patron = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise ValidationError('Ingrese un correo electrónico válido.')

        # ─── CORRECCIÓN: se eliminó la lista blanca de dominios ──────────────
        # La versión anterior solo aceptaba gmail, hotmail, outlook, yahoo y
        # sena.edu.co. Eso impedía registrarse a cualquier persona con un
        # correo institucional, universitario o corporativo diferente.
        # Ahora se acepta cualquier dominio con formato válido.
        # ─────────────────────────────────────────────────────────────────────

        qs = Administrador.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Este correo electrónico ya está registrado.')

        return email

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena', '')
        if not contrasena:
            raise ValidationError('La contraseña es obligatoria.')
        if len(contrasena) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', contrasena):
            raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
        if not re.search(r'[0-9]', contrasena):
            raise ValidationError('La contraseña debe contener al menos un número.')
        return contrasena

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        confirmar  = cleaned_data.get('confirmar_contrasena')
        if contrasena and confirmar and contrasena != confirmar:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.contrasena = make_password(self.cleaned_data['contrasena'])
        if commit:
            admin.save()
        return admin


class ventaForm(forms.Form):
    cliente = forms.CharField(max_length=100)
    estado  = forms.ChoiceField(choices=[
        ('Completada', 'Completada'),
        ('Pendiente',  'Pendiente'),
    ])

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente', '').strip()
        if not cliente:
            raise ValidationError('Por favor ingrese un nombre de cliente.')
        if re.search(r'\d', cliente):
            raise ValidationError('El nombre del cliente no puede contener números.')
        if len(cliente) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')
        return cliente