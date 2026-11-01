# Enrique Sánchez Polo · Arquitecto (Algeciras)

Web estática del estudio. Abrir `index.html` en el navegador; no necesita instalación.

**Web publicada (GitHub Pages):** https://carlotapalomarsanchez-beep.github.io/Enrique-Sanchez-Polo/

## Activar GitHub Pages (una sola vez)
1. En GitHub: **Settings → Pages**.
2. En *Build and deployment* → *Source*: **Deploy from a branch**.
3. Elegir la rama `claude/beautiful-hopper-ncgtac` (o `main` si se fusiona) y la carpeta **/ (root)** → **Save**.
4. Cuando aparezca la dirección, marcar **Enforce HTTPS**.

## Páginas
- `index.html` – Inicio: edificio 3D que gira y se construye al bajar, especialidades, método, clientes
- `estudio.html`, `servicios.html`, `proyectos.html`, `contacto.html`
- `aviso-legal.html` (aviso legal y condiciones de uso), `privacidad.html`, `cookies.html`
- `404.html` – página de error

## Archivos
- `styles.css` – diseño y efectos · `script.js` – animaciones, modelo 3D, formulario, cookies y Analytics
- `tools/build.py` – genera todas las páginas (`python3 tools/build.py .`). **Los textos se editan aquí.**
- `tools/check_links.py` – revisa enlaces rotos e imágenes sin texto alternativo (`python3 tools/check_links.py .`)
- `sitemap.xml`, `robots.txt`, `site.webmanifest`, favicons, `og-image.png` (vista previa al compartir)

## Lista de comprobación
| # | Punto | Estado |
|---|---|---|
| 1 | Política de privacidad | `privacidad.html` (RGPD/LOPDGDD) |
| 2 | Términos y condiciones | `aviso-legal.html` (LSSI-CE + condiciones de uso) |
| 3 | API y secretos | No hay claves en el código. `.gitignore` excluye `.env`. El ID de GA4 es público |
| 4 | Forzar HTTPS | Redirección en cada página + `upgrade-insecure-requests` + *Enforce HTTPS* en Pages |
| 5 | Banner de cookies | Aceptar/Rechazar; Analytics solo se carga tras aceptar; "Preferencias de cookies" en el pie |
| 6 | Metadescripciones | Una propia en cada página + URL canónica |
| 7 | Vista previa del enlace | Open Graph y Twitter Card con `og-image.png` (1200×630) |
| 8 | Favicon | SVG, PNG 32, Apple 180, iconos 192/512 y manifest |
| 9 | Sitemap y robots.txt | Generados por `tools/build.py` |
| 10 | Texto alternativo | Dibujos decorativos ocultos a lectores de pantalla; comprobado con `check_links.py` |
| 11 | Imágenes comprimidas | PNG optimizados (la imagen social pesa 22 KB); el resto son dibujos vectoriales |
| 12 | Velocidad de carga | Sin imágenes pesadas, JS con `defer`, fuentes con `display=swap` |
| 13 | Contraste de color | Dorado de textos `#8a6a35` (5:1) y gris `#6b6b6b` (5,3:1), cumplen WCAG AA |
| 14 | Web en móvil | Diseño adaptado, menú móvil y botón fijo de presupuesto |
| 15 | Página 404 | `404.html` |
| 16 | Enlaces rotos | `tools/check_links.py` → 0 problemas |
| 17 | Validar formularios | Mensajes de error por campo, accesibles |
| 18 | Antispam | Campo trampa, tiempo mínimo, límite de envíos y email protegido contra robots |
| 19 | Google Analytics 4 | Preparado: poner el ID en `GA_ID` al principio de `script.js` |
| 20 | CTA claro | "Pedir presupuesto" en menú, portada, final de cada página y botón fijo en móvil |

## Datos pendientes de confirmar
Buscar `por confirmar` en `tools/build.py`: dirección, teléfono, email (`data-u`/`data-d`), NIF, nº de colegiado.
Y el ID de Google Analytics (`GA_ID` en `script.js`).
