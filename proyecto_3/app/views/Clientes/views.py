"""Vistas para gestión de clientes"""
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...models import Cliente


@login_required
def clientes(request):
    """Lista de clientes con filtros"""
    clientes_list = Cliente.objects.all()
    
    # Filtro por búsqueda
    busqueda = request.GET.get('busqueda', '').strip()
    if busqueda:
        clientes_list = clientes_list.filter(nombre__icontains=busqueda)
    
    # Filtro por estado
    estado = request.GET.get('estado', '').strip()
    if estado:
        clientes_list = clientes_list.filter(estado=estado)
    
    return render(request, "Clientes/clientes.html", {
        'clientes': clientes_list
    })


@login_required
def crear_cliente(request):
    """Crear un nuevo cliente"""
    if request.method == 'POST':
        try:
            # Obtener y validar datos
            nombre = request.POST.get('nombre', '').strip()
            documento = request.POST.get('documento', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            email = request.POST.get('email', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            estado = request.POST.get('estado', '').strip()
            
            # Validar nombre (solo letras y espacios)
            if not nombre or len(nombre) < 3:
                messages.error(request, 'El nombre debe tener al menos 3 caracteres.')
                return redirect('clientes')
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                messages.error(request, 'El nombre solo puede contener letras y espacios.')
                return redirect('clientes')
            
            # Validar documento (solo números, 6-15 dígitos)
            if not documento or len(documento) < 6 or len(documento) > 15:
                messages.error(request, 'El documento debe tener entre 6 y 15 dígitos.')
                return redirect('clientes')
            if not documento.isdigit():
                messages.error(request, 'El documento solo puede contener números.')
                return redirect('clientes')
            
            # Validar teléfono (solo números, 7-15 dígitos)
            if not telefono or len(telefono) < 7 or len(telefono) > 15:
                messages.error(request, 'El teléfono debe tener entre 7 y 15 dígitos.')
                return redirect('clientes')
            if not telefono.isdigit():
                messages.error(request, 'El teléfono solo puede contener números.')
                return redirect('clientes')
            
            # Validar email
            if not email or '@' not in email:
                messages.error(request, 'Debe ingresar un email válido.')
                return redirect('clientes')
            
            # Validar dirección
            if not direccion or len(direccion) < 5:
                messages.error(request, 'La dirección debe tener al menos 5 caracteres.')
                return redirect('clientes')
            
            # Validar estado
            if estado not in ['Activo', 'Inactivo']:
                messages.error(request, 'Debe seleccionar un estado válido.')
                return redirect('clientes')
            
            # Verificar duplicados
            if Cliente.objects.filter(documento=documento).exists():
                messages.error(request, 'Ya existe un cliente con ese documento.')
                return redirect('clientes')
            
            if Cliente.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe un cliente con ese email.')
                return redirect('clientes')
            
            # Crear cliente
            Cliente.objects.create(
                nombre=nombre,
                documento=documento,
                telefono=telefono,
                email=email,
                direccion=direccion,
                estado=estado,
            )
            messages.success(request, f'Cliente "{nombre}" creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el cliente: {str(e)}')
    
    return redirect('clientes')


@login_required
def editar_cliente(request, id):
    """Editar un cliente existente"""
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        try:
            # Obtener y validar datos
            nombre = request.POST.get('nombre', '').strip()
            documento = request.POST.get('documento', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            email = request.POST.get('email', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            estado = request.POST.get('estado', '').strip()
            
            # Validar nombre (solo letras y espacios)
            if not nombre or len(nombre) < 3:
                messages.error(request, 'El nombre debe tener al menos 3 caracteres.')
                return redirect('clientes')
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                messages.error(request, 'El nombre solo puede contener letras y espacios.')
                return redirect('clientes')
            
            # Validar documento (solo números, 6-15 dígitos)
            if not documento or len(documento) < 6 or len(documento) > 15:
                messages.error(request, 'El documento debe tener entre 6 y 15 dígitos.')
                return redirect('clientes')
            if not documento.isdigit():
                messages.error(request, 'El documento solo puede contener números.')
                return redirect('clientes')
            
            # Validar teléfono (solo números, 7-15 dígitos)
            if not telefono or len(telefono) < 7 or len(telefono) > 15:
                messages.error(request, 'El teléfono debe tener entre 7 y 15 dígitos.')
                return redirect('clientes')
            if not telefono.isdigit():
                messages.error(request, 'El teléfono solo puede contener números.')
                return redirect('clientes')
            
            # Validar email
            if not email or '@' not in email:
                messages.error(request, 'Debe ingresar un email válido.')
                return redirect('clientes')
            
            # Validar dirección
            if not direccion or len(direccion) < 5:
                messages.error(request, 'La dirección debe tener al menos 5 caracteres.')
                return redirect('clientes')
            
            # Validar estado
            if estado not in ['Activo', 'Inactivo']:
                messages.error(request, 'Debe seleccionar un estado válido.')
                return redirect('clientes')
            
            # Verificar duplicados (excluyendo el cliente actual)
            if Cliente.objects.filter(documento=documento).exclude(id=id).exists():
                messages.error(request, 'Ya existe otro cliente con ese documento.')
                return redirect('clientes')
            
            if Cliente.objects.filter(email=email).exclude(id=id).exists():
                messages.error(request, 'Ya existe otro cliente con ese email.')
                return redirect('clientes')
            
            # Actualizar cliente
            cliente.nombre = nombre
            cliente.documento = documento
            cliente.telefono = telefono
            cliente.email = email
            cliente.direccion = direccion
            cliente.estado = estado
            cliente.save()
            
            messages.success(request, f'Cliente "{cliente.nombre}" actualizado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
    
    return redirect('clientes')


@login_required
def eliminar_cliente(request, id):
    """Eliminar un cliente"""
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        try:
            nombre = cliente.nombre
            cliente.delete()
            messages.success(request, f'Cliente "{nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('clientes')



@login_required
def clientes_json(request):
    """Lista de clientes en formato JSON"""
    from django.http import JsonResponse
    lista = list(Cliente.objects.all().values('id', 'nombre', 'documento', 'telefono', 'email', 'direccion', 'estado'))
    return JsonResponse({'clientes': lista})
