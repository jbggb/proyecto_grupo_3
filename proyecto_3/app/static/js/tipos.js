function bloquearNombreTipo(input) {
    var antes = input.value;
    var limpio = antes.replace(/[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]/g, '');
    limpio = limpio.replace(/ {2,}/g, ' ');
    if (antes !== limpio) {
        input.value = limpio;
        var el = document.getElementById('tipo_error');
        el.textContent = 'Solo se permiten letras y espacios.';
        el.style.display = 'block';
        clearTimeout(el._timer);
        el._timer = setTimeout(function() { el.style.display = 'none'; }, 3000);
    }
}

//por ahora no se valida el precio del tipo, pero se podría agregar una función similar a validarPrecio() de productos.js si se decide hacerlo en el futuro.