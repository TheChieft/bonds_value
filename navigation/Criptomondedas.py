import streamlit as st
import hydralit_components as hc

def Criptomonedas():
    a = 'Análisis Técnico'
    b = 'Modelos'

    tabs = [
        a,
        b
    ]

    option_data = [
        {'icon': "", 'label': a},
        {'icon': "", 'label': b},
    ]

    # Define el tema para el NavBar
    theme = {
        'menu_background': '#000020',  # Color de fondo del menú
        'txc_inactive': '#999999',  # Color del texto de las pestañas inactivas
        'txc_active': 'white',  # Color del texto de la pestaña activa
        'option_active': '#183E88'  # Color de la pestaña activa
    }

    # Crea el NavBar con los datos y el tema especificados
    # -------------------------------------------------------------

    chosen_tab = hc.option_bar(
        option_definition=option_data,
        title='',
        key='PrimaryOptionx2',
        override_theme=theme,
        horizontal_orientation=True)

    if chosen_tab == a:
        pass

    elif chosen_tab == b:
        pass
