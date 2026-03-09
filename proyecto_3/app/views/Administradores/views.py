"""Vistas para gestión de administradores"""
from django.shortcuts import render, redirect
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


admin_registro = AdminRegistroView.as_view()
