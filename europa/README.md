# Beta: terrorismo en Europa por provincias

Mapa paralelo, más preciso, solo de Europa. Sin enlazar desde la web principal: https://hraesverlg104.github.io/mapa-terrorismo-europa/europa/

## Qué muestra

- **Mapa de calor por provincia** (NUTS-3): número de casos en cada provincia, con filtro de periodo (30 días, 90 días, 5 meses, 12 meses), de tipo TE-SAT y de qué se cuenta (detenciones, incidentes o ambos).
- **Detenciones de los últimos 12 meses** y **incidentes de los últimos cinco**, como puntos con su ficha y su fuente. Sin nombres de detenidos.
- **Zonas de los grupos**: al abrir un grupo, en relleno liso las provincias con detenciones atribuidas a él en el periodo; en rayas, su zona de referencia según las fuentes del grupo.
- **Ficha de provincia**: cifras, tipos, grupos con casos atribuidos y lista de casos.

## Ficheros

- `index.html`: la página (Leaflet, sin compilación).
- `datos/detenciones.json`, `datos/incidentes.json`, `datos/grupos.json`: generados; no se editan a mano.
- `geo/provincias.geojson`: 1.440 provincias (NUTS-3 de Eurostat 2021; Bosnia y Herzegovina y Kosovo con geoBoundaries).
- `herramientas/detenciones_previas.json`: detenciones del 3-11-2025 al 1-6-2026, que no están en la beta.
- `herramientas/construir_datos.py`: une las detenciones de la beta y las previas, toma los incidentes y los grupos de Europa de la beta y asigna a cada caso su provincia.
- `herramientas/construir_provincias.py`: cómo se generó `geo/provincias.geojson`.
- `../scripts/comprobar_europa.py`: valida los datos. Ejecútalo antes de cada commit.

Para actualizar: edita los datos de la beta (o `detenciones_previas.json`), ejecuta `python3 europa/herramientas/construir_datos.py` y después `python3 scripts/comprobar_europa.py`.

## Criterios

- Cada caso cuenta una vez en cada provincia donde hubo detenciones (campo `puntos` para las operaciones en varias ciudades).
- Los casos sin lugar publicado (`"precision": "pais"`) salen en las listas, pero no en el mapa ni en el recuento por provincia.
- Las detenciones por mostrar apoyo a Palestine Action (`"apoyo_proscrita": true`) se pueden ocultar desde el panel.
- Sin nombres de detenidos. Nada sobre menores salvo que existen. Líderes solo si son públicos, sancionados o condenados.
- No se marcan edificios ni comunidades como «centros de terrorismo».
