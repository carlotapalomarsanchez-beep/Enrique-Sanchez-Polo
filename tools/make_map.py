"""Genera el mapa de puntos de Andalucía y la ampliación del Campo de Gibraltar.

Uso:  python3 tools/make_map.py <spain-provinces.geojson> tools/map_fragment.html
El GeoJSON de provincias se descarga de:
https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain-provinces.geojson
"""
import json, math, sys

SRC, DEST = sys.argv[1], sys.argv[2]
ANDALUCIA = ["Huelva", "Sevilla", "Córdoba", "Jaén", "Cádiz", "Málaga", "Granada", "Almería"]

TOWNS = [  # nombre, lon, lat, posición de la etiqueta (r = derecha, l = izquierda)
    ("Algeciras", -5.4562, 36.1408, "l", True),
    ("La Línea de la Concepción", -5.3478, 36.1681, "r", False),
    ("San Roque", -5.3842, 36.2106, "r", False),
    ("Los Barrios", -5.4920, 36.1847, "l", False),
    ("Tarifa", -5.6044, 36.0143, "l", False),
    ("Jimena de la Frontera", -5.4532, 36.4357, "r", False),
    ("Castellar de la Frontera", -5.4544, 36.3183, "r", False),
    ("Sotogrande", -5.2797, 36.2867, "r", False),
]
SHORT = {"La Línea de la Concepción": "La Línea"}  # nombre corto en el mapa
GIBRALTAR = [(-5.3575, 36.1555), (-5.3390, 36.1555), (-5.3380, 36.1200), (-5.3437, 36.1090), (-5.3560, 36.1250)]

feats = {f["properties"]["name"]: f["geometry"] for f in json.load(open(SRC, encoding="utf-8"))["features"]}

def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        yield poly[0]  # solo el contorno exterior

def dp(pts, tol):
    """Simplificación Douglas-Peucker."""
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1e-9
    i, dmax = 0, 0
    for k in range(1, len(pts) - 1):
        d = abs(dy * pts[k][0] - dx * pts[k][1] + x2 * y1 - y2 * x1) / n
        if d > dmax:
            i, dmax = k, d
    if dmax > tol:
        return dp(pts[: i + 1], tol)[:-1] + dp(pts[i:], tol)
    return [pts[0], pts[-1]]

class Proj:
    def __init__(self, lon0, lon1, lat0, lat1, width, pad):
        self.c = math.cos(math.radians((lat0 + lat1) / 2))
        self.lon0, self.lat1, self.pad = lon0, lat1, pad
        self.k = (width - 2 * pad) / ((lon1 - lon0) * self.c)
        self.w = width
        self.h = (lat1 - lat0) * self.k + 2 * pad
    def __call__(self, lon, lat):
        return ((lon - self.lon0) * self.c * self.k + self.pad, (self.lat1 - lat) * self.k + self.pad)

def path(geom, P, tol, minarea=0):
    out = []
    for ring in rings(geom):
        raw = [P(*p) for p in ring]
        mid = len(raw) // 2  # anillo cerrado: se simplifica en dos mitades
        pts = dp(raw[: mid + 1], tol)[:-1] + dp(raw[mid:], tol)
        if len(pts) < 4:
            continue
        area = abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))) / 2
        if area < minarea:
            continue
        out.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
    return "".join(out)

def centroid(geom, P):
    ring = max(rings(geom), key=len)
    xs, ys = zip(*[P(*p) for p in ring])
    return sum(xs) / len(xs), sum(ys) / len(ys)

# ---------- Mapa general de Andalucía ----------
M = Proj(-7.62, -1.55, 35.95, 38.78, 1000, 24)
prov_paths = []
labels = []
for name in ANDALUCIA:
    g = feats[name]
    cls = "prov prov--cadiz" if name == "Cádiz" else "prov"
    prov_paths.append(f'<path class="{cls}" d="{path(g, M, 0.7, 4)}"/>')
    cx, cy = centroid(g, M)
    adj = {"Cádiz": (-10, -40), "Huelva": (0, -20), "Málaga": (10, -8), "Almería": (10, 0), "Granada": (0, -10)}.get(name, (0, 0))
    labels.append(f'<text class="map__prov" x="{cx + adj[0]:.0f}" y="{cy + adj[1]:.0f}">{name}</text>')

cadiz = feats["Cádiz"]
ax, ay = M(-5.4562, 36.1408)
cgx, cgy = M(-5.43, 36.24)
fx0, fy0 = M(-5.9, 36.55)
fx1, fy1 = M(-5.0, 35.95)

