from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views import View
from ...models import Administrador
from ...forms import AdministradorRegistroForm


class LoginView(View):
    template_name = 'Login/login.html'

    def get(self, request):
        if request.session.get('admin_id'):
            return redirect('inicio')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        try:
            admin = Administrador.objects.get(usuario=username)
            if check_password(password, admin.contrasena):
                request.session['admin_id']      = admin.id
                request.session['admin_nombre']  = admin.nombre
                request.session['admin_usuario'] = admin.usuario
                messages.success(request, f'¡Bienvenido, {admin.nombre}!')
                return redirect('inicio')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Administrador.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        messages.success(request, 'Sesión cerrada correctamente.')
        return redirect('login')

    def post(self, request):
        return self.get(request)


class RegistrarAdministradorView(View):
    template_name = 'Login/registro.html'

    def get(self, request):
        return render(request, self.template_name, {'form': AdministradorRegistroForm()})

    def post(self, request):
        form = AdministradorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Administrador registrado exitosamente!')
            return redirect('login')
        messages.error(request, 'Por favor corrige los errores del formulario.')
        return render(request, self.template_name, {'form': form})


# Compatibilidad con urls.py
login_view              = LoginView.as_view()
logout_view             = LogoutView.as_view()
registrar_administrador = RegistrarAdministradorView.as_view()
