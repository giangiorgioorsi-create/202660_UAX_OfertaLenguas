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

GRUPO_NIVEL_INGLES = {
    "0A": "Propedéutico Elementary", "0B": "Propedéutico Elementary",
    "1": "Pre Intermediate", "2": "Pre Intermediate",
    "3": "Intermediate", "4": "Intermediate",
    "5": "Upper Intermediate", "6": "Upper Intermediate",
}
PARTE_POR_NIVEL = {
    "0A": "A", "1": "A", "3": "A", "5": "A",
    "0B": "B", "2": "B", "4": "B", "6": "B",
}
ORDEN_GRUPOS_INGLES = ["Propedéutico Elementary", "Pre Intermediate", "Intermediate", "Upper Intermediate"]
CEFR_POR_GRUPO_INGLES = {
    "Propedéutico Elementary": "Pre-A1",
    "Pre Intermediate": "A2",
    "Intermediate": "B1",
    "Upper Intermediate": "B2",
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


def construir_fila(fila, es_nuevo, con_plan=False, con_parte=False):
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
    if con_parte:
        base["parte"] = PARTE_POR_NIVEL.get(fila.get("NivelEtiqueta", ""), "")
    return base


def agrupar_ingles(df_sec, nrc_es_nuevo):
    df_sec = df_sec.copy()
    df_sec["_grupo"] = df_sec["NivelEtiqueta"].map(GRUPO_NIVEL_INGLES).fillna(df_sec["NombreMateria"])
    niveles = []
    grupos_presentes = [g for g in ORDEN_GRUPOS_INGLES if g in df_sec["_grupo"].unique()]
    otros = [g for g in df_sec["_grupo"].unique() if g not in ORDEN_GRUPOS_INGLES]
    for grupo in grupos_presentes + otros:
        df_niv = df_sec[df_sec["_grupo"] == grupo].sort_values(by=["Docente", "HoraInicio", "NivelEtiqueta"])
        filas = [construir_fila(f, nrc_es_nuevo(f["NRC"]), con_parte=True) for _, f in df_niv.iterrows()]
        niveles.append({"nombre": grupo, "cefr": CEFR_POR_GRUPO_INGLES.get(grupo, ""), "filas": filas})
    return niveles


def agrupar_certificaciones(df_sec, orden_explicito, nrc_es_nuevo):
    niveles = []
    valores = df_sec["NivelEtiqueta"].unique().tolist()
    ordenados = [v for v in orden_explicito if v in valores] + [v for v in valores if v not in orden_explicito]
    for valor in ordenados:
        df_niv = df_sec[df_sec["NivelEtiqueta"] == valor]
        filas = [construir_fila(f, nrc_es_nuevo(f["NRC"]), con_plan=True) for _, f in df_niv.iterrows()]
        niveles.append({"nombre": valor, "cefr": "", "filas": filas})
    return niveles


def agrupar_sabatino(df_sec, nrc_es_nuevo):
    niveles = []
    orden = [n for n in df_sec["NombreMateria"].unique()]
    for nombre in orden:
        df_niv = df_sec[df_sec["NombreMateria"] == nombre]
        filas = [construir_fila(f, nrc_es_nuevo(f["NRC"])) for _, f in df_niv.iterrows()]
        niveles.append({"nombre": nombre, "cefr": "", "filas": filas})
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
        "ingles", "Inglés", "🇬🇧", "hora", False,
        agrupar_ingles(df_ing_semana, nrc_es_nuevo)
    )
    agregar_seccion(
        "ingles-sabatino", "Inglés sabatino", "🇬🇧", "none", False,
        agrupar_sabatino(df_ing_sabado, nrc_es_nuevo)
    )

    df_cert = df[df["Lengua"] == "Inglés certificación"]
    agregar_seccion(
        "certificaciones", "Inglés certificaciones B2 First y CAE", "🇬🇧", "plan", True,
        agrupar_certificaciones(df_cert, ORDEN_NIVELES_CERT, nrc_es_nuevo),
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
