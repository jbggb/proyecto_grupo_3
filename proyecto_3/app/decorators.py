from functools import wraps         
from django.shortcuts import redirect

def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            return redirect('login')
        from app.models import Administrador
        try:
            Administrador.objects.get(idAdministrador=request.session['admin_id'])  # ← cambiar id por idAdministrador
        except Administrador.DoesNotExist:
            request.session.flush()
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper