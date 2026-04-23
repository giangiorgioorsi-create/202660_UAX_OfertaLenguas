import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
    }
    button[data-baseweb="tab"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #FF6600 !important;
    }
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        border: 2px solid #FF6600 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stAlert"] * {
        color: #1A1A1A !important;
        fill: #FF6600 !important;
    }
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D3D3D3 !important;
        border-radius: 8px !important;
    }
    [data-testid="stExpander"] summary {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    [data-testid="stExpander"] summary p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] * {
        color: #1A1A1A !important;
    }
    .course-card {
        border: 2px solid #FF6600;
        border-radius: 12px;
        padding: 20px;
        background-color: #FFFFFF;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .course-card h3 { color: #FF6600 !important; margin-top: 0; }
    .course-card p, .course-card b, .course-card strong { color: #1A1A1A !important; }
    .reminder-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FF6600;
        border-radius: 6px;
        padding: 10px 14px;
        margin-top: 10px;
        color: #1A1A1A !important;
        font-size: 0.92em;
    }
    .nrc-tag {
        background-color: #FF6600;
        color: #FFFFFF;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
    }
    /* NUEVO: Estilo para el NRC seleccionado */
    .nrc-tag-selected {
        background-color: #2ecc71 !important;
        color: #FFFFFF !important;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid #27ae60;
    }
    .legend-box {
        background-color: #F1F3F5;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.85em;
        color: #1A1A1A;
        border-left: 4px solid #FF6600;
        margin-top: 6px;
    }
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #D3D3D3 !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)


def es_valor_valido(valor):
    """Devuelve True si el valor tiene contenido real (no es NaN, vacío ni 'No asignado')."""
    if pd.isna(valor):
        return False
    return str(valor).strip() not in ("", "No asignado", "nan")


@st.cache_data(ttl=60)
def cargar_datos():
    archivo = "202660_UAX_OfertaLenguas.xlsx"
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]

    if 'Recordatorio' not in df.columns:
        df['Recordatorio'] = ""

    cols_texto = ['Docente', 'NombreMateria', 'MetodoInstruccion', 'Fechas',
                  'Weekdays', 'Status', 'Notas', 'Recordatorio', 'ClaveBanner', 'ListaCruzada']
    for c in cols_texto:
        if c in df.columns:
            df[c] = df[c].fillna("").str.strip()

    df['Hora_Ref'] = df['HoraInicio'].str.strip()
    return df


try:
    df = cargar_datos()
    st.markdown("<h1 style='color: #FF6600 !important;'>🏛️ Centro de Lenguas UAX — Oferta Académica 202660</h1>", unsafe_allow_html=True)

    t1, t2 = st.tabs(["🏠 Inicio y Guía", "🔍 Buscador de Cursos"])

    with t1:
        cola, colb = st.columns([2, 1])
        with cola:
           st.markdown("""
            ### 📝 Guía rápida de planificación
            1. **Abre la barra lateral:** haz clic en el botón en la parte superior izquierda, te aparecerá una barra lateral. 
            2. **Filtra con cuidado:** selecciona entre las opciones propuestas.
            3. **Conoce los detalles:** ve a la pestaña 'Buscador de Cursos'.
            4. **Verifica los datos:** toma nota del NRC y de la Clave Banner.
            5. **Listas Cruzadas:** si tu curso tiene varios NRC, elige el que corresponde a tu plan de estudios.
            6. **Planifica en Banner:** agrega el curso a tu planificación a través del SIU.
            """)
           with st.expander("✨ Un mensaje para tu camino"):
                 st.info("*'Un idioma diferente es una visión diferente de la vida.'* — Federico Fellini")
                 st.write("Aprender una lengua abre puertas no solo profesionales, sino humanas. ¡Mucho éxito en tu elección!")

        with colb:
            st.markdown(f"""
            <div style="background-color: #FFF5EE; padding: 25px; border-radius: 12px; border: 1px dashed #FF6600;">
                <h4 style="color: #FF6600 !important; margin-top:0;">🆘 Soporte</h4>
                <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=l2uNDV3gDEa2tRm30CD0ep7ari_US8VMvJq8b3TFkrRUNlRKSEpGRENUVUk2MFJWTFJaOEU4QzEyOS4u' target='_blank'>
                    <button style='width:100%; padding:12px; background-color:#FF6600; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;'>
                        Abrir Formulario
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

    with t2:
        if 'rk' not in st.session_state:
            st.session_state.rk = 0
        st.sidebar.header("Búsqueda")

        nrc_input =
