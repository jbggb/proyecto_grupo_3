"""Decoradores personalizados para autenticación con tabla Administrador"""
from functools import wraps
from django.shortcuts import redirect


def admin_login_required(view_func):
    """
    Reemplaza @admin_login_required para verificar la sesión del Administrador
    en vez del sistema auth de Django.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper