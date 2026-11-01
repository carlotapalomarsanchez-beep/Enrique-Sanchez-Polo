"""Genera las páginas HTML del sitio con cabecera y pie compartidos."""
import sys, pathlib, re

OUT = pathlib.Path(sys.argv[1])

LOGO = '<svg viewBox="0 0 40 40"><path d="M6 34V14L20 6l14 8v20" /><path class="g" d="M15 34V23h10v11" /></svg>'

# Dirección pública de la web (GitHub Pages). Cambiar si se usa un dominio propio.
SITE = "https://carlotapalomarsanchez-beep.github.io/Enrique-Sanchez-Polo/"
OG_IMAGE = SITE + "og-image.png"
PAGES = []  # para el sitemap


def head(name, title, desc, base=None, noindex=False):
    file = "" if name == "inicio" else f"{name}.html"
    url = SITE + file
    base_tag = f'\n  <base href="{base}">' if base else ""
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">{base_tag}
  <title>{title}</title>
  <meta name="description" content="{desc}">{robots}
  <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{url}">

  <!-- Vista previa al compartir el enlace (WhatsApp, LinkedIn, Facebook, X...) -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Enrique Sánchez Polo · Arquitecto">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Enrique Sánchez Polo, estudio de arquitectura en Algeciras">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{OG_IMAGE}">

  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">

  <script>
    (function (r, l) {{
      // Forzar HTTPS (GitHub Pages también lo fuerza desde sus ajustes)
      if (l.protocol === 'http:' && !/^(localhost|127\\.|192\\.168\\.)/.test(l.hostname)) l.replace('https:' + l.href.slice(5));
      r.classList.add('js');
      var seen = false;
      try {{ seen = !!sessionStorage.getItem('esp-intro'); }} catch (e) {{}}
      r.classList.add(seen ? 'entering' : 'first-visit');
      setTimeout(function () {{ r.classList.remove('entering'); }}, 2500);
    }})(document.documentElement, location);
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600&family=Cormorant+Garamond:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script src="script.js" defer></script>
</head>'''

INTRO = f'''
  <a href="#contenido" class="skip">Saltar al contenido</a>

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
      <a href="index.html" class="brand" aria-label="Enrique Sánchez Polo, arquitecto. Ir al inicio">
        <span class="brand__mark" aria-hidden="true">{LOGO}</span>
        <span class="brand__text"><strong>Enrique Sánchez Polo</strong><small>Arquitecto</small></span>
      </a>
      <button class="nav__toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
      <nav class="nav__links" id="menu" aria-label="Principal">
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
        <a href="contacto.html"{cls('contacto')} data-btn>Pedir presupuesto</a>
      </nav>
    </div>
  </header>
'''

CTA_BAND = '''
  <section class="cta-band">
    <div class="container cta-band__inner">
      <div>
        <h2 data-split>¿Tienes un proyecto en mente?</h2>
        <p class="cta-band__sub">Primera consulta y presupuesto sin compromiso. Respuesta en 24–48 h laborables.</p>
      </div>
      <a href="contacto.html" class="btn btn--gold">Pedir presupuesto <span aria-hidden="true">→</span></a>
    </div>
  </section>
'''

FOOT = f'''
  <footer class="footer">
    <div class="container footer__inner">
      <div class="brand brand--footer">
        <span class="brand__mark" aria-hidden="true">{LOGO}</span>
        <span class="brand__text"><strong>Enrique Sánchez Polo</strong><small>Arquitecto · Algeciras</small></span>
      </div>
      <nav class="footer__links" aria-label="Pie">
        <a href="index.html">Inicio</a><a href="estudio.html">Estudio</a><a href="servicios.html">Servicios</a><a href="proyectos.html">Proyectos</a><a href="contacto.html">Contacto</a>
      </nav>
      <div class="footer__legal">
        <p>© <span id="year">2026</span> Enrique Sánchez Polo · Arquitecto colegiado en el COA de Cádiz <span class="todo">[nº por confirmar]</span></p>
        <p class="footer__legal-links"><a href="aviso-legal.html">Aviso legal y condiciones de uso</a><a href="privacidad.html">Privacidad</a><a href="cookies.html">Cookies</a><button type="button" class="link-btn" data-cookie-settings>Preferencias de cookies</button></p>
      </div>
    </div>
  </footer>

  <!-- Botón fijo de presupuesto (móvil) -->
  <a href="contacto.html" class="fab-cta">Pedir presupuesto <span aria-hidden="true">→</span></a>

  <!-- Aviso de cookies -->
  <div class="cookie" role="dialog" aria-live="polite" aria-label="Aviso de cookies" hidden>
    <p><strong>Tu privacidad importa.</strong> Usamos cookies analíticas (Google Analytics) solo si las aceptas, para saber cómo se usa la web y mejorarla. <a href="cookies.html">Más información</a>.</p>
    <div class="cookie__actions">
      <button type="button" class="btn btn--small btn--ghost" data-cookie="reject">Rechazar</button>
      <button type="button" class="btn btn--small" data-cookie="accept">Aceptar</button>
    </div>
  </div>
</body>
</html>
'''

def page(name, title, desc, body, cta=True, base=None, noindex=False, in_sitemap=True, priority="0.8"):
    html = (head(name, title, desc, base, noindex) + f'\n<body data-page="{name}">\n' + INTRO + nav(name)
            + '\n  <main id="contenido">\n' + body + '\n  </main>\n' + (CTA_BAND if cta else '') + FOOT)
    # Dibujos decorativos: ocultos para lectores de pantalla (accesibilidad)
    html = re.sub(r'<svg (?![^>]*aria-)', '<svg aria-hidden="true" focusable="false" ', html)
    (OUT / f"{'index' if name == 'inicio' else name}.html").write_text(html, encoding="utf-8")
    if in_sitemap:
        PAGES.append(("" if name == "inicio" else f"{name}.html", priority))


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
        out.append(f'''          <article class="service{' service--featured' if feat else ''} reveal" id="{sid}">
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

# Al pasar por encima: servicio del formulario y tres puntos de información
PROJECT_INFO = {
    "Viviendas unifamiliares": ("Proyecto de edificación", ["Estudio de parcela y normativa", "Proyecto básico y de ejecución", "Licencia y dirección de obra"]),
    "Edificios de viviendas": ("Proyecto de edificación", ["Promociones y vivienda protegida", "Estudio de viabilidad", "Coordinación con promotora y constructora"]),
    "Centros de transformación y subestaciones": ("Infraestructura eléctrica", ["Obra civil y cimentaciones", "Edificios prefabricados y casetas", "Canalizaciones y tramitación"]),
    "Naves industriales y logísticas": ("Proyecto de edificación", ["Naves y almacenes", "Licencia de actividad", "Estructura e instalaciones"]),
    "Tasaciones inmobiliarias": ("Tasación / valoración", ["Herencias y compraventas", "Divorcios y repartos", "Solares y fincas rústicas"]),
    "Rehabilitación de edificios": ("Rehabilitación o reforma", ["Fachadas y cubiertas", "Accesibilidad y ascensores", "Refuerzo estructural"]),
    "Peritaciones y patologías": ("Peritación o informe", ["Informes judiciales y de parte", "Grietas y humedades", "Siniestros y aseguradoras"]),
    "Locales y edificios terciarios": ("Licencia o legalización", ["Adecuación de locales", "Licencia de apertura", "Oficinas y hostelería"]),
    "Legalizaciones, AFO y segregaciones": ("Licencia o legalización", ["Asimilado a Fuera de Ordenación", "Legalización de ampliaciones", "Segregaciones de fincas"]),
}

def animate_svg(svg):
    """Prepara cada trazo para dibujarse de nuevo al pasar por encima."""
    n = [0]
    def rep(m):
        tag = m.group(0)
        if "stroke-dasharray" in tag:
            return tag
        n[0] += 1
        tag = tag.replace(m.group(1), f'{m.group(1)} pathLength="1" style="--i:{n[0] - 1}"', 1)
        return re.sub(r'class="([^"]*)"', lambda k: f'class="{k.group(1)} u"', tag, count=1)
    return re.sub(r"(<path|<circle)[^>]*>", rep, svg)

def project_cards(items):
    from urllib.parse import quote
    out = []
    for cat, c1, c2, t, d, svg in items:
        serv = PROJECT_INFO[t][0]
        href = f"contacto.html?servicio={quote(serv)}&amp;tipo={quote(t)}#contact-form"
        out.append(f'''          <article class="project reveal" data-cat="{cat}" tabindex="0" aria-label="{t}">
            <div class="project__img">
              <svg viewBox="0 0 400 280" aria-hidden="true">{animate_svg(svg)}</svg>
              <a class="project__cta" href="{href}">Consultar <span aria-hidden="true">→</span></a>
            </div>
            <h3>{t}</h3>
            <div class="project__details">
              <div class="project__details-inner">
                <div class="project__meta"><span>{c1}</span><span>{c2}</span></div>
                <p>{d}</p>
              </div>
            </div>
          </article>''')
    return "\n".join(out)

