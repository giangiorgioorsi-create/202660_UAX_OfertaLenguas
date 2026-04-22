import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- BLOQUEO AGRESIVO DE TEMA (PARA MENÚS Y SELECTBOXES) ---
st.markdown("""
    <style>
    /* 1. Fondo global y texto base */
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 2. FORZAR VISIBILIDAD EN MENÚS DESPLEGABLES (Selectboxes) */
    /* Caja del menú */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #FF6600 !important;
    }
    
    /* Lista de opciones (el menú que cae) */
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
    }
    
    /* Elementos individuales de la lista */
    li[data-baseweb="menu-item"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    
    /* Hover (cuando pasas el mouse por las opciones) */
    li[data-baseweb="menu-item"]:hover {
        background-color: #FF6600 !important;
        color: #FFFFFF !important;
    }

    /* Etiquetas de los filtros en la barra lateral */
    [data-testid="stSidebar"] label {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }

    /* 3. Estilo de las Tarjetas de Cursos */
    .card { 
        border: 2px solid #FF6600 !important; 
        padding: 25px !important; 
        border-radius: 15px !important; 
        background-color: #FFFFFF !important; 
        color: #1A1A1A !important;
        margin-bottom: 25px !important; 
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05) !important;
    }
    
    /* Forzado general de color en títulos y párrafos */
    h1, h2, h3, h4, h5, h6, p, span, strong, li, small {
        color: #1A1A1A !important;
    }

    .nrc-box { 
        background-color: #FF6600 !important; 
        color: #FFFFFF !important; 
        padding: 8px 15px !important; 
        border-radius: 8px !important; 
        font-weight: bold !important;
        display: inline-block !important;
    }
    
    .banner-text { color: #FF6600 !important; font-weight: 800 !important; }

    .help-card {
        background-color: #FFF5EE !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px dashed #FF6600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'reset_cnt' not in st.session_state: st.session_state.reset_cnt = 0
def clean_reset(): st.session_state.reset_cnt += 1

@st.cache_data
def cargar_datos():
    archivo = "202660_UAX_OfertaLenguas.xlsx"
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    for col in ['Docente', 'NombreMateria', 'MetodoInstruccion', 'Fechas', 'Weekdays', 'Status', 'Notas', 'Recordatorio', 'ClaveBanner']:
        if col in df.columns: df[col] = df[col].fillna("No asignado")
    df['Hora_Ref'] = df['HoraInicio'].str.strip()
    return df

try:
    df = cargar_datos()
    st.markdown("<h1 style='color: #FF6600 !important;'>🏛️ Centro de Lenguas — Oferta Académica 2026-60</h1>", unsafe_allow_html=True)

    tab_inicio, tab_buscar = st.tabs(["🏠 Inicio y Guía", "🔍 Buscador de Cursos"])

    with tab_inicio:
        st.subheader("Bienvenid@ al portal de consulta")
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas ofertados", df['Lengua'].nunique())
        c2.metric("Total de grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())

        st.divider()

        col_info, col_ayuda = st.columns([2, 1])

        with col_info:
            st.markdown("""
            ### 📝 Guía Rápida de planificación/inscripción
            1. **Encuentra tu curso:** ve a la pestaña 'Buscador de Cursos'.
            2. **Filtra con cuidado:** selecciona idioma, materia y horario.
            3. **Verifica el NRC:** toma nota del número de 5 dígitos (NRC) y la Clave Banner.
            4. **Listas cruzadas:** si tu curso tiene varios NRC, elige el que corresponde a tu plan de estudios.
            5. **Planifica e inscribe en Banner:** realiza el proceso en el SIU.
            """)
            
            with st.expander("✨ Un mensaje para tu camino"):
                # Frase inspiradora solicitada
                st.info("*'Un idioma diferente es una visión diferente de la vida.'* — Federico Fellini")
                st.write("Aprender una lengua abre puertas no solo profesionales, sino humanas. ¡Mucho éxito en tu elección!")

        with col_ayuda:
            # Enlace actualizado al formulario de Microsoft Forms
            st.markdown("""
            <div class='help-card'>
                <h4 style='margin-top:0;'>🆘 ¿Necesitas Ayuda?</h4>
                <p>Si tienes problemas con un NRC, dudas de niveles o requieres atención personalizada:</p>
                <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=l2uNDV3gDEa2tRm30CD0ep7ari_US8VMvJq8b3TFkrRUNlRKSEpGRENUVUk2MFJWTFJaOEU4QzEyOS4u' target='_blank' style='text-decoration:none;'>
                    <button style='width:100%; padding:12px; background-color:#FF6600; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;'>
                        📝 Formulario de atención
                    </button>
                </a>
                <br><br>
                <p style='font-size:0.8em; text-align:center;'>Horario de atención de la Coordinación:<br>Lunes a Viernes 08:30 - 14:30 y 16:30 - 19:00 hrs</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_buscar:
        st.sidebar.header("Filtros")
        sel_idioma = st.sidebar.selectbox("1. Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"i_{st.session_state.reset_cnt}")
        
        if sel_idioma:
            df_f = df[df['Lengua'] == sel_idioma]
            sel_materia = st.sidebar.selectbox("2. Asignatura", [""] + sorted(df_f['NombreMateria'].unique().tolist()), key=f"m_{st.session_state.reset_cnt}")
            
            if sel_materia:
                df_f = df_f[df_f['NombreMateria'] == sel_materia]
                sel_metodo = st.sidebar.selectbox("3. Modalidad", [""] + sorted(df_f['MetodoInstruccion'].unique().tolist()), key=f"me_{st.session_state.reset_cnt}")
                
                if sel_metodo:
                    df_f = df_f[df_f['MetodoInstruccion'] == sel_metodo]
                    sel_fecha = st.sidebar.selectbox("4. Fechas", [""] + sorted(df_f['Fechas'].unique().tolist()), key=f"f_{st.session_state.reset_cnt}")
                    
                    if sel_fecha:
                        df_f = df_f[df_f['Fechas'] == sel_fecha]
                        sel_horario = st.sidebar.selectbox("5. Horario", [""] + sorted(df_f['Hora_Ref'].unique().tolist()), key=f"h_{st.session_state.reset_cnt}")
                        
                        if sel_horario:
                            res = df_f[df_f['Hora_Ref'] == sel_horario].copy()
                            res['GroupKey'] = res['ListaCruzada'].fillna(res['NRC'])
                            
                            for _, fila in res.drop_duplicates(subset=['GroupKey']).iterrows():
                                id_cruzada = fila['ListaCruzada']
                                if pd.notna(id_cruzada) and id_cruzada != "No asignado":
                                    cruzados = df[df['ListaCruzada'] == id_cruzada]
                                    es_cruzada = True
                                else:
                                    cruzados = df[df['NRC'] == fila['NRC']]
                                    es_cruzada = False

                                if fila['Recordatorio'] != "No asignado":
                                    st.warning(f"🔔 **Recordatorio:** {fila['Recordatorio']}")

                                st.markdown(f"""
                                <div class="card">
                                    <h3 style="color: #FF6600 !important; margin-top: 0;">{fila['NombreMateria']}</h3>
                                    <p><strong>Catedrático:</strong> {fila['Docente']}</p>
                                    <p><strong>Horario:</strong> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                                    <hr style="border: 1px solid #FF6600; margin: 15px 0;">
                                    <p style="font-weight: bold; margin-bottom: 10px;">
                                        {"NRCs para inscripción (Lista Cruzada):" if es_cruzada else "NRC para inscripción:"}
                                    </p>
                                """, unsafe_allow_html=True)
                                
                                cols = st.columns(min(len(cruzados), 4))
                                for i, (_, n_d) in enumerate(cruzados.iterrows()):
                                    with cols[i % 4]:
                                        st.markdown(f"<div class='nrc-box'>NRC {n_d['NRC']}</div>", unsafe_allow_html=True)
                                        st.markdown(f"<span class='banner-text'>{n_d['ClaveBanner']}</span>", unsafe_allow_html=True)
                                        if es_cruzada: st.markdown(f"<small style='color:#1A1A1A;'>{n_d['NombreMateria']}</small>", unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                with st.expander("🔍 Detalles Técnicos"):
                                    ca, cb = st.columns(2)
                                    with ca:
                                        st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                                        st.write(f"**Fechas:** {fila['Fechas']}")
                                    with cb:
                                        st.write(f"**Días:** {fila['Weekdays']}")
                                        st.markdown("<div class='legend-box'>1:Lu | 2:Ma | 3:Mi | 4:Ju | 5:Vi | 6:Sa | 7:Do</div>", unsafe_allow_html=True)
                                    st.info(f"**Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Reiniciar Filtros", on_click=clean_reset): st.rerun()

except Exception as e:
    st.error(f"⚠️ Error: {e}")
