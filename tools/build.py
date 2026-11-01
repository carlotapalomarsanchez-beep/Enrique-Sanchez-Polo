"""Genera las páginas HTML del sitio con cabecera y pie compartidos."""
import sys, pathlib

OUT = pathlib.Path(sys.argv[1])

LOGO = '<svg viewBox="0 0 40 40"><path d="M6 34V14L20 6l14 8v20" /><path class="g" d="M15 34V23h10v11" /></svg>'

def head(title, desc):
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <script>
    document.documentElement.classList.add('js');
    (function (r) {{
      var seen = false;
      try {{ seen = !!sessionStorage.getItem('esp-intro'); }} catch (e) {{}}
      r.classList.add(seen ? 'entering' : 'first-visit');
      setTimeout(function () {{ r.classList.remove('entering'); }}, 2500);
    }})(document.documentElement);
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23fff'/%3E%3Cpath d='M14 50V22l18-10 18 10v28' fill='none' stroke='%23B08D57' stroke-width='3'/%3E%3Cpath d='M26 50V34h12v16' fill='none' stroke='%23111' stroke-width='3'/%3E%3C/svg%3E">
</head>'''

INTRO = f'''
  <!-- Animación de entrada (solo la primera visita) -->
  <div class="intro" aria-hidden="true">
    <div class="intro__panel intro__panel--a"></div>
    <div class="intro__panel intro__panel--b"></div>
    <div class="intro__content">
      <svg class="intro__logo" viewBox="0 0 40 40"><path d="M6 34V14L20 6l14 8v20" /><path class="g" d="M15 34V23h10v11" /></svg>
      <p class="intro__name"><span>Enrique</span> <span>Sánchez</span> <span>Polo</span></p>
      <p class="intro__role">Arquitecto · Algeciras</p>
      <div class="intro__bar"><span></span></div>
      <p class="intro__count"><span class="intro__num">0</span>%</p>
    </div>
  </div>

  <!-- Transición entre páginas -->
  <div class="curtain" aria-hidden="true"><span></span><span></span></div>
  <div class="progress" aria-hidden="true"><span></span></div>
  <div class="cursor" aria-hidden="true"></div>
'''

SUB = [
    ("servicios.html#edificacion", "Proyectos de edificación"),
    ("servicios.html#tasaciones", "Tasaciones y valoraciones"),
    ("servicios.html#electricas", "Infraestructuras eléctricas"),
    ("servicios.html#rehabilitacion", "Rehabilitación y reforma"),
    ("servicios.html#licencias", "Licencias y legalizaciones"),
    ("servicios.html#peritaciones", "Peritaciones e informes"),
    ("servicios.html#direccion", "Dirección de obra"),
    ("servicios.html#industrial", "Naves industriales"),
]

def nav(page):
    def cls(p):
        return ' class="is-active" aria-current="page"' if p == page else ''
    sub = "\n".join(f'              <a href="{h}">{t}</a>' for h, t in SUB)
    return f'''
  <header class="nav" id="top">
    <div class="nav__inner">
      <a href="index.html" class="brand" aria-label="Inicio">
        <span class="brand__mark" aria-hidden="true">{LOGO}</span>
        <span class="brand__text"><strong>Enrique Sánchez Polo</strong><small>Arquitecto</small></span>
      </a>
      <button class="nav__toggle" aria-label="Abrir menú" aria-expanded="false"><span></span><span></span></button>
      <nav class="nav__links" aria-label="Principal">
        <a href="index.html"{cls('inicio')}>Inicio</a>
        <a href="estudio.html"{cls('estudio')}>Estudio</a>
        <div class="nav__item has-sub">
          <a href="servicios.html"{cls('servicios')}>Servicios <i class="chev" aria-hidden="true"></i></a>
          <div class="sub">
            <div class="sub__inner">
              <p class="sub__title">Servicios</p>
{sub}
              <a href="servicios.html" class="sub__all">Ver los 12 servicios →</a>
            </div>
          </div>
        </div>
        <a href="proyectos.html"{cls('proyectos')}>Proyectos</a>
        <a href="contacto.html"{cls('contacto')} data-btn>Contacto</a>
      </nav>
    </div>
  </header>
