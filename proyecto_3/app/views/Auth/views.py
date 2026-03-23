from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils.decorators import method_decorator
from app.decorators import admin_login_required


class LoginView(View):
    template_name = 'Login/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('inicio')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.get_full_name() or user.username}!')
                return redirect('inicio')
            else:
                messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente.')
        return redirect('login')

    def post(self, request):
        return self.get(request)


login_view  = LoginView.as_view()
logout_view = LogoutView.as_view()