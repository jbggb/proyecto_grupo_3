/**
 * confirmaciones.js — Diálogos de confirmación globales (SweetAlert2)
 * Namespace: window.App.confirmar
 *
 * MIGRACIÓN: La función global confirmarEliminar() fue separada en
 * funciones con nombre específico para evitar conflictos con
 * marcas.js y unidades.js.
 *
 * USO EN TEMPLATES:
 *   onclick="App.confirmar.eliminar('Nombre', this.closest('form'))"
 *   onclick="App.confirmar.eliminarMarca('Nombre', this.closest('form'))"
 *   onclick="App.confirmar.eliminarUnidad('Nombre', this.closest('form'))"
 */

(function () {
  'use strict';

  window.App = window.App || {};
  window.App.confirmar = window.App.confirmar || {};

  /**
   * Diálogo genérico de eliminación.
   * @param {string} nombre     - Nombre del elemento a eliminar.
   * @param {HTMLFormElement} formulario - Formulario que se enviará si confirma.
   */
  App.confirmar.eliminar = function (nombre, formulario) {
    Swal.fire({
      title: 'Eliminar "' + nombre + '"?',
      text: 'Esta acción no se puede deshacer.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar',
    }).then(function (result) {
      if (result.isConfirmed) {
        formulario.submit();
      }
    });
  };

  /**
   * Alias de compatibilidad — Marcas.
   * Igual al genérico pero con título específico.
   */
  App.confirmar.eliminarMarca = function (nombre, form) {
    Swal.fire({
      title: '¿Eliminar marca?',
      html: 'Estás a punto de eliminar <strong>"' + nombre + '"</strong>.<br>Esta acción no se puede deshacer.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar',
    }).then(function (result) {
      if (result.isConfirmed) { form.submit(); }
    });
  };

  /**
   * Alias de compatibilidad — Unidades de medida.
   */
  App.confirmar.eliminarUnidad = function (nombre, form) {
    Swal.fire({
      title: '¿Eliminar unidad?',
      html: 'Estás a punto de eliminar <strong>"' + nombre + '"</strong>.<br>Esta acción no se puede deshacer.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar',
    }).then(function (result) {
      if (result.isConfirmed) { form.submit(); }
    });
  };

  /**
   * Alias de compatibilidad — Tipos de producto.
   */
  App.confirmar.eliminarTipo = function (nombre, form) {
    App.confirmar.eliminar(nombre, form);
  };

  // ── Retrocompatibilidad global ──────────────────────────────────
  // Mantiene confirmarEliminar() funcional mientras se migran los
  // templates. REMOVER en la siguiente iteración.
  window.confirmarEliminar = App.confirmar.eliminar;

})();
