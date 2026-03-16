// Bloquea números y caracteres especiales completamente
function bloquearNumeros(input, errorId) {
    var antes = input.value;
    var limpio = input.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]/g, '');
    limpio = limpio.replace(/ {2,}/g, ' ');
    if (antes !== limpio) {
        input.value = limpio;
        mostrarError(errorId, 'Solo se permiten letras y espacios.');
    } else {
        ocultarError(errorId);
    }
}

// Solo numeros enteros en precio, máximo 800000
function validarPrecio(input, errorId) {
    var limpio = input.value.replace(/[^\d]/g, '');
    limpio = limpio.replace(/^0+(\d)/, '$1');
    if (limpio && parseInt(limpio) > 800000) {
        limpio = '800000';
        mostrarError(errorId, 'El precio máximo es $800.000.');
    } else {
        ocultarError(errorId);
    }
    input.value = limpio;
}

function validarStock(input, errorId) {
    var limpio = input.value.replace(/[^\d]/g, '');
    if (limpio.length > 1) limpio = limpio.replace(/^0+/, '');
    if (parseInt(limpio) > 1000) {
        limpio = '1000';
    }
    if (input.value !== limpio) {
        mostrarError(errorId, '⚠ El stock solo acepta números enteros.');
    }
    input.value = limpio;
}

function mostrarError(errorId, msg) {
    var el = document.getElementById(errorId);
    if (el) {
        el.textContent = '⚠ ' + msg;
        el.style.display = 'block';
        clearTimeout(el._timer);
        el._timer = setTimeout(function () {
            el.style.display = 'none';
        }, 3000);
    }
}

function ocultarError(errorId) {
    var el = document.getElementById(errorId);
    if (el) el.style.display = 'none';
}

// Ver producto con SweetAlert
function verProducto(id, nombre, precio, stock, marca, tipo, unidad) {
    Swal.fire({
        title: '<strong>' + nombre + '</strong>',
        icon: 'info',
        html:
            '<table class="table table-bordered text-start">' +
            '<tr><th>ID</th><td>' + id + '</td></tr>' +
            '<tr><th>Nombre</th><td>' + nombre + '</td></tr>' +
            '<tr><th>Precio</th><td>$' + precio + '</td></tr>' +
            '<tr><th>Stock</th><td>' + stock + ' unidades</td></tr>' +
            '<tr><th>Marca</th><td>' + marca + '</td></tr>' +
            '<tr><th>Tipo</th><td>' + tipo + '</td></tr>' +
            '<tr><th>Unidad</th><td>' + unidad + '</td></tr>' +
            '</table>',
        confirmButtonText: 'Cerrar',
        confirmButtonColor: '#6c757d'
    });
}

// Eliminar producto con SweetAlert — usa POST para evitar Method Not Allowed
function eliminarProducto(url, nombre) {
    Swal.fire({
        title: '¿Eliminar producto?',
        html: 'Estás a punto de eliminar <strong>"' + nombre + '"</strong>.<br>Esta acción no se puede deshacer.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then(function(result) {
        if (result.isConfirmed) {
            var form = document.createElement('form');
            form.method = 'POST';
            form.action = url;
            var csrf = document.createElement('input');
            csrf.type  = 'hidden';
            csrf.name  = 'csrfmiddlewaretoken';
            csrf.value = document.cookie.split('; ')
                .find(row => row.startsWith('csrftoken='))
                .split('=')[1];
            form.appendChild(csrf);
            document.body.appendChild(form);
            form.submit();
        }
    });
}

// Abrir modal automáticamente si viene de gestionar marcas, tipos o unidades
window.addEventListener('DOMContentLoaded', function () {
    var params = new URLSearchParams(window.location.search);
    if (params.get('abrir_modal') === '1') {
        var modal = new bootstrap.Modal(document.getElementById('modalAgregar'));
        modal.show();
    }
});