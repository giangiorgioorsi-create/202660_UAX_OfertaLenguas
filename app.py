import streamlit as st
import pandas as pd

# 1. Configuración de la Plataforma
st.set_page_config(page_title="Portal de Oferta Académica 2026-60", layout="wide")

# Estilos CSS institucionales (Mise en place visual)
st.markdown("""
    <style>
    .card { 
        border: 1px solid #e0e0e0; padding: 25px; border-radius: 12px; 
        background-color: #ffffff; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
    }
    .nrc-box { 
        background-color: #ff6600; color: white; padding: 6px 12px; 
        border-radius: 6px; font-weight: bold; display: inline-block; margin: 5px 0;
    }
    .banner-text { color: #444; font-size: 0.9em; font-weight: 700; display: block; }
    .legend-box { 
        background-color: #f0f2f6; padding: 12px; border-radius: 8px; 
        font-size: 0.85em; color: #444; border-left: 5px solid #ff6600; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Gestión de Estado para el Restablecimiento (Reset)
filtros_keys = ['id', 'mat', 'met', 'fec', 'hr']
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def restablecer_todo():
    st.session_state.reset_counter += 1

# 3. Carga de Base de Datos
@st.cache_data
def cargar_datos():
    # CAMBIO DE NOMBRE DEL ARCHIVO PARA EL PERIODO 202660
    archivo = "202660_UAX_OfertaLenguas.xlsx"
    df = pd.read_excel(archivo, dtype={'Weekdays': str, 'ListaCruzada': str, 'Recordatorio': str})
    df.columns = [c.strip() for c in df.columns]
    df['Hora_Ref'] = df['HoraInicio'].astype(str)
    return df

try:
    df_full = cargar_datos()
    st.markdown("<h1 style='color: #ff6600;'>🏛️ Portal de Consulta Académica — Ciclo 2026-60</h1>", unsafe_allow_html=True)

    tab_explorar, tab_buscar = st.tabs(["📊 Panorama General", "🔍 Buscador de Asignaturas"])

    with tab_explorar:
        # Métricas de gestión para la Coordinación
        c1, c2, c3 = st.columns(3)
        c1.metric("Idiomas", df_full['Lengua'].nunique())
        c2.metric("Grupos Totales", df_full['NRC'].count())
        c3.metric("Cuerpo Docente", df_full['Docente'].nunique())
        st.divider()
        col_graf1, col_graf2 = st.columns(2)
        with col_graf1: st.bar_chart(df_full['Lengua'].value_counts(), color="#ff6600")
        with col_graf2: st.bar_chart(df_full['MetodoInstruccion'].value_counts(), color="#ffb380")

    with tab_buscar:
        st.sidebar.header("Filtros de Inscripción")
        
        # Filtros en cascada (5 niveles de organización)
        idiomas = sorted(df_full['Lengua'].unique().tolist())
        sel_idioma = st.sidebar.selectbox("1. Idioma", [""] + idiomas, key=f"id_{st.session_state.reset_counter}")
        
        if sel_idioma:
            df_f = df_full[df_full['Lengua'] == sel_idioma]
            materias = sorted(df_f['NombreMateria'].unique().tolist())
            sel_materia = st.sidebar.selectbox("2. Asignatura", [""] + materias, key=f"mat_{st.session_state.reset_counter}")
            
            if sel_materia:
                df_f = df_f[df_f['NombreMateria'] == sel_materia]
                metodos = sorted(df_f['MetodoInstruccion'].unique().tolist())
                sel_metodo = st.sidebar.selectbox("3. Modalidad", [""] + metodos, key=f"met_{st.session_state.reset_counter}")
                
                if sel_metodo:
                    df_f = df_f[df_f['MetodoInstruccion'] == sel_metodo]
                    fechas = sorted(df_f['Fechas'].unique().tolist())
                    sel_fecha = st.sidebar.selectbox("4. Periodo / Fechas", [""] + fechas, key=f"fec_{st.session_state.reset_counter}")
                    
                    if sel_fecha:
                        df_f = df_f[df_f['Fechas'] == sel_fecha]
                        horarios = sorted(df_f['Hora_Ref'].unique().tolist())
                        sel_horario = st.sidebar.selectbox("5. Horario", [""] + horarios, key=f"hr_{st.session_state.reset_counter}")
                        
                        if sel_horario:
                            target_cursos = df_f[df_f['Hora_Ref'] == sel_horario]
                            st.success(f"Resultados encontrados para {sel_materia}")
                            
                            # Clave de agrupación para evitar duplicados en la vista
                            target_cursos['GroupKey'] = target_cursos['ListaCruzada'].fillna(target_cursos['NRC'].astype(str))
                            
                            for _, row in target_cursos.drop_duplicates(subset=['GroupKey']).iterrows():
                                
                                # Lógica de Lista Cruzada
                                if pd.notna(row['ListaCruzada']):
                                    lista_cruzada = df_full[df_full['ListaCruzada'] == row['ListaCruzada']]
                                    es_lista_cruzada = True
                                else:
                                    lista_cruzada = df_full[df_full['NRC'] == row['NRC']]
                                    es_lista_cruzada = False

                                # --- Recordatorio de Carga en Pareja ---
                                if pd.notna(row['Recordatorio']):
                                    st.warning(f"⚠️ **Aviso Importante:** {row['Recordatorio']}")

                                st.markdown(f"""
                                <div class="card">
                                    <h3 style="color: #ff6600; margin-bottom: 5px;">{row['NombreMateria']}</h3>
                                    <p style="margin: 0;"><strong>Catedrático:</strong> {row['Docente']}</p>
                                    <p style="margin: 0;"><strong>Horario:</strong> {row['HoraInicio']} - {row['HoraFin']}</p>
                                    <hr style="margin: 15px 0; border: 0; border-top: 1px solid #eee;">
                                    <p style="font-weight: bold; margin-bottom: 10px;">
                                        {"NRC(s) vinculados (Lista Cruzada):" if es_lista_cruzada else "NRC para inscripción:"}
                                    </p>
                                """, unsafe_allow_html=True)
                                
                                # Despliegue de NRCs
                                cols = st.columns(len(lista_cruzada) if len(lista_cruzada) < 5 else 4)
                                for i, (_, item) in enumerate(lista_cruzada.iterrows()):
                                    with cols[i % 4]:
                                        st.markdown(f"<div class='nrc-box'>NRC {item['NRC']}</div>", unsafe_allow_html=True)
                                        st.markdown(f"<span class='banner-text'>{item['ClaveBanner']}</span>", unsafe_allow_html=True)
                                        if es_lista_cruzada:
                                            st.caption(item['NombreMateria'])
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                with st.expander("📚 Detalles Académicos Completos"):
                                    c_a, c_b = st.columns(2)
                                    with c_a:
                                        st.write(f"**Créditos:** {row['CreditosAcademicos']}")
                                        st.write(f"**Fechas:** {row['Fechas']}")
                                        st.write(f"**Estatus:** {row['Status']}")
                                    with c_b:
                                        dias_raw = str(row['Weekdays']) if pd.notna(row['Weekdays']) else "No especificado"
                                        st.write(f"**Días de sesión:** `{dias_raw}`")
                                        st.markdown("""
                                        <div class='legend-box'>
                                        1: Lunes | 2: Martes | 3: Miércoles | 4: Jueves<br>
                                        5: Viernes | 6: Sábado | 7: Domingo
                                        </div>
                                        """, unsafe_allow_html=True)
                                    st.info(f"**Notas:** {row['Notas'] if pd.notna(row['Notas']) else 'Sin observaciones.'}")

        st.sidebar.divider()
        if st.sidebar.button("🔄 Restablecer Filtros", on_click=restablecer_todo):
            st.rerun()

except Exception as e:
    st.error(f"⚠️ Error al cargar la base de datos: {e}")
    st.info("Verifica que el archivo '202660_UAX_OfertaLenguas.xlsx' esté en la raíz del repositorio.")