'''

FOOTER = f'''
  <section class="cta-band">
    <div class="container cta-band__inner">
      <h2 data-split>¿Tienes un proyecto en mente?</h2>
      <a href="contacto.html" class="btn btn--gold magnetic">Hablemos <span aria-hidden="true">→</span></a>
    </div>
  </section>

  <footer class="footer">
    <div class="container footer__inner">
      <div class="brand brand--footer">
        <span class="brand__mark" aria-hidden="true">{LOGO}</span>
        <span class="brand__text"><strong>Enrique Sánchez Polo</strong><small>Arquitecto · Algeciras</small></span>
      </div>
      <nav class="footer__links" aria-label="Pie">
        <a href="index.html">Inicio</a><a href="estudio.html">Estudio</a><a href="servicios.html">Servicios</a><a href="proyectos.html">Proyectos</a><a href="contacto.html">Contacto</a>
      </nav>
      <p class="footer__legal">© <span id="year"></span> Enrique Sánchez Polo · Arquitecto colegiado COA Cádiz <span class="todo">[nº por confirmar]</span> · <a href="#">Aviso legal</a> · <a href="#">Privacidad</a></p>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>
'''

def page(name, title, desc, body, cta=True):
    footer = FOOTER if cta else '\n  <footer' + FOOTER.split('<footer', 1)[1]
    html = head(title, desc) + f'\n<body data-page="{name}">\n' + INTRO + nav(name) + '\n  <main>\n' + body + '\n  </main>\n' + footer
    (OUT / f"{'index' if name == 'inicio' else name}.html").write_text(html, encoding="utf-8")


def page_hero(num, kicker, title, intro, art):
    return f'''
    <section class="page-hero">
      <div class="container page-hero__grid">
        <div>
          <p class="crumbs reveal"><a href="index.html">Inicio</a> <span>/</span> {kicker}</p>
          <p class="eyebrow reveal">{num} — {kicker}</p>
          <h1 data-split>{title}</h1>
          <p class="lead reveal">{intro}</p>
        </div>
        <div class="page-hero__art" aria-hidden="true" data-parallax="0.12">
          <svg viewBox="0 0 400 320" class="drawing">{art}</svg>
        </div>
      </div>
    </section>
'''

MARQUEE_ITEMS = ["Edificación", "Tasaciones", "Infraestructuras eléctricas", "Rehabilitación", "Licencias", "Legalizaciones AFO", "Peritaciones", "Dirección de obra", "Naves industriales", "Eficiencia energética", "ITE / IEE", "Urbanismo"]
def marquee():
    items = "".join(f"<span>{t}</span><i>✦</i>" for t in MARQUEE_ITEMS)
    return f'''
    <div class="marquee" aria-hidden="true">
      <div class="marquee__track">{items}{items}</div>
    </div>
