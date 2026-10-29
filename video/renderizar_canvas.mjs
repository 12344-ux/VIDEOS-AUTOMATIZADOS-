/*
 * Convierte una escena HTML animada en MP4: Chromium pinta cada cuadro y ffmpeg
 * los une. La escena tiene que definir window.listo (una promesa) y
 * window.cuadro(t), que pinta el instante t (en segundos) y devuelve el cuadro
 * como data URL PNG. Como cada cuadro depende solo de t, el render es exacto y
 * repetible. Ver video/plantilla_titulo.html.
 *
 *   node video/renderizar_canvas.mjs escena.html salida.mp4 --duracion 5
 *   node video/renderizar_canvas.mjs escena.html salida.mp4 --ancho 1280 --alto 720 --fps 30 \
 *     --audio pista.wav --param titulo="El faro" --param acento=#F2A541
 *
 * Para el desenfoque de movimiento se pintan varios instantes por cuadro
 * (--subcuadros, 2 por defecto) y ffmpeg los promedia: un obturador de 180°.
 * Necesita Playwright con Chromium y ffmpeg.
 */
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const [escena, salida, ...resto] = process.argv.slice(2);
if (!escena || !salida) {
  console.error('Uso: node video/renderizar_canvas.mjs escena.html salida.mp4 [--duracion 5] [--ancho 1920] [--alto 1080] [--fps 60] [--subcuadros 2] [--audio pista.wav] [--param clave=valor]');
  process.exit(1);
}
const opciones = { ancho: 1920, alto: 1080, duracion: 5, fps: 60, subcuadros: 2, audio: null };
const parametros = new URLSearchParams();
for (let i = 0; i < resto.length; i += 2) {
  const clave = resto[i].replace(/^--/, '');
  if (clave === 'param') {
    const [k, ...v] = resto[i + 1].split('=');
    parametros.set(k, v.join('='));
  } else {
    opciones[clave] = clave === 'audio' ? resto[i + 1] : Number(resto[i + 1]);
  }
}
const { ancho, alto, duracion, fps, subcuadros } = opciones;
parametros.set('render', '');
parametros.set('w', ancho);
parametros.set('h', alto);
parametros.set('duracion', duracion);

const navegador = await chromium.launch();
try {
  const pagina = await navegador.newPage({ viewport: { width: ancho, height: alto } });
  pagina.on('pageerror', e => console.error('error en la escena:', e.message));
  const url = pathToFileURL(path.resolve(escena));
  url.search = parametros.toString();
  await pagina.goto(url.href);
  await pagina.evaluate(() => window.listo);

  const ffmpeg = spawn('ffmpeg', [
    '-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(fps * subcuadros), '-c:v', 'png', '-i', '-',
    ...(opciones.audio ? ['-i', opciones.audio] : []),
    '-vf', `tmix=frames=${subcuadros},framestep=${subcuadros},scale=out_color_matrix=bt709:out_range=tv,format=yuv420p`,
    '-r', String(fps),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    ...(opciones.audio ? ['-c:a', 'aac', '-b:a', '192k'] : []),
    '-t', String(duracion), '-movflags', '+faststart', salida,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });
  const terminado = new Promise((resolver, rechazar) => {
    ffmpeg.on('error', rechazar);
    ffmpeg.on('close', codigo => (codigo === 0 ? resolver() : rechazar(new Error(`ffmpeg salió con ${codigo}`))));
  });

  const total = Math.round(duracion * fps * subcuadros);
  const inicio = Date.now();
  for (let i = 0; i < total; i++) {
    const png = await pagina.evaluate(t => window.cuadro(t), i / (fps * subcuadros));
    const bytes = Buffer.from(png.slice(png.indexOf(',') + 1), 'base64');
    if (!ffmpeg.stdin.write(bytes)) await new Promise(r => ffmpeg.stdin.once('drain', r));
    if (i % (fps * subcuadros) === 0) process.stdout.write(`\r${Math.round((i / total) * 100)} %`);
  }
  ffmpeg.stdin.end();
  await terminado;
  console.log(`\r${salida}: ${duracion} s en ${((Date.now() - inicio) / 1000).toFixed(1)} s de render`);
} finally {
  await navegador.close();
}