# Servicios con el mismo formato que los proyectos: dibujo + nombre; al pasar por encima, todo lo demás
SERVICE_ART = {
    "edificacion": ("Proyecto de edificación", "Obra nueva",
        '<path class="ink" d="M70 240V110h130v130M200 240V60h110v180M50 240h290"/><path class="ink" d="M100 140h30v30h-30zM150 140h30v30h-30zM100 190h30v30h-30zM230 90h50v30h-50zM230 150h50v30h-50z"/><path class="gold-stroke" d="M50 255h290M200 60l55-30 55 30"/>'),
    "tasaciones": ("Tasación / valoración", "Valoración",
        '<path class="ink" d="M70 240V140l75-55 75 55v100M50 240h200"/><path class="ink" d="M125 240v-55h40v55M95 160h25v25H95z"/><path class="gold-stroke" d="M250 95h80l22 25-22 25h-80z"/><circle class="gold-stroke" cx="268" cy="120" r="6"/><path class="gold-stroke" d="M220 140l30-20"/>'),
    "electricas": ("Infraestructura eléctrica", "Energía",
        '<path class="ink" d="M50 240h300M70 240v-70h90v70M95 240v-40h40v40"/><path class="ink" d="M40 95q90 40 160 15M200 110q90 25 160-15"/><path class="gold-stroke" d="M250 40l-40 200M250 40l40 200M222 100h56M212 150h76M230 60h40"/>'),
    "rehabilitacion": ("Rehabilitación o reforma", "Rehabilitación",
        '<path class="ink" d="M110 240V70h180v170M90 240h220"/><path class="ink" d="M140 100h40v45h-40zM220 100h40v45h-40zM140 175h40v45h-40zM220 175h40v45h-40z"/><path class="gold-stroke" d="M90 60v180M310 60v180M90 120h220M90 180h220" stroke-dasharray="6 6"/>'),
    "licencias": ("Licencia o legalización", "Tramitación",
        '<path class="ink" d="M120 40h120l40 40v160H120zM240 40v40h40M145 110h110M145 135h110M145 160h70"/><circle class="gold-stroke" cx="255" cy="205" r="28"/><path class="gold-stroke" d="M242 205l10 10 18-20"/>'),
    "legalizaciones": ("Licencia o legalización", "Regularización",
        '<path class="ink" d="M60 240V140l70-55 70 55v100M40 240h300M110 240v-50h40v50"/><path class="gold-stroke" d="M200 240V150h110v90M230 180h40v30h-40z" stroke-dasharray="5 6"/>'),
    "peritaciones": ("Peritación o informe", "Peritación",
        '<path class="ink" d="M60 240V70h170v170M40 240h210"/><path class="gold-stroke" d="M140 70l18 45-26 28 22 40-10 57"/><circle class="ink" cx="285" cy="130" r="42"/><path class="ink" d="M315 160l40 40"/>'),
    "direccion": ("Dirección de obra", "Obra",
        '<path class="ink" d="M110 200q0-90 90-90t90 90zM80 200h240v18H80z"/><path class="gold-stroke" d="M200 110v90M160 125v40M240 125v40"/><path class="ink" d="M60 250h280"/>'),
    "industrial": ("Naves e industria", "Industrial",
        '<path class="ink" d="M50 240V140l60-45v45l60-45v45l60-45v45l60-45v145M30 240h340"/><path class="ink" d="M90 240v-60h60v60M220 190h80v30h-80z"/><path class="gold-stroke" d="M50 140h240"/>'),
    "eficiencia": ("Eficiencia energética", "Energía",
        '<path class="ink" d="M60 240V150l70-55 70 55v90M40 240h180M110 240v-45h40v45"/><circle class="gold-stroke" cx="300" cy="70" r="22"/><path class="gold-stroke" d="M250 130h50M250 160h75M250 190h100M250 220h120"/>'),
    "ite": ("ITE / IEE", "Inspección",
        '<path class="ink" d="M70 240V60h150v180M50 240h190M100 90h30v30h-30zM160 90h30v30h-30zM100 150h30v30h-30zM160 150h30v30h-30z"/><path class="ink" d="M255 80h90v150h-90zM280 70h40v20h-40z"/><path class="gold-stroke" d="M270 120l8 8 14-14M270 160l8 8 14-14M270 200l8 8 14-14M302 125h30M302 165h30M302 205h30"/>'),
    "urbanismo": ("Urbanismo y suelo", "Urbanismo",
        '<path class="ink" d="M50 60h300v180H50zM50 150h120V60M170 150l80 90M250 60v90h100"/><path class="gold-stroke" d="M50 260h300M50 252v16M350 252v16M170 150h80v-90"/>'),
}

def service_drawing_cards():
    from urllib.parse import quote
    out = []
    for i, (sid, title, text, bullets, feat) in enumerate(SERVICES, 1):
        serv, tag, svg = SERVICE_ART[sid]
        href = f"contacto.html?servicio={quote(serv)}&amp;tipo={quote(title)}#contact-form"
        badge = '<span class="project__badge">Especialidad</span>' if feat else ''
        out.append(f"""          <article class="project reveal" id="{sid}" tabindex="0" aria-label="{title}">
            <div class="project__img">
              <svg viewBox="0 0 400 280" aria-hidden="true">{animate_svg(svg)}</svg>{badge}
              <a class="project__cta" href="{href}">Consultar <span aria-hidden="true">→</span></a>
            </div>
            <h3><span class="project__num">{i:02d}</span> {title}</h3>
            <div class="project__details">
              <div class="project__details-inner">
                <div class="project__meta"><span>Servicio</span><span>{tag}</span></div>
                <p>{text}</p>
              </div>
            </div>
          </article>""")
    return "\n".join(out)

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
PHASES = ["Proyecto", "Cimentación", "Estructura", "Cerramientos", "Cubierta e instalaciones", "Entrega"]

