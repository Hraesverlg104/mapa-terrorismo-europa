"""Comprueba los datos de la beta (beta/datos/*.json) antes de cada commit.

Uso: python3 scripts/comprobar_beta.py
Sale con código 1 si hay errores. Los avisos no bloquean.
"""
import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "beta" / "datos"
TIPOS = {"yihadista", "derecha", "izquierda", "separatista", "otros"}
ESTADOS = {"calificado", "investigacion", "descartado"}
PRECISION = {"exacta", "aproximada", "ciudad", "region"}
CATS = {"terrorismo", "accion-militar", "golpe", "rebelion", "secuestro", "mediatico"}
IMPS = {"muy-alta", "alta"}
GCATS = {"yihadista", "rebelde", "separatista", "milicia", "criminal", "fuerza-estatal", "pmc", "mision",
         "extrema-derecha", "extrema-izquierda", "nihilista", "red-estatal", "otros"}
NIVELES = {"control", "influencia", "presencia"}
BTIPOS = {"extranjera", "despliegue", "mision", "clave"}

errores, avisos = [], []


def cargar(nombre):
    return json.loads((DATOS / nombre).read_text(encoding="utf-8"))


def fecha_ok(ref, f, desde, hasta):
    try:
        d = date.fromisoformat(f)
    except Exception:
        errores.append(f"{ref}: fecha no válida «{f}»")
        return
    if d > hasta:
        errores.append(f"{ref}: fecha posterior a la actualización")
    if d < desde:
        avisos.append(f"{ref}: fuera del periodo (anterior a {desde})")


def url_ok(ref, f):
    if not (isinstance(f, dict) and str(f.get("url", "")).startswith("http")):
        errores.append(f"{ref}: la fuente no tiene URL")


def coords_ok(ref, lat, lon, caja):
    if not (caja[0] <= lat <= caja[1] and caja[2] <= lon <= caja[3]):
        errores.append(f"{ref}: coordenadas fuera del ámbito ({lat}, {lon})")


def ids_unicos(nombre, lista):
    vistos = set()
    for x in lista:
        if x["id"] in vistos:
            errores.append(f"{nombre}: id repetido {x['id']}")
        vistos.add(x["id"])


