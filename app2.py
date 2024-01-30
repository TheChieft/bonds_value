import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime
from streamlit_option_menu import option_menu

GENERAL = pd.read_csv('data/db/bonds_public.csv', sep=',', index_col=0)
INFO_DATAFRAME = pd.read_csv('data/db/info_bonds_public.csv', sep=',')

#Filtrar códigos que contienen 'TFIT'
df_tfit = INFO_DATAFRAME[INFO_DATAFRAME['Nemotécnico'].str.contains('TFIT')]

# Filtrar códigos que contienen 'TCO'
df_tco =INFO_DATAFRAME[INFO_DATAFRAME['Nemotécnico'].str.contains('TCO')]

# selector de opciones
st.set_page_config(layout="wide", page_title='Valuación de Instrumentos Financieros', page_icon=':dollar:', initial_sidebar_state='auto')

# MAIN ---------------------------------------
with st.sidebar:
    st.markdown("<h1 style='font-size: 50px; text-align: left;'>Valuación de Instrumentos Financieros</h1>",
                unsafe_allow_html=True)
    selected = st.selectbox(
        label='Seleccione una opción:',
        options=['Bono cupón', 'Bono sin cupón', 'General'],
        index=0
    )
    
if selected == 'Bono cupón':
    st.dataframe(df_tfit)
    
    selector_nemotecnico = st.selectbox(
        label='Seleccione un Nemotécnico:',
        options=df_tfit['Nemotécnico'].unique(),
        index=0
    )
    
    st.dataframe(df_tfit[df_tfit['Nemotécnico'] == selector_nemotecnico])
    
elif selected == 'Bono sin cupón':
    st.dataframe(df_tco)
    
else:
    st.markdown("<h1 style='font-size: 50px; text-align: left;'>Valuación de Instrumentos Financieros</h1>",
                unsafe_allow_html=True)
    st.dataframe(GENERAL)
    # contador de bonos
    st.dataframe(GENERAL['Emisor'].value_counts())  