JOURNEY = f'''
    <section class="journey" aria-label="Presentación del estudio">
      <div class="container journey__grid">
        <div class="journey__art" aria-hidden="true" data-phases="{'|'.join(PHASES)}">
          <canvas class="model"></canvas>
          <div class="journey__meter">
            <p class="obra__label"><span class="obra__n">00</span> <span class="obra__phase">{PHASES[0]}</span></p>
            <p class="obra__pct"><span class="build__pct">0</span>%</p>
            <div class="build__bar"><i></i></div>
          </div>
        </div>

        <div class="journey__content">
          <div class="journey__hero">
            <p class="eyebrow reveal">Estudio de arquitectura · Algeciras</p>
            <h1 data-split>Arquitectura rigurosa, <em class="gold">pensada para durar.</em></h1>
            <p class="lead reveal">Más de 25 años proyectando, valorando y dirigiendo obras en Algeciras y el Campo de Gibraltar. Edificación, tasaciones, infraestructuras eléctricas, licencias y peritaciones con un único interlocutor técnico.</p>
            <div class="hero__cta reveal">
              <a href="contacto.html" class="btn">Pedir presupuesto sin compromiso</a>
              <a href="servicios.html" class="link-arrow">Ver servicios <span aria-hidden="true">→</span></a>
            </div>
            <ul class="stats">
              <li class="reveal"><strong><span data-count="25">25</span><span class="gold">+</span></strong><span>años de ejercicio profesional</span></li>
              <li class="reveal"><strong><span data-count="12">12</span></strong><span>áreas de servicio técnico</span></li>
              <li class="reveal"><strong><span data-count="1">1</span></strong><span>interlocutor de principio a fin</span></li>
              <li class="reveal"><strong class="stats__text">Campo de Gibraltar</strong><span>ámbito principal de trabajo</span></li>
            </ul>
          </div>

          <div class="obra__block" id="estudio">
            <p class="eyebrow reveal">01 — El estudio</p>
            <h2 data-split>Un cuarto de siglo construyendo en el sur.</h2>
            <p class="obra__text reveal">El estudio de <strong>Enrique Sánchez Polo</strong> nace en Algeciras con una idea sencilla: que cada proyecto, desde una vivienda unifamiliar hasta un centro de transformación, se resuelva con el mismo rigor técnico, claridad y cumplimiento de plazos.</p>
            <p class="obra__text reveal">Más de 25 años acompañando a particulares, comunidades, empresas y compañías del sector energético en todas las fases: proyecto, licencias, obra, legalización y valoración.</p>
            <a href="estudio.html" class="link-arrow reveal">Conocer el estudio <span aria-hidden="true">→</span></a>
          </div>

          <div class="obra__block">
            <p class="eyebrow reveal">02 — Especialidades</p>
            <h2 data-split>Lo que más nos piden.</h2>
            <div class="services services--two">
{service_cards([SERVICES[i] for i in (1, 2, 0, 4, 6, 7)])}
            </div>
            <a href="servicios.html" class="link-arrow reveal obra__more">Ver los 12 servicios <span aria-hidden="true">→</span></a>
          </div>

          <div class="obra__block">
            <p class="eyebrow reveal">03 — Método de trabajo</p>
            <h2 data-split>Un proceso claro, sin sorpresas.</h2>
            <ol class="steps steps--light">
              <li class="reveal"><span class="steps__n">01</span><h3>Primera reunión</h3><p>Escuchamos tus necesidades, visitamos el inmueble o la parcela y analizamos la normativa aplicable.</p></li>
              <li class="reveal"><span class="steps__n">02</span><h3>Propuesta y presupuesto</h3><p>Te entregamos una propuesta de honorarios cerrada, con plazos y alcance de cada fase.</p></li>
              <li class="reveal"><span class="steps__n">03</span><h3>Proyecto y tramitación</h3><p>Redactamos la documentación técnica, la visamos y la presentamos ante ayuntamiento, Junta o compañía.</p></li>
              <li class="reveal"><span class="steps__n">04</span><h3>Obra y entrega</h3><p>Dirigimos la ejecución, controlamos calidad y costes y emitimos el certificado final de obra.</p></li>
            </ol>
          </div>

          <div class="obra__block">
            <p class="eyebrow reveal">04 — Para quién trabajamos</p>
            <h2 data-split>Particulares, empresas e instituciones.</h2>
            <ul class="clients">
              <li class="reveal"><h3>Particulares</h3><p>Viviendas, reformas, tasaciones, herencias y legalizaciones.</p></li>
              <li class="reveal"><h3>Comunidades de propietarios</h3><p>ITE, rehabilitación, accesibilidad y patologías.</p></li>
              <li class="reveal"><h3>Empresas y promotoras</h3><p>Naves, locales, promociones y licencias de actividad.</p></li>
              <li class="reveal"><h3>Sector energético</h3><p>Obra civil de infraestructuras eléctricas y edificaciones técnicas.</p></li>
            </ul>
          </div>
        </div>
      </div>
    </section>
'''

