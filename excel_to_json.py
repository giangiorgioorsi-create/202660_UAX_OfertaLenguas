"""
Convierte el Excel real de oferta de lenguas (formato Banner, columnas:
ClaveBanner, NRC, Lengua, NombreMateria, NivelEtiqueta, MetodoInstruccion,
Status, Fechas, Docente, HoraInicio, HoraFin, Weekdays, CreditosAcademicos,
ListaCruzada, Plan, Recordatorio) a data.json para la pagina estatica.

Uso:
    python excel_to_json.py archivo.xlsx

Genera:
    data.json          -> datos para la pagina (se sobreescribe cada vez)
    new_tracker.json   -> historial de "primera vez visto" por NRC (persiste)
"""

import sys
import re
import json
from datetime import datetime, timedelta
import pandas as pd

DIAS_DE_VIGENCIA_NUEVO = 7

INICIO_CLASES = "11 de agosto"
FIN_CLASES = "26 de noviembre"

ORDEN_NIVELES_INGLES = ["0A", "0B", "1", "2", "3", "4", "5", "6"]
CEFR_POR_NIVEL_INGLES = {
    "0A": "Pre-A1", "0B": "Pre-A1",
    "1": "A2", "2": "A2",
    "3": "B1", "4": "B1",
    "5": "B2", "6": "B2",
}
ETIQUETA_NIVEL_INGLES = {
    "0A": "Nivel 0A", "0B": "Nivel 0B",
    "1": "Nivel 1", "2": "Nivel 2", "3": "Nivel 3",
    "4": "Nivel 4", "5": "Nivel 5", "6": "Nivel 6",
}
ORDEN_NIVELES_CERT = ["Preparación B2 First", "Preparación C1 Advanced"]

LEYENDA_PLAN_3 = [
    {"clave": "2016", "titulo": "Plan 2016", "color": "blue",
     "texto": "Para alumnos de plan 2016-2019. 6 créditos. Sí aplica beca."},
    {"clave": "2020", "titulo": "Plan 2020", "color": "none",
     "texto": "Para alumnos de plan 2020, incluyendo quienes cursan el minor en esta lengua. 6 créditos. Sí aplica beca."},
    {"clave": "0creditos", "titulo": "Tercera lengua", "color": "red",
     "texto": "Requisito de titulación (RELI-TINT) o para que la calificación no afecte el promedio. 6 créditos, no aplica beca."},
]
LEYENDA_PLAN_CERT = [
    {"clave": "2016", "titulo": "Plan 2016", "color": "blue", "texto": "Para alumnos de plan 2016-2019."},
    {"clave": "2020", "titulo": "Plan 2020", "color": "none", "texto": "Para alumnos de plan 2020."},
]


def es_valor_valido(valor):
    if pd.isna(valor):
        return False
    return str(valor).strip() not in ("", "No asignado", "nan")


def normalizar_plan(valor):
    v = str(valor).strip().lower()
    if "tercera" in v:
        return "0creditos"
    if "2016" in v:
        return "2016"
    if "2020" in v:
        return "2020"
    return "2020"


def normalizar_modalidad(valor):
    v = str(valor).strip().lower()
    return "Virtual" if "virtual" in v else "Presencial"


def orden_numero_nivel(nombre):
    m = re.search(r"(\d+)", str(nombre))
    return int(m.group(1)) if m else 999


def construir_fila(fila, es_nuevo, con_plan=False):
    base = {
        "nrc": fila["NRC"],
        "claveBanner": fila["ClaveBanner"],
        "materia": fila["NombreMateria"],
        "docente": fila["Docente"],
        "horaInicio": fila["HoraInicio"],
        "horaFin": fila["HoraFin"],
        "dias": fila["Weekdays"],
        "periodo": fila["Fechas"],
        "creditos": fila.get("CreditosAcademicos", ""),
        "modalidad": normalizar_modalidad(fila.get("MetodoInstruccion", "")),
        "estatus": fila.get("Status", ""),
        "notas": "",
        "recordatorio": fila.get("Recordatorio", ""),
        "esNuevo": es_nuevo,
    }
    if con_plan:
        plan_original = fila.get("Plan", "")
        base["plan"] = normalizar_plan(plan_original)
        base["planTexto"] = plan_original
    return base


def agrupar_por_nivel(df_sec, columna_grupo, orden_explicito=None, con_plan=False, nrc_es_nuevo=None):
    niveles = []
    valores = df_sec[columna_grupo].unique().tolist()
    if orden_explicito:
        ordenados = [v for v in orden_explicito if v in valores] + [v for v in valores if v not in orden_explicito]
    else:
        ordenados = sorted(valores, key=orden_numero_nivel)
    for valor in ordenados:
        df_niv = df_sec[df_sec[columna_grupo] == valor]
        filas = [construir_fila(f, nrc_es_nuevo(f["NRC"]), con_plan=con_plan) for _, f in df_niv.iterrows()]
        nombre_mostrado = ETIQUETA_NIVEL_INGLES.get(valor, valor)
        niveles.append({"nombre": nombre_mostrado, "cefr": CEFR_POR_NIVEL_INGLES.get(valor, ""), "filas": filas})
    return niveles


def etiqueta_del_grupo(df_grupo):
    for _, f in df_grupo.iterrows():
        if es_valor_valido(f["NivelEtiqueta"]):
            return f["NivelEtiqueta"]
    return "Nivel"


