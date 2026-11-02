"""Genera las capas geográficas de la beta a partir de geoBoundaries y Natural Earth.

Entradas (descargadas a una carpeta de trabajo, ver README):
  <src>/gb/adm1/<ISO3>.geojson   geoBoundaries ADM1 simplificado (África)
  <src>/gb/adm2/<ISO3>.geojson   geoBoundaries ADM2 simplificado (países en conflicto)
  <src>/geo/admin1.geojson       Natural Earth 10m admin-1 (solo para Níger)
Salidas:
  beta/geo/africa_regiones.geojson   ADM1 de toda África (agrupación de burbujas y zonas)
  beta/fuentes/unidades_adm2.geojson ADM2 de países en conflicto (solo para construir zonas)
  beta/fuentes/unidades.csv          índice de nombres para escribir zonas en grupos.json
Uso: python3 beta/herramientas/geo_base.py <carpeta_src>
"""
import csv
import json
import sys
from pathlib import Path

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

SRC = Path(sys.argv[1])
BETA = Path(__file__).resolve().parent.parent

PAIS = {"DZA": "Argelia", "AGO": "Angola", "BEN": "Benín", "BWA": "Botsuana", "BFA": "Burkina Faso",
        "BDI": "Burundi", "CPV": "Cabo Verde", "CMR": "Camerún", "CAF": "República Centroafricana",
        "TCD": "Chad", "COM": "Comoras", "COD": "R. D. del Congo", "COG": "República del Congo",
        "CIV": "Costa de Marfil", "DJI": "Yibuti", "EGY": "Egipto", "GNQ": "Guinea Ecuatorial",
        "ERI": "Eritrea", "SWZ": "Esuatini", "ETH": "Etiopía", "GAB": "Gabón", "GMB": "Gambia",
        "GHA": "Ghana", "GIN": "Guinea", "GNB": "Guinea-Bisáu", "KEN": "Kenia", "LSO": "Lesoto",
        "LBR": "Liberia", "LBY": "Libia", "MDG": "Madagascar", "MWI": "Malaui", "MLI": "Malí",
        "MRT": "Mauritania", "MUS": "Mauricio", "MAR": "Marruecos", "MOZ": "Mozambique",
        "NAM": "Namibia", "NER": "Níger", "NGA": "Nigeria", "RWA": "Ruanda",
        "STP": "Santo Tomé y Príncipe", "SEN": "Senegal", "SYC": "Seychelles", "SLE": "Sierra Leona",
        "SOM": "Somalia", "ZAF": "Sudáfrica", "SSD": "Sudán del Sur", "SDN": "Sudán", "TZA": "Tanzania",
        "TGO": "Togo", "TUN": "Túnez", "UGA": "Uganda", "ZMB": "Zambia", "ZWE": "Zimbabue"}

# Nombres en español de las regiones más citadas; el resto se deja como en la fuente.
ES = {
    "COD": {"North Kivu": "Kivu del Norte", "South Kivu": "Kivu del Sur", "Upper Uele": "Alto Uele",
            "Lower Uele": "Bajo Uele", "Central Kasai": "Kasai Central", "Kongo-Central": "Congo Central",
            "Haut-Katanga": "Alto Katanga", "Haut-Lomami": "Alto Lomami"},
    "SDN": {"North Darfur": "Darfur del Norte", "South Darfur": "Darfur del Sur", "West Darfur": "Darfur Occidental",
            "East Darfur": "Darfur Oriental", "Central Darfur": "Darfur Central", "North Kordofan": "Kordofán del Norte",
            "South Kordofan": "Kordofán del Sur", "West Kordofan": "Kordofán Occidental", "Khartoum": "Jartum",
            "Blue Nile": "Nilo Azul", "White Nile": "Nilo Blanco", "River Nile": "Río Nilo", "Northern": "Norte",
            "Red Sea": "Mar Rojo", "Gezira": "Gezira", "Abyei PCA": "Abyei"},
    "SSD": {"Central Equatoria": "Ecuatoria Central", "Eastern Equatoria": "Ecuatoria Oriental",
            "Western Equatoria": "Ecuatoria Occidental", "Upper Nile": "Alto Nilo", "Unity": "Unidad",
            "Lakes": "Lagos", "Northern Bahr el Ghazal": "Bahr el Ghazal del Norte",
            "Western Bahr el Ghazal": "Bahr el Ghazal Occidental"},
    "SOM": {"Lower Juba": "Bajo Juba", "Middle Juba": "Juba Medio", "Lower Shebelle": "Bajo Shabelle",
            "Middle Shebelle": "Shabelle Medio", "Banadir": "Banadir (Mogadiscio)", "Galgaduud": "Galguduud",
            "Hiiraan": "Hiran", "Woqooyi Galbeed": "Woqooyi Galbeed (Somalilandia)",
            "Awdal": "Awdal (Somalilandia)", "Togdheer": "Togdheer (Somalilandia)",
            "Sool": "Sool", "Sanaag": "Sanaag"},
    "CMR": {"Far North": "Extremo Norte", "North-West": "Noroeste", "South-West": "Suroeste", "North": "Norte",
            "South": "Sur", "East": "Este", "West": "Oeste", "Centre": "Centro"},
    "ETH": {"Addis Ababa": "Adís Abeba", "Beneshangul Gumu": "Benishangul-Gumuz", "SNNPR": "Pueblos del Sur (SNNPR)",
            "Somali": "Somalí", "Hareri": "Harar"},
    "NGA": {"Abuja Federal Capital Territory": "Abuya (Territorio Federal)"},
    "MLI": {"Koulikouro": "Koulikoro", "Segou": "Ségou", "Tombouctou": "Tombuctú"},
    "LBY": {"Surt": "Sirte", "Misratah": "Misrata", "Al Kufrah": "Kufra", "Al Jufrah": "Yufra", "Sabha": "Sebha",
            "Al Butnan": "Butnan (Tobruk)", "Tajura' wa an Nawahi al Arba": "Tajura", "Al Marqab": "Murqub",
            "Al Jifarah": "Yifara", "Az Zawiyah": "Zauiya", "Ghadamis": "Gadames", "Murzuq": "Murzuk"},
    "MAR": {"Laâyoune-Sakia El Hamra": "Laayún-Saguía el Hamra", "Dakhla-Oued Ed-Dahab": "Dajla-Río de Oro",
            "Tangier-Tetouan-Al Hoceima": "Tánger-Tetuán-Alhucemas", "Fez-Meknes": "Fez-Mequinez"},
    "EGY": {"North Sinai Governorate": "Sinaí del Norte", "South Sinai Governorate": "Sinaí del Sur",
            "Cairo Governorate": "El Cairo", "Alexandria Governorate": "Alejandría", "Giza Governorate": "Guiza"},
    "MOZ": {"Zambézia": "Zambezia"},
    "TCD": {"N'Djamena Region": "Yamena"},
    "CAF": {"Bangui": "Bangui"},
}
SAHARA = {"Laâyoune-Sakia El Hamra", "Dakhla-Oued Ed-Dahab"}