SCHEMA = '''
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ProfessionalService",
      "name": "Enrique Sánchez Polo · Arquitecto",
      "description": "Estudio de arquitectura en Algeciras con más de 25 años de experiencia: edificación, tasaciones, infraestructuras eléctricas, licencias, legalizaciones y peritaciones.",
      "url": "https://carlotapalomarsanchez-beep.github.io/Enrique-Sanchez-Polo/",
      "image": "https://carlotapalomarsanchez-beep.github.io/Enrique-Sanchez-Polo/og-image.png",
      "address": { "@type": "PostalAddress", "addressLocality": "Algeciras", "addressRegion": "Cádiz", "addressCountry": "ES" },
      "areaServed": ["Algeciras", "La Línea de la Concepción", "San Roque", "Los Barrios", "Tarifa", "Jimena de la Frontera", "Castellar de la Frontera"],
      "knowsAbout": ["Arquitectura", "Tasaciones", "Infraestructuras eléctricas", "Licencias de obra", "Peritaciones", "Rehabilitación"]
    }
    </script>
'''

inicio = JOURNEY + marquee() + SCHEMA

page("inicio", "Enrique Sánchez Polo · Arquitecto en Algeciras",
     "Estudio de arquitectura de Enrique Sánchez Polo en Algeciras. Más de 25 años en edificación, tasaciones, infraestructuras eléctricas, licencias y peritaciones.",
     inicio, priority="1.0")

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
servicios = page_hero("02", "Servicios", "Todo lo que tu proyecto necesita, <em class=\"gold\">en un mismo estudio.</em>",
    "Servicios profesionales de arquitectura con visado colegial, desde la idea inicial hasta el certificado final de obra.",
    '<g class="ink"><path class="draw" d="M40 290h320"/><path class="draw" d="M70 290V170h100v120"/><path class="draw" d="M100 290v-60h40v60"/></g><g class="gold-line"><path class="draw" d="M260 290V60M235 85h50M222 120h76M260 60l-25 25M260 60l25 25M170 190l90-70M298 120l52 60v110"/></g>') + f'''
    <section class="section">
      <div class="container">
        <div class="projects projects--services">
{service_drawing_cards()}
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
          <div class="filters reveal" role="group" aria-label="Filtrar tipologías">
            <button class="filter is-active" data-filter="all" aria-pressed="true">Todos</button>
            <button class="filter" data-filter="residencial" aria-pressed="false">Residencial</button>
            <button class="filter" data-filter="tecnico" aria-pressed="false">Técnico</button>
            <button class="filter" data-filter="consultoria" aria-pressed="false">Consultoría</button>
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
            <div><dt>Email</dt><dd><a class="js-email todo" data-u="info" data-d="enriquesanchezpolo.es" href="contacto.html#contact-form">[Email por confirmar]</a></dd></div>
            <div><dt>Horario</dt><dd>Lunes a viernes · 9:00 – 14:00 / 17:00 – 20:00</dd></div>
          </dl>
        </div>

        <form class="form reveal" id="contact-form" novalidate aria-describedby="form-help">
          <p class="form__help" id="form-help">Los campos con <span aria-hidden="true">*</span><span class="sr-only">asterisco</span> son obligatorios.</p>
          <div class="form__row">
            <div class="field">
              <label for="f-nombre">Nombre *</label>
              <input id="f-nombre" type="text" name="nombre" required minlength="2" maxlength="80" autocomplete="name" aria-describedby="e-nombre">
              <p class="field__error" id="e-nombre"></p>
            </div>
            <div class="field">
              <label for="f-telefono">Teléfono</label>
              <input id="f-telefono" type="tel" name="telefono" maxlength="20" pattern="[+0-9 ()-]{9,20}" autocomplete="tel" inputmode="tel" aria-describedby="e-telefono">
              <p class="field__error" id="e-telefono"></p>
            </div>
          </div>
          <div class="field">
            <label for="f-email">Email *</label>
            <input id="f-email" type="email" name="email" required maxlength="120" autocomplete="email" aria-describedby="e-email">
            <p class="field__error" id="e-email"></p>
          </div>
          <div class="field">
            <label for="f-servicio">Tipo de servicio</label>
            <select id="f-servicio" name="servicio">
              <option>Proyecto de edificación</option>
              <option>Tasación / valoración</option>
              <option>Infraestructura eléctrica</option>
              <option>Rehabilitación o reforma</option>
              <option>Licencia o legalización</option>
              <option>Peritación o informe</option>
              <option>Dirección de obra</option>
              <option>Naves e industria</option>
              <option>Eficiencia energética</option>
              <option>ITE / IEE</option>
              <option>Urbanismo y suelo</option>
              <option>Otro</option>
            </select>
          </div>
          <div class="field">
            <label for="f-mensaje">Mensaje *</label>
            <textarea id="f-mensaje" name="mensaje" rows="5" required minlength="10" maxlength="2000" aria-describedby="e-mensaje"></textarea>
            <p class="field__error" id="e-mensaje"></p>
          </div>
          <!-- Antispam: campo trampa invisible para personas -->
          <div class="hp" aria-hidden="true">
            <label for="f-web">No rellenar</label>
            <input id="f-web" type="text" name="web" tabindex="-1" autocomplete="off">
          </div>
          <div class="field">
            <label class="check" for="f-privacidad"><input id="f-privacidad" type="checkbox" name="privacidad" required aria-describedby="e-privacidad"> <span>He leído y acepto la <a href="privacidad.html">política de privacidad</a>. *</span></label>
            <p class="field__error" id="e-privacidad"></p>
          </div>
          <button type="submit" class="btn">Enviar consulta</button>
          <p class="form__legal"><strong>Información básica sobre protección de datos.</strong> Responsable: Enrique Sánchez Polo. Finalidad: responder a tu consulta y, en su caso, preparar un presupuesto. Legitimación: tu consentimiento. Destinatarios: no se ceden datos a terceros salvo obligación legal. Derechos: acceso, rectificación, supresión y otros, como se explica en la <a href="privacidad.html">política de privacidad</a>.</p>
          <p class="form__status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>

    <section class="section section--grey zona" id="zona">
      <div class="container">
        <div class="section__head section__head--row">
          <div>
            <p class="eyebrow reveal">Zona de actuación</p>
            <h2 data-split>Desde Algeciras, para todo el Campo de Gibraltar.</h2>
          </div>
          <p class="reveal muted zona__note">Y en el resto de la provincia de Cádiz y Andalucía bajo consulta.</p>
        </div>
        <div class="zona__grid">
          <figure class="zona__main reveal">
            @@MAP_MAIN@@
            <figcaption><span class="legend legend--gold"></span> Campo de Gibraltar <span class="legend legend--dark"></span> Provincia de Cádiz <span class="legend"></span> Andalucía</figcaption>
          </figure>
          <div class="zona__detail reveal">
            <p class="zona__kicker">Detalle · Campo de Gibraltar</p>
            @@MAP_ZOOM@@
          </div>
        </div>
      </div>
    </section>
'''