'''

SERVICES = [
    ("edificacion", "Proyectos de edificación", "Proyecto básico y de ejecución de viviendas unifamiliares, plurifamiliares, locales y edificios de uso terciario. Obra nueva y ampliaciones.", ["Vivienda unifamiliar y plurifamiliar", "Ampliaciones y remontes", "Edificios terciarios y equipamientos"], False),
    ("tasaciones", "Tasaciones y valoraciones", "Valoración de inmuebles, solares y fincas rústicas. Tasaciones para herencias, divorcios, compraventas, expropiaciones y fines hipotecarios.", ["Herencias y repartos", "Compraventas y divorcios", "Expropiaciones y valor catastral"], True),
    ("electricas", "Infraestructuras eléctricas", "Proyectos de obra civil para centros de transformación, subestaciones, líneas de media y baja tensión, canalizaciones y edificaciones técnicas.", ["Centros de transformación", "Subestaciones y casetas técnicas", "Canalizaciones y zanjas"], True),
    ("rehabilitacion", "Rehabilitación y reforma", "Reformas integrales, rehabilitación de fachadas y cubiertas, cambios de uso, adecuación de locales y mejora de la accesibilidad.", ["Reformas integrales", "Fachadas y cubiertas", "Accesibilidad y ascensores"], False),
    ("licencias", "Licencias y actividades", "Licencias de obra, de apertura y de actividad, declaraciones responsables y licencias de primera ocupación o utilización.", ["Licencia de obra", "Apertura y actividad", "Primera ocupación"], False),
    ("legalizaciones", "Legalizaciones y AFO", "Legalización de edificaciones existentes y expedientes de Asimilado a Fuera de Ordenación según la normativa andaluza (LISTA).", ["Asimilado a Fuera de Ordenación", "Legalización de ampliaciones", "Regularización catastral"], False),
    ("peritaciones", "Peritaciones e informes", "Informes periciales judiciales y de parte, dictámenes de patologías, humedades, grietas, vicios constructivos y daños por siniestros.", ["Periciales judiciales", "Patologías y humedades", "Siniestros y aseguradoras"], False),
    ("direccion", "Dirección de obra", "Dirección facultativa, control de calidad, coordinación de seguridad y salud y certificación final de obra.", ["Dirección facultativa", "Seguridad y salud", "Certificado final de obra"], False),
    ("industrial", "Naves y proyectos industriales", "Naves industriales y logísticas, almacenes, talleres y edificios vinculados a la actividad portuaria y empresarial de la comarca.", ["Naves y almacenes", "Talleres", "Logística portuaria"], False),
    ("eficiencia", "Eficiencia energética", "Certificados energéticos, auditorías y propuestas de mejora: aislamiento, envolvente, instalaciones y energías renovables.", ["Certificado energético", "Auditorías", "Mejora de la envolvente"], False),
    ("ite", "ITE / IEE", "Inspección Técnica de Edificios e Informe de Evaluación del Edificio para comunidades de propietarios y administradores de fincas.", ["Inspección técnica", "Informe de evaluación", "Plan de actuaciones"], False),
    ("urbanismo", "Urbanismo y suelo", "Segregaciones, agrupaciones, levantamientos planimétricos, estudios de detalle, informes urbanísticos y viabilidad de solares.", ["Segregaciones", "Levantamientos", "Viabilidad de solares"], False),
]

def service_cards(items, detailed=False):
    out = []
    for i, (sid, title, text, bullets, feat) in enumerate(items, 1):
        extra = ""
        if detailed:
            extra = "<ul class=\"service__list\">" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
        out.append(f'''          <article class="service{' service--featured' if feat else ''} reveal tilt" id="{sid}">
            <span class="service__num">{i:02d}</span>
            <h3>{title}</h3>
            <p>{text}</p>{extra}
          </article>''')
    return "\n".join(out)

PROJECTS = [
    ("residencial", "Residencial", "Obra nueva", "Viviendas unifamiliares", "Casas aisladas, pareadas y adosadas adaptadas a la parcela, la orientación y el clima del Estrecho.",
     '<path class="ink" d="M40 240V130l90-60 90 60v110M220 240V150h140v90M30 240h340"/><path class="ink" d="M100 240v-60h60v60M250 180h30v30h-30zM310 180h30v30h-30z"/><path class="gold-stroke" d="M130 70V40"/>'),
    ("residencial", "Residencial", "Plurifamiliar", "Edificios de viviendas", "Promociones plurifamiliares, viviendas protegidas y edificios mixtos con locales en planta baja.",
     '<path class="ink" d="M90 250V40h220v210M60 250h280"/><path class="ink" d="M90 80h220M90 120h220M90 160h220M90 200h220M145 40v210M200 40v210M255 40v210"/><path class="gold-stroke" d="M320 60h40M320 250V60"/>'),
    ("tecnico", "Técnico", "Energía", "Centros de transformación y subestaciones", "Edificios prefabricados y de obra, cimentaciones, casetas técnicas y canalizaciones para distribuidoras eléctricas.",
     '<path class="ink" d="M60 240V140h120v100M40 240h320"/><path class="ink" d="M90 240v-50h60v50"/><path class="gold-stroke" d="M250 240V60M230 80h40M220 110h60M250 60l-20 20M250 60l20 20M180 150l70-40M280 110l60 40v90"/>'),
    ("tecnico", "Técnico", "Industrial", "Naves industriales y logísticas", "Naves, almacenes y talleres en polígonos de Algeciras, Los Barrios y San Roque, con licencia de actividad.",
     '<path class="ink" d="M40 240V120l160-60 160 60v120M30 240h340"/><path class="ink" d="M80 240v-80h80v80M240 160h80v40h-80z"/><path class="gold-stroke" d="M40 120h320"/>'),
    ("consultoria", "Consultoría", "Valoración", "Tasaciones inmobiliarias", "Valoraciones de viviendas, locales, naves, solares y fincas rústicas con informe técnico detallado.",
     '<path class="ink" d="M70 240V100h160v140M50 240h300"/><path class="ink" d="M100 130h40v40h-40zM160 130h40v40h-40z"/><circle class="gold-stroke" cx="280" cy="120" r="44"/><path class="gold-stroke" d="M312 152l40 40"/><path class="ink" d="M262 120h36M280 102v36"/>'),
    ("residencial", "Residencial", "Rehabilitación", "Rehabilitación de edificios", "Fachadas, cubiertas, estructuras y accesibilidad en edificios existentes y comunidades de propietarios.",
     '<path class="ink" d="M80 250V60h240v190M60 250h280"/><path class="ink" d="M120 100h40v50h-40zM240 100h40v50h-40zM120 180h40v50h-40zM240 180h40v50h-40z"/><path class="gold-stroke" d="M60 60l40-30M340 60l-40-30M100 30h200" stroke-dasharray="6 6"/>'),
    ("consultoria", "Consultoría", "Peritación", "Peritaciones y patologías", "Diagnóstico de grietas, humedades y defectos constructivos. Informes con validez ante juzgados y aseguradoras.",
     '<path class="ink" d="M80 240V80h200v160M60 240h260"/><path class="gold-stroke" d="M150 80l20 50-30 30 25 40-10 40"/><path class="ink" d="M300 100h60M300 130h60M300 160h40"/>'),
    ("tecnico", "Técnico", "Terciario", "Locales y edificios terciarios", "Adecuación de locales comerciales, oficinas, hostelería y equipamientos, con su licencia de apertura.",
     '<path class="ink" d="M40 240h320M60 240V150h80v90M160 240V110h80v130M260 240V170h80v70"/><path class="gold-stroke" d="M40 90h320" stroke-dasharray="4 8"/><path class="ink" d="M190 140h20v20h-20z"/>'),
    ("consultoria", "Consultoría", "Urbanismo", "Legalizaciones, AFO y segregaciones", "Regularización de edificaciones, divisiones de fincas y estudios de viabilidad urbanística de solares.",
     '<path class="ink" d="M40 60h320v180H40z"/><path class="ink" d="M40 140h140V60M180 140l80 100M260 60v80h100"/><path class="gold-stroke" d="M180 140h80v-80"/>'),
]

def project_cards(items):
    return "\n".join(f'''          <article class="project reveal" data-cat="{cat}">
            <div class="project__img"><svg viewBox="0 0 400 280" aria-hidden="true">{svg}</svg><span class="project__more">Consultar →</span></div>
            <div class="project__meta"><span>{c1}</span><span>{c2}</span></div>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>''' for cat, c1, c2, t, d, svg in items)

STEPS = '''
    <section class="section section--dark">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow reveal">Método de trabajo</p>
          <h2 data-split>Un proceso claro, sin sorpresas.</h2>
        </div>
        <ol class="steps">
          <li class="reveal"><span class="steps__n">01</span><h3>Primera reunión</h3><p>Escuchamos tus necesidades, visitamos el inmueble o la parcela y analizamos la normativa aplicable.</p></li>
          <li class="reveal"><span class="steps__n">02</span><h3>Propuesta y presupuesto</h3><p>Te entregamos una propuesta de honorarios cerrada, con plazos y alcance de cada fase.</p></li>
          <li class="reveal"><span class="steps__n">03</span><h3>Proyecto y tramitación</h3><p>Redactamos la documentación técnica, la visamos y la presentamos ante ayuntamiento, Junta o compañía.</p></li>
          <li class="reveal"><span class="steps__n">04</span><h3>Obra y entrega</h3><p>Dirigimos la ejecución, controlamos calidad y costes y emitimos el certificado final de obra.</p></li>
        </ol>
      </div>
    </section>
