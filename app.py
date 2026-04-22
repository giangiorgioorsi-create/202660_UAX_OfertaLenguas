import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# Estilos CSS Reforzados (Forzamos color de texto para evitar el "blanco sobre blanco")
st.markdown("""
    <style>
    /* Forzar fondo de la app y colores base */
    .stApp { background-color: #f4f4f4; }
    
    /* Tarjeta con colores forzados */
    .card { 
        border: 1px solid #ff6600; 
        padding: 25px; 
        border-radius: 12px; 
        background-color: #ffffff !important; 
        color: #1a1a1a !important; /* Texto casi negro */
        margin-bottom: 20px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
    }
    
    /* Aseguramos que TODO el texto dentro de la tarjeta sea visible */
    .card h3, .card p, .card strong, .card span, .card div {
        color: #1a1a1a !important;
    }

    .nrc-box { 
        background-color: #ff6600 !important; 
        color: #ffffff !important; 
        padding: 6px 12px; 
        border-radius: 6px; 
        font-weight: bold; 
        display: inline-block; 
        margin: 5px 0;
    }
    
    .banner-text { 
        color: #ff6600 !important; 
        font-size: 1em; 
        font-weight: 800; 
        display: block; 
        margin-top: 5px;
    }
    
    .legend-box { 
        background-color: #e9ecef !important; 
        padding: 12px; 
        border-radius: 8px; 
        font-size: 0.85em; 
        color: #333333 !important; 
        border-left: 5px solid #ff6600; 
    }
    </style>
    """, unsafe_allow_html=True)

if 'reset_cnt' not in st.session_state:
    st.session_state.reset_cnt = 0

def clean_reset():
    st.session_state.reset_cnt += 1

# 2. Carga de Datos
@st.cache_data
def cargar_datos_limpios():
    archivo = "202660_UAX_OfertaLenguas.xlsx"
    df = pd.read_excel(archivo, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    
    # Rellenar nulos para evitar errores visuales
    columnas_txt = ['Docente', 'NombreMateria', 'MetodoInstruccion', 'Fechas', 'Weekdays', 'Status', 'Notas', 'Recordatorio', 'ClaveBanner']
    for col in columnas_txt:
        if col in df.columns:
            df[col] = df[col].fillna("No asignado")
    
    df['Hora_Ref'] = df['HoraInicio'].str.strip()
    return df

try:
    df = cargar_datos_limpios()
    st.markdown("<h1 style='color: #ff6600;'>🏛️ Portal Académico — Ciclo 2026-60</h1>", unsafe_allow_html=True)

    tab_explorar, tab_buscar = st.tabs(["📊 Panorama General", "🔍 Buscador Inteligente"])

    with tab_explorar:
        m1, m2, m3 = st.columns(3)
        m1.metric("Idiomas", df['Lengua'].nunique())
        m2.metric("Total Grupos", df['NRC'].count())
        m3.metric("Cuerpo Docente", df[df['Docente'] != "No asignado"]['Docente'].nunique())
        
        st.divider()
        c_a, c_b = st.columns(2)
        with c_a:
            st.write("**Oferta por Lengua**")
            st.bar_chart(df['Lengua'].value_counts(), color="#ff6600")
        with c_b:
            st.write("**Oferta por Modalidad**")
            st.bar_chart(df['MetodoInstruccion'].value_counts(), color="#ffb380")

    with tab_buscar:
        st.sidebar.header("Filtros de Búsqueda")
        
        # Filtros encadenados
        sel_idioma = st.sidebar.selectbox("1. Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"idi_{st.session_state.reset_cnt}")
        
        if sel_idioma:
            df_f = df[df['Lengua'] == sel_idioma]
            sel_materia = st.sidebar.selectbox("2. Asignatura", [""] + sorted(df_f['NombreMateria'].unique().tolist()), key=f"mat_{st.session_state.reset_cnt}")
            
            if sel_materia:
                df_f = df_f[df_f['NombreMateria'] == sel_materia]
                sel_metodo = st.sidebar.selectbox("3. Modalidad", [""] + sorted(df_f['MetodoInstruccion'].unique().tolist()), key=f"met_{st.session_state.reset_cnt}")
                
                if sel_metodo:
                    df_f = df_f[df_f['MetodoInstruccion'] == sel_metodo]
                    sel_fecha = st.sidebar.selectbox("4. Fechas", [""] + sorted(df_f['Fechas'].unique().tolist()), key=f"fec_{st.session_state.reset_cnt}")
                    
                    if sel_fecha:
                        df_f = df_f[df_f['Fechas'] == sel_fecha]
                        sel_horario = st.sidebar.selectbox("5. Horario", [""] + sorted(df_f['Hora_Ref'].unique().tolist()), key=f"hor_{st.session_state.reset_cnt}")
                        
                        if sel_horario:
                            res = df_f[df_f['Hora_Ref'] == sel_horario].copy()
                            res['GroupKey'] = res['ListaCruzada'].fillna(res['NRC'])
                            
                            for _, fila in res.drop_duplicates(subset=['GroupKey']).iterrows():
                                
                                # Lógica de Lista Cruzada
                                id_cruzada = fila['ListaCruzada']
                                if pd.notna(id_cruzada) and id_cruzada != "No asignado":
                                    cruzados = df[df['ListaCruzada'] == id_cruzada]
                                    es_cruzada = True
                                else:
                                    cruzados = df[df['NRC'] == fila['NRC']]
                                    es_cruzada = False

                                if fila['Recordatorio'] != "No asignado":
                                    st.warning(f"🔔 **Aviso:** {fila['Recordatorio']}")

                                # TARJETA REFORZADA
                                st.markdown(f"""
                                <div class="card">
                                    <h3 style="margin-top: 0;">{fila['NombreMateria']}</h3>
                                    <p><strong>Catedrático:</strong> {fila['Docente']}</p>
                                    <p><strong>Horario:</strong> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                                    <hr style="border: 0.5px solid #ff6600; margin: 15px 0;">
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
                                            st.caption(f"<span style='color:#555;'>{nrc_data['NombreMateria']}</span>", unsafe_allow_html=True)
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                with st.expander("📚 Ver Detalles"):
                                    c1, c2 = st.columns(2)
                                    with c1:
                                        st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                                        st.write(f"**Periodo:** {fila['Fechas']}")
                                    with c2:
                                        st.write(f"**Días:** {fila['Weekdays']}")
                                        st.markdown("<div class='legend-box'>1: Lu | 2: Ma | 3: Mi | 4: Ju | 5: Vi | 6: Sa | 7: Do</div>", unsafe_allow_html=True)
                                    st.info(f"**Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Restablecer Filtros", on_click=clean_reset):
            st.rerun()

except Exception as e:
    st.error(f"⚠️ Error: {e}")
