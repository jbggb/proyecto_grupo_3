// Función para mostrar el mensaje de error
function mostrarErrorCompra(campo, mensaje) {
    var span = document.createElement("span");
    span.className = "error-msg";
    span.style.color = "red";
    span.style.fontSize = "12px";
    span.style.display = "block";
    span.style.marginTop = "4px";
    span.textContent = mensaje;
    campo.parentNode.appendChild(span);
    campo.style.borderColor = "red";
}

document.addEventListener("DOMContentLoaded", function() {

    // =====================
    // VALIDAR FORMULARIO AGREGAR
    // =====================
    var formAgregar = document.querySelector("#modalAgregarCompra form");

    if (formAgregar) {
        formAgregar.addEventListener("submit", function(e) {

            var valido = true;

            var errores = formAgregar.querySelectorAll(".error-msg");
            for (var i = 0; i < errores.length; i++) {
                errores[i].remove();
            }

            // Validar Fecha
            var fecha = formAgregar.querySelector("input[name='fecha']");

            var hoy = new Date();
            var anio = hoy.getFullYear();
            var mes = String(hoy.getMonth() + 1).padStart(2, "0");
            var dia = String(hoy.getDate()).padStart(2, "0");

            var unaSemanaAtras = new Date();
            unaSemanaAtras.setDate(unaSemanaAtras.getDate() - 7);
            var anioS = unaSemanaAtras.getFullYear();
            var mesS = String(unaSemanaAtras.getMonth() + 1).padStart(2, "0");
            var diaS = String(unaSemanaAtras.getDate()).padStart(2, "0");
            var fechaSemana = anioS + "-" + mesS + "-" + diaS;

            if (fecha.value === "") {
                mostrarErrorCompra(fecha, "La fecha es obligatoria.");
                valido = false;
            } else if (fecha.value < fechaSemana) {
                mostrarErrorCompra(fecha, "La fecha no puede ser mayor a una semana en el pasado.");
                valido = false;
            } else if (fechaDuplicada(fecha.value, null)) {
                mostrarErrorCompra(fecha, "Ya existe una compra registrada en esa fecha.");
                valido = false;
            }

            // Validar Proveedor
            var proveedor = formAgregar.querySelector("select[name='proveedor']");
            if (proveedor.value === "") {
                mostrarErrorCompra(proveedor, "Seleccione un proveedor.");
                valido = false;
            }

            // Validar Producto
            var producto = formAgregar.querySelector("select[name='producto']");
            if (producto.value === "") {
                mostrarErrorCompra(producto, "Seleccione un producto.");
                valido = false;
            }

            // Validar Estado
            var estado = formAgregar.querySelector("select[name='estado']");
            if (estado.value === "") {
                mostrarErrorCompra(estado, "Seleccione un estado.");
                valido = false;
            }

            if (!valido) {
                e.preventDefault();
            }
        });
    }

    // =====================
    // VALIDAR FORMULARIOS EDITAR
    // =====================
    var formsEditar = document.querySelectorAll("[id^='modalEditarCompra'] form");

    for (var j = 0; j < formsEditar.length; j++) {
        formsEditar[j].addEventListener("submit", function(e) {

            var formActual = e.target;
            var valido = true;

            var errores = formActual.querySelectorAll(".error-msg");
            for (var i = 0; i < errores.length; i++) {
                errores[i].remove();
            }

            // Obtener id actual desde la action
            var action = formActual.getAttribute("action");
            var partes = action.split("/");
            var idActual = null;
            for (var k = 0; k < partes.length; k++) {
                if (partes[k] !== "" && !isNaN(partes[k])) {
                    idActual = partes[k];
                }
            }

            // Validar Fecha
            var fecha = formActual.querySelector("input[name='fecha']");

            var hoy = new Date();
            var unaSemanaAtras = new Date();
            unaSemanaAtras.setDate(unaSemanaAtras.getDate() - 7);
            var anioS = unaSemanaAtras.getFullYear();
            var mesS = String(unaSemanaAtras.getMonth() + 1).padStart(2, "0");
            var diaS = String(unaSemanaAtras.getDate()).padStart(2, "0");
            var fechaSemana = anioS + "-" + mesS + "-" + diaS;

            if (fecha.value === "") {
                mostrarErrorCompra(fecha, "La fecha es obligatoria.");
                valido = false;
            } else if (fecha.value < fechaSemana) {
                mostrarErrorCompra(fecha, "La fecha no puede ser mayor a una semana en el pasado.");
                valido = false;
            } else if (fechaDuplicada(fecha.value, idActual)) {
                mostrarErrorCompra(fecha, "Ya existe una compra registrada en esa fecha.");
                valido = false;
            }

            // Validar Proveedor
            var proveedor = formActual.querySelector("select[name='proveedor']");
            if (proveedor.value === "") {
                mostrarErrorCompra(proveedor, "Seleccione un proveedor.");
                valido = false;
            }

            // Validar Producto
            var producto = formActual.querySelector("select[name='producto']");
            if (producto.value === "") {
                mostrarErrorCompra(producto, "Seleccione un producto.");
                valido = false;
            }

            // Validar Estado
            var estado = formActual.querySelector("select[name='estado']");
            if (estado.value === "") {
                mostrarErrorCompra(estado, "Seleccione un estado.");
                valido = false;
            }

            if (!valido) {
                e.preventDefault();
            }
        });
    }

});

// =====================
// FUNCIÓN PARA DETECTAR FECHA DUPLICADA
// =====================
function fechaDuplicada(valor, idExcluir) {
    var filas = document.querySelectorAll("table tbody tr");
    for (var i = 0; i < filas.length; i++) {
        var celdas = filas[i].querySelectorAll("td");
        if (celdas.length > 0) {
            var idFila = celdas[0].textContent.trim();
            var fechaFila = celdas[4].textContent.trim();
            var partes = fechaFila.split("/");
            if (partes.length === 3) {
                var fechaConvertida = partes[2] + "-" + partes[1] + "-" + partes[0];
                if (fechaConvertida === valor && idFila !== idExcluir) {
                    return true;
                }
            }
        }
    }
    return false;
}