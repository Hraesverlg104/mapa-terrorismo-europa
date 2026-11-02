# Beta: terrorismo y conflicto armado en Europa y África

Versión en pruebas, sin enlazar desde la web principal: https://hraesverlg104.github.io/mapa-terrorismo-europa/beta/

## Qué muestra

- **Europa** (UE, Reino Unido, EFTA y Balcanes occidentales): incidentes terroristas de los últimos cinco meses con taxonomía TE-SAT y estado, y detenciones publicadas en investigaciones antiterroristas. Sin nombres de detenidos.
- **Grupos**: células, redes y grupos que operan en Europa y actores armados de África (yihadistas, rebeldes, milicias, ejércitos, empresas militares privadas y misiones), con zonas de control, influencia o presencia, bastiones, líderes públicos y fuentes.
- **África**: eventos de importancia alta o muy alta de los últimos cinco meses, y bases y despliegues activos entre julio de 2025 y noviembre de 2026.

## Ficheros

- `index.html`: la página (Leaflet, sin compilación).
- `datos/europa_incidentes.json`: incidentes (mismo formato que `../incidentes.json`).
- `datos/europa_detenciones.json`: operaciones con detenidos.
- `datos/africa_eventos.json`: eventos en África.
- `datos/grupos.json`: grupos de Europa y África.
- `datos/bases.json`: bases y despliegues.
- `geo/africa_regiones.geojson`: regiones de primer nivel de África (geoBoundaries y Natural Earth). Las regiones europeas se leen de `../regiones.geojson`.
- `herramientas/geo_base.py`: cómo se generaron las regiones africanas.
- `../scripts/comprobar_beta.py`: valida todos los datos. Ejecútalo antes de cada commit.

## Formatos

**Detención**

```json
{"id": "2026-10-17-irun", "fecha": "2026-10-17", "lugar": "Irún", "pais": "España",
 "lat": 43.338, "lon": -1.789, "precision": "ciudad",
 "tipo": "separatista", "subetiqueta": "disidencia de la izquierda abertzale",
 "detenidos": 2, "detenidos_texto": "2 detenidos", "plan_atentado": true,
 "objetivo": "…", "grupo": "jardun", "resumen": "…",
 "fuente": {"titulo": "…", "url": "https://…"}}
```

**Evento en África**: `categoria` es `terrorismo`, `accion-militar`, `golpe`, `rebelion`, `secuestro` o `mediatico`; `importancia` es `muy-alta` o `alta`; `actores` son ids de `grupos.json`; `fecha_fin` es opcional.

**Grupo**: `categoria` es `yihadista`, `rebelde`, `separatista`, `milicia`, `criminal`, `fuerza-estatal`, `pmc`, `mision`, `extrema-derecha`, `extrema-izquierda`, `nihilista`, `red-estatal` u `otros`. Cada zona es `{"pais", "region", "nivel"}`, con `nivel` = `control`, `influencia` o `presencia`; en Europa `"region": "*"` significa todo el país. Los nombres de región deben existir en el GeoJSON correspondiente.

**Base**: `tipo` es `extranjera`, `despliegue`, `mision` o `clave` (base nacional clave en una zona de guerra).

## Criterios

- Importancia muy alta en África: 50 muertos o más, ataques a capitales o infraestructuras estratégicas, golpes, asesinatos de altos cargos, secuestros o liberaciones de occidentales o asiáticos, tomas de ciudades importantes y choques entre Estados. Alta: entre 15 y 49 muertos, ataques importantes a bases, secuestros masivos, grandes operaciones y atentados terroristas con al menos 10 muertos. Quedan fuera los choques comunitarios y la delincuencia común.
- Detenciones: se excluyen los casos de mera apología tramitados como delito común.
- Líderes: solo los públicos, sancionados o condenados. Nada sobre menores salvo que existen.
- Las zonas son aproximadas, por regiones administrativas.