main_svg = f'''<svg class="map map--main" viewBox="0 0 {M.w:.0f} {M.h:.0f}" role="img" aria-labelledby="map-title">
  <title id="map-title">Mapa de Andalucía: el estudio trabaja desde Algeciras en todo el Campo de Gibraltar</title>
  <defs>
    <pattern id="dots-a" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="1.9" class="dot dot--base"/></pattern>
    <pattern id="dots-c" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="1.9" class="dot dot--cadiz"/></pattern>
    <pattern id="dots-g" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="2.2" class="dot dot--gold"/></pattern>
    <clipPath id="clip-cg"><circle cx="{cgx:.1f}" cy="{cgy:.1f}" r="58"/></clipPath>
  </defs>
  <g class="map__land">{"".join(prov_paths)}</g>
  <path class="prov prov--gold" clip-path="url(#clip-cg)" d="{path(cadiz, M, 0.7, 4)}"/>
  <g class="map__labels">{"".join(labels)}</g>
  <text class="map__sea" x="{M(-7.25, 36.45)[0]:.0f}" y="{M(-7.25, 36.45)[1]:.0f}">Océano Atlántico</text>
  <text class="map__sea" x="{M(-3.3, 36.25)[0]:.0f}" y="{M(-3.3, 36.25)[1]:.0f}">Mar Mediterráneo</text>
  <rect class="map__frame" x="{fx0:.1f}" y="{fy0:.1f}" width="{fx1 - fx0:.1f}" height="{fy1 - fy0:.1f}"/>
  <text class="map__frame-label" x="{fx1 + 10:.0f}" y="{fy0 + 4:.0f}">Campo de Gibraltar</text>
  <g class="map__hq">
    <circle class="map__pulse" cx="{ax:.1f}" cy="{ay:.1f}" r="7"/>
    <circle class="map__pin" cx="{ax:.1f}" cy="{ay:.1f}" r="5.5"/>
  </g>
</svg>'''

# ---------- Ampliación: Campo de Gibraltar ----------
Z = Proj(-5.92, -5.02, 35.93, 36.56, 560, 0)
zp = []
for name in ("Cádiz", "Málaga"):
    zp.append(f'<path class="prov{" prov--cadiz" if name == "Cádiz" else ""}" d="{path(feats[name], Z, 0.5, 2)}"/>')
gib = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (Z(*p) for p in GIBRALTAR)) + "Z"
pins = []
for i, (name, lon, lat, side, hq) in enumerate(TOWNS):
    x, y = Z(lon, lat)
    tx = x + (12 if side == "r" else -12)
    anchor = "start" if side == "r" else "end"
    dy = 16 if name == "Algeciras" else 4
    slug = name.lower().replace(" ", "-").replace("í", "i").replace("ó", "o")
    pins.append(f'''<g class="town{" town--hq" if hq else ""}" data-town="{slug}" style="--d:{i * 90}ms">
      {'<circle class="map__pulse" cx="%.1f" cy="%.1f" r="7"/>' % (x, y) if hq else ''}<circle class="town__dot" cx="{x:.1f}" cy="{y:.1f}" r="{6 if hq else 4.5}"/>
      <text x="{tx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}">{SHORT.get(name, name)}</text>
    </g>''')

zoom_svg = f'''<svg class="map map--zoom" viewBox="0 0 {Z.w:.0f} {Z.h:.0f}" role="img" aria-labelledby="zoom-title">
  <title id="zoom-title">Detalle del Campo de Gibraltar con los municipios donde trabaja el estudio</title>
  <defs>
    <pattern id="dots-z" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="1.6" class="dot dot--base"/></pattern>
    <pattern id="dots-zc" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="1.6" class="dot dot--cadiz"/></pattern>
    <pattern id="dots-zg" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="1.4" class="dot dot--gib"/></pattern>
  </defs>
  <g class="map__land map__land--zoom">{"".join(zp)}</g>
  <path class="gib" d="{gib}"/>
  <text class="map__sea map__sea--small" x="{Z(-5.37, 36.085)[0]:.0f}" y="{Z(-5.37, 36.085)[1]:.0f}" text-anchor="middle">Gibraltar</text>
  <text class="map__sea" x="{Z(-5.62, 35.955)[0]:.0f}" y="{Z(-5.62, 35.955)[1]:.0f}" text-anchor="middle">Estrecho de Gibraltar</text>
  <text class="map__sea" x="{Z(-5.17, 36.13)[0]:.0f}" y="{Z(-5.17, 36.13)[1]:.0f}" text-anchor="middle">Mar Mediterráneo</text>
  {"".join(pins)}
</svg>'''

open(DEST, "w", encoding="utf-8").write(main_svg + "\n<!--ZOOM-->\n" + zoom_svg)
print("mapa:", M.w, round(M.h), "| zoom:", Z.w, round(Z.h), "| bytes:", len(main_svg) + len(zoom_svg))