MAP_MAIN, MAP_ZOOM = pathlib.Path(__file__).with_name("map_fragment.html").read_text(encoding="utf-8").split("<!--ZOOM-->")
contacto = contacto.replace("@@MAP_MAIN@@", MAP_MAIN.strip()).replace("@@MAP_ZOOM@@", MAP_ZOOM.strip())

page("contacto", "Contacto · Enrique Sánchez Polo Arquitecto",
     "Contacta con el estudio de arquitectura de Enrique Sánchez Polo en Algeciras. Presupuesto sin compromiso.", contacto, cta=False)

# ---------------- PÁGINAS LEGALES ----------------
TODO = lambda t: f'<span class="todo">[{t}]</span>'
TITULAR = f"""<ul>
          <li><strong>Titular:</strong> Enrique Sánchez Polo</li>
          <li><strong>NIF:</strong> {TODO('NIF por confirmar')}</li>
          <li><strong>Domicilio profesional:</strong> {TODO('Dirección por confirmar')}, Algeciras (Cádiz)</li>
          <li><strong>Email:</strong> <a class="js-email" data-u="info" data-d="enriquesanchezpolo.es" href="contacto.html">{TODO('Email por confirmar')}</a></li>
          <li><strong>Teléfono:</strong> {TODO('Teléfono por confirmar')}</li>
          <li><strong>Colegio profesional:</strong> Colegio Oficial de Arquitectos de Cádiz (COA Cádiz), n.º de colegiado {TODO('por confirmar')}</li>
          <li><strong>Titulación:</strong> Arquitecto, título oficial expedido en España</li>
        </ul>"""

def legal_page(name, kicker, title, updated, body, desc):
    html = f'''
    <section class="page-hero page-hero--small">
      <div class="container">
        <p class="crumbs reveal"><a href="index.html">Inicio</a> <span>/</span> {kicker}</p>
        <h1 data-split>{title}</h1>
        <p class="muted reveal">Última actualización: {updated}</p>
      </div>
    </section>
    <section class="section section--legal">
      <div class="container legal">
{body}
      </div>
    </section>
'''
    page(name, f"{kicker} · Enrique Sánchez Polo Arquitecto", desc, html, cta=False, priority="0.3")

UPDATED = "noviembre de 2026"

