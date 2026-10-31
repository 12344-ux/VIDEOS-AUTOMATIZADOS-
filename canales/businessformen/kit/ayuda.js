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
      // Entrada de la escena sobre la anterior (montar.py: escena(…, entrada=…)); la anterior sigue debajo mientras dura.
      const ENTRADA = /*ENTRADA*/null;
      const entradaEscena = () => {
        if (!ENTRADA) return;
        const d = ENTRADA.d, t = ENTRADA.tipo, filo = (css) => { const f = document.createElement("div"); f.style.cssText = "position:absolute;z-index:60;background:#b0122f;" + css; RAIZ.appendChild(f); return f; };
        const x = ENTRADA.x != null ? ENTRADA.x : {{ANCHO}} / 2, y = ENTRADA.y != null ? ENTRADA.y : {{ALTO}} / 2;
        // [recorte inicial, recorte final, curva, fracción de la duración]
        const CLIP = {
          cortina: ["inset(0% 100% 0% 0%)", "inset(0% 0% 0% 0%)", "power3.in", 0.5],
          barrido: ["inset(0% 0% 0% 100%)", "inset(0% 0% 0% 0%)", "power3.inOut", 1],
          subida: ["inset(100% 0% 0% 0%)", "inset(0% 0% 0% 0%)", "power3.inOut", 1],
          iris: [`circle(0% at ${x}px ${y}px)`, `circle(150% at ${x}px ${y}px)`, "power2.in", 1],
        }[t];
        tl.fromTo(RAIZ, { clipPath: CLIP[0] }, { clipPath: CLIP[1], duration: d * CLIP[3], ease: CLIP[2] }, 0);
        if (t === "cortina") {
          // El rojo cruza la escena anterior de izquierda a derecha y, al retirarse, descubre esta.
          const c = filo("left:0;top:0;width:100%;height:100%;");
          tl.fromTo(c, { scaleX: 1 }, { scaleX: 0, duration: d / 2, ease: "power3.out", transformOrigin: "right center" }, d / 2);
        } else if (t === "barrido" || t === "subida") {
          // El filo rojo va con el borde de la escena que entra.
          const f = t === "barrido" ? filo("left:0;top:0;width:10px;height:100%;") : filo("left:0;top:0;width:100%;height:10px;");
          tl.fromTo(f, t === "barrido" ? { x: {{ANCHO}} } : { y: {{ALTO}} }, Object.assign(t === "barrido" ? { x: 0 } : { y: 0 }, { duration: d, ease: "power3.inOut" }), 0);
          tl.to(f, { autoAlpha: 0, duration: 0.12 }, d);
        }
      };
      // 2.5D por capas (imagen/capas25d.py): el fondo se mueve poco y el frente recortado, más; la cámara parece avanzar.
      const profundidad = (t0, d, o = {}) => {
        tl.fromTo(o.fondo || ".fondo25", { scale: o.f0 || 1, x: 0, y: 0 }, { scale: o.f1 || 1.05, x: o.fx || 0, y: o.fy || 0, duration: d, ease: o.ease || "none" }, t0);
        tl.fromTo(o.frente || ".frente25", { scale: o.s0 || 1, x: 0, y: 0 }, { scale: o.s1 || 1.13, x: o.sx || 0, y: o.sy || 0, duration: d, ease: o.ease || "none" }, t0);
      };
      const fin = () => { entradaEscena(); tl.set({}, {}, DUR); window.__timelines["{{ID}}"] = tl; };
