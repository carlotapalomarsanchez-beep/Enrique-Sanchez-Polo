(() => {
  /* =========================================================
     CONFIGURACIÓN
     ========================================================= */
  // ID de medición de Google Analytics 4 (p. ej. 'G-ABC123XYZ').
  // Vacío = no se carga Analytics. No es un secreto: es público por diseño.
  const GA_ID = '';

  const root = document.documentElement;
  const body = document.body;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const remember = () => { try { sessionStorage.setItem('esp-intro', '1'); } catch (e) {} };

  /* ---------- Títulos palabra a palabra ---------- */
  $$('[data-split]').forEach(el => {
    let i = 0;
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            const w = document.createElement('span');
            const inner = document.createElement('span');
            w.className = 'w';
            inner.textContent = part;
            inner.style.setProperty('--i', i++);
            w.appendChild(inner);
            frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') {
          walk(n);
        }
      });
    };
    walk(el);
  });

  /* ---------- Aparición al hacer scroll ---------- */
  const countUp = el => {
    const target = +el.dataset.count;
    if (reduce) { el.textContent = target; return; }
    const t0 = performance.now();
    const step = t => {
      const p = clamp((t - t0) / 1600);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-visible');
      $$('[data-count]', e.target).forEach(countUp);
      io.unobserve(e.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  const startPage = () => {
    body.classList.add('intro-finished');
    $$('.reveal, [data-split]').forEach(el => io.observe(el));
  };

  /* ---------- Intro de la primera visita ---------- */
  const intro = $('.intro');
  const firstVisit = root.classList.contains('first-visit') && intro && !reduce;
  if (firstVisit) {
    remember();
    $$('[data-count]').forEach(el => (el.textContent = '0'));
    const num = $('.intro__num');
    const bar = $('.intro__bar span');
    const t0 = performance.now();
    const tick = t => {
      const p = clamp((t - t0) / 1900);
      const e = 1 - Math.pow(1 - p, 3);
      num.textContent = Math.round(e * 100);
      bar.style.transform = `scaleX(${e})`;
      if (p < 1) return requestAnimationFrame(tick);
      setTimeout(() => {
        intro.classList.add('is-done');
        setTimeout(startPage, 350);
        setTimeout(() => intro.classList.add('is-gone'), 1200);
      }, 250);
    };
    requestAnimationFrame(tick);
  } else {
    remember();
    if (intro) intro.classList.add('is-gone');
    if (!reduce) $$('[data-count]').forEach(el => (el.textContent = '0'));
    startPage();
  }

  /* ---------- Cortina entre páginas ---------- */
  const curtain = $('.curtain');
  if (curtain && root.classList.contains('entering')) {
    curtain.classList.add('out');
    requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove('entering')));
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (!a || reduce || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
    const href = a.getAttribute('href') || '';
    if (!href || href.startsWith('#') || /^(mailto|tel):/.test(href)) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || url.pathname === location.pathname) return;
    e.preventDefault();
    curtain.classList.remove('out');
    body.classList.add('is-leaving');
    setTimeout(() => { location.href = a.href; }, 650);
  });
  window.addEventListener('pageshow', e => {
    if (e.persisted) { body.classList.remove('is-leaving'); curtain.classList.add('out'); }
  });

  /* ---------- Menú ---------- */
  const nav = $('.nav');
  const toggle = $('.nav__toggle');
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });
  $$('.nav__links a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', false);
  }));

  /* =========================================================
     PORTADA: EDIFICIO 3D QUE GIRA Y SE CONSTRUYE AL BAJAR
     ========================================================= */
  const journey = $('.journey');
  if (journey) {
    const art = $('.journey__art', journey);
    const canvas = $('.model', journey);
    const ctx = canvas.getContext('2d');
    const names = art.dataset.phases.split('|');
    const T = [0, 0.08, 0.22, 0.55, 0.75, 0.9]; // inicio de cada fase
    const pctEl = $('.build__pct', journey);
    const barEl = $('.build__bar i', journey);
    const labelEl = $('.obra__phase', journey);
    const numEl = $('.obra__n', journey);

    // --- Modelo: aristas con su momento de construcción [t0, t1] ---
    const E = [];
    const WIN = [];
    const add = (a, b, t0, t1, kind = 'ink') => E.push({ a, b, t0, t1, kind });
    const poly = (pts, t0, t1, kind) => {
      const n = pts.length;
      pts.forEach((p, i) => add(p, pts[(i + 1) % n], t0 + (t1 - t0) * i / n, t0 + (t1 - t0) * (i + 1) / n, kind));
    };
    const rectY = (x0, x1, z0, z1, y) => [[x0, y, z0], [x1, y, z0], [x1, y, z1], [x0, y, z1]];
    const X = [-3, -1, 1, 3], Z = [-2, 0, 2], FL = 5;

    // Cimentación: parcela y zapatas
    poly(rectY(-4.6, 4.6, -3.6, 3.6, 0), 0.08, 0.13, 'gold');
    X.forEach((x, i) => Z.forEach((z, j) => {
      const t = 0.13 + ((i * 3 + j) / 12) * 0.07;
      poly(rectY(x - 0.35, x + 0.35, z - 0.35, z + 0.35, 0), t, t + 0.02);
    }));

    // Estructura: pilares y forjados planta a planta
    for (let k = 0; k < FL; k++) {
      const t0 = 0.22 + k * 0.066, tm = t0 + 0.033, t1 = t0 + 0.066;
      X.forEach(x => Z.forEach(z => add([x, k, z], [x, k + 1, z], t0, tm)));
      poly(rectY(-3, 3, -2, 2, k + 1), tm, t1);
      add([-1, k + 1, -2], [-1, k + 1, 2], tm, t1);
      add([1, k + 1, -2], [1, k + 1, 2], tm, t1);
      add([-3, k + 1, 0], [3, k + 1, 0], tm, t1);
    }

    // Grúa
    add([4.3, 0, -2.9], [4.3, 7.4, -2.9], 0.2, 0.26, 'crane');
    add([5.8, 7.4, -2.9], [-2.6, 7.4, -2.9], 0.26, 0.3, 'crane');
    add([4.3, 8.2, -2.9], [-2.6, 7.4, -2.9], 0.28, 0.31, 'crane');
    add([4.3, 8.2, -2.9], [5.8, 7.4, -2.9], 0.28, 0.31, 'crane');
    add([-0.6, 7.4, -2.9], [-0.6, 6.2, -2.9], 0.3, 0.32, 'crane');

    // Cerramientos: ventanas en las cuatro fachadas
    const win = (pts, t0, t1) => { poly(pts, t0, t1); WIN.push(pts); };
    for (let k = 0; k < FL; k++) {
      const t0 = 0.55 + k * 0.04, y0 = k + 0.3, y1 = k + 0.78;
      [[-3, -1], [-1, 1], [1, 3]].forEach(([a, b], i) => {
        const tt = t0 + i * 0.008;
        if (k === 0 && i === 1) {
          poly([[a + 0.6, 0, 2], [b - 0.6, 0, 2], [b - 0.6, 0.78, 2], [a + 0.6, 0.78, 2]], tt, tt + 0.012);
        } else {
          win([[a + 0.3, y0, 2], [b - 0.3, y0, 2], [b - 0.3, y1, 2], [a + 0.3, y1, 2]], tt, tt + 0.012);
        }
        win([[a + 0.3, y0, -2], [b - 0.3, y0, -2], [b - 0.3, y1, -2], [a + 0.3, y1, -2]], tt + 0.01, tt + 0.022);
      });
      [[-2, 0], [0, 2]].forEach(([a, b], i) => {
        const tt = t0 + 0.02 + i * 0.008;
        win([[3, y0, a + 0.3], [3, y0, b - 0.3], [3, y1, b - 0.3], [3, y1, a + 0.3]], tt, tt + 0.01);
        win([[-3, y0, a + 0.3], [-3, y0, b - 0.3], [-3, y1, b - 0.3], [-3, y1, a + 0.3]], tt, tt + 0.01);
      });
    }

    // Cubierta e instalaciones
    poly(rectY(-3, 3, -2, 2, 5.3), 0.75, 0.79);
    [[-3, -2], [3, -2], [3, 2], [-3, 2]].forEach(([x, z]) => add([x, 5, z], [x, 5.3, z], 0.75, 0.78));
    poly(rectY(-2.5, -1.2, -1.3, 0, 5), 0.79, 0.81);
    poly(rectY(-2.5, -1.2, -1.3, 0, 5.6), 0.81, 0.83);
    [[-2.5, -1.3], [-1.2, -1.3], [-1.2, 0], [-2.5, 0]].forEach(([x, z]) => add([x, 5, z], [x, 5.6, z], 0.81, 0.83));
    [-1.4, -0.3, 0.8].forEach((z, i) => {
      const t = 0.83 + i * 0.02;
      poly([[0.2, 5.1, z + 0.8], [2.6, 5.1, z + 0.8], [2.6, 5.55, z], [0.2, 5.55, z]], t, t + 0.02, 'gold');
    });

    // Entrega: cotas y vegetación
    add([-3, 0, 3], [3, 0, 3], 0.9, 0.94, 'dim');
    add([-3, 0, 2.8], [-3, 0, 3.2], 0.9, 0.91, 'dim');
    add([3, 0, 2.8], [3, 0, 3.2], 0.93, 0.94, 'dim');
    add([4, 0, 2], [4, 5.3, 2], 0.93, 0.97, 'dim');
    [[-4, 2.9], [4.1, -1], [-4.1, -2.6]].forEach(([x, z], i) => {
      const t = 0.94 + i * 0.015;
      add([x, 0, z], [x, 0.6, z], t, t + 0.01, 'dim');
      poly([[x - 0.45, 0.6, z], [x, 1.7, z], [x + 0.45, 0.6, z]], t + 0.01, t + 0.02, 'dim');
    });

    // Rejilla del suelo (siempre visible, muy suave)
    const GRID = [];
    for (let v = -6; v <= 6; v += 1.5) {
      GRID.push([[v, 0, -6], [v, 0, 6]], [[-6, 0, v], [6, 0, v]]);
    }

    // --- Proyección ---
    let W = 0, H = 0, dpr = 1, scale = 1, cx = 0, baseCx = 0.5;
    const resize = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = canvas.clientWidth; H = canvas.clientHeight;
      canvas.width = W * dpr; canvas.height = H * dpr;
      scale = Math.min(W * 0.9, H * 1.05) / 14;
      // en pantallas anchas el edificio se coloca a la derecha para dejar sitio al texto
      baseCx = W > 900 ? 0.7 : 0.5;
    };
    const PHI = 0.42, D = 24;
    let cosT = 1, sinT = 0;
    const cosP = Math.cos(PHI), sinP = Math.sin(PHI);
    const project = ([x, y, z]) => {
      const xr = x * cosT - z * sinT;
      const zr = x * sinT + z * cosT;
      const yc = y - 3;
      const y2 = yc * cosP - zr * sinP;
      const z2 = yc * sinP + zr * cosP;
      const f = D / (D - z2);
      return [cx + xr * f * scale, H * 0.52 - y2 * f * scale, z2];
    };

    const COLORS = { ink: '17,17,17', gold: '176,141,87', crane: '176,141,87', dim: '120,120,120' };
    let cur = { c: 0, th: -0.65 };
    let target = { c: 0, th: -0.65 };
    let phase = -1;

    const draw = () => {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      cosT = Math.cos(cur.th); sinT = Math.sin(cur.th);
      // a la derecha en la portada; se centra detrás del contenido al bajar
      cx = W * (baseCx - (baseCx - 0.5) * clamp(cur.c / 0.25));
      const c = cur.c;
      ctx.lineCap = 'round';

      // rejilla
      ctx.lineWidth = 1;
      ctx.strokeStyle = 'rgba(17,17,17,0.06)';
      ctx.beginPath();
      GRID.forEach(([a, b]) => { const p = project(a), q = project(b); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); });
      ctx.stroke();

      // proyecto (fantasma discontinuo)
      ctx.setLineDash([3, 5]);
      ctx.strokeStyle = `rgba(17,17,17,${0.3 * (1 - c * 0.75)})`;
      ctx.beginPath();
      E.forEach(e => {
        if (e.kind === 'crane' || e.kind === 'dim') return;
        const p = project(e.a), q = project(e.b);
        ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]);
      });
      ctx.stroke();
      ctx.setLineDash([]);

      // ventanas iluminadas al final
      const lit = clamp((c - 0.96) / 0.04);
      if (lit > 0) {
        ctx.fillStyle = `rgba(201,169,110,${0.32 * lit})`;
        WIN.forEach(pts => {
          ctx.beginPath();
          pts.forEach((pt, i) => { const p = project(pt); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
          ctx.closePath(); ctx.fill();
        });
      }

      // obra construida
      const craneAlpha = c < 0.86 ? 1 : clamp((0.95 - c) / 0.09);
      E.forEach(e => {
        const f = clamp((c - e.t0) / (e.t1 - e.t0));
        if (f <= 0) return;
        if (e.kind === 'crane' && craneAlpha <= 0) return;
        const p = project(e.a);
        const end = [e.a[0] + (e.b[0] - e.a[0]) * f, e.a[1] + (e.b[1] - e.a[1]) * f, e.a[2] + (e.b[2] - e.a[2]) * f];
        const q = project(end);
        const depth = clamp(((p[2] + q[2]) / 2 + 5) / 10);
        let alpha = 0.35 + 0.65 * depth;
        if (e.kind === 'crane') alpha *= craneAlpha;
        ctx.strokeStyle = `rgba(${COLORS[e.kind]},${alpha})`;
        ctx.lineWidth = e.kind === 'ink' ? 1.4 : e.kind === 'dim' ? 1 : 1.7;
        ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
      });

      // fase y porcentaje escritos en el propio dibujo, bajo el edificio
      let phI = 0;
      T.forEach((t, i) => { if (c >= t - 1e-6 && c > 0.005) phI = i; });
      const base = project([0, 0, 0]);
      const ly = Math.min(base[1] + scale * 4.6, H - 70);
      const txt = phI === T.length - 1 && c > 0.98 ? 'Entrega · Certificado final de obra' : names[phI];
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(138,106,53,0.9)';
      ctx.font = `600 ${W > 600 ? 12 : 11}px Manrope, sans-serif`;
      ctx.fillText(`${String(phI).padStart(2, '0')} · ${txt.toUpperCase()}`, base[0], ly);
      ctx.fillStyle = 'rgba(17,17,17,0.55)';
      ctx.font = `300 ${W > 600 ? 30 : 24}px Manrope, sans-serif`;
      ctx.fillText(`${Math.round(c * 100)}%`, base[0], ly + 38);

      // indicador de fase
      let ph = 0;
      T.forEach((t, i) => { if (c >= t - 1e-6 && c > 0.005) ph = i; });
      if (ph !== phase) {
        phase = ph;
        labelEl.textContent = ph === T.length - 1 && c > 0.98 ? 'Entrega · Certificado final de obra' : names[ph];
        numEl.textContent = String(ph).padStart(2, '0');
      }
      if (ph === T.length - 1) labelEl.textContent = c > 0.98 ? 'Entrega · Certificado final de obra' : names[ph];
      pctEl.textContent = Math.round(c * 100);
      barEl.style.transform = `scaleX(${c})`;
    };

    const readScroll = () => {
      const r = journey.getBoundingClientRect();
      const s = clamp(-r.top / (r.height - window.innerHeight));
      target.c = clamp((s - 0.05) / 0.88);
      target.th = -0.65 + s * Math.PI * 1.6; // gira algo más de tres cuartos de vuelta
    };

    let running = false;
    let idle = 0;
    const loop = () => {
      if (!running) return;
      readScroll();
      const k = reduce ? 1 : 0.1;
      cur.c += (target.c - cur.c) * k;
      if (!reduce) idle += 0.0016; // giro lento continuo además del giro con el scroll
      cur.th += (target.th + idle - cur.th) * k;
      draw();
      requestAnimationFrame(loop);
    };
    new IntersectionObserver(([e]) => {
      running = e.isIntersecting;
      if (running) requestAnimationFrame(loop);
    }).observe(journey);
    window.addEventListener('resize', () => { resize(); draw(); });
    resize();
    readScroll();
    cur = { ...target };
    draw();
  }

  /* ---------- Scroll: barra de progreso, cabecera, parallax, botón fijo ---------- */
  const progress = $('.progress span');
  const parallax = $$('[data-parallax]');
  const fab = $('.fab-cta');
  let ticking = false;
  const onScroll = () => {
    ticking = false;
    const y = window.scrollY;
    const vh = window.innerHeight;
    const max = document.documentElement.scrollHeight - vh;
    nav.classList.toggle('is-scrolled', y > 10);
    if (progress) progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    if (!reduce) parallax.forEach(el => {
      if (y < vh * 1.5) el.style.transform = `translateY(${y * +el.dataset.parallax}px)`;
    });
    if (fab) fab.classList.toggle('is-on', y > vh * 0.7 && y < max - 500);
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- Filtro de proyectos ---------- */
  const filters = $$('.filter');
  const projects = $$('.project');
  filters.forEach(btn => btn.addEventListener('click', () => {
    filters.forEach(b => { b.classList.remove('is-active'); b.setAttribute('aria-pressed', 'false'); });
    btn.classList.add('is-active');
    btn.setAttribute('aria-pressed', 'true');
    const f = btn.dataset.filter;
    projects.forEach(p => {
      const show = f === 'all' || p.dataset.cat === f;
      p.classList.toggle('is-hidden', !show);
      p.classList.remove('is-in');
      if (show) { void p.offsetWidth; p.classList.add('is-in', 'is-visible'); }
    });
  }));

  /* ---------- Mapa: resaltar municipio ---------- */
  const towns = $$('.town');
  const setTown = slug => {
    towns.forEach(t => t.classList.toggle('is-active', t.dataset.town === slug));
    $$('.town-chip').forEach(c => c.classList.toggle('is-active', c.dataset.town === slug));
  };
  $$('.town-chip').forEach(c => {
    c.addEventListener('mouseenter', () => setTown(c.dataset.town));
    c.addEventListener('focus', () => setTown(c.dataset.town));
    c.addEventListener('click', () => setTown(c.dataset.town));
    c.addEventListener('mouseleave', () => setTown(null));
    c.addEventListener('blur', () => setTown(null));
  });
  towns.forEach(t => {
    t.addEventListener('mouseenter', () => setTown(t.dataset.town));
    t.addEventListener('mouseleave', () => setTown(null));
  });

  /* ---------- Email protegido contra robots ---------- */
  // El email no aparece escrito en el HTML: se compone aquí.
  const emailLinks = $$('.js-email');
  const STUDIO_EMAIL = emailLinks.length ? `${emailLinks[0].dataset.u}@${emailLinks[0].dataset.d}` : '';
  emailLinks.forEach(a => {
    const em = `${a.dataset.u}@${a.dataset.d}`;
    a.href = `mailto:${em}`;
    if (!a.classList.contains('todo') && !a.querySelector('.todo')) a.textContent = em;
  });

  /* ---------- Formulario: validación y antispam ---------- */
  const form = $('#contact-form');
  if (form) {
    const status = $('.form__status', form);
    const loadedAt = Date.now();
    let submitting = false;
    const submitBtn = $('button[type=submit]', form);
    submitBtn.addEventListener('pointerdown', () => { submitting = true; setTimeout(() => { submitting = false; }, 600); });
    const rules = {
      nombre: el => el.value.trim().length >= 2 || 'Escribe tu nombre (mínimo 2 caracteres).',
      telefono: el => !el.value.trim() || /^[+0-9 ()-]{9,20}$/.test(el.value.trim()) || 'Escribe un teléfono válido, con al menos 9 cifras.',
      email: el => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim()) || 'Escribe un email válido, por ejemplo nombre@correo.es.',
      mensaje: el => el.value.trim().length >= 10 || 'Cuéntanos un poco más sobre tu proyecto (mínimo 10 caracteres).',
      privacidad: el => el.checked || 'Debes aceptar la política de privacidad para enviar la consulta.',
    };
    const check = el => {
      const rule = rules[el.name];
      if (!rule) return true;
      const res = rule(el);
      const err = $(`#e-${el.name}`);
      const ok = res === true;
      el.setAttribute('aria-invalid', ok ? 'false' : 'true');
      if (err) err.textContent = ok ? '' : res;
      return ok;
    };
    Object.keys(rules).forEach(name => {
      const el = form.elements[name];
      // Si se sale del campo pulsando "Enviar", no se valida aquí (lo hace el envío):
      // así el botón no se desplaza bajo el dedo o el ratón y el clic no se pierde.
      el.addEventListener('blur', e => {
        if (e.relatedTarget && e.relatedTarget.type === 'submit') return;
        setTimeout(() => { if (!submitting) check(el); }, 180);
      });
      el.addEventListener(el.type === 'checkbox' ? 'change' : 'input', () => {
        if (el.getAttribute('aria-invalid') === 'true') check(el);
      });
    });

    form.addEventListener('submit', e => {
      e.preventDefault();
      status.className = 'form__status';
      // Antispam: campo trampa relleno o envío demasiado rápido = robot
      const bot = form.elements.web.value || Date.now() - loadedAt < 3000;
      let last = 0;
      try { last = +sessionStorage.getItem('esp-sent') || 0; } catch (err) {}
      if (Date.now() - last < 30000) {
        status.classList.add('is-error');
        status.textContent = 'Ya has enviado una consulta hace un momento. Espera unos segundos antes de enviar otra.';
        return;
      }
      const fields = Object.keys(rules).map(n => form.elements[n]);
      const invalid = fields.filter(el => !check(el));
      if (invalid.length) {
        status.classList.add('is-error');
        status.textContent = invalid.length === 1 ? 'Revisa el campo marcado.' : `Revisa los ${invalid.length} campos marcados.`;
        invalid[0].focus();
        return;
      }
      if (bot) {
        status.classList.add('is-ok');
        status.textContent = 'Gracias. Hemos recibido tu consulta.';
        return;
      }
      const d = new FormData(form);
      const clean = v => String(v || '').replace(/[\r\n]+/g, ' ').trim();
      const subject = `Consulta web: ${clean(d.get('servicio'))}`;
      const text = `Nombre: ${clean(d.get('nombre'))}\nTeléfono: ${clean(d.get('telefono'))}\nEmail: ${clean(d.get('email'))}\nServicio: ${clean(d.get('servicio'))}\n\n${String(d.get('mensaje')).trim()}`;
      try { sessionStorage.setItem('esp-sent', String(Date.now())); } catch (err) {}
      window.location.href = `mailto:${STUDIO_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(text)}`;
      status.classList.add('is-ok');
      status.textContent = 'Gracias. Se abrirá tu programa de correo con la consulta preparada; solo tienes que pulsar Enviar.';
      if (window.gtag) window.gtag('event', 'generate_lead', { form: 'contacto' });
    });
  }

  /* ---------- Cookies y Google Analytics 4 ---------- */
  const CK = 'esp-cookies';
  const getConsent = () => {
    try {
      const v = JSON.parse(localStorage.getItem(CK));
      if (v && Date.now() - v.t < 365 * 864e5) return v.v;
    } catch (e) {}
    return null;
  };
  const setConsent = v => { try { localStorage.setItem(CK, JSON.stringify({ v, t: Date.now() })); } catch (e) {} };
  const loadGA = () => {
    if (!GA_ID || window.gtag) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
    const s = document.createElement('script');
    s.async = true;
    s.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.appendChild(s);
  };
  const clearGA = () => {
    document.cookie.split(';').forEach(c => {
      const n = c.split('=')[0].trim();
      if (!/^_ga/.test(n)) return;
      document.cookie = `${n}=; Max-Age=0; path=/`;
      document.cookie = `${n}=; Max-Age=0; path=/; domain=${location.hostname}`;
    });
  };
  const banner = $('.cookie');
  const showBanner = () => {
    banner.hidden = false;
    requestAnimationFrame(() => requestAnimationFrame(() => banner.classList.add('is-on')));
  };
  const hideBanner = () => {
    banner.classList.remove('is-on');
    setTimeout(() => { banner.hidden = true; }, 500);
  };
  if (banner) {
    const consent = getConsent();
    if (consent === 'accept') loadGA();
    else if (!consent) setTimeout(showBanner, firstVisit ? 3000 : 700);
    $$('[data-cookie]', banner).forEach(b => b.addEventListener('click', () => {
      const v = b.dataset.cookie;
      setConsent(v);
      hideBanner();
      if (v === 'accept') loadGA(); else clearGA();
    }));
    $$('[data-cookie-settings]').forEach(b => b.addEventListener('click', showBanner));
  }

  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();
})();