'''

# ---------- Edificio que se construye con el scroll ----------
def build_svg():
    els = []
    # Fase 0: replanteo y cimentación
    p0 = ['M40 520H560', 'M95 520v34h40v-34', 'M215 520v34h40v-34', 'M335 520v34h40v-34', 'M455 520v34h40v-34']
    p0g = ['M100 500l-10 10M90 500l10 10', 'M480 500l-10 10M470 500l10 10']
    # Fase 1: estructura (pilares y forjados)
    p1 = []
    for x in (115, 235, 355, 475):
        p1.append(f'M{x} 520V170')
    for y in (440, 360, 280, 200):
        p1.append(f'M100 {y}H490')
    p1g = ['M530 520V90', 'M530 100H300', 'M530 100l-40-40v40', 'M380 100v60', 'M370 160h20v14h-20z']  # grúa
    # Fase 2: cerramientos y ventanas
    p2 = ['M100 520V200H490V520']
    wins = []
    for y in (380, 300, 220):
        for x in (135, 255, 375):
            wins.append(f'M{x} {y}h80v44h-80z')
    p2 += wins
    p2 += ['M150 520v-58h50v58', 'M260 462h70v40h-70z', 'M380 462h70v40h-70z']
    # Fase 3: cubierta e instalaciones
    p3 = ['M90 200H500', 'M90 200v-14H500v14', 'M140 186v-30h60v30', 'M380 186v-22h50v22', 'M400 164v-14']
    p3g = ['M220 186V120', 'M196 120h48', 'M206 136h28', 'M220 120l-14 16M220 120l14 16']
    # Fase 4: entrega (cotas, vegetación, luz)
    p4 = ['M100 580H490', 'M100 572v16M490 572v16', 'M580 520V200', 'M572 520h16M572 200h16',
          'M60 520c0-30 10-40 20-40s20 10 20 40', 'M80 520v-20', 'M520 520c0-24 8-32 16-32s16 8 16 32']
    p4g = ['M100 200l195-0 195 0', 'M295 120l18 10-18 10-18-10z']

    def grp(paths, phase, cls):
        return "".join(f'<path class="{cls}" data-phase="{phase}" d="{d}"/>' for d in paths)

    els.append('<g class="b-grid">' + "".join(f'<path d="M{x} 40V600"/>' for x in range(40, 600, 60)) + "".join(f'<path d="M0 {y}H600"/>' for y in range(40, 620, 60)) + '</g>')
    els.append(grp(p0, 0, 'b-ink') + grp(p0g, 0, 'b-gold'))
    els.append(grp(p1, 1, 'b-ink') + grp(p1g, 1, 'b-gold b-crane'))
    els.append(grp(p2, 2, 'b-ink b-win'))
    els.append(grp(p3, 3, 'b-ink') + grp(p3g, 3, 'b-gold'))
    els.append(grp(p4, 4, 'b-dim') + grp(p4g, 4, 'b-gold'))
    els.append('<text class="b-label" x="295" y="604" text-anchor="middle">Certificado final de obra</text>')
    return "".join(els)

BUILD = f'''
    <section class="build" id="construccion">
      <div class="build__sticky">
        <div class="container build__grid">
          <div class="build__copy">
            <p class="eyebrow">Del plano a la obra</p>
            <h2>Así levantamos <span class="gold serif">cada proyecto.</span></h2>
            <ol class="build__phases">
              <li data-step="0"><span>01</span><div><h3>Replanteo y cimentación</h3><p>Estudio del terreno, normativa y bases sólidas.</p></div></li>
              <li data-step="1"><span>02</span><div><h3>Estructura</h3><p>Pilares y forjados calculados con precisión.</p></div></li>
              <li data-step="2"><span>03</span><div><h3>Cerramientos</h3><p>Fachada, huecos y envolvente eficiente.</p></div></li>
              <li data-step="3"><span>04</span><div><h3>Cubierta e instalaciones</h3><p>Electricidad, climatización y renovables.</p></div></li>
              <li data-step="4"><span>05</span><div><h3>Entrega</h3><p>Control de calidad y certificado final.</p></div></li>
            </ol>
            <p class="build__now">Replanteo y cimentación</p>
            <div class="build__meter"><span class="build__pct">0</span><small>% de obra</small><div class="build__bar"><i></i></div></div>
          </div>
          <div class="build__art">
            <svg viewBox="0 0 600 620" class="build__svg" aria-label="Dibujo de un edificio que se construye al hacer scroll" role="img">{build_svg()}</svg>
          </div>
        </div>
      </div>
    </section>
