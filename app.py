import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- BLOQUEO NUCLEAR DE TEMA (FONDO BLANCO / TEXTO NEGRO) ---
st.markdown("""
    <style>
    /* 1. Fondo Global y Texto Base */
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 2. BARRA LATERAL (SIDEBAR) */
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
    }

    /* 3. PESTAÑAS (TABS) */
    button[data-baseweb="tab"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #FF6600 !important;
    }

    /* 4. ARREGLO PARA ALERTAS (st.warning / st.info) */
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        border: 2px solid #FF6600 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stAlert"] * {
        color: #1A1A1A !important;
        fill: #FF6600 !important;
    }

    /* 5. ARREGLO PARA EXPANDERS (Detalles Técnicos) */
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
        width: 100% !important;
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

    t1, t2 = st.tabs(["🏠 Inicio y Guía", "🔍 Buscador de Cursos"])

    with t1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas", df['Lengua'].nunique())
        c2.metric("Total Grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())
        
        st.divider()
        cola, colb = st.columns([2, 1])
        with cola:
            st.markdown("### 📝 Guía de Inscripción")
            st.write("1. Localiza tu curso usando el buscador por NRC o los filtros.")
            st.write("2. Verifica que el horario y periodo sean los correctos.")
            with st.expander("✨ Mensaje de la Coordinación"):
                st.info("*'Un idioma diferente es una visión diferente de la vida.'* — Federico Fellini")

        with colb:
            st.markdown(f"""
            <div style="background-color: #FFF5EE; padding: 25px; border-radius: 12px; border: 1px dashed #FF6600;">
                <h4 style="color: #FF6600 !important; margin-top:0;">🆘 Soporte</h4>
                <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=l2uNDV3gDEa2tRm30CD0ep7ari_US8VMvJq8b3TFkrRUNlRKSEpGRENUVUk2MFJWTFJaOEU4QzEyOS4u' target='_blank'>
                    <button style='width:100%; padding:12px; background-color:#FF6600; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold; width:100%;'>
                        Abrir Formulario
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

    with t2:
        if 'rk' not in st.session_state: st.session_state.rk = 0
        st.sidebar.header("Búsqueda")
        
        # BUSCADOR POR NRC
        nrc_input = st.sidebar.text_input("🔍 Buscar por NRC", key=f"nrc_{st.session_state.rk}")
        
        st.sidebar.divider()
        
        df_res = df.copy()
        show_results = False

        if nrc_input:
            df_res = df_res[df_res['NRC'].str.contains(nrc_input, na=False)]
            show_results = True
        else:
            # FILTROS EN CASCADA COMPLETOS
            idi = st.sidebar.selectbox("1. Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"i{st.session_state.rk}")
            if idi:
                df_res = df_res[df_res['Lengua'] == idi]
                mat = st.sidebar.selectbox("2. Asignatura", [""] + sorted(df_res['NombreMateria'].unique().tolist()), key=f"m{st.session_state.rk}")
                if mat:
                    df_res = df_res[df_res['NombreMateria'] == mat]
                    met = st.sidebar.selectbox("3. Modalidad", [""] + sorted(df_res['MetodoInstruccion'].unique().tolist()), key=f"e{st.session_state.rk}")
                    if met:
                        df_res = df_res[df_res['MetodoInstruccion'] == met]
                        fec = st.sidebar.selectbox("4. Periodo", [""] + sorted(df_res['Fechas'].unique().tolist()), key=f"f{st.session_state.rk}")
                        if fec:
                            df_res = df_res[df_res['Fechas'] == fec]
                            hor = st.sidebar.selectbox("5. Horario", [""] + sorted(df_res['Hora_Ref'].unique().tolist()), key=f"h{st.session_state.rk}")
                            if hor:
                                df_res = df_res[df_res['Hora_Ref'] == hor]
                                show_results = True

        if show_results:
            if df_res.empty:
                st.warning("No se encontraron resultados para los criterios seleccionados.")
            else:
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

                    with st.expander("🔍 Detalles Técnicos"):
                        c_a, c_b = st.columns(2)
                        with c_a:
                            st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                            st.write(f"**Periodo:** {fila['Fechas']}")
                        with c_b:
                            st.write(f"**Días:** {fila['Weekdays']}")
                            st.markdown("<div style='background-color:#F1F3F5; padding:10px; border-radius:5px; font-size:0.8em; color:#1A1A1A;'>1:Lu | 2:Ma | 3:Mi | 4:Ju | 5:Vi | 6:Sa | 7:Do</div>", unsafe_allow_html=True)
                        st.info(f"**Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Reiniciar"):
            st.session_state.rk += 1
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
