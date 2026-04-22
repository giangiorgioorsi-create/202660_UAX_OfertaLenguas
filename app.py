import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- BLOQUEO TOTAL DE TEMA (FONDO BLANCO / TEXTO NEGRO) ---
st.markdown("""
    <style>
    /* Reset Global */
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    /* Barra Lateral */
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
    }
    /* Tarjetas de Cursos */
    .card { 
        border: 2px solid #FF6600 !important; 
        padding: 25px !important; 
        border-radius: 15px !important; 
        background-color: #FFFFFF !important; 
        color: #1A1A1A !important;
        margin-bottom: 25px !important; 
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05) !important;
    }
    /* Forzado de texto negro en todo lugar */
    h1, h2, h3, h4, h5, h6, p, span, label, strong, li {
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
        # SECCIÓN PROMOCIONAL Y MÉTRICAS
        st.subheader("Bienvenido al Portal de Consulta")
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas Ofertados", df['Lengua'].nunique())
        c2.metric("Total de Grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())

        st.divider()

        col_info, col_ayuda = st.columns([2, 1])

        with col_info:
            st.markdown("""
            ### 📝 Guía Rápida de Inscripción
            1. **Encuentra tu curso:** Ve a la pestaña 'Buscador de Cursos'.
            2. **Filtra con cuidado:** Selecciona idioma, materia y horario.
            3. **Verifica el NRC:** Toma nota del número de 5 dígitos (NRC) y la Clave Banner.
            4. **Listas Cruzadas:** Si tu curso tiene varios NRC, asegúrate de elegir el que corresponde a tu plan de estudios.
            5. **Inscribe en Banner:** Realiza el proceso oficial en el portal de alumnos.
            """)
            
            with st.expander("📌 Avisos Importantes del Periodo"):
                st.info("Recuerda que las bajas de materias tienen fechas límite. Consulta el calendario académico.")
                st.warning("Los grupos con menos de 10 inscritos están sujetos a cambios.")

        with col_ayuda:
            st.markdown("""
            <div class='help-card'>
                <h4 style='margin-top:0;'>🆘 ¿Necesitas Ayuda?</h4>
                <p>Si tienes problemas con un NRC o no encuentras tu nivel:</p>
                <a href='mailto:lenguas.xalapa@anahuac.mx' style='text-decoration:none;'>
                    <button style='width:100%; padding:10px; background-color:#FF6600; color:white; border:none; border-radius:5px; cursor:pointer;'>
                        📧 Contactar por Correo
                    </button>
                </a>
                <br><br>
                <p style='font-size:0.8em; text-align:center;'>Horario de atención:<br>Lunes a Viernes 9:00 - 18:00 hrs</p>
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
