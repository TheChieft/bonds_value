import streamlit as st


# Configuración de la página
st.set_page_config(
    page_title="Valuación de instrumentos financieros",
    page_icon=":moneybag:"
)

# Estilo personalizado para centrar los enlaces de página y darle estilo al contenedor
st.markdown(
    """
    <style>
        .st-emotion-cache-j7qwjs {
            padding: 5px 10px; /* Agrega espacio alrededor del texto */
        }
        .st-emotion-cache-j7qwjs .home_bar {
            padding: 5px 10px; /* Agrega espacio alrededor del texto */
            border-radius: 10px; /* Bordes redondeados */
            font-size: 24px; /* Tamaño de texto más grande */
            text-decoration: none; /* Eliminar subrayado del enlace */
            text-color: black; /* Color del texto */
            background-color: #F6F6F6; /* Color de fondo */
        }
        .st-emotion-cache-j7qwjs .home_bar:hover {
            background-color: #D3D3D3; /* Color de fondo al pasar el mouse */
        }

        .st-emotion-cache-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título e icono
st.markdown(
    """
    <div style='display: flex; justify-content: center; align-items: center; flex-direction: column;'>
        <h2 style='font-size: 80px; text-align: center; padding: 0px'>💰</h2>
        <h1 style='font-size: 50px; text-align: center;'>Una manera sencilla de valorar los instrumentos financieros</h1>
        <p style='text-align: center; font-size: 25px'>Esta aplicación te permite valorar los instrumentos financieros de manera sencilla y rápida.</p>
        <hr>
        <div class="st-emotion-cache-container">
            <div class="st-emotion-cache-j7qwjs">
                <a class="home_bar" href="Home" target="" rel="noreferrer">🏠 Home</a>
            </div>
            <div class="st-emotion-cache-j7qwjs">
                <a class="home_bar" href="Acciones" target="" rel="noreferrer">1️⃣ Page 1</a>
            </div>
            <div class="st-emotion-cache-j7qwjs">
                <a class="home_bar" href="Bonds_cupon" target="" rel="noreferrer">2️⃣ Page 2</a>
            </div>
            <div class="st-emotion-cache-j7qwjs">
                <a class="home_bar" href="Bonds_sin_cupon" target="" rel="noreferrer">🌎 Google</a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
