import streamlit as st
from navigation.Acciones import Acciones
from navigation.Criptomondedas import Criptomonedas
from components.footer import footer_style
import hydralit_components as hc


# Configuración de la página
st.set_page_config(
    page_title='FT',
    initial_sidebar_state="expanded",
    page_icon="assets/images/ICONO.png"
)


with st.sidebar:
    st.image("assets/images/LOGO.png")
    "Tu guía inteligente para inversiones informadas basado en ciencia de datos."
    ''

# --------------- menú -------------------------

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

principal = 'Principal'
bonos = 'Bonos'
acciones = 'Acciones'
criptomonedas = 'Criptomonedas'

tabs = [
    acciones,
    bonos,
    acciones,
    criptomonedas
]

option_data = [
    {'icon': "", 'label': 'Principal'},
    {'icon': "", 'label': 'Bonos'},
    {'icon': "", 'label': 'Acciones'},
    {'icon': "", 'label': 'Criptomonedas'}
]

# Define el tema para el NavBar
theme = {
    'menu_background': '#000020',  # Color de fondo del menú
    'txc_inactive': '#999999',  # Color del texto de las pestañas inactivas
    'txc_active': 'white',  # Color del texto de la pestaña activa
    'option_active': '#183E88'  # Color de la pestaña activa
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

if chosen_tab == bonos:
    pass

if chosen_tab == acciones:
    pass

if chosen_tab == criptomonedas:
    Criptomonedas()