def redondear(geom, nd=3):
    """Redondea coordenadas para aligerar el fichero (≈100 m de precisión)."""
    def r(c):
        if isinstance(c[0], (float, int)):
            return [round(c[0], nd), round(c[1], nd)]
        return [r(x) for x in c]
    return {"type": geom["type"], "coordinates": r(geom["coordinates"])}


def limpiar(nombre):
    for suf in (" Governorate", " Governate", " Region", " Province", " State"):
        if nombre.endswith(suf):
            nombre = nombre[: -len(suf)]
    return nombre.strip()


def titulo(n):
    return n.title() if n.isupper() else n


def main():
    feats, filas = [], []
    for f in sorted((SRC / "gb" / "adm1").glob("*.geojson")):
        iso = f.stem
        if iso not in PAIS or iso == "NER":
            continue
        for ft in json.loads(f.read_text())["features"]:
            orig = ft["properties"]["shapeName"]
            nombre = ES.get(iso, {}).get(orig) or limpiar(orig)
            pais = PAIS[iso]
            if iso == "MAR" and orig in SAHARA:
                pais = "Sáhara Occidental"
            feats.append({"type": "Feature", "properties": {"pais": pais, "nombre": nombre, "iso": iso},
                          "geometry": ft["geometry"]})
    # Níger: geoBoundaries agrupa regiones; se usan las 8 de Natural Earth
    ne = json.loads((SRC / "geo" / "admin1.geojson").read_text())
    nombres_ner = {"Tillabéri": "Tillabéri", "Tahoua": "Tahoua", "Agadez": "Agadez", "Diffa": "Diffa",
                   "Zinder": "Zinder", "Maradi": "Maradi", "Dosso": "Dosso", "Niamey": "Niamey"}
    for ft in ne["features"]:
        p = ft["properties"]
        if p.get("adm0_a3") == "NER":
            nombre = nombres_ner.get(p["name"], p["name"])
            feats.append({"type": "Feature", "properties": {"pais": "Níger", "nombre": nombre, "iso": "NER"},
                          "geometry": ft["geometry"]})
    # Unir piezas con el mismo nombre dentro de un país
    agr = {}
    for ft in feats:
        k = (ft["properties"]["pais"], ft["properties"]["nombre"])
        agr.setdefault(k, []).append(ft)
    salida = []
    for (pais, nombre), lst in agr.items():
        g = unary_union([shape(x["geometry"]).buffer(0) for x in lst]).simplify(0.01, preserve_topology=True)
        salida.append({"type": "Feature", "properties": {"pais": pais, "nombre": nombre,
                                                         "iso": lst[0]["properties"]["iso"]},
                       "geometry": redondear(mapping(g))})
        filas.append((pais, "1", "", nombre))
    (BETA / "geo" / "africa_regiones.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": salida}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    adm1_geoms = {(f["properties"]["pais"], f["properties"]["nombre"]): shape(f["geometry"]) for f in salida}

    # ADM2 de países en conflicto, con su ADM1 calculado por posición
    sal2 = []
    for f in sorted((SRC / "gb" / "adm2").glob("*.geojson")):
        iso = f.stem
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        cand = {k: g for k, g in adm1_geoms.items() if k[0] in (PAIS[iso], "Sáhara Occidental")}
        for ft in data["features"]:
            nombre = titulo(ft["properties"]["shapeName"].strip())
            g = shape(ft["geometry"]).buffer(0)
            pt = g.representative_point()
            padre = next((k[1] for k, gg in cand.items() if gg.contains(pt)), "")
            g = g.simplify(0.004, preserve_topology=True)
            sal2.append({"type": "Feature", "properties": {"pais": PAIS[iso], "adm1": padre, "nombre": nombre},
                         "geometry": redondear(mapping(g))})
            filas.append((PAIS[iso], "2", padre, nombre))
    (BETA / "fuentes" / "unidades_adm2.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": sal2}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    with open(BETA / "fuentes" / "unidades.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["pais", "nivel", "adm1", "nombre"])
        for r in sorted(filas):
            w.writerow(r)
    print(len(salida), "regiones ADM1;", len(sal2), "unidades ADM2")


if __name__ == "__main__":
    main()