def agrupar_por_listacruzada(df_sec, con_plan=True, nrc_es_nuevo=None):
    bloques = []
    grupos = df_sec["Key"].unique().tolist()
    for key in grupos:
        df_grupo = df_sec[df_sec["Key"] == key]
        etiqueta = etiqueta_del_grupo(df_grupo)
        filas = [construir_fila(f, nrc_es_nuevo(f["NRC"]), con_plan=con_plan) for _, f in df_grupo.iterrows()]
        bloques.append((etiqueta, filas))

    niveles_por_nombre = {}
    orden_nombres = []
    for nombre, filas in bloques:
        if nombre not in niveles_por_nombre:
            niveles_por_nombre[nombre] = []
            orden_nombres.append(nombre)
        niveles_por_nombre[nombre].extend(filas)

    niveles = [{"nombre": n, "cefr": "", "filas": niveles_por_nombre[n]} for n in orden_nombres]
    niveles.sort(key=lambda n: orden_numero_nivel(n["nombre"]))
    return niveles


def main():
    if len(sys.argv) < 2:
        print("Uso: python excel_to_json.py archivo.xlsx")
        sys.exit(1)

    archivo = sys.argv[1]
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]

    for c in ["Recordatorio", "Plan", "NivelEtiqueta", "ListaCruzada"]:
        if c not in df.columns:
            df[c] = ""

    cols_texto = ["Docente", "NombreMateria", "NivelEtiqueta", "MetodoInstruccion", "Fechas", "Weekdays",
                  "Status", "Recordatorio", "ClaveBanner", "ListaCruzada", "Lengua", "NRC", "Plan"]
    for c in cols_texto:
        if c in df.columns:
            df[c] = df[c].fillna("").astype(str).str.strip()

    df["Key"] = df.apply(
        lambda r: r["ListaCruzada"] if es_valor_valido(r["ListaCruzada"]) else r["NRC"],
        axis=1
    )

    hoy = datetime.now().date()
    try:
        with open("new_tracker.json", "r", encoding="utf-8") as f:
            tracker = json.load(f)
    except FileNotFoundError:
        tracker = {}

    todos_los_nrc_hoy = set(df["NRC"])
    for nrc in todos_los_nrc_hoy:
        if nrc not in tracker:
            tracker[nrc] = hoy.isoformat()
    tracker = {nrc: fecha for nrc, fecha in tracker.items() if nrc in todos_los_nrc_hoy}

    def nrc_es_nuevo(nrc):
        fecha_vista = datetime.fromisoformat(tracker[nrc]).date()
        return (hoy - fecha_vista) <= timedelta(days=DIAS_DE_VIGENCIA_NUEVO)

    secciones_out = []

    def agregar_seccion(key, label, icono, colorMode, mostrarMateria, niveles, leyendaPlan=None):
        if not niveles:
            return
        secciones_out.append({
            "key": key, "label": label, "icono": icono, "colorMode": colorMode,
            "mostrarMateria": mostrarMateria,
            "inicioClases": INICIO_CLASES, "finClases": FIN_CLASES,
            "niveles": niveles, "leyendaPlan": leyendaPlan,
        })

    df_ing = df[df["Lengua"] == "Inglés requisito"]
    df_ing_semana = df_ing[df_ing["Weekdays"] != "6"]
    df_ing_sabado = df_ing[df_ing["Weekdays"] == "6"]

    agregar_seccion(
        "ingles", "Inglés", "🇬🇧", "hora", True,
        agrupar_por_nivel(df_ing_semana, "NivelEtiqueta", ORDEN_NIVELES_INGLES, con_plan=False, nrc_es_nuevo=nrc_es_nuevo)
    )
    agregar_seccion(
        "ingles-sabatino", "Inglés sabatino", "🇬🇧", "none", True,
        agrupar_por_nivel(df_ing_sabado, "NivelEtiqueta", ORDEN_NIVELES_INGLES, con_plan=False, nrc_es_nuevo=nrc_es_nuevo)
    )

    df_cert = df[df["Lengua"] == "Inglés certificación"]
    agregar_seccion(
        "certificaciones", "Inglés certificaciones B2 First y CAE", "🇬🇧", "plan", True,
        agrupar_por_nivel(df_cert, "NivelEtiqueta", ORDEN_NIVELES_CERT, con_plan=True, nrc_es_nuevo=nrc_es_nuevo),
        leyendaPlan=LEYENDA_PLAN_CERT
    )

    for key, label, icono, lengua in [
        ("aleman", "Alemán", "🇩🇪", "Alemán"),
        ("frances", "Francés", "🇫🇷", "Francés"),
        ("italiano", "Italiano", "🇮🇹", "Italiano"),
        ("chino", "Chino", "🇨🇳", "Chino"),
    ]:
        df_l = df[df["Lengua"] == lengua]
        if df_l.empty:
            continue
        agregar_seccion(
            key, label, icono, "plan", True,
            agrupar_por_listacruzada(df_l, con_plan=True, nrc_es_nuevo=nrc_es_nuevo),
            leyendaPlan=LEYENDA_PLAN_3
        )

    salida = {"generado": datetime.now().isoformat(), "secciones": secciones_out}

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    with open("new_tracker.json", "w", encoding="utf-8") as f:
        json.dump(tracker, f, ensure_ascii=False, indent=2)

    print(f"data.json generado con {len(todos_los_nrc_hoy)} NRC en {len(secciones_out)} secciones.")


if __name__ == "__main__":
    main()
