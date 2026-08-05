import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Nueva página disponible", page_icon="🌐", layout="centered")

CANVA_URL = "https://canva.link/ip80odtkn9luggs"

# Redirección automática (window.top escapa del iframe del componente)
components.html(
    f"""
    <script>
        window.top.location.href = "{CANVA_URL}";
    </script>
    """,
    height=0,
)

st.markdown(
    f"""
    <style>
        .redirect-card {{
            text-align: center;
            padding-top: 15vh;
            font-family: Georgia, 'Times New Roman', serif;
            color: #eef1f6;
        }}
        .redirect-card p {{
            font-family: Helvetica, Arial, sans-serif;
            color: #a9b6cc;
        }}
        .redirect-card a {{
            display: inline-block;
            background: #c9a24b;
            color: #0b2545;
            text-decoration: none;
            font-weight: 700;
            font-family: Helvetica, Arial, sans-serif;
            padding: 14px 34px;
            border-radius: 2px;
            margin-top: 12px;
        }}
    </style>
    <div class="redirect-card">
        <h2>La información se mudó a nuestra nueva página</h2>
        <p>Si no fuiste redirigido automáticamente, entra aquí:</p>
        <a href="{CANVA_URL}" target="_top">Ir a la nueva página</a>
    </div>
    """,
    unsafe_allow_html=True,
)
