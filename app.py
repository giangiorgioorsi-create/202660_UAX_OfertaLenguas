import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- BLOQUEO TOTAL DE INVISIBILIDAD (TABS Y BOTONES) ---
st.markdown("""
    <style>
    /* 1. Reset General de Fondo y Texto */
    :root {
        --primary-color: #FF6600;
    }
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 2. VISIBILIDAD DE PESTAÑAS (TABS) */
    /* Texto de la pestaña en reposo */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
    }
    button[data-baseweb="tab"] p {
        color: #1A1A1A !important; /* Texto negro permanente */
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    /* Pestaña seleccionada */
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #FF6600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #FF6600 !important; /* Naranja si está activa */
    }

    /* 3. VISIBILIDAD DEL BOTÓN DE REINICIO (RESET) */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important; /* Texto negro */
        border: 1px solid #D3D3D3 !important; /* Borde gris visible */
        border-radius: 8px !important;
        padding: 10px 20px !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }
    /* Hover del botón */
    div.stButton > button:hover {
        border-color: #FF6600 !important;
        color: #FF6600 !important;
        background-color: #FFF5EE !important;
    }

    /* 4. ARREGLO DE MENÚS (SELECTBOXES) */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #FF6600 !important;
    }
    /* Lista de opciones */
    div[role="listbox"] ul {
        background-color: #FFFFFF !important;
    }
    div[role="option"] {
        color: #1A1A1A !important;
    }

    /* 5. Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #EEEEEE !important;
    }

    /* 6. Tarjetas de Cursos */
    .card { 
        border: 2px solid #FF6600 !important; 
        padding: 25px !important; 
        border-radius: 15px !important; 
        background-color: #FFFFFF !important; 
        color: #1A1A1A !important;
        margin-bottom: 25px !important; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    .card h3, .card p, .card strong { color: #1A1A1A !important; }

    .nrc-box { 
        background-color: #FF6600 !important; 
        color: #FFFFFF !important; 
        padding: 8px 15px !important; 
        border-radius: 8px !important; 
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Gestión de Datos
@st.cache_data
def cargar_datos():
    archivo = "202660_UAX_OfertaLenguas.xlsx"
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    columnas_txt = ['Docente', 'NombreMateria', 'MetodoInstruccion', 'Fechas', 'Weekdays', 'Status', 'Notas', 'Recordatorio', 'ClaveBanner']
    for col in columnas_txt:
        if col in df.columns: df[col] = df[col].fillna("No asignado")
    df['Hora_Ref'] = df['HoraInicio'].str.strip()
    return df

try:
    df = cargar_datos()
    st.markdown("<h1 style='color: #FF6600 !important;'>🏛️ Centro de Lenguas — Oferta Académica</h1>", unsafe_allow_html=True)

    tab_inicio, tab_buscar = st.tabs(["🏠 Inicio y Guía", "🔍 Buscador de Cursos"])

    with tab_inicio:
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas", df['Lengua'].nunique())
        c2.metric("Total Grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())
        
        st.divider()
        col_info, col_ayuda = st.columns([2, 1])

        with col_info:
            st.markdown("### 📝 Guía de Inscripción")
            st.write("1. Localiza tu asignatura en el buscador.")
            st.write("2. Verifica que el horario y modalidad se ajusten a tu carga académica.")
            st.write("3. Copia el NRC para realizar el proceso oficial en Banner.")
            
            with st.expander("✨ Mensaje Inspirador"):
                st.info("*'Un idioma diferente es una visión diferente de la vida.'* — Federico Fellini")

        with col_ayuda:
            st.markdown(f"""
            <div style="background-color: #FFF5EE; padding: 20px; border-radius: 12px; border: 1px dashed #FF6600;">
                <h4 style="color: #FF6600 !important; margin-top:0;">🆘 ¿Necesitas Ayuda?</h4>
                <p style="color: #1A1A1A !important;">Si tienes dudas sobre tu nivel o algún NRC:</p>
                <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=l2uNDV3gDEa2tRm30CD0ep7ari_US8VMvJq8b3TFkrRUNlRKSEpGRENUVUk2MFJWTFJaOEU4QzEyOS4u' target='_blank'>
                    <button style='width:100%; padding:12px; background-color:#FF6600; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;'>
                        📝 Formulario de Atención
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

    with tab_buscar:
        st.sidebar.header("Configuración")
        if 'reset_key' not in st.session_state: st.session_state.reset_key = 0
        
        sel_idioma = st.sidebar.selectbox("1. Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"i{st.session_state.reset_key}")
        
        if sel_idioma:
            df_f = df[df['Lengua'] == sel_idioma]
            sel_materia = st.sidebar.selectbox("2. Asignatura", [""] + sorted(df_f['NombreMateria'].unique().tolist()), key=f"m{st.session_state.reset_key}")
            
            if sel_materia:
                df_f = df_f[df_f['NombreMateria'] == sel_materia]
                sel_metodo = st.sidebar.selectbox("3. Modalidad", [""] + sorted(df_f['MetodoInstruccion'].unique().tolist()), key=f"e{st.session_state.reset_key}")
                
                if sel_metodo:
                    df_f = df_f[df_f['MetodoInstruccion'] == sel_metodo]
                    sel_fecha = st.sidebar.selectbox("4. Periodo", [""] + sorted(df_f['Fechas'].unique().tolist()), key=f"f{st.session_state.reset_key}")
                    
                    if sel_fecha:
                        df_f = df_f[df_f['Fechas'] == sel_fecha]
                        sel_horario = st.sidebar.selectbox("5. Horario", [""] + sorted(df_f['Hora_Ref'].unique().tolist()), key=f"h{st.session_state.reset_key}")
                        
                        if sel_horario:
                            res = df_f[df_f['Hora_Ref'] == sel_horario].copy()
                            res['Key'] = res['ListaCruzada'].fillna(res['NRC'])
                            
                            for _, fila in res.drop_duplicates(subset=['Key']).iterrows():
                                if fila['Recordatorio'] != "No asignado":
                                    st.warning(f"🔔 {fila['Recordatorio']}")

                                st.markdown(f"""
                                <div class="card">
                                    <h3 style="margin-top: 0;">{fila['NombreMateria']}</h3>
                                    <p><strong>Catedrático:</strong> {fila['Docente']}</p>
                                    <p><strong>Horario:</strong> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                                    <hr style="border: 1px solid #FF6600; margin: 15px 0;">
                                """, unsafe_allow_html=True)
                                
                                l_c = df[df['ListaCruzada'] == fila['ListaCruzada']] if pd.notna(fila['ListaCruzada']) and fila['ListaCruzada'] != "No asignado" else df[df['NRC'] == fila['NRC']]
                                cols = st.columns(min(len(l_c), 4))
                                for i, (_, n) in enumerate(l_c.iterrows()):
                                    with cols[i % 4]:
                                        st.markdown(f"<div class='nrc-box'>NRC {n['NRC']}</div>", unsafe_allow_html=True)
                                        st.markdown(f"<span style='color:#FF6600; font-weight:800;'>{n['ClaveBanner']}</span>", unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)

        st.sidebar.divider()
        if st.sidebar.button("🔄 Reiniciar Búsqueda"):
            st.session_state.reset_key += 1
            st.rerun()

except Exception as e:
    st.error(f"Error de sistema: {e}")
