/**
 * ═══════════════════════════════════════════════════════════════════════
 * MÓDULO DE REGISTRO - JavaScript
 * Funcionalidad para mostrar/ocultar contraseñas y validación en tiempo real
 * ═══════════════════════════════════════════════════════════════════════
 */

document.addEventListener('DOMContentLoaded', function() {

    // ── Toggle contraseña ───────────────────────────────────────────────
    const togglePassword1 = document.getElementById('togglePassword1');
    const passwordInput1  = document.getElementById('id_contrasena');
    const eyeIcon1        = document.getElementById('eyeIcon1');

    if (togglePassword1 && passwordInput1 && eyeIcon1) {
        togglePassword1.addEventListener('click', function() {
            const type = passwordInput1.type === 'password' ? 'text' : 'password';
            passwordInput1.type = type;
            eyeIcon1.classList.toggle('fa-eye', type === 'password');
            eyeIcon1.classList.toggle('fa-eye-slash', type === 'text');
        });
    }

    // ── Toggle confirmar contraseña ─────────────────────────────────────
    const togglePassword2 = document.getElementById('togglePassword2');
    const passwordInput2  = document.getElementById('id_confirmar_contrasena');
    const eyeIcon2        = document.getElementById('eyeIcon2');

    if (togglePassword2 && passwordInput2 && eyeIcon2) {
        togglePassword2.addEventListener('click', function() {
            const type = passwordInput2.type === 'password' ? 'text' : 'password';
            passwordInput2.type = type;
            eyeIcon2.classList.toggle('fa-eye', type === 'password');
            eyeIcon2.classList.toggle('fa-eye-slash', type === 'text');
        });
    }

    // ── Nombre: solo letras, espacios y tildes ──────────────────────────
    const inputNombre = document.getElementById('id_nombre');
    if (inputNombre) {
        inputNombre.addEventListener('keypress', function(e) {
            if (e.key.length > 1) return; // permitir Backspace, flechas, etc.
            if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]$/.test(e.key)) e.preventDefault();
        });
        inputNombre.addEventListener('paste', function(e) {
            const texto = (e.clipboardData || window.clipboardData).getData('text');
            if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(texto)) e.preventDefault();
        });
    }

    // ── Usuario: solo letras, números y guión bajo ──────────────────────
    const inputUsuario = document.getElementById('id_usuario');
    if (inputUsuario) {
        inputUsuario.addEventListener('keypress', function(e) {
            if (e.key.length > 1) return;
            if (!/^[a-zA-Z0-9_]$/.test(e.key)) e.preventDefault();
        });
        inputUsuario.addEventListener('paste', function(e) {
            const texto = (e.clipboardData || window.clipboardData).getData('text');
            if (!/^[a-zA-Z0-9_]+$/.test(texto)) e.preventDefault();
        });
    }

    // ── Validar que las contraseñas coincidan al enviar ─────────────────
    const form = document.querySelector('form');
    if (form && passwordInput1 && passwordInput2) {
        form.addEventListener('submit', function(e) {
            if (passwordInput1.value !== passwordInput2.value) {
                e.preventDefault();
                alert('Las contraseñas no coinciden. Por favor verifica e intenta nuevamente.');
                passwordInput2.focus();
            }
        });
    }

});