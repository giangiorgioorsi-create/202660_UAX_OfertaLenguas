import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- BLOQUEO AGRESIVO DE TEMA (FONDO BLANCO / TEXTO NEGRO) ---
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
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #FF6600 !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] summary p { color: #1A1A1A !important; font-weight: bold !important; }
    [data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p { color: #1A1A1A !important; }
    
    .course-card {
        border: 2px solid #FF6600;
        border-radius: 12px;
        padding: 20px;
        background-color: #FFFFFF;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .course-card h3, .course-card p { color: #1A1A1A !important; }
    .nrc-tag {
        background-color: #FF6600;
        color: #FFFFFF;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
    }
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        border: 2px solid #FF6600 !important;
        color: #1A1A1A !important;
    }
    /* Estilo para el input de texto */
    input { color: #1A1A1A !important; }
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

    tab_inicio, tab_buscar = st.tabs(["🏠 Inicio y Guía", "🔍 Buscador de Cursos"])

    with tab_inicio:
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas", df['Lengua'].nunique())
        c2.metric("Total Grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())
        st.divider()
        cola, colb = st.columns([2, 1])
        with cola:
            st.markdown("### 📝 Guía de Inscripción")
            st.write("1. Localiza tu curso usando el buscador por NRC o los filtros por idioma.")
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

    with tab_buscar:
        if 'rk' not in st.session_state: st.session_state.rk = 0
        st.sidebar.header("Búsqueda Directa")
        
        # BUSCADOR TEXTUAL POR NRC
        nrc_input = st.sidebar.text_input("🔍 Ingresa el NRC", key=f"nrc_{st.session_state.rk}", help="Escribe los 5 dígitos del NRC")
        
        st.sidebar.divider()
        st.sidebar.header("Filtros por Idioma")
        
        # Lógica de filtrado
        df_final = df.copy()
        
        if nrc_input:
            # Si el usuario escribe algo, filtramos por NRC
            df_final = df_final[df_final['NRC'].str.contains(nrc_input, na=False)]
        else:
            # Si no hay NRC, usamos los filtros en cascada
            idi = st.sidebar.selectbox("1. Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"i{st.session_state.rk}")
            if idi:
                df_final = df_final[df_final['Lengua'] == idi]
                mat = st.sidebar.selectbox("2. Materia", [""] + sorted(df_final['NombreMateria'].unique().tolist()), key=f"m{st.session_state.rk}")
                if mat:
                    df_final = df_final[df_final['NombreMateria'] == mat]
                    met = st.sidebar.selectbox("3. Modalidad", [""] + sorted(df_final['MetodoInstruccion'].unique().tolist()), key=f"e{st.session_state.rk}")
                    if met:
                        df_final = df_final[df_final['MetodoInstruccion'] == met]
                        fec = st.sidebar.selectbox("4. Periodo", [""] + sorted(df_final['Fechas'].unique().tolist()), key=f"f{st.session_state.rk}")
                        if fec:
                            df_final = df_final[df_final['Fechas'] == fec]
                            hor = st.sidebar.selectbox("5. Horario", [""] + sorted(df_final['Hora_Ref'].unique().tolist()), key=f"h{st.session_state.rk}")
                            if hor:
                                df_final = df_final[df_final['Hora_Ref'] == hor]

        # Mostrar resultados
        if nrc_input or (not nrc_input and 'hor' in locals() and hor):
            if df_final.empty:
                st.warning("No se encontraron resultados para los criterios seleccionados.")
            else:
                # Agrupamos para mostrar tarjetas maestras (por ListaCruzada o NRC único)
                df_final['Key'] = df_final['ListaCruzada'].fillna(df_final['NRC'])
                for _, fila in df_final.drop_duplicates(subset=['Key']).iterrows():
                    
                    if fila['Recordatorio'] != "No asignado":
                        st.warning(f"🔔 **Recordatorio:** {fila['Recordatorio']}")

                    st.markdown(f"""
                    <div class="course-card">
                        <h3 style="color: #FF6600 !important; margin-top: 0;">{fila['NombreMateria']}</h3>
                        <p style="color: #1A1A1A !important;"><b>Catedrático:</b> {fila['Docente']}<br>
                        <b>Horario:</b> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    lc = df[df['ListaCruzada'] == fila['ListaCruzada']] if pd.notna(fila['ListaCruzada']) and fila['ListaCruzada'] != "No asignado" else df[df['NRC'] == fila['NRC']]
                    cols_nrc = st.columns(min(len(lc), 4))
                    for i, (_, n) in enumerate(lc.iterrows()):
                        with cols_nrc[i % 4]:
                            st.markdown(f"<div class='nrc-tag'>NRC {n['NRC']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<span style='color:#FF6600; font-weight:800;'>{n['ClaveBanner']}</span>", unsafe_allow_html=True)

                    with st.expander("🔍 Detalles Técnicos"):
                        c_a, c_b = st.columns(2)
                        with c_a:
                            st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                            st.write(f"**Fechas:** {fila['Fechas']}")
                        with c_b:
                            st.write(f"**Días:** {fila['Weekdays']}")
                            st.markdown("<div style='background-color:#F1F3F5; padding:10px; border-radius:5px; font-size:0.8em; color:#1A1A1A;'>1:Lu | 2:Ma | 3:Mi | 4:Ju | 5:Vi | 6:Sa | 7:Do</div>", unsafe_allow_html=True)
                        st.info(f"**Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Reiniciar Búsqueda"):
            st.session_state.rk += 1
            st.rerun()

except Exception as e:
    st.error(f"Error de sistema: {e}")
