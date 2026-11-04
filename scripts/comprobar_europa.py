"""Comprueba los datos del mapa por provincias (europa/datos/*.json) antes de cada commit.

Uso: python3 scripts/comprobar_europa.py
Sale con código 1 si hay errores. Los avisos no bloquean.
"""
import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EU = RAIZ / "europa"
TIPOS = {"yihadista", "derecha", "izquierda", "separatista", "otros"}
ESTADOS = {"calificado", "investigacion", "descartado"}
PRECISION = {"exacta", "aproximada", "ciudad", "region", "pais"}
NIVELES = {"control", "influencia", "presencia"}

errores, avisos = [], []


def cargar(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main():
    prov = {f["properties"]["id"]: f["properties"]["pais"] for f in cargar(EU / "geo/provincias.geojson")["features"]}
    grupos = cargar(EU / "datos/grupos.json")["grupos"]
    gid = {g["id"] for g in grupos}
    for g in grupos:
        for z in g["zonas_nuts"]:
            if z["id"] not in prov: errores.append(f"grupo {g['id']}: provincia desconocida {z['id']}")
            if z["nivel"] not in NIVELES: errores.append(f"grupo {g['id']}: nivel no válido")
        if not g["fuentes"]: errores.append(f"grupo {g['id']}: sin fuentes")

    for nombre, clave, extra in [("detenciones.json", "detenciones", ["detenidos", "detenidos_texto", "plan_atentado"]),
                                 ("incidentes.json", "incidentes", ["metodo", "muertos", "heridos", "estado"])]:
        d = cargar(EU / "datos" / nombre)
        desde, hasta = date.fromisoformat(d["periodo"]["desde"]), date.fromisoformat(d["periodo"]["hasta"])
        vistos = set()
        for r in d[clave]:
            ref = f"{clave[:3]} {r['id']}"
            if r["id"] in vistos: errores.append(f"{ref}: id repetido")
            vistos.add(r["id"])
            for c in ["fecha", "lugar", "pais", "lat", "lon", "precision", "tipo", "resumen", "fuente", "nuts3"] + extra:
                if c not in r: errores.append(f"{ref}: falta «{c}»")
            if r.get("tipo") not in TIPOS: errores.append(f"{ref}: tipo no válido")
            if r.get("precision") not in PRECISION: errores.append(f"{ref}: precisión no válida")
            if clave == "incidentes" and r.get("estado") not in ESTADOS: errores.append(f"{ref}: estado no válido")
            f = date.fromisoformat(r["fecha"])
            if not desde <= f <= hasta: errores.append(f"{ref}: fecha fuera del periodo {desde}–{hasta}")
            if not str(r.get("fuente", {}).get("url", "")).startswith("http"): errores.append(f"{ref}: la fuente no tiene URL")
            if "news.google.com" in r["fuente"]["url"]: avisos.append(f"{ref}: la fuente es un enlace de Google News")
            if r.get("grupo") and r["grupo"] not in gid: errores.append(f"{ref}: grupo desconocido «{r['grupo']}»")
            if r["precision"] == "pais":
                if r["nuts3"] is not None: errores.append(f"{ref}: sin lugar publicado pero con provincia")
            elif r["nuts3"] not in prov:
                errores.append(f"{ref}: sin provincia válida")
            elif prov[r["nuts3"]] != r["pais"]:
                avisos.append(f"{ref}: la provincia {r['nuts3']} es de {prov[r['nuts3']]}, no de {r['pais']}")
            for p in r.get("puntos", []):
                if p.get("nuts3") not in prov: errores.append(f"{ref}: punto «{p.get('lugar')}» sin provincia")
        print(f"{len(d[clave])} {clave} ({desde} – {hasta})")

    for a in avisos:
        print("AVISO", a)
    for e in errores:
        print("ERROR", e)
    print(f"{len(grupos)} grupos · {len(errores)} errores, {len(avisos)} avisos")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
