import streamlit as st
import hydralit_components as hc
from components.Acciones.ana_tecnico import analisis_tec


def Acciones():
    a = 'Análisis Técnico'
    b = 'Valoración'
    c = 'Modelos'

    tabs = [
        a,
        b,
        c,
    ]

    option_data = [
        {'icon': "", 'label': a},
        {'icon': "", 'label': b},
        {'icon': "", 'label': c}
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

    st.divider()

    chosen_tab = hc.option_bar(
        option_definition=option_data,
        title='',
        key='PrimaryOptionx2',
        override_theme=theme,
        horizontal_orientation=True)

    if chosen_tab == a:
        analisis_tec()

    elif chosen_tab == b:
        pass

    elif chosen_tab == c:
        pass
# -------------------------------------------------------------
