// Saca el banner (2560 × 1440) y la foto del canal (800 × 800) a salidas/businessformen/marca/canal/, comprueba que el
// logo y el lema caben en la zona segura del banner y deja las vistas de móvil, escritorio y tele.
//   node canales/businessformen/marca/canal/sacar.js
const { chromium } = require("playwright");
const path = require("path"), fs = require("fs");
const AQUI = __dirname, REPO = path.resolve(AQUI, "../../../.."), SAL = path.join(REPO, "salidas/businessformen/marca/canal");
(async () => {
  fs.mkdirSync(SAL, { recursive: true });
  const b = await chromium.launch();
  for (const [nombre, w, h] of [["banner", 2560, 1440], ["avatar", 800, 800]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto("file://" + path.join(AQUI, nombre + ".html"));
    await p.evaluate(() => document.fonts.ready);
    if (nombre === "banner") {
      const r = await p.evaluate(() => { const a = document.getElementById("bloque").getBoundingClientRect(); return [a.left, a.top, a.right, a.bottom].map(Math.round); });
      const dentro = r[0] >= 507 && r[1] >= 508 && r[2] <= 2053 && r[3] <= 931;
      console.log(`logo y lema en x ${r[0]}–${r[2]}, y ${r[1]}–${r[3]}: ${dentro ? "dentro" : "FUERA"} de la zona segura (507–2053, 508–931)`);
    }
    await p.screenshot({ path: path.join(SAL, nombre + ".png") });
    await p.close();
  }
  await b.close();
})();