'''

HERO = '''
    <section class="hero">
      <div class="hero__grid container">
        <div class="hero__copy">
          <p class="eyebrow reveal">Estudio de arquitectura · Algeciras</p>
          <h1 data-split>Arquitectura rigurosa, <em class="gold">pensada para durar.</em></h1>
          <p class="lead reveal">Más de 25 años proyectando, valorando y dirigiendo obras en Algeciras y el Campo de Gibraltar. Edificación, tasaciones, infraestructuras eléctricas, licencias y peritaciones con un único interlocutor técnico.</p>
          <div class="hero__cta reveal">
            <a href="contacto.html" class="btn magnetic">Solicitar presupuesto</a>
            <a href="servicios.html" class="link-arrow">Ver servicios <span aria-hidden="true">→</span></a>
          </div>
        </div>

        <div class="hero__art" aria-hidden="true" data-parallax="0.1">
          <svg viewBox="0 0 520 560" class="drawing">
            <g class="grid-lines">
              <path d="M40 0v560M140 0v560M240 0v560M340 0v560M440 0v560"/>
              <path d="M0 80h520M0 180h520M0 280h520M0 380h520M0 480h520"/>
            </g>
            <g class="ink">
              <path class="draw" d="M80 500V200h220v300"/>
              <path class="draw" d="M300 500V120h140v380"/>
              <path class="draw" d="M40 500h460"/>
              <path class="draw" d="M80 260h220M80 320h220M80 380h220M80 440h220"/>
              <path class="draw" d="M135 200v300M190 200v300M245 200v300"/>
              <path class="draw" d="M330 160h80v60h-80zM330 260h80v60h-80zM330 360h80v60h-80z"/>
            </g>
            <g class="gold-line">
              <path class="draw" d="M300 120l70-50 70 50"/>
              <path class="draw" d="M60 530h400"/>
              <circle cx="460" cy="70" r="26" class="draw sun"/>
            </g>
            <g class="dim">
              <path d="M80 540h360M80 534v12M440 534v12"/>
              <text x="250" y="556" text-anchor="middle">25+ años</text>
            </g>
          </svg>
        </div>
      </div>

      <div class="container">
        <ul class="stats">
          <li class="reveal"><strong><span data-count="25">25</span><span class="gold">+</span></strong><span>años de ejercicio profesional</span></li>
          <li class="reveal"><strong><span data-count="12">12</span></strong><span>áreas de servicio técnico</span></li>
          <li class="reveal"><strong><span data-count="1">1</span></strong><span>interlocutor de principio a fin</span></li>
          <li class="reveal"><strong class="stats__text">Campo de Gibraltar</strong><span>ámbito principal de trabajo</span></li>
        </ul>
      </div>
      <a href="#estudio" class="scroll-cue" aria-label="Bajar"><span></span></a>
    </section>
