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
            ### 📝 Guía rápida de inscripción
            1. **Abre la barra lateral:** haz clic en el botón en la parte superior izquierda. 
            2. **Filtra con cuidado:** selecciona idioma, materia y horario.
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

        nrc_input = st.sidebar.text_input("🔍 Buscar por NRC", key=f"nrc_{st.session_state.rk}")
        st.sidebar.divider()

        df_res = df.copy()
        show_results = False

        if nrc_input:
            df_res = df_res[df_res['NRC'].str.contains(nrc_input.strip(), na=False)]
            show_results = True
        else:
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
                # IDENTIFICAR NRCs SELECCIONADOS: Guardamos los NRC que pasaron el filtro
                nrcs_seleccionados = set(df_res['NRC'].unique())

                df_res['Key'] = df_res.apply(
                    lambda r: r['ListaCruzada'] if es_valor_valido(r['ListaCruzada']) else r['NRC'],
                    axis=1
                )

                for _, fila in df_res.drop_duplicates(subset=['Key']).iterrows():

                    if es_valor_valido(fila['ListaCruzada']):
                        lc = df[df['ListaCruzada'] == fila['ListaCruzada']]
                    else:
                        lc = df[df['NRC'] == fila['NRC']]

                    st.markdown(f"""
                    <div class="course-card">
                        <h3>{fila['NombreMateria']}</h3>
                        <p>
                            <b>Docente:</b> {fila['Docente']}<br>
                            <b>Horario:</b> {fila['HoraInicio']} – {fila['HoraFin']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    if es_valor_valido(fila['Recordatorio']):
                        st.markdown(f"""
                        <div class="reminder-box">
                            🔔 <strong>Recordatorio:</strong> {fila['Recordatorio']}
                        </div>
                        """, unsafe_allow_html=True)

                    with st.expander("🔍 Detalles Técnicos"):
                        c_a, c_b = st.columns(2)
                        with c_a:
                            st.write(f"**Créditos académicos:** {fila['CreditosAcademicos']}")
                            st.write(f"**Periodo:** {fila['Fechas']}")
                            st.write(f"**Estatus:** {fila['Status']}")
                            st.divider()
                            st.markdown("**NRC(s) para inscripción:**")
                            
                            # Renderizado de NRCs con resaltado de selección
                            for _, n in lc.iterrows():
                                # Verificamos si este NRC específico es el que el usuario buscó/filtró
                                es_el_buscado = n['NRC'] in nrcs_seleccionados
                                tag_class = "nrc-tag-selected" if es_el_buscado else "nrc-tag"
                                label_seleccion = " <span style='color:#27ae60; font-weight:bold; font-size:0.85em;'>← Tu selección</span>" if es_el_buscado else ""
                                
                                st.markdown(
                                    f"<div style='display:flex; align-items:center; gap:10px; margin-bottom:10px;'>"
                                    f"<div class='{tag_class}'>NRC {n['NRC']}</div>"
                                    f"<div style='display:flex; flex-direction:column;'>"
                                    f"<span style='color:#555; font-size:0.9em;'>Clave Banner: <strong style='color:#FF6600;'>{n['ClaveBanner']}</strong>{label_seleccion}</span>"
                                    f"<span style='color:#888; font-size:0.75em; font-style:italic;'>{n['NombreMateria']}</span>"
                                    f"</div>"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )
                        with c_b:
                            dias_raw = fila['Weekdays'] if fila['Weekdays'] else "No especificado"
                            st.markdown(f"**Días de sesión:** <span style='color:#2ecc71; font-weight:600;'>{dias_raw}</span>", unsafe_allow_html=True)
                            st.markdown("""
                            <div class='legend-box'>
                                <strong>Guía de nomenclatura de días:</strong><br>
                                1: Lunes | 2: Martes | 3: Miércoles | 4: Jueves<br>
                                5: Viernes | 6: Sábado | 7: Domingo
                            </div>
                            """, unsafe_allow_html=True)

                        if es_valor_valido(fila['Notas']):
                            st.info(f"📌 **Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Reiniciar"):
            st.session_state.rk += 1
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
