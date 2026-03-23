from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from app.decorators import superadmin_required
from .models import PerfilUsuario
from .forms import AdminCrearForm, AdminEditarForm, PerfilForm


@method_decorator(superadmin_required, name='dispatch')
class ListarUsuariosView(ListView):
    model                = User
    template_name        = 'usuarios/listar.html'
    context_object_name  = 'usuarios'

    def get_queryset(self):
        # Listar solo admins normales (no superadmins)
        return User.objects.filter(is_superuser=False).select_related('perfil').order_by('username')


@method_decorator(superadmin_required, name='dispatch')
class CrearUsuarioView(View):
    def get(self, request):
        return render(request, 'usuarios/crear.html', {
            'user_form':   AdminCrearForm(),
            'perfil_form': PerfilForm(),
        })

    def post(self, request):
        user_form   = AdminCrearForm(request.POST)
        perfil_form = PerfilForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_superuser = False   # siempre admin normal
            user.is_staff     = False
            user.save()

            perfil      = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            messages.success(request, f'Admin "{user.username}" creado exitosamente.')
            return redirect('usuarios:listar')

        return render(request, 'usuarios/crear.html', {
            'user_form':   user_form,
            'perfil_form': perfil_form,
        })


@method_decorator(superadmin_required, name='dispatch')
class EditarUsuarioView(View):
    def get(self, request, pk):
        usuario = get_object_or_404(User, pk=pk, is_superuser=False)
        perfil, _ = PerfilUsuario.objects.get_or_create(user=usuario)
        return render(request, 'usuarios/editar.html', {
            'user_form':   AdminEditarForm(instance=usuario),
            'perfil_form': PerfilForm(instance=perfil),
            'usuario':     usuario,
        })

    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk, is_superuser=False)
        perfil  = get_object_or_404(PerfilUsuario, user=usuario)

        user_form   = AdminEditarForm(request.POST, instance=usuario)
        perfil_form = PerfilForm(request.POST, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            nueva_password = user_form.cleaned_data.get('password')
            if nueva_password:
                user.set_password(nueva_password)
            user.save()
            perfil_form.save()
            messages.success(request, f'Admin "{usuario.username}" actualizado.')
            return redirect('usuarios:listar')

        return render(request, 'usuarios/editar.html', {
            'user_form':   user_form,
            'perfil_form': perfil_form,
            'usuario':     usuario,
        })


@method_decorator(superadmin_required, name='dispatch')
class CambiarEstadoUsuarioView(View):
    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk, is_superuser=False)
        usuario.is_active = not usuario.is_active
        usuario.save()
        estado = 'activado' if usuario.is_active else 'desactivado'
        messages.success(request, f'Admin "{usuario.username}" {estado} correctamente.')
        return redirect('usuarios:listar')