legal_page("aviso-legal", "Aviso legal", "Aviso legal y condiciones de uso", UPDATED, f"""
        <h2>1. Datos identificativos</h2>
        <p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
        {TITULAR}
        <p>El ejercicio de la profesión de arquitecto está sujeto a los Estatutos Generales de los Colegios Oficiales de Arquitectos, al Código Deontológico del Consejo Superior de los Colegios de Arquitectos de España (CSCAE) y a la normativa reguladora de la edificación (Ley 38/1999 de Ordenación de la Edificación y Código Técnico de la Edificación), disponibles en <a href="https://www.cscae.com" rel="noopener" target="_blank">cscae.com</a>.</p>

        <h2>2. Objeto y aceptación</h2>
        <p>Estas condiciones regulan el acceso y uso de este sitio web, cuya finalidad es informar sobre los servicios profesionales de arquitectura del estudio. Navegar por la web implica aceptar estas condiciones. Si no estás de acuerdo, te pedimos que no la utilices.</p>

        <h2>3. Condiciones de uso</h2>
        <p>Te comprometes a usar la web de forma lícita, sin dañar su funcionamiento ni los derechos de terceros, y a no enviar a través del formulario información falsa, ofensiva o que no te pertenezca.</p>

        <h2>4. Información sobre servicios y presupuestos</h2>
        <p>La información publicada tiene carácter orientativo. Ningún contenido de la web constituye una oferta vinculante: cada encargo profesional se formaliza mediante presupuesto u hoja de encargo específica, con su alcance, honorarios y plazos, y, cuando proceda, visado colegial.</p>

        <h2>5. Propiedad intelectual e industrial</h2>
        <p>Los textos, dibujos, diseño gráfico, logotipo y código de esta web pertenecen a su titular o se usan con autorización. Queda prohibida su reproducción, distribución o transformación sin permiso expreso, salvo para uso personal y privado.</p>

        <h2>6. Responsabilidad</h2>
        <p>El titular procura que la información sea correcta y esté actualizada, pero no garantiza la ausencia de errores ni se responsabiliza de decisiones tomadas únicamente a partir de ella. Tampoco responde del contenido de sitios externos enlazados ni de interrupciones del servicio ajenas a su control.</p>

        <h2>7. Protección de datos y cookies</h2>
        <p>El tratamiento de datos personales se explica en la <a href="privacidad.html">política de privacidad</a> y el uso de cookies en la <a href="cookies.html">política de cookies</a>.</p>

        <h2>8. Legislación aplicable</h2>
        <p>Estas condiciones se rigen por la legislación española. Para cualquier controversia serán competentes los juzgados y tribunales que correspondan conforme a la normativa vigente, y en el caso de consumidores, los de su domicilio.</p>
""", "Aviso legal y condiciones de uso del sitio web del estudio de arquitectura de Enrique Sánchez Polo en Algeciras.")

legal_page("privacidad", "Privacidad", "Política de privacidad", UPDATED, f"""
        <p>Esta política explica cómo se tratan los datos personales que nos facilitas a través de esta web, conforme al Reglamento (UE) 2016/679 (RGPD) y a la Ley Orgánica 3/2018 de Protección de Datos Personales y garantía de los derechos digitales (LOPDGDD).</p>

        <h2>1. Responsable del tratamiento</h2>
        {TITULAR}

        <h2>2. Qué datos tratamos</h2>
        <p>Los que nos facilitas en el formulario de contacto o por email y teléfono: nombre, email, teléfono, tipo de servicio y el contenido de tu mensaje. Si aceptas las cookies analíticas, también datos de navegación anónimos o seudonimizados (ver <a href="cookies.html">política de cookies</a>).</p>

        <h2>3. Para qué los usamos</h2>
        <ul>
          <li>Responder a tus consultas y preparar presupuestos.</li>
          <li>Gestionar, en su caso, el encargo profesional y las obligaciones legales, fiscales y colegiales que conlleva.</li>
          <li>Conocer de forma agregada cómo se usa la web para mejorarla (solo con tu consentimiento).</li>
        </ul>
        <p>No tomamos decisiones automatizadas ni elaboramos perfiles con tus datos.</p>

        <h2>4. Base legal</h2>
        <ul>
          <li><strong>Consentimiento</strong> (art. 6.1.a RGPD) para atender tu consulta y para la analítica web.</li>
          <li><strong>Medidas precontractuales y contrato</strong> (art. 6.1.b RGPD) si solicitas presupuesto o realizas un encargo.</li>
          <li><strong>Obligación legal</strong> (art. 6.1.c RGPD) para conservar la documentación exigida por la normativa fiscal y profesional.</li>
        </ul>

        <h2>5. Cuánto tiempo los conservamos</h2>
        <p>Las consultas que no den lugar a un encargo se conservan como máximo un año. Los datos de encargos se conservan mientras dure la relación profesional y, después, durante los plazos legales de responsabilidad (incluidos los de la Ley de Ordenación de la Edificación) y fiscales.</p>

        <h2>6. Destinatarios</h2>
        <p>No cedemos tus datos a terceros salvo obligación legal (por ejemplo, Administración tributaria, ayuntamientos o colegio profesional cuando el encargo lo requiera). Esta web está alojada en GitHub Pages (GitHub Inc.) y, si aceptas la analítica, usa Google Analytics (Google Ireland Ltd.). Ambos pueden implicar transferencias internacionales amparadas por el Marco de Privacidad de Datos UE-EE. UU. o cláusulas contractuales tipo.</p>

        <h2>7. Tus derechos</h2>
        <p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, así como retirar tu consentimiento en cualquier momento, escribiendo al email indicado arriba e identificándote debidamente. Si consideras que no hemos tratado bien tus datos, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" rel="noopener" target="_blank">aepd.es</a>).</p>

        <h2>8. Seguridad</h2>
        <p>Aplicamos medidas técnicas y organizativas adecuadas para proteger tus datos. La web funciona siempre bajo conexión cifrada (HTTPS).</p>
""", "Política de privacidad del estudio de arquitectura de Enrique Sánchez Polo: qué datos tratamos, para qué y cómo ejercer tus derechos.")

