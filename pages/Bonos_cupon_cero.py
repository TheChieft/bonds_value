import streamlit as st
from datetime import datetime
import numpy as np
from src.FuncionesBonos import calcular_precio_bono
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Valuación de instrumentos financieros",
    page_icon=":moneybag:"
)        

st.title('Calculadora Avanzada de Bonos Sin Cupón')
st.write('Esta aplic ación te permite calcular el precio de un bono sin cupón y evaluar la rentabilidad de la inversión.')
st.markdown('---')
col1, col2, col3 = st.columns(3)
with col1:
    fecha_emision = st.date_input('Fecha emisión', value=datetime.now(), key='fecha_tasa_emicion')
    tasa_facial = st.number_input('Tasa de facial', min_value=0.0000, value=0.0000, format='%f', key='tasa_facial')
with col2:
    fecha_compra = st.date_input('Fecha compra', value=datetime.now(), min_value=datetime.now(), key='fecha_compra')
    valor_inicial = st.number_input('Valor inicial de la inversión', min_value=0, value=1000000, format='%i', key='valor_inicial')
with col3:
    fecha_vencimiento = st.date_input('Fecha de vencimiento del bono', min_value=fecha_compra + pd.Timedelta(days=365), value=fecha_compra + pd.Timedelta(days=365), key='fecha_vencimiento')
    tasa_referencia = st.number_input('Tasa actual del mercado', min_value=0.0000, value=0.0000, format='%f', key='tasa_referencia')
precio_bono = calcular_precio_bono(fecha_emision, fecha_compra, fecha_vencimiento,tasa_facial,tasa_referencia, valor_inicial)
precio_bono_formatted = "{:,.2f}".format(precio_bono)
st.write(f'Valor actual del bono: {precio_bono_formatted}')
