import streamlit as st
import hydralit_components as hc
from components.bonds.ZeroBonds import ZeroBonds
from components.bonds.CuponBonds import CuponBonds


def Bonds():
    TYPE_1 = 'Bonos con Cupón'
    TYPE_2 = 'Bonos Cero Cupón'
    
    tabs = [
        TYPE_1,
        TYPE_2,
    ]
    
    option_data = [
        {'icon': "", 'label': TYPE_1},
        {'icon': "", 'label': TYPE_2},
    ]
    
    theme = {
        'menu_background': '#000020',  # Color de fondo del menú
        'txc_inactive': '#999999',  # Color del texto de las pestañas inactivas
        'txc_active': 'white',  # Color del texto de la pestaña activa
        'option_active': '#183E88'  # Color de la pestaña activa
    }
    
    chosen_tab = hc.option_bar(
        option_definition=option_data,
        title='',
        key='PrimaryOptionx2',
        override_theme=theme,
        horizontal_orientation=True)
    
    # Descargar el contenido pre-renderizado
    
    
    # Seleccionar el contenido a mostrar
    
    if chosen_tab == TYPE_1:
        CuponBonds()
    elif chosen_tab == TYPE_2:
        ZeroBonds()
    
    