legal_page("cookies", "Cookies", "Política de cookies", UPDATED, f"""
        <p>Una cookie es un pequeño archivo que un sitio web guarda en tu navegador. Esta web solo usa las cookies estrictamente necesarias y, <strong>únicamente si las aceptas</strong>, cookies analíticas.</p>

        <h2>Cookies y almacenamiento que utilizamos</h2>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Nombre</th><th>Titular</th><th>Finalidad</th><th>Duración</th><th>Tipo</th></tr></thead>
            <tbody>
              <tr><td>esp-cookies</td><td>Propia</td><td>Recordar si has aceptado o rechazado las cookies</td><td>12 meses</td><td>Necesaria (almacenamiento local)</td></tr>
              <tr><td>esp-intro</td><td>Propia</td><td>No repetir la animación de entrada durante la visita</td><td>Sesión</td><td>Necesaria (almacenamiento de sesión)</td></tr>
              <tr><td>_ga</td><td>Google</td><td>Distinguir usuarios de forma seudónima para estadísticas</td><td>2 años</td><td>Analítica (solo con consentimiento)</td></tr>
              <tr><td>_ga_&lt;ID&gt;</td><td>Google</td><td>Mantener el estado de la sesión en Google Analytics 4</td><td>2 años</td><td>Analítica (solo con consentimiento)</td></tr>
            </tbody>
          </table>
        </div>

        <h2>Cómo gestionar tu consentimiento</h2>
        <p>Puedes cambiar tu elección en cualquier momento: <button type="button" class="link-btn" data-cookie-settings>abrir preferencias de cookies</button>. También puedes borrar o bloquear las cookies desde la configuración de tu navegador (Chrome, Firefox, Safari o Edge). Rechazar las cookies analíticas no afecta al funcionamiento de la web.</p>

        <h2>Más información</h2>
        <p>Consulta la <a href="privacidad.html">política de privacidad</a> o la información de Google sobre <a href="https://policies.google.com/technologies/cookies?hl=es" rel="noopener" target="_blank">cómo usa las cookies</a>.</p>
""", "Política de cookies del sitio web del estudio de arquitectura de Enrique Sánchez Polo.")

# ---------------- 404 ----------------
page("404", "Página no encontrada · Enrique Sánchez Polo Arquitecto", "La página que buscas no existe o ha cambiado de dirección.", '''
    <section class="notfound">
      <div class="container notfound__inner">
        <svg class="notfound__art drawing" viewBox="0 0 400 260" aria-hidden="true">
          <g class="ink"><path class="draw" d="M30 230h340"/><path class="draw" d="M70 230V120h90v110"/><path class="draw" d="M240 230V90h90v140"/><path class="draw" d="M95 150h40v30H95zM265 120h40v30h-40z"/></g>
          <g class="gold-line"><path class="draw" d="M160 140c30-40 50-40 80-40" stroke-dasharray="6 8"/><path class="draw" d="M190 230v-30h20v30"/></g>
        </svg>
        <p class="eyebrow">Error 404</p>
        <h1 data-split>Esta página <em class="gold">no está en el plano.</em></h1>
        <p class="lead">Puede que el enlace sea antiguo o tenga un error. Te ayudamos a encontrar lo que buscas.</p>
        <div class="hero__cta">
          <a href="index.html" class="btn">Volver al inicio</a>
          <a href="servicios.html" class="link-arrow">Ver servicios <span aria-hidden="true">→</span></a>
          <a href="contacto.html" class="link-arrow">Contactar <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </section>
''', cta=False, base="/Enrique-Sanchez-Polo/", noindex=True, in_sitemap=False)

# ---------------- SITEMAP Y ROBOTS ----------------
import datetime
today = datetime.date.today().isoformat()
urls = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>" for u, pr in PAGES)
(OUT / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
''', encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")

print("ok")
