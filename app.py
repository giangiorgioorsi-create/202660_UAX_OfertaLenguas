import streamlit as st
import pandas as pd

# 1. Configuración Institucional
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# Estilos CSS de alta visibilidad (Mise en place visual)
st.markdown("""
    <style>
    .card { 
        border: 1px solid #ff6600; padding: 25px; border-radius: 12px; 
        background-color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(255,102,0,0.1); 
    }
    .nrc-box { 
        background-color: #ff6600; color: white; padding: 6px 12px; 
        border-radius: 6px; font-weight: bold; display: inline-block; margin: 5px 0;
    }
    .banner-text { color: #333; font-size: 0.95em; font-weight: 800; display: block; margin-top: 5px;}
    .legend-box { 
        background-color: #f8f9fa; padding: 12px; border-radius: 8px; 
        font-size: 0.85em; color: #444; border-left: 5px solid #ff6600; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Gestión de Estado (Reset)
if 'reset_cnt' not in st.session_state:
    st.session_state.reset_cnt = 0

def clean_reset():
    st.session_state.reset_cnt += 1

# 3. Carga y Limpieza Profunda de Datos
@st.cache_data
def cargar_datos_limpios():
    archivo = "202660_UAX_OfertaLenguas.xlsx"
    # Cargamos todo como objeto/string para evitar que Excel "adivine" formatos
    df = pd.read_excel(archivo, dtype=str)
    
    # Limpieza de nombres de columnas (espacios al principio/final)
    df.columns = [str(c).strip() for c in df.columns]
    
    # Rellenar vacíos para evitar que desaparezcan datos en el buscador
    columnas_clave = ['Docente', 'ClaveBanner', 'NRC', 'Status', 'Fechas', 'Weekdays', 'Notas', 'Recordatorio', 'CreditosAcademicos', 'MetodoInstruccion']
    for col in columnas_clave:
        if col in df.columns:
            df[col] = df[col].fillna("Pendiente/No asignado")
    
    # Estandarización de la columna de Horario para el filtro
    if 'HoraInicio' in df.columns:
        df['Hora_Ref'] = df['HoraInicio'].str.strip()
    
    return df

try:
    df = cargar_datos_limpios()
    st.markdown("<h1 style='color: #ff6600;'>🏛️ Portal de Consulta Académica — Ciclo 2026-60</h1>", unsafe_allow_html=True)

    tab_explorar, tab_buscar = st.tabs(["📊 Panorama General", "🔍 Buscador Inteligente"])

    with tab_explorar:
        m1, m2, m3 = st.columns(3)
        m1.metric("Idiomas", df['Lengua'].nunique())
        m2.metric("Total Grupos", df['NRC'].count())
        docentes_count = df[df['Docente'] != "Pendiente/No asignado"]['Docente'].nunique()
        m3.metric("Cuerpo Docente", docentes_count)
        
        st.divider()
        c_a, c_b = st.columns(2)
        with c_a:
            st.write("**Oferta por Lengua**")
            st.bar_chart(df['Lengua'].value_counts(), color="#ff6600")
        with c_b:
            st.write("**Oferta por Modalidad**")
            st.bar_chart(df['MetodoInstruccion'].value_counts(), color="#ffb380")

    with tab_buscar:
        st.sidebar.header("Filtros de Inscripción")
        
        # Filtros encadenados dinámicos
        sel_idioma = st.sidebar.selectbox("1. Idioma", [""] + sorted(df['Lengua'].unique().tolist()), key=f"idi_{st.session_state.reset_cnt}")
        
        if sel_idioma:
            df_1 = df[df['Lengua'] == sel_idioma]
            sel_materia = st.sidebar.selectbox("2. Asignatura", [""] + sorted(df_1['NombreMateria'].unique().tolist()), key=f"mat_{st.session_state.reset_cnt}")
            
            if sel_materia:
                df_2 = df_1[df_1['NombreMateria'] == sel_materia]
                sel_metodo = st.sidebar.selectbox("3. Modalidad", [""] + sorted(df_2['MetodoInstruccion'].unique().tolist()), key=f"met_{st.session_state.reset_cnt}")
                
                if sel_metodo:
                    df_3 = df_2[df_2['MetodoInstruccion'] == sel_metodo]
                    sel_fecha = st.sidebar.selectbox("4. Periodo / Fechas", [""] + sorted(df_3['Fechas'].unique().tolist()), key=f"fec_{st.session_state.reset_cnt}")
                    
                    if sel_fecha:
                        df_4 = df_3[df_3['Fechas'] == sel_fecha]
                        sel_horario = st.sidebar.selectbox("5. Horario", [""] + sorted(df_4['Hora_Ref'].unique().tolist()), key=f"hor_{st.session_state.reset_cnt}")
                        
                        if sel_horario:
                            # RESULTADOS FINALES
                            res = df_4[df_4['Hora_Ref'] == sel_horario]
                            
                            st.info(f"Mostrando opciones para **{sel_materia}**")
                            
                            # Evitar duplicar tarjetas si hay varios NRC en la misma lista cruzada
                            res['GroupKey'] = res['ListaCruzada'].fillna(res['NRC'])
                            
                            for _, fila in res.drop_duplicates(subset=['GroupKey']).iterrows():
                                
                                # Lógica de Lista Cruzada
                                id_cruzada = fila['ListaCruzada']
                                if pd.notna(id_cruzada) and id_cruzada != "Pendiente/No asignado":
                                    cruzados = df[df['ListaCruzada'] == id_cruzada]
                                    es_cruzada = True
                                else:
                                    cruzados = df[df['NRC'] == fila['NRC']]
                                    es_cruzada = False

                                # Recordatorio destacado
                                if fila['Recordatorio'] != "Pendiente/No asignado":
                                    st.warning(f"🔔 **Nota Importante:** {fila['Recordatorio']}")

                                # Render de la Tarjeta Principal
                                st.markdown(f"""
                                <div class="card">
                                    <h3 style="color: #ff6600; margin-top: 0;">{fila['NombreMateria']}</h3>
                                    <p style="margin-bottom: 5px;"><strong>Docente:</strong> {fila['Docente']}</p>
                                    <p style="margin-bottom: 5px;"><strong>Horario:</strong> {fila['HoraInicio']} - {fila['HoraFin']}</p>
                                    <hr style="border: 0.5px solid #eee; margin: 15px 0;">
                                    <p style="font-weight: bold; margin-bottom: 10px;">
                                        {"NRCs disponibles en este grupo (Lista Cruzada):" if es_cruzada else "NRC para inscripción:"}
                                    </p>
                                """, unsafe_allow_html=True)
                                
                                # Grid de NRCs
                                cols_nrc = st.columns(min(len(cruzados), 4))
                                for i, (_, nrc_data) in enumerate(cruzados.iterrows()):
                                    with cols_nrc[i % 4]:
                                        st.markdown(f"<div class='nrc-box'>NRC {nrc_data['NRC']}</div>", unsafe_allow_html=True)
                                        st.markdown(f"<span class='banner-text'>{nrc_data['ClaveBanner']}</span>", unsafe_allow_html=True)
                                        if es_cruzada:
                                            st.caption(nrc_data['NombreMateria'])
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                with st.expander("📚 Ver Detalles Académicos Completos"):
                                    c1, c2 = st.columns(2)
                                    with c1:
                                        st.write(f"**Créditos:** {fila['CreditosAcademicos']}")
                                        st.write(f"**Periodo:** {fila['Fechas']}")
                                        st.write(f"**Estatus:** {fila['Status']}")
                                    with c2:
                                        st.write(f"**Días:** {fila['Weekdays']}")
                                        st.markdown("""
                                        <div class='legend-box'>
                                        1: Lun | 2: Mar | 3: Mié | 4: Jue | 5: Vie | 6: Sáb | 7: Dom
                                        </div>
                                        """, unsafe_allow_html=True)
                                    st.info(f"**Notas:** {fila['Notas']}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Restablecer Filtros", on_click=clean_reset):
            st.rerun()

except Exception as e:
    st.error(f"⚠️ Error Crítico: {e}")
    st.info("Asegúrate de que el archivo '202660_UAX_OfertaLenguas.xlsx' esté en la raíz de tu GitHub.")
