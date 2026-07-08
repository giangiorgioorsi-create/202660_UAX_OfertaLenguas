"""
Convierte el Excel de oferta de lenguas (formato Banner) a data.json
para la página estática del Centro de Lenguas.

Uso:
    python excel_to_json.py archivo.xlsx

Genera:
    data.json         -> datos para la página (se sobreescribe cada vez)
    new_tracker.json   -> historial de "primera vez visto" por NRC (persiste)
"""

import sys
import json
from datetime import datetime, timedelta
import pandas as pd

DIAS_DE_VIGENCIA_NUEVO = 7

NIVELES_INGLES_ORDEN = [
    "Elementary A", "Pre-Intermediate A", "Intermediate A", "Upper Intermediate A"
]
CEFR_POR_NIVEL = {
    "Elementary A": "A1",
    "Pre-Intermediate A": "A2",
    "Intermediate A": "B1",
    "Upper Intermediate A": "B1+",
}

SECCIONES = [
    {"key": "ingles", "label": "Inglés", "lengua": "Inglés requisito LV", "tipo": "niveles"},
    {"key": "ingles-sabatino", "label": "Inglés sabatino", "lengua": "Inglés requisito SAB", "tipo": "plano"},
    {"key": "certificaciones", "label": "Inglés certificaciones B2 First y CAE", "lengua": "Inglés certificación", "tipo": "plano"},
    {"key": "aleman", "label": "Alemán", "lengua": "Alemán", "tipo": "plano"},
    {"key": "chino", "label": "Chino", "lengua": "Chino", "tipo": "plano"},
    {"key": "frances", "label": "Francés", "lengua": "Francés", "tipo": "plano"},
    {"key": "italiano", "label": "Italiano", "lengua": "Italiano", "tipo": "plano"},
]


def es_valor_valido(valor):
    if pd.isna(valor):
        return False
    return str(valor).strip() not in ("", "No asignado", "nan")


def cargar_tracker(ruta="new_tracker.json"):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def guardar_tracker(tracker, ruta="new_tracker.json"):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(tracker, f, ensure_ascii=False, indent=2)


def construir_curso(fila, grupo, es_nuevo):
    return {
        "nrcs": [n["NRC"] for _, n in grupo.iterrows()],
        "clavesBanner": [n["ClaveBanner"] for _, n in grupo.iterrows()],
        "materia": fila["NombreMateria"],
        "docente": fila["Docente"],
        "horario": f"{fila['HoraInicio']} - {fila['HoraFin']}",
        "dias": fila["Weekdays"],
        "periodo": fila["Fechas"],
        "creditos": fila.get("CreditosAcademicos", ""),
        "modalidad": fila.get("MetodoInstruccion", ""),
        "estatus": fila.get("Status", ""),
        "notas": fila.get("Notas", ""),
        "recordatorio": fila.get("Recordatorio", ""),
        "esNuevo": es_nuevo,
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python excel_to_json.py archivo.xlsx")
        sys.exit(1)

    archivo = sys.argv[1]
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]

    if "Recordatorio" not in df.columns:
        df["Recordatorio"] = ""

    cols_texto = ["Docente", "NombreMateria", "MetodoInstruccion", "Fechas", "Weekdays",
                  "Status", "Notas", "Recordatorio", "ClaveBanner", "ListaCruzada", "Lengua", "NRC"]
    for c in cols_texto:
        if c in df.columns:
            df[c] = df[c].fillna("").str.strip()

    df["Key"] = df.apply(
        lambda r: r["ListaCruzada"] if es_valor_valido(r["ListaCruzada"]) else r["NRC"],
        axis=1
    )

    hoy = datetime.now().date()
    tracker = cargar_tracker()
    todos_los_nrc_hoy = set(df["NRC"])

    for nrc in todos_los_nrc_hoy:
        if nrc not in tracker:
            tracker[nrc] = hoy.isoformat()

    tracker = {nrc: fecha for nrc, fecha in tracker.items() if nrc in todos_los_nrc_hoy}

    def nrc_es_nuevo(nrc):
        fecha_vista = datetime.fromisoformat(tracker[nrc]).date()
        return (hoy - fecha_vista) <= timedelta(days=DIAS_DE_VIGENCIA_NUEVO)

    salida = {"generado": datetime.now().isoformat(), "secciones": []}

    for sec in SECCIONES:
        df_sec = df[df["Lengua"] == sec["lengua"]]
        if df_sec.empty:
            continue

        if sec["tipo"] == "niveles":
            niveles = []
            nombres_presentes = [n for n in NIVELES_INGLES_ORDEN if n in df_sec["NombreMateria"].unique()]
            otros = [n for n in df_sec["NombreMateria"].unique() if n not in NIVELES_INGLES_ORDEN]
            for nombre in nombres_presentes + otros:
                df_niv = df_sec[df_sec["NombreMateria"] == nombre]
                cursos = []
                for _, fila in df_niv.drop_duplicates(subset=["Key"]).iterrows():
                    grupo = df[df["ListaCruzada"] == fila["ListaCruzada"]] if es_valor_valido(fila["ListaCruzada"]) else df[df["NRC"] == fila["NRC"]]
                    es_nuevo = any(nrc_es_nuevo(n) for n in grupo["NRC"])
                    cursos.append(construir_curso(fila, grupo, es_nuevo))
                niveles.append({"nombre": nombre, "cefr": CEFR_POR_NIVEL.get(nombre, ""), "cursos": cursos})
            salida["secciones"].append({"key": sec["key"], "label": sec["label"], "tipo": "niveles", "niveles": niveles})
        else:
            cursos = []
            for nombre in sorted(df_sec["NombreMateria"].unique()):
                df_mat = df_sec[df_sec["NombreMateria"] == nombre]
                for _, fila in df_mat.drop_duplicates(subset=["Key"]).iterrows():
                    grupo = df[df["ListaCruzada"] == fila["ListaCruzada"]] if es_valor_valido(fila["ListaCruzada"]) else df[df["NRC"] == fila["NRC"]]
                    es_nuevo = any(nrc_es_nuevo(n) for n in grupo["NRC"])
                    cursos.append(construir_curso(fila, grupo, es_nuevo))
            salida["secciones"].append({"key": sec["key"], "label": sec["label"], "tipo": "plano", "cursos": cursos})

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    guardar_tracker(tracker)
    print(f"data.json generado con {len(todos_los_nrc_hoy)} NRC.")


if __name__ == "__main__":
    main()
