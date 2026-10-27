# Incidentes terroristas en Europa

Mapa de puntos de ataques e incidentes terroristas en Europa, clasificados con la taxonomía TE-SAT de Europol.

- `index.html`: la página (Leaflet, sin compilación).
- `incidentes.json`: los datos. Es el único fichero que cambia con las actualizaciones.
- `europa.geojson`: fronteras de respaldo si el mapa base no carga.

## Criterios

**Tipo (TE-SAT):** `yihadista`, `derecha`, `izquierda` (extrema izquierda y anarquista), `separatista` (etnonacionalista y separatista), `otros` (otros o no especificado). Ecoterrorismo, patrocinio estatal, etc. van en `subetiqueta`.

**Estado:**
- `calificado`: la fiscalía o la policía antiterrorista lo investiga formalmente como terrorismo, o las autoridades lo han declarado atentado terrorista.
- `investigacion`: se estudia un posible móvil terrorista sin calificación formal confirmada.
- `descartado`: las autoridades han descartado el terrorismo.

Muertos y heridos no incluyen al autor. Cada incidente lleva una fuente enlazada.
