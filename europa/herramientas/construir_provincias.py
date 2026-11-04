"""Genera europa/geo/provincias.geojson (provincias NUTS-3 y equivalentes).

Fuentes, descargadas en una carpeta que se pasa como argumento:
- nuts3_10M.json: NUTS-3 2021 de Eurostat (Nuts2json), EPSG:4326, escala 1:10M
  https://raw.githubusercontent.com/eurostat/Nuts2json/master/pub/v2/2021/4326/10M/nutsrg_3.json
- BIH_ADM2.geojson y XKX_ADM1.geojson: geoBoundaries (gbOpen, versión simplificada) para
  Bosnia y Herzegovina (cantones y distritos) y Kosovo (distritos), que no tienen NUTS.

Uso: python3 europa/herramientas/construir_provincias.py carpeta_de_descargas/
"""
import json
import sys
from pathlib import Path
from shapely.geometry import shape, mapping
D = sys.argv[1].rstrip('/') + '/'
SALIDA = Path(__file__).resolve().parents[1] / 'geo' / 'provincias.geojson'
PAIS={'AL':'Albania','AT':'Austria','BE':'Bélgica','BG':'Bulgaria','CH':'Suiza','CY':'Chipre','CZ':'Chequia','DE':'Alemania','DK':'Dinamarca','EE':'Estonia',
 'EL':'Grecia','ES':'España','FI':'Finlandia','FR':'Francia','HR':'Croacia','HU':'Hungría','IE':'Irlanda','IS':'Islandia','IT':'Italia','LI':'Liechtenstein',
 'LT':'Lituania','LU':'Luxemburgo','LV':'Letonia','ME':'Montenegro','MK':'Macedonia del Norte','MT':'Malta','NL':'Países Bajos','NO':'Noruega','PL':'Polonia',
 'PT':'Portugal','RO':'Rumanía','RS':'Serbia','SE':'Suecia','SI':'Eslovenia','SK':'Eslovaquia','UK':'Reino Unido'}
def red(g,nd=3):
    def r(c):
        if isinstance(c[0],(int,float)): return [round(c[0],nd),round(c[1],nd)]
        return [r(x) for x in c]
    m=mapping(g); return {'type':m['type'],'coordinates':r(m['coordinates'])}
out=[]
for f in json.load(open(D+'nuts3_10M.json'))['features']:
    i=f['properties']['id']; c=i[:2]
    if c not in PAIS: continue
    g=shape(f['geometry']).buffer(0).simplify(0.004,preserve_topology=True)
    if g.is_empty: continue
    out.append({'type':'Feature','properties':{'id':i,'nombre':f['properties']['na'],'pais':PAIS[c]},'geometry':red(g)})
for fn,pais,pref in [('BIH_ADM2','Bosnia y Herzegovina','BA'),('XKX_ADM1','Kosovo','XK')]:
    for k,f in enumerate(json.load(open(D+fn+'.geojson'))['features']):
        g=shape(f['geometry']).buffer(0).simplify(0.004,preserve_topology=True)
        n=f['properties']['shapeName'].replace('District of ','').replace('Canton 10','Cantón 10').replace(' Canton','').replace('Canton ','')
        out.append({'type':'Feature','properties':{'id':f'{pref}{k:02d}','nombre':n,'pais':pais},'geometry':red(g)})
json.dump({'type':'FeatureCollection','features':out},open(SALIDA,'w'),ensure_ascii=False,separators=(',',':'))
print(len(out))
