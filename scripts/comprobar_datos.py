"""Comprueba incidentes.json antes de cada commit.

Uso: python3 scripts/comprobar_datos.py
Sale con código 1 si hay errores. Los avisos no bloquean.
"""
import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TIPOS = {"yihadista", "derecha", "izquierda", "separatista", "otros"}
ESTADOS = {"calificado", "investigacion", "descartado"}
PRECISION = {"exacta", "aproximada", "ciudad", "region"}
CAMPOS = ["id", "fecha", "lugar", "pais", "lat", "lon", "precision", "tipo", "subetiqueta",
          "metodo", "muertos", "heridos", "estado", "resumen", "fuente"]


def en_anillo(x, y, r):
    dentro = False
    j = len(r) - 1
    for i in range(len(r)):
        xi, yi = r[i]
        xj, yj = r[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            dentro = not dentro
        j = i
    return dentro


def en_geom(x, y, g):
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    return any(en_anillo(x, y, p[0]) and not any(en_anillo(x, y, h) for h in p[1:]) for p in polys)


def main():
    datos = json.loads((RAIZ / "incidentes.json").read_text(encoding="utf-8"))
    regiones = json.loads((RAIZ / "regiones.geojson").read_text(encoding="utf-8"))["features"]
    errores, avisos, vistos = [], [], set()
    hoy = date.fromisoformat(datos["actualizado"])
    for n, i in enumerate(datos["incidentes"]):
        ref = i.get("id", f"#{n}")
        for c in CAMPOS:
            if c not in i:
                errores.append(f"{ref}: falta el campo «{c}»")
        if ref in vistos:
            errores.append(f"{ref}: id repetido")
        vistos.add(ref)
        if i.get("tipo") not in TIPOS:
            errores.append(f"{ref}: tipo no válido «{i.get('tipo')}»")
        if i.get("estado") not in ESTADOS:
            errores.append(f"{ref}: estado no válido «{i.get('estado')}»")
        if i.get("precision") not in PRECISION:
            errores.append(f"{ref}: precisión no válida «{i.get('precision')}»")
        try:
            f = date.fromisoformat(i["fecha"])
            if f > hoy:
                errores.append(f"{ref}: fecha posterior a «actualizado»")
            if (hoy - f).days > 186:
                avisos.append(f"{ref}: tiene más de seis meses; el mapa solo muestra el último semestre")
        except Exception:
            errores.append(f"{ref}: fecha no válida")
        if not (25 <= i.get("lat", 0) <= 75 and -45 <= i.get("lon", 0) <= 60):
            errores.append(f"{ref}: coordenadas fuera de Europa")
        elif not any(en_geom(i["lon"], i["lat"], r["geometry"]) for r in regiones):
            avisos.append(f"{ref}: no cae en ninguna región; se mostrará suelto")
        fu = i.get("fuente") or {}
        if not str(fu.get("url", "")).startswith("http"):
            errores.append(f"{ref}: la fuente no tiene URL")
    for a in avisos:
        print("AVISO", a)
    for e in errores:
        print("ERROR", e)
    print(f"{len(datos['incidentes'])} incidentes, {len(errores)} errores, {len(avisos)} avisos")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
