const TEXTO = 'Bienvenidos a la raza humana';

const btn    = document.getElementById('save-button');
const status = document.getElementById('status');

btn.addEventListener('click', async () => {
  btn.disabled = true;
  status.className = '';
  status.textContent = 'Guardando…';

  try {
    const res = await fetch('/api/count', {
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
    status.textContent = `❌ Error al conectar con el backend. Notificar a GG.`;
    console.error('Backend error:', e.message);
  } finally {
    btn.disabled = false;
  }
});
