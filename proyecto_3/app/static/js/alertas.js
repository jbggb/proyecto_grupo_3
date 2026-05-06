/**
 * alertas.js — Auto-cierre de alertas Django después de 3 segundos.
 * Encapsulado en IIFE; no expone globals.
 * Requiere Bootstrap JS cargado antes (usa bootstrap.Alert).
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
      document.querySelectorAll('.alert').forEach(function (alerta) {
        var bsAlert = bootstrap.Alert.getOrCreateInstance(alerta);
        bsAlert.close();
      });
    }, 3000);
  });

})();
