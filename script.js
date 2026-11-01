(() => {
  const root = document.documentElement;
  const body = document.body;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
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
  if (root.classList.contains('first-visit') && intro && !reduce) {
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
  });
  $$('.nav__links a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', false);
  }));

  /* ---------- Edificio que se construye ---------- */
  const build = $('.build');
  let updateBuild = () => {};
  if (build) {
    const svg = $('.build__svg', build);
    const phases = [[], [], [], [], []];
    $$('[data-phase]', svg).forEach(el => {
      const L = el.getTotalLength();
      el._L = L;
      el.style.strokeDasharray = L;
      el.style.strokeDashoffset = L;
      phases[+el.dataset.phase].push(el);
    });
    const steps = $$('.build__phases li', build);
    const pct = $('.build__pct', build);
    const bar = $('.build__bar i', build);
    const now = $('.build__now', build);
    updateBuild = () => {
      const r = build.getBoundingClientRect();
      const p = clamp(-r.top / (r.height - window.innerHeight) / 0.94);
      const P = p * 5;
      phases.forEach((list, i) => {
        const t = P - i;
        list.forEach((el, j) => {
          const start = list.length > 1 ? (j / list.length) * 0.6 : 0;
          el.style.strokeDashoffset = el._L * (1 - clamp((t - start) / 0.4));
        });
      });
      const active = Math.min(4, Math.floor(P));
      steps.forEach((li, i) => {
        li.classList.toggle('is-active', i === active);
        li.classList.toggle('is-done', i < active);
      });
      if (now && steps[active]) now.textContent = $('h3', steps[active]).textContent;
      pct.textContent = Math.round(p * 100);
      bar.style.transform = `scaleX(${p})`;
      svg.classList.toggle('is-lit', p >= 0.99);
    };
  }

  /* ---------- Scroll: barra de progreso, cabecera, parallax ---------- */
  const progress = $('.progress span');
  const parallax = $$('[data-parallax]');
  let ticking = false;
  const onScroll = () => {
    ticking = false;
    const y = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    nav.classList.toggle('is-scrolled', y > 10);
    if (progress) progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    if (!reduce) parallax.forEach(el => {
      if (y < window.innerHeight * 1.5) el.style.transform = `translateY(${y * +el.dataset.parallax}px)`;
    });
    updateBuild();
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- Cursor, tarjetas 3D y botones magnéticos ---------- */
  if (finePointer && !reduce) {
    const cursor = $('.cursor');
    let mx = 0, my = 0, cx = 0, cy = 0;
    window.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; cursor.classList.add('is-on'); });
    document.addEventListener('mouseleave', () => cursor.classList.remove('is-on'));
    const loop = () => {
      cx += (mx - cx) * 0.18; cy += (my - cy) * 0.18;
      cursor.style.transform = `translate(${cx}px, ${cy}px)`;
      requestAnimationFrame(loop);
    };
    loop();
    document.addEventListener('mouseover', e => cursor.classList.toggle('is-hover', !!e.target.closest('a, button, .project, .service, label')));

    $$('.tilt').forEach(card => {
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(900px) rotateX(${-y * 5}deg) rotateY(${x * 5}deg) translateZ(0)`;
      });
      card.addEventListener('mouseleave', () => { card.style.transform = ''; });
    });

    $$('.magnetic').forEach(btn => {
      btn.addEventListener('mousemove', e => {
        const r = btn.getBoundingClientRect();
        btn.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.25}px, ${(e.clientY - r.top - r.height / 2) * 0.35}px)`;
      });
      btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
    });
  }

  /* ---------- Pestañas de servicios: marcar la activa ---------- */
  const chips = $$('.chips a');
  if (chips.length) {
    const bar = $('.chips__inner');
    const chipIo = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        chips.forEach(c => {
          const on = c.getAttribute('href') === '#' + e.target.id;
          c.classList.toggle('is-active', on);
          if (on) bar.scrollTo({ left: c.offsetLeft - 32, behavior: 'smooth' });
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    $$('.services--detailed .service').forEach(s => chipIo.observe(s));
  }

  /* ---------- Filtro de proyectos ---------- */
  const filters = $$('.filter');
  const projects = $$('.project');
  filters.forEach(btn => btn.addEventListener('click', () => {
    filters.forEach(b => b.classList.remove('is-active'));
    btn.classList.add('is-active');
    const f = btn.dataset.filter;
    projects.forEach(p => {
      const show = f === 'all' || p.dataset.cat === f;
      p.classList.toggle('is-hidden', !show);
      p.classList.remove('is-in');
      if (show) { void p.offsetWidth; p.classList.add('is-in', 'is-visible'); }
    });
  }));

  /* ---------- Formulario ---------- */
  const form = $('#contact-form');
  if (form) {
    const status = $('.form__status', form);
    const EMAIL_ESTUDIO = 'info@enriquesanchezpolo.es'; // cambiar por el email real
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.checkValidity()) {
        status.textContent = 'Por favor, completa los campos obligatorios y acepta la política de privacidad.';
        return;
      }
      const d = new FormData(form);
      const subject = `Consulta web: ${d.get('servicio')}`;
      const text = `Nombre: ${d.get('nombre')}\nTeléfono: ${d.get('telefono')}\nEmail: ${d.get('email')}\nServicio: ${d.get('servicio')}\n\n${d.get('mensaje')}`;
      window.location.href = `mailto:${EMAIL_ESTUDIO}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(text)}`;
      status.textContent = 'Gracias. Se abrirá tu programa de correo para enviar la consulta.';
    });
  }

  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();
})();
