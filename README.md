# Incidentes terroristas en Europa

Mapa de ataques e incidentes terroristas en Europa de los últimos seis meses, clasificados con la taxonomía TE-SAT de Europol.

Web: https://hraesverlg104.github.io/mapa-terrorismo-europa/

## Ficheros

- `index.html`: la página (Leaflet, sin compilación).
- `incidentes.json`: los datos. Es el único fichero que cambia con las actualizaciones.
- `regiones.geojson`: divisiones administrativas de cada país (comunidades autónomas, régions, Länder, regioni, voivodatos, cantones…), de Natural Earth. La página asigna cada caso a su región por sus coordenadas.
- `europa.geojson`: fronteras de respaldo si el mapa base no carga.
- `scripts/comprobar_datos.py`: valida `incidentes.json`. Ejecútalo antes de cada commit.

## Ámbito

- **Países:** Unión Europea, Reino Unido, EFTA (Noruega, Suiza, Islandia, Liechtenstein) y Balcanes occidentales. Fuera Ucrania, Rusia y Turquía.
- **Periodo:** los últimos seis meses.
- **Casos:** ataques consumados y tentativas (artefactos colocados que no estallan, intentos frustrados en el lugar). No entran los planes desarticulados antes de ejecutarse ni las detenciones preventivas.
- **Series:** una campaña de varios ataques va punto por punto cuando se conoce cada ubicación, con el campo `serie` para agruparlos.
- **Sabotaje estatal:** entra como tipo `otros` con subetiqueta «patrocinio estatal (país)» o «patrocinio estatal (sospecha)».

## Criterios

**Tipo (TE-SAT):** `yihadista`, `derecha` (extrema derecha), `izquierda` (extrema izquierda y anarquista), `separatista` (etnonacionalista y separatista), `otros` (otros o no especificado). Ecoterrorismo, extremismo nihilista, patrocinio estatal, etc. van en `subetiqueta`. En los descartados, el tipo es la hipótesis que se llegó a considerar.

**Estado:**
- `calificado`: la fiscalía o la policía antiterrorista lo investiga formalmente como terrorismo, o las autoridades lo han declarado atentado terrorista.
- `investigacion`: se estudia un posible móvil terrorista, extremista o de sabotaje, sin calificación formal.
- `descartado`: se consideró terrorismo y las autoridades lo descartaron.

**Precisión de la ubicación:** `exacta`, `aproximada` (calle o barrio), `ciudad` o `region` (no se ha publicado el lugar).

Muertos y heridos no incluyen al autor. Cada incidente lleva una fuente enlazada.

## Formato de un incidente

```json
{
  "id": "2026-10-23-trappes",
  "fecha": "2026-10-23",
  "lugar": "Trappes y La Verrière",
  "pais": "Francia",
  "lat": 48.7765, "lon": 2.0026, "precision": "aproximada",
  "tipo": "derecha", "subetiqueta": "racista",
  "metodo": "Tiroteo desde un coche",
  "muertos": 1, "heridos": 4,
  "estado": "calificado",
  "resumen": "Dos o tres frases en español, con palabras propias.",
  "fuente": {"titulo": "Medio: titular resumido", "url": "https://..."},
  "serie": "opcional: nombre de la campaña"
}
```
