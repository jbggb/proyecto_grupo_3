/**
 * escaner.js — Escáner de código de barras con Html5-Qrcode
 * Integración con Open Food Facts para productos colombianos
 * Solo se inicializa en la página de productos
 */
(function () {
  'use strict';

  // Solo ejecutar en página de productos
  if (!document.getElementById('btnAbrirEscaner')) return;

  var scanner      = null;
  var scanning     = false;
  var lastCode     = '';
  var lastTime     = 0;
  var DEBOUNCE_MS  = 2500;

  var btnAbrir     = document.getElementById('btnAbrirEscaner');
  var modalEl      = document.getElementById('modalEscaner');
  var modalBS      = null;
  var btnCamara    = document.getElementById('escaner-btn-camara');
  var btnImagen    = document.getElementById('escaner-btn-imagen');
  var inputImagen  = document.getElementById('escaner-input-imagen');
  var areaLector   = document.getElementById('escaner-area-lector');
  var statusEl     = document.getElementById('escaner-status');
  var resultadoEl  = document.getElementById('escaner-resultado');

  // ── Abrir modal ──
  btnAbrir.addEventListener('click', function () {
    modalBS = bootstrap.Modal.getOrCreateInstance(modalEl);
    modalBS.show();
  });

  modalEl.addEventListener('hidden.bs.modal', function () {
    detenerCamara();
    resetResultado();
  });

  // ── Cambiar modo ──
  btnCamara.addEventListener('click', function () {
    btnCamara.classList.add('active');
    btnImagen.classList.remove('active');
    inputImagen.style.display = 'none';
    areaLector.innerHTML = '';
    iniciarCamara();
  });

  btnImagen.addEventListener('click', function () {
    btnImagen.classList.add('active');
    btnCamara.classList.remove('active');
    detenerCamara();
    areaLector.innerHTML = '';
    inputImagen.style.display = 'block';
    inputImagen.click();
  });

  inputImagen.addEventListener('change', function () {
    if (!this.files || !this.files[0]) return;
    var file = this.files[0];
    setStatus('Analizando imagen...', 'info');
    resetResultado();

    var html5qr = new Html5Qrcode('escaner-area-lector');
    html5qr.scanFile(file, true)
      .then(function (codigo) {
        html5qr.clear();
        procesarCodigo(codigo);
      })
      .catch(function () {
        html5qr.clear();
        setStatus('No se pudo leer el código de barras en la imagen. Intenta con mejor iluminación.', 'error');
      });

    this.value = '';
  });

  // ── Cámara ──
  function iniciarCamara() {
    if (scanning) return;
    areaLector.innerHTML = '';
    setStatus('Apunta la cámara al código de barras...', 'info');
    resetResultado();

    scanner = new Html5Qrcode('escaner-area-lector');
    scanner.start(
      { facingMode: 'environment' },
      { fps: 10, qrbox: { width: 260, height: 120 }, aspectRatio: 1.5 },
      function (codigo) {
        var now = Date.now();
        if (codigo === lastCode && (now - lastTime) < DEBOUNCE_MS) return;
        lastCode = codigo;
        lastTime = now;
        procesarCodigo(codigo);
      },
      function () {}
    ).then(function () {
      scanning = true;
    }).catch(function (err) {
      setStatus('No se pudo acceder a la cámara. Revisa los permisos del navegador.', 'error');
    });
  }

  function detenerCamara() {
    if (scanner && scanning) {
      scanner.stop().catch(function(){});
      scanning = false;
      scanner = null;
    }
  }

  // ── Procesar código ──
  function procesarCodigo(codigo) {
    setStatus('Buscando: ' + codigo + '...', 'info');
    resetResultado();

    fetch('/productos/buscar-escaner/?codigo=' + encodeURIComponent(codigo))
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.estado === 'encontrado') {
          mostrarEncontrado(data);
        } else {
          mostrarNoEncontrado(data);
        }
      })
      .catch(function () {
        setStatus('Error de conexión al buscar el producto.', 'error');
      });
  }

  // ── Mostrar producto encontrado ──
  function mostrarEncontrado(data) {
    setStatus('', '');
    resultadoEl.innerHTML = `
      <div style="background:var(--c-success-l);border:1px solid rgba(39,174,96,0.25);border-radius:var(--r-md);padding:18px;margin-top:14px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
          <div style="width:40px;height:40px;background:var(--c-success-l);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:var(--c-success);">
            <i class="fa-solid fa-circle-check"></i>
          </div>
          <div>
            <div style="font-weight:700;font-size:.95rem;color:var(--tx-primary);">${data.nombre}</div>
            <div style="font-size:.78rem;color:var(--tx-muted);">Código: ${data.codigo} · Stock actual: <strong style="color:var(--c-success);">${data.stock}</strong></div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
          <label style="font-size:.82rem;color:var(--tx-secondary);white-space:nowrap;">Agregar al stock:</label>
          <input type="number" id="escaner-cantidad" value="1" min="1" max="9999"
            style="width:80px;padding:7px 10px;background:var(--bg-input);border:1px solid var(--bd-default);border-radius:var(--r-sm);color:var(--tx-primary);font-size:.9rem;">
          <button onclick="window.escaner_agregarStock(${data.id})" class="btn btn-success btn-sm" style="flex:1;">
            <i class="fa-solid fa-plus"></i> Actualizar stock
          </button>
        </div>
      </div>`;
  }

  // ── Mostrar no encontrado ──
  function mostrarNoEncontrado(data) {
    var infoExtra = '';
    if (data.nombre_sugerido) {
      infoExtra = `
        <div style="background:var(--c-info-l);border:1px solid rgba(41,128,185,0.2);border-radius:var(--r-sm);padding:10px 14px;margin-bottom:12px;font-size:.82rem;">
          <i class="fa-solid fa-lightbulb" style="color:var(--c-info);margin-right:6px;"></i>
          <strong>Open Food Facts encontró:</strong> ${data.nombre_sugerido}
          ${data.marca_sugerida ? ' · <em>' + data.marca_sugerida + '</em>' : ''}
          <br><small style="color:var(--tx-muted);">Estos datos se pre-llenarán en el formulario.</small>
        </div>`;
    }

    setStatus('', '');
    resultadoEl.innerHTML = `
      <div style="background:var(--c-gold-l);border:1px solid rgba(232,168,56,0.25);border-radius:var(--r-md);padding:18px;margin-top:14px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
          <div style="width:40px;height:40px;background:var(--c-gold-l);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:var(--c-gold);">
            <i class="fa-solid fa-circle-question"></i>
          </div>
          <div>
            <div style="font-weight:700;font-size:.95rem;color:var(--tx-primary);">Producto no registrado</div>
            <div style="font-size:.78rem;color:var(--tx-muted);">Código: ${data.codigo}</div>
          </div>
        </div>
        ${infoExtra}
        <button onclick="window.escaner_abrirFormulario('${data.codigo}', '${(data.nombre_sugerido || '').replace(/'/g, "\\'")}', '${(data.marca_sugerida || '').replace(/'/g, "\\'")}')"
          class="btn btn-warning w-100">
          <i class="fa-solid fa-plus"></i> Registrar este producto
        </button>
      </div>`;
  }

  // ── Actualizar stock ──
  window.escaner_agregarStock = function (productoId) {
    var cantidadEl = document.getElementById('escaner-cantidad');
    var cantidad   = parseInt(cantidadEl ? cantidadEl.value : 1);
    if (!cantidad || cantidad < 1) {
      Swal.fire({ icon: 'warning', title: 'Cantidad inválida', text: 'Ingresa una cantidad mayor a 0.',
        background: '#0e1420', color: '#f0f4ff', confirmButtonColor: '#c0392b' });
      return;
    }

    var csrf = document.cookie.split(';').map(function(c){ return c.trim(); })
      .find(function(c){ return c.startsWith('csrftoken='); });
    csrf = csrf ? csrf.split('=')[1] : '';

    fetch('/productos/actualizar-stock-nuevo/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
      body: JSON.stringify({ id: productoId, cantidad: cantidad })
    })
    .then(function(r){ return r.json(); })
    .then(function(data) {
      if (data.ok) {
        Swal.fire({
          icon: 'success',
          title: 'Stock actualizado',
          html: '<strong>' + data.nombre + '</strong><br>Nuevo stock: <strong style="color:#27ae60;">' + data.stock_nuevo + '</strong>',
          background: '#0e1420', color: '#f0f4ff', confirmButtonColor: '#27ae60', timer: 3000, timerProgressBar: true,
        }).then(function() {
          if (modalBS) modalBS.hide();
          window.location.reload();
        });
      } else {
        Swal.fire({ icon: 'error', title: 'Error', text: data.error,
          background: '#0e1420', color: '#f0f4ff', confirmButtonColor: '#c0392b' });
      }
    })
    .catch(function() {
      Swal.fire({ icon: 'error', title: 'Error de conexión',
        background: '#0e1420', color: '#f0f4ff', confirmButtonColor: '#c0392b' });
    });
  };

  // ── Abrir formulario de creación ──
  window.escaner_abrirFormulario = function (codigo, nombre, marca) {
    if (modalBS) modalBS.hide();
    // Pre-llenar el formulario del modal de agregar producto
    setTimeout(function () {
      var inputCodigo = document.querySelector('#modalAgregar [name="codigo_barras"]');
      var inputNombre = document.querySelector('#modalAgregar [name="nombre"]');
      if (inputCodigo) inputCodigo.value = codigo;
      if (inputNombre && nombre) inputNombre.value = nombre;
      bootstrap.Modal.getOrCreateInstance(document.getElementById('modalAgregar')).show();
    }, 400);
  };

  // ── Helpers ──
  function setStatus(msg, tipo) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    statusEl.style.color = tipo === 'error' ? 'var(--c-danger)' :
                           tipo === 'info'  ? 'var(--tx-secondary)' : '';
  }

  function resetResultado() {
    if (resultadoEl) resultadoEl.innerHTML = '';
  }

})();
