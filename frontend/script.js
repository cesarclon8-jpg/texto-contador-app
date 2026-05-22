// En Cloud Run el backend corre como servicio separado.
// BACKEND_URL se sustituye en build time via envsubst en el Dockerfile,
// o usa la URL hardcodeada de producción como fallback.
const BACKEND_URL = window.BACKEND_URL || 'https://dpa-texto-contador-app-t-run-backend-551e-c6a35nwrna-ew.a.run.app';
const TEXTO = 'Bienvenidos a la raza humana';

const btn    = document.getElementById('save-button');
const status = document.getElementById('status');

btn.addEventListener('click', async () => {
  btn.disabled = true;
  status.className = '';
  status.textContent = 'Guardando…';

  try {
    const res = await fetch(`${BACKEND_URL}/count`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: TEXTO }),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    status.className = 'ok';
    status.textContent = `✅ Guardado. Palabras: ${data.word_count} | Caracteres: ${data.char_count}`;
  } catch (e) {
    status.className = 'error';
    status.textContent = `❌ Error al guardar: ${e.message}`;
  } finally {
    btn.disabled = false;
  }
});
