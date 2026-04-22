import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- BLOQUEO TOTAL DE TEMA Y CONTRASTE (VERSIÓN FINAL) ---
st.markdown("""
    <style>
    /* Reset de variables y fondo global */
    :root { --primary-color: #FF6600; }
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* BARRA LATERAL VISIBLE */
    [data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #EEEEEE !important; }
    [data-testid="stSidebar"] * { color: #1A1A1A !important; }

    /* PESTAÑAS (TABS) VISIBLES */
    button[data-baseweb="tab"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p { color: #FF6600 !important; }

    /* MENÚS DESPLEGABLES (SELECTBOX) */
    div[data-baseweb="select"] > div { background-color: #FFFFFF !important; color: #1A1A1A !important; border: 1px solid #FF6600 !important; }
    div[role="listbox"] ul { background-color: #FFFFFF !important; }
    div[role="option"] { color: #1A1A1A !important; background-color: #FFFFFF !important; }

    /* TARJETA DE CURSO (CARD) */
    .course-card {
        border: 2px solid #FF6600;
        border-radius: 12px;
        padding: 20px;
        background-color: #FFFFFF;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* EXPANDER Y DETALLES (FORZAR VISIBILIDAD) */
    .st-ae summary { color: #1A1A1A !important; font-weight: bold !important; }
    .st-ae div[data-testid="stMarkdownContainer"] p { color: #1A1A1A !important; }
    .st-ae { background-color: #FFFFFF !important; border: 1px solid #EEEEEE !important; border-radius: 8px !important; }

    /* BOTÓN REINICIAR */
    div.stButton > button {
        color: #1A1A1A !important;
        background-color: #FFFFFF !important;
        border: 1px solid #D3D3D3 !important;
        font-weight: bold !important;
        width: 100% !important;
    }

    /* ELEMENTOS DE DISEÑO */
    .nrc-tag {
        background-color: #FF6600;
        color: #FFFFFF;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
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

    t_inicio, t_buscar = st.tabs(["🏠 Inicio y Guía", "🔍 Buscador de Cursos"])

    with t_inicio:
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas", df['Lengua'].nunique())
        c2.metric("Total Grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())
        st.divider()
        cola, colb = st.columns([2, 1])
        with cola:
            st.markdown("### 📝 Guía de Inscripción")
            st.write("1. Busca tu NRC en la pestaña correspondiente.")
            st.write("2. Verifica modalidad y horario.")
            with st.expander("✨ Mensaje de la Coordinación"):
                st.info("*'Un idioma diferente es una visión diferente de la vida.'* — Federico Fellini")
        with colb:
            st.markdown(f"""
            <div style="background-color: #FFF5EE; padding: 20px; border-radius: 12px; border: 1px dashed #FF6600;">
                <h4 style="color: #FF6600 !important; margin-top:0;">🆘 Soporte</h4>
                <p style="color: #1A1A1A !important; font-size: 0.9em;">Dudas de niveles o NRC:</p>
                <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=l2uNDV3gDEa2tRm30CD0ep7ari_US8VMvJq8b3TFkrRUNlRKSEpGRENUVUk2MFJWTFJaOEU4QzEyOS4u' target='_blank'>
                    <button style='width:100%; padding:10px; background-color:#FF6600; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;'>
                        Ir al Formulario
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

    with t_buscar:
        if 'rk' not in st.session_state: st.session_state.rk = 0
        st.sidebar.header("Filtros")
        
        idi = st.sidebar.selectbox("1. Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"i{st.session_state.rk}")
        if idi:
            df1 = df[df['Lengua'] == idi]
            mat = st.sidebar.selectbox("2. Materia", [""] + sorted(df1['NombreMateria'].unique().tolist()), key=f"m{st.session_state.rk}")
            if mat:
                df2 = df1[df1['NombreMateria'] == mat]
                met = st.sidebar.selectbox("3. Modalidad", [""] + sorted(df2['MetodoInstruccion'].unique().tolist()), key=f"e{st.session_state.rk}")
                if met:
                    df3 = df2[df2['MetodoInstruccion'] == met]
                    fec = st.sidebar.selectbox("4. Periodo", [""] + sorted(df3['Fechas'].unique().tolist()), key=f"f{st.session_state.rk}")
                    if fec:
                        df4 = df3[df3['Fechas'] == fec]
                        hor = st.sidebar.selectbox("5. Horario", [""] + sorted(df4['Hora_Ref'].unique().tolist()), key=f"h{st.session_state.rk}")
                        
                        if hor:
                            res = df4[df4['Hora_Ref'] == hor].copy()
                            res['Key'] = res['ListaCruzada'].fillna(res['NRC'])
                            
                            for _, fila in res.drop_duplicates(subset=['Key']).iterrows():
                                if fila['Recordatorio'] != "No asignado": st.warning(f"🔔 {fila['Recordatorio']}")
                                
                                # TARJETA UNIFICADA
                                with st.container():
                                    st.markdown(f"""
                                    <div class="course-card">
                                        <h3 style="color: #FF6600 !important; margin-top:0;">{fila['NombreMateria']}</h3>
                                        <p style="color: #1A1A1A !important;"><b>Catedrático:</b> {fila['Docente']}<br>
                                        <b>Horario:</b> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # NRCs vinculados
                                    lc = df[df['ListaCruzada'] == fila['ListaCruzada']] if pd.notna(fila['ListaCruzada']) and fila['ListaCruzada'] != "No asignado" else df[df['NRC'] == fila['NRC']]
                                    cols_nrc = st.columns(min(len(lc), 4))
                                    for i, (_, n) in enumerate(lc.iterrows()):
                                        with cols_nrc[i % 4]:
                                            st.markdown(f"<div class='nrc-tag'>NRC {n['NRC']}</div>", unsafe_allow_html=True)
                                            st.markdown(f"<span style='color:#FF6600; font-weight:bold;'>{n['ClaveBanner']}</span>", unsafe_allow_html=True)
                                            if len(lc) > 1: st.caption(n['NombreMateria'])

                                    # DETALLES TÉCNICOS (EXPANDER)
                                    with st.expander("🔍 Detalles Técnicos"):
                                        ca, cb = st.columns(2)
                                        with ca:
                                            st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                                            st.write(f"**Fechas:** {fila['Fechas']}")
                                        with cb:
                                            st.write(f"**Días:** {fila['Weekdays']}")
                                            st.markdown("<div style='background-color:#F1F3F5; padding:10px; border-radius:5px; font-size:0.8em; color:#1A1A1A;'>1:Lu | 2:Ma | 3:Mi | 4:Ju | 5:Vi | 6:Sa | 7:Do</div>", unsafe_allow_html=True)
                                        st.info(f"**Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Reiniciar Filtros"):
            st.session_state.rk += 1
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
