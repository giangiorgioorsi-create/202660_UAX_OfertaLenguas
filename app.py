import streamlit as st
import pandas as pd

# 1. Configuración de la Plataforma
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- LA SOLUCIÓN NUCLEAR: SOBREESCRITURA DE VARIABLES RAÍZ ---
st.markdown("""
    <style>
    /* 1. Forzamos las variables que Streamlit usa para su tema */
    :root {
        --primary-color: #FF6600;
        --background-color: #FFFFFF;
        --secondary-background-color: #F8F9FA;
        --text-color: #1A1A1A;
        --font: 'Source Sans Pro', sans-serif;
    }

    /* 2. Reset General de Colores */
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 3. Blindaje de la Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }

    /* 4. ARREGLO DE MENÚS (Selectboxes) - Fondo siempre blanco, texto siempre negro */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    
    /* El menú que cae (dropdown) */
    div[role="listbox"] ul {
        background-color: #FFFFFF !important;
    }
    
    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 5. Tarjetas de Cursos Institucionales */
    .card { 
        border: 2px solid #FF6600 !important; 
        padding: 25px !important; 
        border-radius: 15px !important; 
        background-color: #FFFFFF !important; 
        color: #1A1A1A !important;
        margin-bottom: 25px !important; 
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Asegurar que el texto dentro de la card sea negro */
    .card h3, .card p, .card strong, .card span {
        color: #1A1A1A !important;
    }

    .nrc-box { 
        background-color: #FF6600 !important; 
        color: #FFFFFF !important; 
        padding: 8px 15px !important; 
        border-radius: 8px !important; 
        font-weight: bold !important;
    }
    
    .help-card {
        background-color: #FFF5EE !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px dashed #FF6600 !important;
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
    st.markdown("<h1 style='color: #FF6600 !important;'>🏛️ Centro de Lenguas — Ciclo 2026-60</h1>", unsafe_allow_html=True)

    tab_inicio, tab_buscar = st.tabs(["🏠 Inicio", "🔍 Buscador"])

    with tab_inicio:
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas", df['Lengua'].nunique())
        c2.metric("Grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())
        
        st.divider()
        col_info, col_ayuda = st.columns([2, 1])

        with col_info:
            st.markdown("### 📝 Guía de Inscripción")
            st.write("1. Busca tu NRC en la siguiente pestaña.")
            st.write("2. Verifica que la modalidad coincida con tu horario.")
            with st.expander("✨ Mensaje de la Coordinación"):
                st.info("*'Un idioma diferente es una visión diferente de la vida.'* — Federico Fellini")

        with col_ayuda:
            st.markdown(f"""
            <div class='help-card'>
                <h4>🆘 ¿Dudas?</h4>
                <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=l2uNDV3gDEa2tRm30CD0ep7ari_US8VMvJq8b3TFkrRUNlRKSEpGRENUVUk2MFJWTFJaOEU4QzEyOS4u' target='_blank'>
                    <button style='width:100%; padding:12px; background-color:#FF6600; color:white; border:none; border-radius:8px; cursor:pointer;'>
                        Formulario de Atención
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

    with tab_buscar:
        st.sidebar.header("Filtros")
        if 'reset' not in st.session_state: st.session_state.reset = 0
        
        sel_idioma = st.sidebar.selectbox("1. Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"i{st.session_state.reset}")
        
        if sel_idioma:
            df_f = df[df['Lengua'] == sel_idioma]
            sel_materia = st.sidebar.selectbox("2. Asignatura", [""] + sorted(df_f['NombreMateria'].unique().tolist()), key=f"m{st.session_state.reset}")
            
            if sel_materia:
                df_f = df_f[df_f['NombreMateria'] == sel_materia]
                sel_metodo = st.sidebar.selectbox("3. Modalidad", [""] + sorted(df_f['MetodoInstruccion'].unique().tolist()), key=f"e{st.session_state.reset}")
                
                if sel_metodo:
                    df_f = df_f[df_f['MetodoInstruccion'] == sel_metodo]
                    sel_fecha = st.sidebar.selectbox("4. Fechas", [""] + sorted(df_f['Fechas'].unique().tolist()), key=f"f{st.session_state.reset}")
                    
                    if sel_fecha:
                        df_f = df_f[df_f['Fechas'] == sel_fecha]
                        sel_horario = st.sidebar.selectbox("5. Horario", [""] + sorted(df_f['Hora_Ref'].unique().tolist()), key=f"h{st.session_state.reset}")
                        
                        if sel_horario:
                            res = df_f[df_f['Hora_Ref'] == sel_horario].copy()
                            res['Key'] = res['ListaCruzada'].fillna(res['NRC'])
                            
                            for _, fila in res.drop_duplicates(subset=['Key']).iterrows():
                                if fila['Recordatorio'] != "No asignado":
                                    st.warning(f"🔔 {fila['Recordatorio']}")

                                st.markdown(f"""
                                <div class="card">
                                    <h3 style="color: #FF6600 !important;">{fila['NombreMateria']}</h3>
                                    <p><strong>Docente:</strong> {fila['Docente']}</p>
                                    <p><strong>Horario:</strong> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                                    <hr style="border: 1px solid #FF6600;">
                                    <p><b>NRC(s) Disponibles:</b></p>
                                """, unsafe_allow_html=True)
                                
                                # Mostramos los NRCs
                                l_c = df[df['ListaCruzada'] == fila['ListaCruzada']] if pd.notna(fila['ListaCruzada']) and fila['ListaCruzada'] != "No asignado" else df[df['NRC'] == fila['NRC']]
                                cols = st.columns(min(len(l_c), 4))
                                for i, (_, n) in enumerate(l_c.iterrows()):
                                    with cols[i % 4]:
                                        st.markdown(f"<div class='nrc-box'>NRC {n['NRC']}</div>", unsafe_allow_html=True)
                                        st.markdown(f"<span style='color:#FF6600; font-weight:bold;'>{n['ClaveBanner']}</span>", unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)

        if st.sidebar.button("🔄 Limpiar"):
            st.session_state.reset += 1
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
