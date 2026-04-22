import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide", initial_sidebar_state="auto")

# --- BLOQUEO NUCLEAR DE TEMA Y OPTIMIZACIÓN MÓVIL ---
st.markdown("""
    <style>
    /* 1. Fondo Global y Texto Base */
    html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 2. OPTIMIZACIÓN MÓVIL: SÚPER BOTÓN DE MENÚ (Floating Action Button) */
    /* Botón para abrir (cuando está cerrado) */
    [data-testid="collapsedControl"] {
        background-color: #FF6600 !important;
        border-radius: 50px !important;
        box-shadow: 0 4px 12px rgba(255, 102, 0, 0.4) !important;
        padding: 5px !important;
        transition: transform 0.2s ease;
        z-index: 999999 !important; /* Siempre al frente */
        /* Ajuste de posición para móviles */
        top: 10px !important;
        left: 10px !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        width: 28px !important; /* Más grande para el dedo */
        height: 28px !important;
    }
    [data-testid="collapsedControl"]:active {
        transform: scale(0.9); /* Efecto de presionar */
    }

    /* Botón para cerrar (dentro de la barra lateral) */
    [data-testid="stSidebarHeader"] button {
        background-color: #EEEEEE !important;
        border: 1px solid #D3D3D3 !important;
        border-radius: 50px !important;
        padding: 5px !important;
    }
    [data-testid="stSidebarHeader"] button svg {
        fill: #1A1A1A !important;
        width: 24px !important;
        height: 24px !important;
    }

    /* 3. BARRA LATERAL (SIDEBAR) */
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
    }

    /* 4. PESTAÑAS (TABS) */
    button[data-baseweb="tab"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
        font-size: 1.1rem !important; /* Más grande para móviles */
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #FF6600 !important;
    }

    /* 5. ARREGLO PARA ALERTAS (st.warning / st.info) */
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        border: 2px solid #FF6600 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stAlert"] * {
        color: #1A1A1A !important;
        fill: #FF6600 !important;
    }

    /* 6. ARREGLO PARA EXPANDERS (Detalles Técnicos) */
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

    /* 7. TARJETAS DE CURSOS */
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

    /* Recordatorio visual */
    .reminder-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FF6600;
        border-radius: 6px;
        padding: 10px 14px;
        margin-top: 10px;
        color: #1A1A1A !important;
        font-size: 0.92em;
    }

    /* 8. ETIQUETAS NRC Y BOTONES */
    .nrc-tag {
        background-color: #FF6600;
        color: #FFFFFF;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
    }
    /* Estilo para el NRC seleccionado */
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
        border: 2px solid #D3D3D3 !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: bold !important;
        padding: 12px !important; /* Más padding para el dedo en móvil */
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
    # Título adaptado a móviles (HTML simple)
    st.markdown("<h2 style='color: #FF6600 !important; text-align: center;'>🏛️ Centro de Lenguas UAX<br><small>Oferta 202660</small></h2>", unsafe_allow_html=True)

    t1, t2 = st.tabs(["🏠 Inicio", "🔍 Buscador"])

    with t1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas", df['Lengua'].nunique())
        c2.metric("Grupos", df['NRC'].count())
        c3.metric("Modalidades", df['MetodoInstruccion'].nunique())

        st.divider()
        cola, colb = st.columns([2, 1])
        with cola:
            st.markdown("""
            ### 📝 Guía Rápida
            1. **Busca tu curso:** Ve a la pestaña 'Buscador'.
            2. **Filtra:** Selecciona idioma, materia y horario.
            3. **NRC:** Anota el número de 5 dígitos (NRC) y la Clave Banner.
            4. **Inscribe:** Realiza el proceso oficial en Anáhuac.
            """)
            with st.expander("✨ Un mensaje para tu camino"):
                st.info("*'Un idioma diferente es una visión diferente de la vida.'* — Federico Fellini")
                st.write("Aprender una lengua abre puertas no solo profesionales, sino humanas. ¡Mucho éxito en tu elección!")

        with colb:
            st.markdown(f"""
            <div style="background-color: #FFF5EE; padding: 25px; border-radius: 12px; border: 1px dashed #FF6600; margin-top: 15px;">
                <h4 style="color: #FF6600 !important; margin-top:0;">🆘 Soporte Técnico</h4>
                <a href='https://forms.office.com/Pages/ResponsePage.aspx?id=l2uNDV3gDEa2tRm30CD0ep7ari_US8VMvJq8b3TFkrRUNlRKSEpGRENUVUk2MFJWTFJaOEU4QzEyOS4u' target='_blank'>
                    <button style='width:100%; padding:14px; background-color:#FF6600; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold; font-size: 1.05em;'>
                        📝 Abrir Formulario
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

    with t2:
        if 'rk' not in st.session_state:
            st.session_state.rk = 0
        
        st.sidebar.markdown("<h3 style='color: #1A1A1A;'>Filtros de Búsqueda</h3>", unsafe_allow_html=True)

        nrc_input = st.sidebar.text_input("🔍 Buscar por NRC directo", key=f"nrc_{st.session_state.rk}")
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
                            🔔 <strong>Aviso:</strong> {fila['Recordatorio']}
                        </div>
                        """, unsafe_allow_html=True)

                    with st.expander("🔍 Detalles Técnicos"):
                        c_a, c_b = st.columns(2)
                        with c_a:
                            st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                            st.write(f"**Fechas:** {fila['Fechas']}")
                            st.write(f"**Estatus:** {fila['Status']}")
                            st.divider()
                            st.markdown("**NRC(s) correspondientes:**")
                            
                            for _, n in lc.iterrows():
                                es_el_buscado = n['NRC'] in nrcs_seleccionados
                                tag_class = "nrc-tag-selected" if es_el_buscado else "nrc-tag"
                                label_seleccion = " <br><span style='color:#27ae60; font-weight:bold; font-size:0.9em;'>← TU SELECCIÓN</span>" if es_el_buscado else ""
                                
                                st.markdown(
                                    f"<div style='display:flex; align-items:flex-start; gap:10px; margin-bottom:12px;'>"
                                    f"<div class='{tag_class}'>NRC {n['NRC']}</div>"
                                    f"<div style='display:flex; flex-direction:column; line-height:1.2;'>"
                                    f"<span style='color:#555; font-size:0.95em;'>Banner: <strong style='color:#FF6600;'>{n['ClaveBanner']}</strong>{label_seleccion}</span>"
                                    f"<span style='color:#888; font-size:0.8em; font-style:italic;'>{n['NombreMateria']}</span>"
                                    f"</div>"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )
                        with c_b:
                            dias_raw = fila['Weekdays'] if fila['Weekdays'] else "No especificado"
                            st.markdown(f"**Días:** <span style='color:#2ecc71; font-weight:600;'>{dias_raw}</span>", unsafe_allow_html=True)
                            st.markdown("""
                            <div class='legend-box' style='font-size: 0.75em;'>
                                <strong>Días:</strong> 1:Lun | 2:Mar | 3:Mié | 4:Jue | 5:Vie | 6:Sáb | 7:Dom
                            </div>
                            """, unsafe_allow_html=True)

                        if es_valor_valido(fila['Notas']):
                            st.info(f"📌 **Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Reiniciar Búsqueda"):
            st.session_state.rk += 1
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
