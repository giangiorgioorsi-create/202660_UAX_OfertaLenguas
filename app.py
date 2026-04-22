import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# --- BLOQUEO TOTAL DE TEMA (MODO ANTI-OSCURO DEFINITIVO) ---
st.markdown("""
    <style>
    /* 1. Fondo global y texto negro */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 2. BLANQUEO DE CONTENEDORES DE GRÁFICOS (Para versiones antiguas) */
    div[data-testid="stVegaLiteChart"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EEEEEE !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }

    /* 3. Barra lateral forzada */
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
    }

    /* 4. Tarjetas de cursos con alto contraste */
    .card { 
        border: 2px solid #FF6600 !important; 
        padding: 25px !important; 
        border-radius: 15px !important; 
        background-color: #FFFFFF !important; 
        color: #1A1A1A !important;
        margin-bottom: 25px !important; 
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05) !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label, strong, small {
        color: #1A1A1A !important;
    }

    /* Estilo de los NRCs */
    .nrc-box { 
        background-color: #FF6600 !important; 
        color: #FFFFFF !important; 
        padding: 8px 15px !important; 
        border-radius: 8px !important; 
        font-weight: bold !important;
        display: inline-block !important;
    }
    
    .banner-text { 
        color: #FF6600 !important; 
        font-weight: 800 !important;
    }

    /* Leyenda informativa */
    .legend-box { 
        background-color: #F1F3F5 !important; 
        color: #1A1A1A !important;
        padding: 15px !important; 
        border-radius: 10px !important; 
        border-left: 6px solid #FF6600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'reset_cnt' not in st.session_state:
    st.session_state.reset_cnt = 0

def clean_reset():
    st.session_state.reset_cnt += 1

# 2. Carga de Datos (Ciclo 202660)
@st.cache_data
def cargar_datos_limpios():
    archivo = "202660_UAX_OfertaLenguas.xlsx"
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    
    columnas_txt = ['Docente', 'NombreMateria', 'MetodoInstruccion', 'Fechas', 'Weekdays', 'Status', 'Notas', 'Recordatorio', 'ClaveBanner']
    for col in columnas_txt:
        if col in df.columns:
            df[col] = df[col].fillna("No asignado")
    
    df['Hora_Ref'] = df['HoraInicio'].str.strip()
    return df

try:
    df = cargar_datos_limpios()
    st.markdown("<h1 style='color: #FF6600 !important;'>🏛️ Portal Académico — Ciclo 2026-60</h1>", unsafe_allow_html=True)

    tab_explorar, tab_buscar = st.tabs(["📊 Panorama General", "🔍 Buscador de Asignaturas"])

    with tab_explorar:
        m1, m2, m3 = st.columns(3)
        m1.metric("Idiomas", df['Lengua'].nunique())
        m2.metric("Total Grupos", df['NRC'].count())
        m3.metric("Cuerpo Docente", df[df['Docente'] != "No asignado"]['Docente'].nunique())
        
        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Oferta por Lengua**")
            # SE ELIMINÓ EL ARGUMENTO 'theme' PARA EVITAR EL ERROR
            st.bar_chart(df['Lengua'].value_counts(), color="#FF6600")
        with col_b:
            st.write("**Oferta por Modalidad**")
            st.bar_chart(df['MetodoInstruccion'].value_counts(), color="#FFB380")

    with tab_buscar:
        st.sidebar.header("Filtros de Búsqueda")
        
        idiomas = sorted(df['Lengua'].unique().tolist())
        sel_idioma = st.sidebar.selectbox("1. Idioma", [""] + idiomas, key=f"idi_{st.session_state.reset_cnt}")
        
        if sel_idioma:
            df_f = df[df['Lengua'] == sel_idioma]
            materias = sorted(df_f['NombreMateria'].unique().tolist())
            sel_materia = st.sidebar.selectbox("2. Asignatura", [""] + materias, key=f"mat_{st.session_state.reset_cnt}")
            
            if sel_materia:
                df_f = df_f[df_f['NombreMateria'] == sel_materia]
                metodos = sorted(df_f['MetodoInstruccion'].unique().tolist())
                sel_metodo = st.sidebar.selectbox("3. Modalidad", [""] + metodos, key=f"met_{st.session_state.reset_cnt}")
                
                if sel_metodo:
                    df_f = df_f[df_f['MetodoInstruccion'] == sel_metodo]
                    fechas = sorted(df_f['Fechas'].unique().tolist())
                    sel_fecha = st.sidebar.selectbox("4. Fechas", [""] + fechas, key=f"fec_{st.session_state.reset_cnt}")
                    
                    if sel_fecha:
                        df_f = df_f[df_f['Fechas'] == sel_fecha]
                        horarios = sorted(df_f['Hora_Ref'].unique().tolist())
                        sel_horario = st.sidebar.selectbox("5. Horario", [""] + horarios, key=f"hor_{st.session_state.reset_cnt}")
                        
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
                                    st.warning(f"🔔 **Aviso:** {fila['Recordatorio']}")

                                st.markdown(f"""
                                <div class="card">
                                    <h3 style="color: #FF6600 !important; margin-top: 0;">{fila['NombreMateria']}</h3>
                                    <p><strong>Catedrático:</strong> {fila['Docente']}</p>
                                    <p><strong>Horario:</strong> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                                    <hr style="border: 1px solid #FF6600; margin: 15px 0;">
                                    <p style="font-weight: bold; margin-bottom: 10px;">
                                        {"NRCs vinculados (Lista Cruzada):" if es_cruzada else "NRC para inscripción:"}
                                    </p>
                                """, unsafe_allow_html=True)
                                
                                cols = st.columns(min(len(cruzados), 4))
                                for i, (_, nrc_data) in enumerate(cruzados.iterrows()):
                                    with cols[i % 4]:
                                        st.markdown(f"<div class='nrc-box'>NRC {nrc_data['NRC']}</div>", unsafe_allow_html=True)
                                        st.markdown(f"<span class='banner-text'>{nrc_data['ClaveBanner']}</span>", unsafe_allow_html=True)
                                        if es_cruzada:
                                            st.markdown(f"<small style='color: #1A1A1A !important;'>{nrc_data['NombreMateria']}</small>", unsafe_allow_html=True)
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                with st.expander("📚 Ver Detalles"):
                                    c1, c2 = st.columns(2)
                                    with c1:
                                        st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                                        st.write(f"**Periodo:** {fila['Fechas']}")
                                    with c2:
                                        st.write(f"**Días:** {fila['Weekdays']}")
                                        st.markdown("""
                                        <div class='legend-box'>
                                        1: Lun | 2: Ma | 3: Mi | 4: Ju | 5: Vi | 6: Sa | 7: Do
                                        </div>
                                        """, unsafe_allow_html=True)
                                    st.info(f"**Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Restablecer Filtros", on_click=clean_reset):
            st.rerun()

except Exception as e:
    st.error(f"⚠️ Error: {e}")
