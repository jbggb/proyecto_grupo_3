"""Vistas para gestión de administradores"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from app.decorators import admin_login_required
from ...models import Administrador
from ...forms import AdministradorRegistroForm


@method_decorator(admin_login_required, name='dispatch')
class AdminRegistroView(View):
    template_name = 'Login/registro.html'

    def get(self, request):
        return render(request, self.template_name, {'form': AdministradorRegistroForm()})

    def post(self, request):
        form = AdministradorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('inicio')
        return render(request, self.template_name, {'form': form})


@method_decorator(admin_login_required, name='dispatch')
class EliminarAdminView(View):
    """
    ✅ NUEVO: Eliminación segura de administradores.
    Impide que un admin se elimine a sí mismo.
    """
    def post(self, request, id):
        admin_sesion_id = request.session.get('admin_id')

        # Protección: no permitir eliminar el admin actualmente logueado
        if str(admin_sesion_id) == str(id):
            messages.error(request, 'No puedes eliminar tu propia cuenta mientras tienes sesión activa.')
            return redirect('inicio')

        admin = get_object_or_404(Administrador, id=id)
        nombre = admin.nombre
        try:
            admin.delete()
            messages.success(request, f'Administrador "{nombre}" eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el administrador: {str(e)}')
        return redirect('inicio')


admin_registro   = AdminRegistroView.as_view()
eliminar_admin   = EliminarAdminView.as_view()