'''

# ---------------- INICIO ----------------
inicio = HERO + marquee() + '''
    <section class="section" id="estudio">
      <div class="container split">
        <div>
          <p class="eyebrow reveal">01 — El estudio</p>
          <h2 data-split>Un cuarto de siglo construyendo en el sur.</h2>
        </div>
        <div class="split__body">
          <p class="reveal">El estudio de <strong>Enrique Sánchez Polo</strong> nace en Algeciras con una idea sencilla: que cada proyecto, desde una vivienda unifamiliar hasta un centro de transformación, se resuelva con el mismo rigor técnico, claridad y cumplimiento de plazos.</p>
          <p class="reveal">Más de 25 años acompañando a particulares, comunidades, empresas y compañías del sector energético en todas las fases: proyecto, licencias, obra, legalización y valoración.</p>
          <a href="estudio.html" class="link-arrow reveal">Conocer el estudio <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </section>
''' + BUILD + f'''
    <section class="section section--grey">
      <div class="container">
        <div class="section__head section__head--row">
          <div>
            <p class="eyebrow reveal">02 — Especialidades</p>
            <h2 data-split>Lo que más nos piden.</h2>
          </div>
          <a href="servicios.html" class="link-arrow reveal">Ver los 12 servicios <span aria-hidden="true">→</span></a>
        </div>
        <div class="services">
{service_cards([SERVICES[i] for i in (1, 2, 0, 4, 6, 7)])}
        </div>
      </div>
    </section>
