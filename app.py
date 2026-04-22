import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- BLOQUEO NUCLEAR DE TEMA (FORZADO DE CONTRASTE TOTAL) ---
st.markdown("""
    <style>
    /* 1. Reset de variables raíz para forzar Tema Claro */
    :root {
        --primary-color: #FF6600;
        --background-color: #FFFFFF;
        --secondary-background-color: #F8F9FA;
        --text-color: #1A1A1A;
    }

    /* 2. Fondo global y texto base */
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 3. ARREGLO PARA ALERTAS (st.warning / st.info) */
    /* Forzamos que el cuadro de advertencia sea legible en cualquier modo */
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        border: 2px solid #FF6600 !important;
        border-radius: 10px !important;
    }
    /* Forzamos el color del texto y del icono dentro de la alerta */
    div[data-testid="stAlert"] * {
        color: #1A1A1A !important;
        fill: #FF6600 !important; /* Color del icono */
    }

    /* 4. ARREGLO PARA EXPANDERS (Detalles Técnicos) */
    /* Contenedor del expander */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D3D3D3 !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
    }
    /* Título del expander (Summary) */
    [data-testid="stExpander"] summary {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    [data-testid="stExpander"] summary p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }
    /* Contenido interno del expander */
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] * {
        color: #1A1A1A !important;
        background-color: transparent !important;
    }

    /* 5. BARRA LATERAL (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #EEEEEE !important;
    }
    [data-testid="stSidebar"] * {
        color: #1A1A1A !important;
    }

    /* 6. TARJETAS DE CURSOS */
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

    /* 7. ETIQUETAS NRC Y BOTONES */
    .nrc-tag {
        background-color: #FF6600;
        color: #FFFFFF;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
    }
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #D3D3D3 !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=60)
def cargar_datos():
    archivo = "202660_UAX_OfertaLenguas.xlsx"
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    cols = ['Docente', 'NombreMateria', 'MetodoInstruccion', 'Fechas', 'Weekdays', 'Status', 'Notas', 'Recordatorio', 'ClaveBanner']
    for c in cols:
        if c in df.columns: df[c] = df[c].fillna("No asignado")
    df['Hora_Ref'] = df['HoraInicio'].str.strip()
    return df

try:
    df = cargar_datos()
    st.markdown("<h1 style='color: #FF6600 !important;'>🏛️ Centro de Lenguas — Oferta Académica</h1>", unsafe_allow_html=True)

    t1, t2 = st.tabs(["🏠 Inicio", "🔍 Buscador"])

    with t1:
        st.subheader("Información General")
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas", df['Lengua'].nunique())
        c2.metric("Total Grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())
        
        st.divider()
        col_inf, col_srv = st.columns([2, 1])
        with col_inf:
            st.markdown("### 📝 Guía de Inscripción")
            st.write("Encuentra tu NRC y Clave Banner para realizar tu proceso oficial.")
            with st.expander("✨ Mensaje de la Coordinación"):
                st.info("*'Un idioma diferente es una visión diferente de la vida.'* — Federico Fellini")

        with col_srv:
            st.markdown(f"""
            <div style="background-color: #FFF5EE; padding: 20px; border-radius: 12px; border: 1px dashed #FF6600;">
                <h4 style="color: #FF6600 !important; margin-top:0;">🆘 Soporte</h4>
                <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=l2uNDV3gDEa2tRm30CD0ep7ari_US8VMvJq8b3TFkrRUNlRKSEpGRENUVUk2MFJWTFJaOEU4QzEyOS4u' target='_blank'>
                    <button style='width:100%; padding:10px; background-color:#FF6600; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%;'>
                        Abrir Formulario
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

    with t2:
        if 'reset' not in st.session_state: st.session_state.reset = 0
        st.sidebar.header("Búsqueda")
        nrc_busq = st.sidebar.text_input("🔍 Buscar por NRC", key=f"n_{st.session_state.reset}")
        
        df_res = df.copy()
        if nrc_busq:
            df_res = df_res[df_res['NRC'].str.contains(nrc_busq, na=False)]
        else:
            idi = st.sidebar.selectbox("Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"i{st.session_state.reset}")
            if idi:
                df_res = df_res[df_res['Lengua'] == idi]
                mat = st.sidebar.selectbox("Asignatura", [""] + sorted(df_res['NombreMateria'].unique().tolist()), key=f"m{st.session_state.reset}")
                if mat:
                    df_res = df_res[df_res['NombreMateria'] == mat]

        if not df_res.empty:
            df_res['Key'] = df_res['ListaCruzada'].fillna(df_res['NRC'])
            for _, fila in df_res.drop_duplicates(subset=['Key']).iterrows():
                if fila['Recordatorio'] != "No asignado":
                    st.warning(f"🔔 **Recordatorio:** {fila['Recordatorio']}")
                
                st.markdown(f"""
                <div class="course-card">
                    <h3>{fila['NombreMateria']}</h3>
                    <p><b>Docente:</b> {fila['Docente']}<br>
                    <b>Horario:</b> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                lc = df[df['ListaCruzada'] == fila['ListaCruzada']] if pd.notna(fila['ListaCruzada']) and fila['ListaCruzada'] != "No asignado" else df[df['NRC'] == fila['NRC']]
                cols = st.columns(min(len(lc), 4))
                for i, (_, n) in enumerate(lc.iterrows()):
                    with cols[i % 4]:
                        st.markdown(f"<div class='nrc-tag'>NRC {n['NRC']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:#FF6600; font-weight:800;'>{n['ClaveBanner']}</span>", unsafe_allow_html=True)

                with st.expander("🔍 Ver Detalles Técnicos"):
                    st.write(f"**Días:** {fila['Weekdays']}")
                    st.write(f"**Periodo:** {fila['Fechas']}")
                    st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                    st.info(f"**Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Reiniciar"):
            st.session_state.reset += 1
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
