
function bloquearNombreUnidad(input) {
    var antes = input.value;
    var limpio = antes.replace(/[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]/g, '');
    limpio = limpio.replace(/ {2,}/g, ' ');
    if (antes !== limpio) {
        input.value = limpio;
        var el = document.getElementById('unidad_error');
        el.textContent = 'Solo se permiten letras y espacios.';
        el.style.display = 'block';
        clearTimeout(el._timer);
        el._timer = setTimeout(function() { el.style.display = 'none'; }, 3000);
    }
}