''' + STEPS

page("inicio", "Enrique Sánchez Polo · Arquitecto en Algeciras",
     "Estudio de arquitectura de Enrique Sánchez Polo en Algeciras. Más de 25 años en edificación, tasaciones, infraestructuras eléctricas, licencias y peritaciones.",
     inicio)

# ---------------- ESTUDIO ----------------
estudio = page_hero("01", "Estudio", "Más de 25 años de oficio, <em class=\"gold\">un único interlocutor.</em>",
    "Un estudio de arquitectura de Algeciras con vocación técnica, trato cercano y conocimiento profundo del Campo de Gibraltar.",
    '<g class="ink"><path class="draw" d="M40 290h320"/><path class="draw" d="M80 290V130h120v160"/><path class="draw" d="M200 290V90h120v200"/><path class="draw" d="M110 170h60v40h-60zM230 130h60v40h-60zM230 210h60v40h-60z"/></g><g class="gold-line"><path class="draw" d="M60 305h280"/><path class="draw" d="M200 90l60-40 60 40"/></g>') + '''
    <section class="section">
      <div class="container split">
        <div>
          <p class="eyebrow reveal">Quiénes somos</p>
          <h2 data-split>Arquitectura útil, bien hecha y a tiempo.</h2>
        </div>
        <div class="split__body">
          <p class="reveal">El estudio de <strong>Enrique Sánchez Polo</strong> nace en Algeciras con una idea sencilla: que cada proyecto, desde una vivienda unifamiliar hasta un centro de transformación, se resuelva con el mismo rigor técnico, claridad y cumplimiento de plazos.</p>
          <p class="reveal">A lo largo de más de 25 años, el estudio ha acompañado a particulares, comunidades de propietarios, empresas, promotoras, entidades financieras y compañías del sector energético en todas las fases: estudio previo, proyecto, tramitación de licencias, dirección de obra, legalización y valoración.</p>
          <p class="reveal">Conocemos la normativa urbanística de los municipios del Campo de Gibraltar, los procedimientos ante la Junta de Andalucía y las particularidades del clima y del entorno costero. Esa experiencia local se traduce en proyectos que se aprueban, se construyen y funcionan.</p>
        </div>
      </div>
    </section>

    <section class="section section--grey">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow reveal">Valores</p>
          <h2 data-split>Cuatro principios en cada encargo.</h2>
        </div>
        <div class="pillars">
          <article class="pillar reveal"><span class="pillar__icon"><svg viewBox="0 0 48 48"><path d="M8 40h32M12 40V18l12-8 12 8v22"/><path class="g" d="M20 40V28h8v12"/></svg></span><h3>Rigor técnico</h3><p>Cálculo, normativa y documentación impecables. Proyectos que se visan y se aprueban a la primera.</p></article>
          <article class="pillar reveal"><span class="pillar__icon"><svg viewBox="0 0 48 48"><circle cx="24" cy="18" r="8"/><path class="g" d="M10 42c2-8 8-12 14-12s12 4 14 12"/></svg></span><h3>Trato directo</h3><p>Hablas siempre con el arquitecto. Sin intermediarios ni cambios de interlocutor.</p></article>
          <article class="pillar reveal"><span class="pillar__icon"><svg viewBox="0 0 48 48"><path d="M24 44s14-12 14-24a14 14 0 0 0-28 0c0 12 14 24 14 24z"/><circle class="g" cx="24" cy="20" r="5"/></svg></span><h3>Conocimiento local</h3><p>Normativa de cada municipio, clima del Estrecho y tramitación ante la Junta de Andalucía.</p></article>
          <article class="pillar reveal"><span class="pillar__icon"><svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="17"/><path class="g" d="M24 13v11l7 5"/></svg></span><h3>Plazos cumplidos</h3><p>Calendario cerrado desde el primer día y seguimiento continuo de cada fase.</p></article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div>
          <p class="eyebrow reveal">Para quién trabajamos</p>
          <h2 data-split>Particulares, empresas e instituciones.</h2>
        </div>
        <ul class="clients">
          <li class="reveal"><h3>Particulares</h3><p>Viviendas, reformas, tasaciones, herencias y legalizaciones.</p></li>
          <li class="reveal"><h3>Comunidades de propietarios</h3><p>ITE, rehabilitación, accesibilidad y patologías.</p></li>
          <li class="reveal"><h3>Empresas y promotoras</h3><p>Naves, locales, promociones y licencias de actividad.</p></li>
          <li class="reveal"><h3>Sector energético</h3><p>Obra civil de infraestructuras eléctricas y edificaciones técnicas.</p></li>
          <li class="reveal"><h3>Entidades financieras y aseguradoras</h3><p>Valoraciones, peritaciones y informes de daños.</p></li>
          <li class="reveal"><h3>Despachos de abogados</h3><p>Informes periciales y dictámenes técnicos para procedimientos judiciales.</p></li>
        </ul>
      </div>
    </section>
''' + STEPS

page("estudio", "Estudio · Enrique Sánchez Polo Arquitecto",
     "Conoce el estudio de arquitectura de Enrique Sánchez Polo en Algeciras: más de 25 años de experiencia en el Campo de Gibraltar.", estudio)

# ---------------- SERVICIOS ----------------
tabs = "".join(f'<a href="#{s[0]}">{s[1]}</a>' for s in SERVICES)
servicios = page_hero("02", "Servicios", "Todo lo que tu proyecto necesita, <em class=\"gold\">en un mismo estudio.</em>",
    "Servicios profesionales de arquitectura con visado colegial, desde la idea inicial hasta el certificado final de obra.",
    '<g class="ink"><path class="draw" d="M40 290h320"/><path class="draw" d="M70 290V170h100v120"/><path class="draw" d="M100 290v-60h40v60"/></g><g class="gold-line"><path class="draw" d="M260 290V60M235 85h50M222 120h76M260 60l-25 25M260 60l25 25M170 190l90-70M298 120l52 60v110"/></g>') + f'''
    <nav class="chips" aria-label="Ir a servicio"><div class="container chips__inner">{tabs}</div></nav>
    <section class="section">
      <div class="container">
        <div class="services services--detailed">
{service_cards(SERVICES, detailed=True)}
        </div>
      </div>
    </section>
