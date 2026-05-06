/**
 * ventas.js — Módulo de Ventas
 * (Renombrado de Ventas.js → ventas.js para consistencia kebab-case)
 * carrito expuesto en App.ventas.carrito en lugar de global var carrito.
 */

(function () {
  'use strict';

  window.App = window.App || {};
  window.App.ventas = {
    carrito: []
  };

  // Alias local para legibilidad interna
  var carrito = App.ventas.carrito;

  document.addEventListener('DOMContentLoaded', function () {

    var modalCrear = document.getElementById('modalCrearVenta');
    if (!modalCrear) return;

    modalCrear.addEventListener('shown.bs.modal', function () {
      var input = document.getElementById('inputClienteCrear');
      if (input) {
        input.oninput = function () {
          validarCliente(
            this,
            document.getElementById('feedbackCliente'),
            document.getElementById('contadorCliente')
          );
        };
      }
    });

    modalCrear.addEventListener('hidden.bs.modal', function () {
      carrito.length = 0; // vaciar sin romper referencia
      renderCarrito();

      var input = document.getElementById('inputClienteCrear');
      if (input) input.value = '';

      var fc = document.getElementById('feedbackCliente');
      if (fc) fc.textContent = '';

      var cc = document.getElementById('contadorCliente');
      if (cc) cc.textContent = '0/30 caracteres';

      var se = document.getElementById('selectEstado');
      if (se) se.value = '';

      var fe = document.getElementById('feedbackEstado');
      if (fe) fe.textContent = '';

      var bus = document.getElementById('busquedaProductos');
      if (bus) {
        bus.value = '';
        document.querySelectorAll('.producto-card').forEach(function (c) {
          c.style.display = 'block';
        });
      }
    });

    var busqueda = document.getElementById('busquedaProductos');
    if (busqueda) {
      busqueda.addEventListener('input', function () {
        var term = this.value.toLowerCase();
        document.querySelectorAll('.producto-card').forEach(function (card) {
          card.style.display = card.getAttribute('data-nombre').includes(term) ? 'block' : 'none';
        });
      });
    }

    document.querySelectorAll('.input-cliente-editar').forEach(function (input) {
      var feedback = input.parentElement.querySelector('.feedback-editar');
      if (input && feedback) {
        input.addEventListener('input', function () {
          validarCliente(input, feedback, null);
        });
      }
    });

  }); // end DOMContentLoaded

  // ── Funciones internas ────────────────────────────────────────────
  // Estas funciones son llamadas desde el HTML inline de Ventas.
  // Se exponen en App.ventas para no contaminar el scope global,
  // pero se mantienen aliases globales por retrocompatibilidad.

  function validarCliente(input, feedback, contador) {
    var val = input ? input.value.trim() : '';
    if (contador) {
      contador.textContent = val.length + '/30 caracteres';
    }
    if (feedback) {
      if (val.length === 0) {
        feedback.textContent = '⚠ El nombre del cliente es obligatorio.';
        feedback.style.color = '#dc3545';
      } else if (val.length < 3) {
        feedback.textContent = '⚠ Mínimo 3 caracteres.';
        feedback.style.color = '#fd7e14';
      } else if (val.length > 30) {
        feedback.textContent = '⚠ Máximo 30 caracteres.';
        feedback.style.color = '#dc3545';
      } else {
        feedback.textContent = '✓ OK';
        feedback.style.color = '#198754';
      }
    }
  }

  function renderCarrito() {
    var tbody = document.getElementById('carritoBody');
    var totalEl = document.getElementById('totalVenta');
    var carritoInput = document.getElementById('carritoInput');

    if (!tbody) return;

    tbody.innerHTML = '';
    var total = 0;

    carrito.forEach(function (item, idx) {
      var subtotal = item.precio * item.cantidad;
      total += subtotal;
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td>' + item.nombre + '</td>' +
        '<td>$' + item.precio.toLocaleString() + '</td>' +
        '<td>' +
          '<input type="number" min="1" value="' + item.cantidad + '" ' +
          'class="form-control form-control-sm" style="width:70px" ' +
          'onchange="App.ventas.actualizarCantidad(' + idx + ', this.value)">' +
        '</td>' +
        '<td>$' + subtotal.toLocaleString() + '</td>' +
        '<td><button class="btn btn-sm btn-danger" onclick="App.ventas.eliminarDelCarrito(' + idx + ')">✕</button></td>';
      tbody.appendChild(tr);
    });

    if (totalEl) totalEl.textContent = '$' + total.toLocaleString();
    if (carritoInput) carritoInput.value = JSON.stringify(carrito);
  }

  App.ventas.agregarAlCarrito = function (id, nombre, precio) {
    var idx = carrito.findIndex(function (i) { return i.id === id; });
    if (idx >= 0) {
      carrito[idx].cantidad++;
    } else {
      carrito.push({ id: id, nombre: nombre, precio: precio, cantidad: 1 });
    }
    renderCarrito();
  };

  App.ventas.eliminarDelCarrito = function (idx) {
    carrito.splice(idx, 1);
    renderCarrito();
  };

  App.ventas.actualizarCantidad = function (idx, val) {
    var n = parseInt(val, 10);
    if (n > 0) { carrito[idx].cantidad = n; }
    renderCarrito();
  };

  // ── Retrocompatibilidad global ──────────────────────────────────
  window.agregarAlCarrito  = App.ventas.agregarAlCarrito;
  window.eliminarDelCarrito= App.ventas.eliminarDelCarrito;
  window.actualizarCantidad= App.ventas.actualizarCantidad;

})();
