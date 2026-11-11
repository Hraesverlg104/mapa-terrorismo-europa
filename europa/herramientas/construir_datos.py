"""Genera europa/datos/*.json a partir de los datos de la beta.

- Detenciones: 12 meses (las de la beta más las anteriores, en herramientas/detenciones_previas.json).
- Incidentes: 5 meses, los de la beta.
- Grupos: los de ámbito europeo, con su zona de referencia pasada a provincias (NUTS-3).

A cada registro se le asigna la provincia NUTS-3 que contiene sus coordenadas.
Los registros sin lugar publicado (precisión «pais») no se asignan a ninguna provincia.

Uso: python3 europa/herramientas/construir_datos.py [ruta de otro fichero de detenciones previas]
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from shapely.geometry import shape, Point
from shapely.strtree import STRtree

RAIZ = Path(__file__).resolve().parents[2]
EU = RAIZ / "europa"
BETA = RAIZ / "beta" / "datos"


def cargar(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


prov = cargar(EU / "geo" / "provincias.geojson")["features"]
formas = [shape(f["geometry"]) for f in prov]
arbol = STRtree(formas)
PROV_PAIS = {f["properties"]["id"]: f["properties"]["pais"] for f in prov}


def nuts(lat, lon, pais=None):
    pt = Point(lon, lat)
    for i in arbol.query(pt):
        if formas[i].contains(pt):
            return prov[i]["properties"]["id"]
    # puntos en la costa o en el borde: la provincia más cercana del mismo país (máx. ~25 km)
    i = arbol.nearest(pt)
    cand = [j for j in arbol.query(pt.buffer(0.25)) if not pais or prov[j]["properties"]["pais"] == pais]
    if cand:
        j = min(cand, key=lambda j: formas[j].distance(pt))
        return prov[j]["properties"]["id"]
    return None


avisos = []


def asignar(r):
    if "no publicado" in r["lugar"] or r["lugar"] == r["pais"]:
        r["precision"] = "pais"
    if r["precision"] == "pais":
        r["nuts3"] = None
    else:
        r["nuts3"] = nuts(r["lat"], r["lon"], r["pais"])
        if r["nuts3"] is None:
            avisos.append(f"{r['id']}: sin provincia ({r['lat']}, {r['lon']})")
        elif PROV_PAIS[r["nuts3"]] != r["pais"]:
            avisos.append(f"{r['id']}: provincia {r['nuts3']} de {PROV_PAIS[r['nuts3']]}, no de {r['pais']}")
    for p in r.get("puntos", []):
        p["nuts3"] = nuts(p["lat"], p["lon"], r["pais"])
    return r


def main():
    previas = cargar(sys.argv[1] if len(sys.argv) > 1 else EU / "herramientas" / "detenciones_previas.json")
    det_b = cargar(BETA / "europa_detenciones.json")
    hasta = det_b["periodo"]["hasta"]
    h = date.fromisoformat(hasta)
    desde = (h.replace(year=h.year - 1) + timedelta(days=1)).isoformat()   # 12 meses
    det = [d for d in det_b["detenciones"] + previas if desde <= d["fecha"] <= hasta]
    ids = [d["id"] for d in det]
    assert len(ids) == len(set(ids)), "ids repetidos entre la beta y det_previas"
    for d in det:
        asignar(d)
        d["apoyo_proscrita"] = d.get("grupo") == "palestine-action"
    det.sort(key=lambda d: d["fecha"], reverse=True)
    criterio = det_b["criterio"] + (" Las detenciones por mostrar apoyo a una organización proscrita (Palestine Action) "
                                    "se marcan aparte y pueden ocultarse.")
    salida = {"actualizado": det_b["actualizado"], "periodo": {"desde": desde, "hasta": hasta},
              "criterio": criterio, "detenciones": det}
    (EU / "datos" / "detenciones.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")

    inc = cargar(BETA / "europa_incidentes.json")
    for i in inc["incidentes"]:
        asignar(i)
    (EU / "datos" / "incidentes.json").write_text(json.dumps(inc, ensure_ascii=False, indent=1), encoding="utf-8")

    # zonas de referencia de los grupos: región de regiones.geojson -> provincias que caen dentro
    # (punto interior dentro, o más de la mitad de la provincia o de la región en común)
    reg = {(f["properties"]["pais"], f["properties"]["nombre"]): shape(f["geometry"])
           for f in cargar(RAIZ / "regiones.geojson")["features"]}
    rep = [f.representative_point() for f in formas]
    grupos = [g for g in cargar(BETA / "grupos.json")["grupos"] if g["ambito"] == "europa"]
    for g in grupos:
        zn = {}
        for z in g["zonas"]:
            if z["region"] == "*":
                sel = [f["properties"]["id"] for f in prov if f["properties"]["pais"] == z["pais"]]
            else:
                geom = reg[(z["pais"], z["region"])]
                sel = []
                for i in arbol.query(geom):
                    a = formas[i].intersection(geom).area
                    if geom.contains(rep[i]) or a > 0.5 * formas[i].area or a > 0.5 * geom.area:
                        sel.append(prov[i]["properties"]["id"])
                if not sel:
                    avisos.append(f"grupo {g['id']}: la región {z['region']} no contiene provincias")
            orden = {"control": 3, "influencia": 2, "presencia": 1}
            for s in sel:
                if s not in zn or orden[z["nivel"]] > orden[zn[s]]:
                    zn[s] = z["nivel"]
        g["zonas_nuts"] = [{"id": k, "nivel": v} for k, v in sorted(zn.items())]
    (EU / "datos" / "grupos.json").write_text(json.dumps({"grupos": grupos}, ensure_ascii=False, indent=1), encoding="utf-8")

    for a in avisos:
        print("AVISO", a)
    print(f"{len(det)} detenciones ({sum(1 for d in det if d['nuts3'])} con provincia), "
          f"{len(inc['incidentes'])} incidentes, {len(grupos)} grupos")


if __name__ == "__main__":
    main()
