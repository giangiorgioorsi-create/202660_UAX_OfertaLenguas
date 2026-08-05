import streamlit as st

st.set_page_config(page_title="Nueva página disponible", page_icon="🌐", layout="centered")

CANVA_URL = "https://canva.link/ip80odtkn9luggs"

st.markdown(
    f"""
    <style>
        #MainMenu, footer, header {{visibility: hidden;}}
        .block-container {{padding-top: 15vh;}}
        .redirect-card {{
            text-align: center;
            font-family: Georgia, 'Times New Roman', serif;
        }}
        .redirect-card .eyebrow {{
            letter-spacing: .18em;
            text-transform: uppercase;
            font-size: .75rem;
            color: #a9832f;
            font-family: Helvetica, Arial, sans-serif;
            margin-bottom: 14px;
        }}
        .redirect-card h1 {{
            color: #0b2545;
            font-weight: 400;
        }}
        .redirect-card p {{
            font-family: Helvetica, Arial, sans-serif;
            color: #4a5568;
        }}
        .redirect-card a {{
            display: inline-block;
            background: #c9a24b;
            color: #0b2545 !important;
            text-decoration: none;
            font-weight: 700;
            font-family: Helvetica, Arial, sans-serif;
            padding: 16px 40px;
            border-radius: 2px;
            margin-top: 12px;
            font-size: 1.05rem;
        }}
    </style>
    <div class="redirect-card">
        <div class="eyebrow">Esta página se actualizó</div>
        <h1>La información se mudó a nuestra nueva página</h1>
        <p>Entra desde aquí para ver la oferta de lenguas:</p>
        <a href="{CANVA_URL}">Ir a la nueva página</a>
    </div>
    """,
    unsafe_allow_html=True,
)