''' + marquee() + STEPS

page("servicios", "Servicios · Enrique Sánchez Polo Arquitecto",
     "Edificación, tasaciones, infraestructuras eléctricas, rehabilitación, licencias, AFO, peritaciones, dirección de obra y más en Algeciras.", servicios)

# ---------------- PROYECTOS ----------------
proyectos = page_hero("03", "Proyectos", "Experiencia en escalas <em class=\"gold\">y usos muy distintos.</em>",
    "De una vivienda unifamiliar a un centro de transformación: tipologías en las que el estudio trabaja habitualmente.",
    '<g class="ink"><path class="draw" d="M40 290h320"/><path class="draw" d="M60 290V150h90v140M170 290V90h90v200M280 290V190h70v100"/><path class="draw" d="M190 120h50v30h-50zM190 180h50v30h-50z"/></g><g class="gold-line"><path class="draw" d="M40 60h320" stroke-dasharray="4 8"/></g>') + f'''
    <section class="section">
      <div class="container">
        <div class="section__head section__head--row">
          <h2 data-split>Tipologías de proyecto.</h2>
          <div class="filters reveal" role="tablist" aria-label="Filtrar tipologías">
            <button class="filter is-active" data-filter="all">Todos</button>
            <button class="filter" data-filter="residencial">Residencial</button>
            <button class="filter" data-filter="tecnico">Técnico</button>
            <button class="filter" data-filter="consultoria">Consultoría</button>
          </div>
        </div>
        <div class="projects">
{project_cards(PROJECTS)}
        </div>
      </div>
    </section>
'''

page("proyectos", "Proyectos · Enrique Sánchez Polo Arquitecto",
     "Tipologías de proyecto del estudio: viviendas, edificios, centros de transformación, naves, tasaciones, peritaciones y legalizaciones.", proyectos)

# ---------------- CONTACTO ----------------
contacto = page_hero("04", "Contacto", "Hablemos de <em class=\"gold\">tu proyecto.</em>",
    "Cuéntanos qué necesitas y te responderemos con una primera valoración sin compromiso.",
    '<g class="ink"><path class="draw" d="M60 90h280v180H60z"/><path class="draw" d="M60 90l140 100 140-100"/></g><g class="gold-line"><path class="draw" d="M40 300h320"/><circle class="draw" cx="330" cy="80" r="18"/></g>') + '''
    <section class="section">
      <div class="container contact">
        <div class="contact__info">
          <h2 data-split>Datos del estudio.</h2>
          <dl class="contact__list reveal">
            <div><dt>Estudio</dt><dd>Algeciras, Cádiz<br><span class="todo">[Dirección por confirmar]</span></dd></div>
            <div><dt>Teléfono</dt><dd><a href="tel:+34000000000" class="todo">[Teléfono por confirmar]</a></dd></div>
            <div><dt>Email</dt><dd><a href="mailto:info@enriquesanchezpolo.es" class="todo">[Email por confirmar]</a></dd></div>
            <div><dt>Horario</dt><dd>Lunes a viernes · 9:00 – 14:00 / 17:00 – 20:00</dd></div>
          </dl>
        </div>

        <form class="form reveal" id="contact-form" novalidate>
          <div class="form__row">
            <label>Nombre<input type="text" name="nombre" required autocomplete="name"></label>
            <label>Teléfono<input type="tel" name="telefono" autocomplete="tel"></label>
          </div>
          <label>Email<input type="email" name="email" required autocomplete="email"></label>
          <label>Tipo de servicio
            <select name="servicio">
              <option>Proyecto de edificación</option>
              <option>Tasación / valoración</option>
              <option>Infraestructura eléctrica</option>
              <option>Rehabilitación o reforma</option>
              <option>Licencia o legalización</option>
              <option>Peritación o informe</option>
              <option>Otro</option>
            </select>
          </label>
          <label>Mensaje<textarea name="mensaje" rows="5" required></textarea></label>
          <label class="check"><input type="checkbox" required> He leído y acepto la política de privacidad.</label>
          <button type="submit" class="btn magnetic">Enviar consulta</button>
          <p class="form__status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>

    <section class="section section--grey" id="zona">
      <div class="container split">
        <div>
          <p class="eyebrow reveal">Zona de actuación</p>
          <h2 data-split>Desde Algeciras, para todo el Campo de Gibraltar.</h2>
          <p class="reveal muted">Y en el resto de la provincia de Cádiz y Andalucía bajo consulta.</p>
        </div>
        <ul class="towns">
          <li class="is-main reveal">Algeciras</li>
          <li class="reveal">La Línea de la Concepción</li>
          <li class="reveal">San Roque</li>
          <li class="reveal">Los Barrios</li>
          <li class="reveal">Tarifa</li>
          <li class="reveal">Jimena de la Frontera</li>
          <li class="reveal">Castellar de la Frontera</li>
          <li class="reveal">Sotogrande</li>
        </ul>
      </div>
    </section>
'''

page("contacto", "Contacto · Enrique Sánchez Polo Arquitecto",
     "Contacta con el estudio de arquitectura de Enrique Sánchez Polo en Algeciras. Presupuesto sin compromiso.", contacto, cta=False)

print("ok")
