import streamlit as st
from navigation.Acciones import Acciones
from components.footer import footer_style
import hydralit_components as hc


# Configuración de la página
st.set_page_config(
    page_title='DeFi II'
    # page_icon="assets/images/JML-sin-fondo.png",
    # initial_sidebar_state="collapsed"
)


max_width_str = f"max-width: {90}%;"

st.markdown(f"""
        <style>
        .appview-container .main .block-container{{{max_width_str}}}
        </style>
        """,
            unsafe_allow_html=True,
            )

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;

                }
        </style>
        """, unsafe_allow_html=True)

# Footer

st.markdown(footer_style, unsafe_allow_html=True)

# NavBar

acciones = 'Acciones'


tabs = [
    acciones
]

option_data = [
    {'icon': "📜", 'label': 'Acciones'}
]

# Define el tema para el NavBar
theme = {
    'menu_background': '#1a1a1a',  # Color de fondo del menú
    'txc_inactive': '#999999',  # Color del texto de las pestañas inactivas
    'txc_active': 'white',  # Color del texto de la pestaña activa
    'option_active': '#007bff'  # Color de la pestaña activa
}

# Crea el NavBar con los datos y el tema especificados
chosen_tab = hc.option_bar(
    option_definition=option_data,
    title='',
    key='PrimaryOptionx',
    override_theme=theme,
    horizontal_orientation=True)


if chosen_tab == acciones:
    Acciones()

# if chosen_tab == punto_1:
#     punto_uno()

# if chosen_tab == punto_2:
#     punto_dos()

# if chosen_tab == punto_3:
#     punto_tres()

# if chosen_tab == punto_4:
#     punto_cuatro()

# if chosen_tab == punto_5:
#     punto_cinco()
