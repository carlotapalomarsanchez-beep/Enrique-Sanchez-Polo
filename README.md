# Enrique Sánchez Polo · Arquitecto (Algeciras)

Web estática del estudio. Abrir `index.html` en el navegador; no necesita instalación.

## Páginas
- `index.html` – Inicio (intro animada, edificio que se construye al hacer scroll, especialidades, método)
- `estudio.html` – Quiénes somos, valores y clientes
- `servicios.html` – Los 12 servicios con pestañas de acceso rápido
- `proyectos.html` – Tipologías de proyecto con filtro
- `contacto.html` – Datos, formulario y zona de actuación

## Archivos
- `styles.css` – diseño (blanco/gris claro, dorado, gris y negro) y efectos
- `script.js` – intro, transiciones entre páginas, animaciones de scroll, cursor, filtro y formulario
- `tools/build.py` – genera las 5 páginas con la misma cabecera y pie:
  `python3 tools/build.py .`
  (si editas el contenido, hazlo en este archivo y vuelve a ejecutarlo)

## Datos pendientes de confirmar
Buscar `por confirmar` en `tools/build.py`:
- Dirección del estudio, teléfono y email (también `EMAIL_ESTUDIO` en `script.js`)
- Número de colegiado (COA Cádiz) y horario
- Fotos reales de proyectos (ahora hay dibujos de línea)
