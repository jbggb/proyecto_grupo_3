from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    """
    Perfil extendido del usuario de Django.
    El rol superadmin se maneja con User.is_superuser=True.
    Este perfil es para admins normales (is_superuser=False).
    """
    user     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cedula   = models.CharField(max_length=20, unique=True, verbose_name='Cédula')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')

    def __str__(self):
        rol = 'Superadmin' if self.user.is_superuser else 'Admin'
        return f"{self.user.username} - {rol}"

    class Meta:
        verbose_name        = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
        db_table            = 'perfil_usuario'