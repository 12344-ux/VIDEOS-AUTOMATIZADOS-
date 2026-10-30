      // Ayudas comunes de las escenas (kit/ayuda.js, las inserta kit/montar.py). Todo es función del tiempo local.
      const W = /*W*/, T0 = {{T0}}, DUR = {{DUR}};
      const RAIZ = document.getElementById("{{ID}}");
      const limpia = (s) => s.toLowerCase().replace(/[^\wáéíóúüñ]/g, "");
      // w("palabra", n): cuándo empieza la aparición n de esa palabra, en el tiempo de la escena; f(): cuándo acaba.
      const w = (p, n = 1, fin = false) => {
        const l = W[limpia(p)];
        if (!l || !l[n - 1]) throw new Error(`{{ID}}: no está «${p}» (${n})`);
        return l[n - 1][fin ? 1 : 0] - T0;
      };
      const f = (p, n = 1) => w(p, n, true);
      // serie("palabra", k, n): el comienzo de las k palabras seguidas desde la aparición n de esa palabra.
      const L = /*L*/;
      const serie = (p, k, n = 1) => {
        const i = L.map((q, j) => (q[0] === limpia(p) ? j : -1)).filter((j) => j >= 0)[n - 1];
        if (i == null) throw new Error(`{{ID}}: no está «${p}» (${n})`);
        return L.slice(i, i + k).map((q) => q[1] - T0);
      };
      const $ = (s) => RAIZ.querySelector(s);
      const $$ = (s) => Array.from(RAIZ.querySelectorAll(s));
      // Cifras a la española: punto de miles y signo menos tipográfico.
      const fmt = (n, signo) => {
        const a = Math.round(Math.abs(n)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        return (n < 0 ? "−" : signo && n > 0 ? "+" : "") + a;
      };
      const tl = gsap.timeline({ paused: true });
      // Sube desde su máscara: 140 % para que las tildes de las mayúsculas (Á, É, Ú) no asomen antes de tiempo.
      const sube = (sel, t, d = 0.45, ease = "expo.out") => tl.fromTo(sel, { yPercent: 140 }, { yPercent: 0, duration: d, ease }, t);
      const entra = (sel, t, d = 0.45, dy = 26) => tl.fromTo(sel, { autoAlpha: 0, y: dy }, { autoAlpha: 1, y: 0, duration: d, ease: "expo.out" }, t);
      const aparece = (sel, t, d = 0.3, max = 1) => tl.fromTo(sel, { autoAlpha: 0 }, { autoAlpha: max, duration: d, ease: "power2.out" }, t);
      const sale = (sel, t, d = 0.2) => tl.to(sel, { autoAlpha: 0, duration: d, ease: "power2.in" }, t);
      // Contador: el texto del elemento va de «desde» a «hasta» entre t y t + d.
      const cuenta = (el, desde, hasta, t, d, o = {}) => {
        el = typeof el === "string" ? $(el) : el;
        const v = { x: desde }, pinta = () => { el.textContent = (o.pre || "") + (o.crudo ? String(Math.round(v.x)) : fmt(v.x, o.signo)) + (o.suf || ""); };
        pinta();
        tl.fromTo(v, { x: desde }, { x: hasta, duration: d, ease: o.ease || "power2.out", onUpdate: pinta }, t);
      };
      // Trazo que se dibuja: el path necesita pathLength="100" y stroke-dasharray="100 100". Se oculta hasta que empieza:
      // con remates redondos o cuadrados, el guion de largo cero deja un punto en el extremo.
      const traza = (sel, t, d, ease = "power2.inOut") => {
        tl.fromTo(sel, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.01 }, t);
        return tl.fromTo(sel, { strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: d, ease }, t);
      };
      // Trocea el texto de un elemento en palabras con máscara (.pal > span) y devuelve los span.
      const trocea = (el) => {
        el = typeof el === "string" ? $(el) : el;
        // Respeta los <br>: cada renglón se trocea por separado.
        el.innerHTML = el.innerHTML.split(/<br\s*\/?>/i).map((h) => h.replace(/<[^>]+>/g, " ").trim().split(/\s+/).filter(Boolean)
          .map((p) => `<span class="pal"><span>${p}</span></span>`).join("")).join("<br>");
        return Array.from(el.querySelectorAll(".pal > span"));
      };
      // Cortinas rojas: la que se lleva la escena (sale) y la que se retira al empezar (entra).
      const cortina = (modo, d) => {
        const c = document.createElement("div");
        c.className = "cortina"; RAIZ.appendChild(c);
        if (modo === "entra") tl.fromTo(c, { scaleX: 1, autoAlpha: 1, transformOrigin: "right center" }, { scaleX: 0, duration: d || 0.42, ease: "power4.out" }, 0);
        else tl.fromTo(c, { scaleX: 0, autoAlpha: 1, transformOrigin: "left center" }, { scaleX: 1, duration: d || 0.3, ease: "power4.in" }, DUR - (d || 0.3));
      };
      // Dibujos en función del tiempo (lo que GSAP no interpola bien: un punto que recorre un círculo, por ejemplo).
      const alBuscar = (dibujar) => { window.addEventListener("hf-seek", (ev) => dibujar(ev.detail.time - T0)); dibujar(0); };
      // Avance 0 → 1 entre t0 y t0 + d, con su curva.
      const paso = (t, t0, d, curva) => gsap.parseEase(curva || "power2.inOut")(Math.min(1, Math.max(0, (t - t0) / d)));
      const fin = () => { tl.set({}, {}, DUR); window.__timelines["{{ID}}"] = tl; };