def main():
    grupos = cargar("grupos.json")["grupos"]
    gid = {g["id"] for g in grupos}
    reg_eu = {(f["properties"]["pais"], f["properties"]["nombre"]) for f in json.loads((RAIZ / "regiones.geojson").read_text())["features"]}
    reg_af = {(f["properties"]["pais"], f["properties"]["nombre"]) for f in json.loads((RAIZ / "beta/geo/africa_regiones.geojson").read_text())["features"]}
    paises = {p for p, _ in reg_eu | reg_af}

    inc = cargar("europa_incidentes.json")
    hasta = date.fromisoformat(inc["actualizado"])
    desde = date.fromisoformat(inc["periodo"]["desde"])
    ids_unicos("incidentes", inc["incidentes"])
    for i in inc["incidentes"]:
        ref = "inc " + i["id"]
        for c in ["fecha", "lugar", "pais", "lat", "lon", "precision", "tipo", "subetiqueta", "metodo", "muertos", "heridos", "estado", "resumen", "fuente"]:
            if c not in i:
                errores.append(f"{ref}: falta «{c}»")
        if i.get("tipo") not in TIPOS: errores.append(f"{ref}: tipo no válido")
        if i.get("estado") not in ESTADOS: errores.append(f"{ref}: estado no válido")
        if i.get("precision") not in PRECISION: errores.append(f"{ref}: precisión no válida")
        fecha_ok(ref, i["fecha"], desde, hasta)
        coords_ok(ref, i["lat"], i["lon"], (25, 75, -45, 60))
        url_ok(ref, i.get("fuente"))

    det = cargar("europa_detenciones.json")
    ids_unicos("detenciones", det["detenciones"])
    for i in det["detenciones"]:
        ref = "det " + i["id"]
        for c in ["fecha", "lugar", "pais", "lat", "lon", "precision", "tipo", "detenidos", "detenidos_texto", "plan_atentado", "resumen", "fuente"]:
            if c not in i:
                errores.append(f"{ref}: falta «{c}»")
        if i.get("tipo") not in TIPOS: errores.append(f"{ref}: tipo no válido")
        if i.get("precision") not in PRECISION: errores.append(f"{ref}: precisión no válida")
        if i.get("grupo") and i["grupo"] not in gid: errores.append(f"{ref}: grupo desconocido «{i['grupo']}»")
        fecha_ok(ref, i["fecha"], desde, hasta)
        coords_ok(ref, i["lat"], i["lon"], (25, 75, -45, 60))
        url_ok(ref, i.get("fuente"))
        if "news.google.com" in str(i.get("fuente", {}).get("url", "")):
            avisos.append(f"{ref}: la fuente es un enlace de Google News; mejor la URL del medio")

    af = cargar("africa_eventos.json")
    ids_unicos("eventos", af["eventos"])
    desde_af = date.fromisoformat(af["periodo"]["desde"])
    for i in af["eventos"]:
        ref = "af " + i["id"]
        for c in ["fecha", "lugar", "pais", "lat", "lon", "precision", "categoria", "importancia", "actores", "autor", "balance", "resumen", "fuente"]:
            if c not in i:
                errores.append(f"{ref}: falta «{c}»")
        if i.get("categoria") not in CATS: errores.append(f"{ref}: categoría no válida")
        if i.get("importancia") not in IMPS: errores.append(f"{ref}: importancia no válida")
        if i.get("precision") not in PRECISION: errores.append(f"{ref}: precisión no válida")
        for a in i.get("actores", []):
            if a not in gid: errores.append(f"{ref}: actor desconocido «{a}»")
        fecha_ok(ref, i["fecha"], desde_af, hasta)
        coords_ok(ref, i["lat"], i["lon"], (-36, 38, -26, 60))
        url_ok(ref, i.get("fuente"))

    for g in grupos:
        ref = "grupo " + g["id"]
        if g.get("categoria") not in GCATS: errores.append(f"{ref}: categoría no válida")
        if g.get("ambito") not in {"europa", "africa"}: errores.append(f"{ref}: ámbito no válido")
        regs = reg_eu if g["ambito"] == "europa" else reg_af
        for z in g["zonas"]:
            if z["nivel"] not in NIVELES: errores.append(f"{ref}: nivel no válido")
            if z["region"] == "*":
                if z["pais"] not in paises: errores.append(f"{ref}: país desconocido «{z['pais']}»")
            elif (z["pais"], z["region"]) not in regs:
                errores.append(f"{ref}: la región «{z['region']}» ({z['pais']}) no existe")
        for x in g["aliados"] + g["enemigos"]:
            if x not in gid: errores.append(f"{ref}: referencia desconocida «{x}»")
        if not g["fuentes"]: errores.append(f"{ref}: sin fuentes")
        for f in g["fuentes"]: url_ok(ref, f)

    bases = cargar("bases.json")["bases"]
    ids_unicos("bases", bases)
    for b in bases:
        ref = "base " + b["id"]
        if b.get("tipo") not in BTIPOS: errores.append(f"{ref}: tipo no válido")
        if b.get("operador_id") and b["operador_id"] not in gid: errores.append(f"{ref}: operador desconocido")
        coords_ok(ref, b["lat"], b["lon"], (-36, 38, -26, 60))
        url_ok(ref, b.get("fuente"))

    for a in avisos:
        print("AVISO", a)
    for e in errores:
        print("ERROR", e)
    print(f"{len(inc['incidentes'])} incidentes, {len(det['detenciones'])} detenciones, {len(af['eventos'])} eventos, "
          f"{len(grupos)} grupos, {len(bases)} bases · {len(errores)} errores, {len(avisos)} avisos")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
