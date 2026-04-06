"""Vistas para gestión de administradores (tabla legacy)"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from app.decorators import superadmin_required
from ...models import Administrador
from ...forms import AdministradorRegistroForm


@method_decorator(superadmin_required, name='dispatch')
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


@method_decorator(superadmin_required, name='dispatch')
class EliminarAdminView(View):
    """Eliminación de registros de la tabla administrador legacy."""
    def post(self, request, id):
        admin = get_object_or_404(Administrador, id=id)
        nombre = admin.nombre
        try:
            admin.delete()
            messages.success(request, f'Administrador "{nombre}" eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el administrador: {str(e)}')
        return redirect('inicio')


admin_registro = AdminRegistroView.as_view()
eliminar_admin = EliminarAdminView.as_view()
