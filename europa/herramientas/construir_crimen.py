"""Genera europa/datos/crimen.json: organizaciones criminales y su peso en cada provincia.

Niveles por provincia (códigos NUTS; un código corto abarca todas sus provincias, p. ej. ITF6 = Calabria):
- dominio: control territorial asentado y reconocido por las autoridades (mafias en su territorio de origen).
- influencia: poder consolidado sobre mercados ilegales, puertos o barrios.
- presencia: actividad documentada, sin control.
Cuando dos organizaciones comparten el nivel más alto en una provincia, el mapa la muestra en disputa.

Líderes: solo públicos, sancionados o condenados. No se señalan edificios, barrios ni comunidades.
Uso: python3 europa/herramientas/construir_crimen.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EU = RAIZ / "europa"
ACTUALIZADO = "2026-11-12"

TIPOS = {"mafia": "Mafia", "red": "Red de narcotráfico", "cartel": "Cártel extranjero", "banda": "Banda urbana"}
NIVELES = ["dominio", "influencia", "presencia"]

F = {  # fuentes reutilizadas
    "socta": ("Europol: el ADN del crimen organizado está cambiando (EU-SOCTA 2025)", "https://europol.europa.eu/media-press/newsroom/news/dna-of-organised-crime-changing-and-so-threat-to-europe"),
    "decoding": ("Europol: Decoding the EU's most threatening criminal networks (2024)", "https://www.europol.europa.eu/cms/sites/default/files/documents/Europol report on Decoding the EU-s most threatening criminal networks.pdf"),
    "puertos": ("EUDA: Seaports, monitoring the EU's floodgates for illicit drugs (2025)", "https://www.euda.europa.eu/system/files/documents/2025-06/seaports-monitoring-the-eus-floodgates-for-illicit-drugs.pdf"),
}

ORG = [
    dict(id="ndrangheta", nombre="'Ndrangheta", tipo="mafia", origen="Calabria (Italia)",
         descripcion="La mafia más poderosa de Italia y uno de los mayores importadores de cocaína de Europa. Se organiza en familias («'ndrine») y, fuera de Calabria, en «locali»: la DIA cuenta al menos 48 en el centro y el norte del país. Tiene redes en Alemania, Bélgica, los Países Bajos y España.",
         actividades=["importación de cocaína", "extorsión", "infiltración en obra pública", "blanqueo"],
         lideres=[],
         zonas=[("ITF6", "dominio"),
                ("ITC4C", "influencia"), ("ITC4D", "influencia"), ("ITC42", "influencia"), ("ITC41", "influencia"), ("ITC43", "influencia"),
                ("ITC11", "influencia"), ("ITC33", "influencia"), ("ITC31", "influencia"), ("ITH53", "influencia"),
                ("ITI43", "presencia"), ("DEA12", "presencia")],
         fuentes=[("L'Espresso: informe DIA, al menos 48 «locali» de la 'Ndrangheta en el centro-norte", "https://lespresso.it/c/attualita/2025/5/27/mafia-relazione-dia-almeno-48-locali-ndrangheta-al-centro-nord-interesse-grandi-opere/54576"),
                  ("Eurojust: nueva acción contra la 'Ndrangheta en Italia, Bélgica y Alemania", "https://www.eurojust.europa.eu/news/new-action-against-ndrangheta-italy-belgium-and-germany"),
                  ("NPR: Alemania e Italia, redadas contra la 'Ndrangheta (2023)", "https://www.npr.org/2023/05/04/1173918842/germany-and-italy-clamp-down-on-italian-mob-with-raids-and-arrests")]),
    dict(id="camorra", nombre="Camorra", tipo="mafia", origen="Campania (Italia)",
         descripcion="Conjunto de clanes, sin cúpula única, que se reparten Nápoles y su provincia (la Alianza de Secondigliano y otros) y la provincia de Caserta (los Casalesi). Las autoridades describen un escenario fragmentado, con clanes que se regeneran con hijos y nietos de los jefes.",
         actividades=["narcotráfico", "extorsión", "residuos", "falsificación", "blanqueo"],
         lideres=[],
         zonas=[("ITF33", "dominio"), ("ITF31", "dominio"), ("ITF35", "influencia"), ("ITI44", "presencia"), ("ITI43", "presencia")],
         fuentes=[("Fanpage: el mapa de los clanes de la Camorra en Nápoles", "https://www.fanpage.it/napoli/mappa-camorra-napoli-clan-nuova/"),
                  ("Cronache della Campania: el fiscal general describe un escenario fragmentado", "https://en.cronachedellacampania.it/2026/01/camorra-il-pg-policastro-scenario-frammentato-ma-due/"),
                  ("Agenzia Nova: 37 detenidos por intentar reconstruir el poder de los Casalesi", "https://www.agenzianova.com/de/news/Schiavone-Clan-und-Bidognetti-37-Festnahmen/"),
                  ("Cronache della Campania: Gratteri, los clanes de Nápoles se regeneran con hijos y nietos (2026)", "https://en.cronachedellacampania.it/2026/03/In-Naples--the-clans-are-regenerating-with-children-and-grandchildren./")]),
    dict(id="cosa-nostra", nombre="Cosa Nostra", tipo="mafia", origen="Sicilia (Italia)",
         descripcion="La mafia siciliana, organizada en familias y «mandamenti». Sigue controlando el territorio en el oeste y el centro de Sicilia y en Catania, con un perfil más bajo que en el pasado y alianzas con la Camorra y la 'Ndrangheta para el narcotráfico.",
         actividades=["extorsión", "narcotráfico", "contratos públicos", "apuestas"],
         lideres=[],
         zonas=[("ITG12", "dominio"), ("ITG11", "dominio"), ("ITG14", "dominio"), ("ITG15", "dominio"), ("ITG16", "dominio"), ("ITG17", "dominio"),
                ("ITG13", "influencia"), ("ITG19", "influencia"), ("ITG18", "influencia")],
         fuentes=[("La Sicilia: el nuevo mapa de la DIA sobre la mafia siciliana", "https://www.lasicilia.it/cronaca/la-nuova-mappa-della-dia-sulla-mafia-siciliana-ecco-chi-comanda-nellisola-1218909/"),
                  ("Cronache della Campania: la nueva Cosa Nostra y sus lazos con la Camorra y la 'Ndrangheta", "https://en.cronachedellacampania.it/2025/12/palermo-la-nuova-cosa-nostra-e-i-legami-con-camorra-e-ndrangheta-i-nomi-dei-50-arresti/")]),
    dict(id="stidda", nombre="Stidda", tipo="mafia", origen="Sicilia (Italia)",
         descripcion="Organización mafiosa nacida como rival de Cosa Nostra en el sur de Sicilia (Gela, Vittoria). Hoy convive con ella en algunas zonas de Agrigento, Caltanissetta y Ragusa.",
         actividades=["extorsión", "narcotráfico", "agricultura y transporte"],
         lideres=[],
         zonas=[("ITG14", "presencia"), ("ITG15", "presencia"), ("ITG18", "presencia")],
         fuentes=[("La Sicilia: el nuevo mapa de la DIA sobre la mafia siciliana", "https://www.lasicilia.it/cronaca/la-nuova-mappa-della-dia-sulla-mafia-siciliana-ecco-chi-comanda-nellisola-1218909/")]),
    dict(id="societa-foggiana", nombre="Società foggiana", tipo="mafia", origen="Foggia (Italia)",
         descripcion="La mafia de Foggia y el Gargano, considerada por los investigadores una de las más violentas de Italia. Se dirige incluso desde la cárcel.",
         actividades=["extorsión", "robos de vehículos", "asaltos a furgones blindados", "narcotráfico"],
         lideres=[],
         zonas=[("ITF46", "dominio")],
         fuentes=[("L'Espresso: Apulia, la cuarta mafia olvidada", "https://lespresso.it/c/attualita/2025/9/15/puglia-quarta-mafia-trascurata-infiltrazioni-racket-furti-auto-assalto-portavalori/56795"),
                  ("Affaritaliani: la DDA golpea a la Società foggiana", "https://www.affaritaliani.it/cronache/puglia-la-dda-colpisce-la-societa-foggiana-ordini-dal-carcere-e-dai-domiciliari.html")]),
    dict(id="scu", nombre="Sacra Corona Unita", tipo="mafia", origen="Salento (Italia)",
         descripcion="Mafia del sur de Apulia (Lecce, Brindisi y Taranto), hoy más fragmentada que en los años noventa pero aún activa, con ritos de afiliación y control de la extorsión y la droga.",
         actividades=["narcotráfico", "extorsión", "usura"],
         lideres=[],
         zonas=[("ITF45", "influencia"), ("ITF44", "influencia"), ("ITF43", "influencia")],
         fuentes=[("AGI: ritos de afiliación de la Sacra Corona Unita (2026)", "https://www.agi.it/cronaca/news/2026-09-26/sacra-corona-unita-riti-affiliazione-39261031/"),
                  ("L'Espresso: Apulia, la cuarta mafia olvidada", "https://lespresso.it/c/attualita/2025/9/15/puglia-quarta-mafia-trascurata-infiltrazioni-racket-furti-auto-assalto-portavalori/56795")]),
    dict(id="clanes-bari", nombre="Clanes de Bari", tipo="mafia", origen="Bari (Italia)",
         descripcion="Clanes mafiosos de la ciudad y la provincia de Bari, enfrentados entre sí por el control de barrios y del narcotráfico.",
         actividades=["narcotráfico", "extorsión", "apuestas"],
         lideres=[],
         zonas=[("ITF47", "influencia"), ("ITF48", "influencia")],
         fuentes=[("L'Espresso: Apulia, la cuarta mafia olvidada", "https://lespresso.it/c/attualita/2025/9/15/puglia-quarta-mafia-trascurata-infiltrazioni-racket-furti-auto-assalto-portavalori/56795")]),
    dict(id="mocro-maffia", nombre="Mocro Maffia", corto="Mocro Maffia", tipo="red", origen="Países Bajos y Bélgica",
         descripcion="Nombre que la prensa da a las redes neerlandesas y belgas que controlan buena parte de la entrada de cocaína por Róterdam y Amberes. Han protagonizado asesinatos de abogados y periodistas y una ola de atentados con explosivos en Amberes.",
         actividades=["importación de cocaína", "asesinatos por encargo", "corrupción de trabajadores portuarios"],
         lideres=[{"nombre": "Ridouan Taghi", "cargo": "jefe de la organización juzgada en el caso Marengo", "estado": "condenado a cadena perpetua (2024)"}],
         zonas=[("NL329", "influencia"), ("NL33C", "influencia"), ("NL310", "influencia"), ("BE211", "influencia"), ("BE100", "presencia")],
         fuentes=[("Brussels Times: cadena perpetua para el jefe de la Mocro Maffia", "https://brusselstimes.com/944003/mocro-mafia-drug-cartel-leader-gets-life-sentence-for-murder-in-the-netherlands"),
                  ("The Irish Times: granadas y armas en Amberes por el auge de la cocaína", "https://www.irishtimes.com/world/europe/2023/09/01/guns-and-grenades-betray-antwerps-struggles-with-rising-cocaine-trade"),
                  ("eNCA: la ciudad portuaria belga aterrorizada por la violencia de la droga", "https://www.enca.com/news/belgian-port-city-terrorised-drug-violence")]),
    dict(id="kinahan", nombre="Cártel Kinahan", corto="Kinahan", tipo="red", origen="Irlanda",
         descripcion="Organización irlandesa de narcotráfico y armas con base histórica en Dublín y en la Costa del Sol. Su guerra con la banda Hutch dejó más de quince muertos. Muy debilitada tras las sanciones de EE. UU. y la detención de Daniel Kinahan en Dubái en 2026.",
         actividades=["narcotráfico", "tráfico de armas", "blanqueo"],
         lideres=[{"nombre": "Christopher Kinahan", "cargo": "fundador", "estado": "sancionado por EE. UU. (2022)"},
                  {"nombre": "Daniel Kinahan", "cargo": "jefe", "estado": "sancionado por EE. UU. (2022); detenido en Dubái en abril de 2026"},
                  {"nombre": "Christopher Kinahan Jr.", "cargo": "dirección financiera", "estado": "sancionado por EE. UU. (2022)"}],
         zonas=[("IE061", "influencia"), ("ES617", "presencia")],
         fuentes=[("Tesoro de EE. UU.: sanciones a la organización Kinahan (2022)", "https://home.treasury.gov/news/press-releases/jy0713"),
                  ("The Olive Press: de las mansiones de Marbella a una celda en Dublín (2026)", "https://www.theolivepress.es/spain-news/2026/08/09/daniel-kinahan-spain-from-marbella-mansions-to-a-dublin-cell/"),
                  ("The Spanish Eye: dónde están los gánsteres que dominaban la Costa del Sol", "https://www.thespanisheye.com/2025/10/29/kinahan-cartel-where-are-the-gangsters-who-once-ruled-the-costa-del-sol-now/")]),
    dict(id="kavac", nombre="Clan Kavač", corto="Kavač", tipo="red", origen="Bahía de Kotor (Montenegro)",
         descripcion="Clan montenegrino del narcotráfico, enfrentado desde 2014 con el clan Škaljari en una guerra que ha dejado decenas de muertos en Montenegro, Serbia, España, Grecia y otros países.",
         actividades=["tráfico de cocaína por mar", "asesinatos por encargo"],
         lideres=[],
         zonas=[("ME000", "influencia"), ("RS110", "presencia")],
         fuentes=[("OCCRP: Bad Blood, la guerra entre clanes montenegrinos de la cocaína", "https://www.occrp.org/en/project/balkan-cocaine-wars/bad-blood-a-war-between-montenegrin-cocaine-clans-engulfs-the-balkans"),
                  ("RUSI: el choque entre los clanes de Kotor", "https://www.rusi.org/networks/shoc/informer/criminal-clash-between-montenegrin-kotor-clans")]),
    dict(id="skaljari", nombre="Clan Škaljari", corto="Škaljari", tipo="red", origen="Bahía de Kotor (Montenegro)",
         descripcion="Clan rival del Kavač, surgido de la misma red de narcotráfico. La guerra entre ambos sigue activa y se ha extendido a Serbia y a otros países europeos.",
         actividades=["tráfico de cocaína por mar", "asesinatos por encargo"],
         lideres=[],
         zonas=[("ME000", "influencia"), ("RS110", "presencia")],
         fuentes=[("OCCRP: Bad Blood, la guerra entre clanes montenegrinos de la cocaína", "https://www.occrp.org/en/project/balkan-cocaine-wars/bad-blood-a-war-between-montenegrin-cocaine-clans-engulfs-the-balkans"),
                  ("Bezbednost: la dimensión regional de un enfrentamiento local de Montenegro", "https://bezbednost.org/en/publication/the-regional-dimension-of-a-montenegro-s-local-feud/")]),
    dict(id="redes-albanesas", nombre="Redes de habla albanesa", corto="Redes albanesas", tipo="red", origen="Albania y Kosovo",
         descripcion="Término de Europol para redes, sin estructura común, que compran la cocaína directamente en Ecuador y Colombia y la introducen por los grandes puertos europeos. Son de las más presentes en la importación al por mayor.",
         actividades=["importación de cocaína", "cultivo de cannabis", "blanqueo"],
         lideres=[],
         zonas=[("AL012", "influencia"), ("AL022", "influencia"), ("BE211", "presencia"), ("NL33C", "presencia")],
         fuentes=[("Global Initiative: cómo las redes albanesas llegaron a dominar el tráfico de cocaína hacia Europa (2025)", "https://globalinitiative.net/analysis/how-have-albanian-networks-come-to-dominate-cocaine-trafficking-to-europe/"),
                  ("Euronews Albania: según Europol, las redes de habla albanesa compran la cocaína en origen", "https://euronews.al/en/?p=19785")]),
    dict(id="clanes-estrecho", nombre="Clanes del narcotráfico del Estrecho", corto="Clanes del Estrecho", tipo="red", origen="Campo de Gibraltar y Guadalquivir (España)",
         descripcion="Clanes locales que dominan la entrada de hachís desde Marruecos y, cada vez más, de cocaína, con cientos de narcolanchas en el Estrecho. En los últimos años se han desplazado al Guadalquivir y han aumentado las armas y la violencia contra los agentes.",
         actividades=["tráfico de hachís", "tráfico de cocaína", "petaqueo (suministro de gasolina)"],
         lideres=[],
         zonas=[("ES612", "influencia"), ("ES615", "presencia"), ("ES618", "presencia")],
         fuentes=[("Público: el narcotráfico en Andalucía, una hidra que ya desafía al Estado", "https://www.publico.es/politica/narcotrafico-andalucia-hidra-infinitas-cabezas-desafia.html"),
                  ("Euronews: armas y nuevas rutas, la transformación del narco en Andalucía (2026)", "https://es.euronews.com/2026/08/23/armas-y-nuevas-rutas-la-transformacion-del-narco-en-andalucia"),
                  ("Noticias de Navarra: el Gobierno reconoce 600 narcolanchas en el Estrecho (2026)", "https://www.noticiasdenavarra.com/politica/2026/05/14/gobierno-espanol-reconoce-hay-600-11066761.html")]),
    dict(id="clan-del-golfo", nombre="Clan del Golfo", tipo="cartel", origen="Colombia",
         descripcion="El mayor grupo armado del narcotráfico colombiano. Envía cocaína a Europa por contenedores y tiene enviados y socios en los puertos; en España se han detenido mandos de la organización.",
         actividades=["exportación de cocaína", "logística portuaria"],
         lideres=[],
         zonas=[("BE211", "presencia")],
         fuentes=[("Brussels Times: los cárteles colombianos se centran en Amberes", "https://brusselstimes.com/785900/breaking-into-europe-through-belgium-colombian-cartels-focus-efforts-on-antwerp"),
                  ("CRHoy: capturados cinco altos mandos del Clan del Golfo en España y Colombia", "https://crhoy.com/capturan-a-cinco-altos-mandos-del-clan-del-golfo-en-espana-y-colombia-con-nexos-en-costa-rica/")]),
    dict(id="carteles-mexicanos", nombre="Cárteles mexicanos (Sinaloa y CJNG)", corto="Cárteles mexicanos", tipo="cartel", origen="México",
         descripcion="El Cártel de Sinaloa y el Cártel Jalisco Nueva Generación venden cocaína a redes europeas y han enviado «cocineros» a laboratorios de metanfetamina en los Países Bajos y Bélgica. En 2025 se desarticuló en Marsella una red ligada al de Sinaloa.",
         actividades=["venta de cocaína al por mayor", "producción de metanfetamina"],
         lideres=[],
         zonas=[("NL41", "presencia"), ("FRL04", "presencia")],
         fuentes=[("Brookings: la política exterior de Sinaloa y el CJNG, los mercados europeos", "https://www.brookings.edu/articles/the-foreign-policies-of-the-sinaloa-cartel-and-cjng-part-iv-europes-cocaine-and-meth-markets/"),
                  ("Global Initiative: el crimen organizado latinoamericano en Europa", "https://globalinitiative.net/analysis/latin-american-organized-crime-europe/"),
                  ("Albanian Daily News: 16 detenidos en Marsella en una red ligada al Cártel de Sinaloa (2025)", "https://albaniandailynews.com/news/marseille-16-arrests-in-a-crackdown-on-a-network-with-ties-to-the-sinaloa-cartel")]),
    dict(id="pcc", nombre="Primeiro Comando da Capital (PCC)", corto="PCC", tipo="cartel", origen="Brasil",
         descripcion="La mayor organización criminal de Brasil. Informes brasileños hablan de cerca de un millar de miembros en Portugal y de inversiones en negocios y fútbol; la Policía Judiciaria portuguesa es más prudente sobre su peso real.",
         actividades=["tráfico de cocaína", "blanqueo", "inversiones en negocios"],
         lideres=[],
         zonas=[("PT170", "presencia")],
         fuentes=[("CNN Brasil: cerca de 1.000 miembros del PCC actúan en Portugal, según un informe", "https://www.cnnbrasil.com.br/internacional/relatorio-aponta-que-cerca-de-1-000-membros-do-pcc-atuam-em-portugal/"),
                  ("Observador: el PCC tiene negocios e inmuebles en Portugal (2025)", "https://observador.pt/2025/09/16/grupo-criminoso-pcc-tem-estabelecimentos-comerciais-imoveis-e-tera-investimentos-em-futebol-em-portugal/"),
                  ("DN: la Policía Judiciaria aún no reconoce la presencia del PCC en Portugal", "https://www.dn.pt/sociedade/judiciaria-ainda-nao-reconhece-presenca-do-pcc-em-portugal-17491889.html")]),
    dict(id="foxtrot", nombre="Red Foxtrot", corto="Foxtrot", tipo="banda", origen="Uppsala (Suecia)",
         descripcion="Red criminal sueca de narcotráfico y violencia que recluta a menores para tiroteos y atentados con explosivos. EE. UU. la sancionó por actuar al servicio de Irán, incluido el ataque contra la embajada de Israel en Estocolmo.",
         actividades=["narcotráfico", "tiroteos y explosiones por encargo", "reclutamiento de menores"],
         lideres=[{"nombre": "Rawa Majid", "cargo": "jefe", "estado": "sancionado por EE. UU. (2025)"}],
         zonas=[("SE121", "influencia"), ("SE110", "influencia")],
         fuentes=[("Tesoro de EE. UU.: sanciones a la red Foxtrot y a su jefe (2025)", "https://home.treasury.gov/news/press-releases/sb0047"),
                  ("The Local: tiroteo triple en Uppsala (2025)", "https://www.thelocal.se/20250506/three-suspects-remanded-in-custody-over-uppsala-triple-shooting")]),
    dict(id="rumba", nombre="Red Rumba", corto="Rumba", tipo="banda", origen="Estocolmo (Suecia)",
         descripcion="Escisión de Foxtrot. Su guerra con la red de origen desató en 2023 la peor ola de tiroteos y explosiones de la historia reciente de Suecia.",
         actividades=["narcotráfico", "tiroteos y explosiones"],
         lideres=[],
         zonas=[("SE110", "influencia")],
         fuentes=[("CBS News: detenido en Turquía uno de los criminales más buscados de Suecia", "https://www.cbsnews.com/news/sweden-wanted-crime-boss-ismail-abdo-arrested-turkey"),
                  ("The Local: récord de muertes por disparos en Suecia (2023)", "https://www.thelocal.se/20230928/three-people-killed-in-12-hours-as-sweden-records-deadliest-month-in-years")]),
    dict(id="dz-mafia", nombre="DZ Mafia", tipo="banda", origen="Marsella (Francia)",
         descripcion="La red de narcotráfico dominante en Marsella. Controla puntos de venta en los barrios del norte y se impuso en una guerra con el clan Yoda que dejó decenas de muertos.",
         actividades=["narcotráfico", "asesinatos por encargo"],
         lideres=[],
         zonas=[("FRL04", "influencia")],
         fuentes=[("Sud Radio: DZ Mafia, ascenso, asesinatos y conquista", "https://www.sudradio.fr/sud-radio/dz-mafia-ascension-meurtres-et-conquete-dun-clan-sans-limite"),
                  ("Sud Radio: derrotados por la DZ Mafia, el jefe de Yoda y los supervivientes del clan, juzgados", "https://www.sudradio.fr/societe/defaits-par-la-dz-mafia-felix-bingui-et-des-rescapes-du-clan-yoda-juges-a-marseille")]),
    dict(id="yoda", nombre="Clan Yoda", corto="Yoda", tipo="banda", origen="Marsella (Francia)",
         descripcion="Clan marsellés rival de la DZ Mafia, muy debilitado tras perder la guerra por los puntos de venta y la condena de su jefe.",
         actividades=["narcotráfico"],
         lideres=[{"nombre": "Félix Bingui", "cargo": "jefe", "estado": "condenado a 12 años de prisión"}],
         zonas=[("FRL04", "presencia")],
         fuentes=[("Sud Radio: el jefe del clan Yoda, condenado a 12 años", "https://www.sudradio.fr/societe/narcotrafic-felix-bingui-chef-presume-du-clan-yoda-condamne-a-12-ans-de-prison")]),
]

PUERTOS = [
    ("Amberes", "Bélgica", 51.29, 4.30), ("Róterdam", "Países Bajos", 51.95, 4.14), ("Hamburgo", "Alemania", 53.54, 9.97),
    ("Algeciras", "España", 36.13, -5.44), ("Valencia", "España", 39.44, -0.32), ("Gioia Tauro", "Italia", 38.45, 15.90),
    ("Le Havre", "Francia", 49.47, 0.15),
]

COLORES = {  # claro, oscuro
    "ndrangheta": ("#b2182b", "#ef6b73"), "camorra": ("#d6604d", "#f4a582"), "cosa-nostra": ("#67001f", "#d6537a"),
    "stidda": ("#a24d84", "#d48ab8"), "societa-foggiana": ("#e08214", "#fdb863"), "scu": ("#8c510a", "#d9a35b"),
    "clanes-bari": ("#bf812d", "#dfc27d"), "mocro-maffia": ("#2166ac", "#6aa9e0"), "kinahan": ("#1b7837", "#5fbf7a"),
    "kavac": ("#542788", "#a08bd6"), "skaljari": ("#c51b7d", "#ee7fbf"), "redes-albanesas": ("#35978f", "#6fd1c4"),
    "clanes-estrecho": ("#d4a000", "#f2cf5b"), "clan-del-golfo": ("#8c6d31", "#d7b46a"), "carteles-mexicanos": ("#993404", "#e3854a"),
    "pcc": ("#525252", "#bdbdbd"), "foxtrot": ("#4393c3", "#8cc3e8"), "rumba": ("#01665e", "#3fb3a5"),
    "dz-mafia": ("#7b3294", "#c08ddc"), "yoda": ("#8073ac", "#b8b0dc"),
}


def main():
    prov = {f["properties"]["id"]: f["properties"] for f in json.loads((EU / "geo/provincias.geojson").read_text())["features"]}
    errores = []
    salida = []
    for o in ORG:
        zn = {}
        for cod, nivel in o["zonas"]:
            assert nivel in NIVELES, (o["id"], nivel)
            ids = [p for p in prov if p.startswith(cod)]
            if not ids:
                errores.append(f"{o['id']}: el código {cod} no corresponde a ninguna provincia")
            for p in ids:
                if p not in zn or NIVELES.index(nivel) < NIVELES.index(zn[p]):
                    zn[p] = nivel
        if o["id"] not in COLORES:
            errores.append(f"{o['id']}: sin color")
        if not o["fuentes"]:
            errores.append(f"{o['id']}: sin fuentes")
        paises = sorted({prov[p]["pais"] for p in zn}, key=lambda x: x)
        salida.append({
            "id": o["id"], "nombre": o["nombre"], "corto": o.get("corto", o["nombre"]), "tipo": o["tipo"], "origen": o["origen"],
            "descripcion": o["descripcion"], "actividades": o["actividades"], "lideres": o["lideres"],
            "paises": paises, "color": COLORES[o["id"]][0], "color_oscuro": COLORES[o["id"]][1],
            "zonas": [{"codigo": c, "nivel": n} for c, n in o["zonas"]],
            "zonas_nuts": [{"id": k, "nivel": v} for k, v in sorted(zn.items())],
            "fuentes": [{"titulo": t, "url": u} for t, u in o["fuentes"]],
        })
    datos = {
        "actualizado": ACTUALIZADO,
        "criterio": ("Peso de cada organización por provincia según informes oficiales (DIA, Europol, EUDA, Tesoro de EE. UU.) y prensa. "
                     "Dominio: control territorial asentado. Influencia: poder consolidado sobre mercados, puertos o barrios. "
                     "Presencia: actividad documentada. Es aproximado: estas organizaciones no tienen fronteras fijas."),
        "tipos": TIPOS,
        "organizaciones": salida,
        "puertos": [{"lugar": l, "pais": p, "lat": la, "lon": lo,
                     "nota": "Uno de los principales puertos de entrada de cocaína en Europa",
                     "fuente": {"titulo": F["puertos"][0], "url": F["puertos"][1]}} for l, p, la, lo in PUERTOS],
        "fuentes_generales": [{"titulo": t, "url": u} for t, u in (F["socta"], F["decoding"], F["puertos"])],
    }
    for e in errores:
        print("ERROR", e)
    if errores:
        raise SystemExit(1)
    (EU / "datos" / "crimen.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    n = {}
    for o in salida:
        for z in o["zonas_nuts"]:
            n.setdefault(z["id"], []).append((o["id"], z["nivel"]))
    print(f"{len(salida)} organizaciones · {len(n)} provincias con datos · {len(PUERTOS)} puertos")


if __name__ == "__main__":
    main()
