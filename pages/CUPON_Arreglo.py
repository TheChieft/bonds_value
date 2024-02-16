import streamlit as st
from datetime import datetime
import numpy as np
import pandas as pd
from src.FuncionesBonos import  generar_tabla_bono_con_cupon

st.title('Calculadora Avanzada de Bonos con Cupón')
st.write('Esta aplicación te permite calcular el precio de un bono con cupón y evaluar la rentabilidad de la inversión.')

# Sección de pestañas
col1,col2,col3 = st.columns(3)
with col1:
    fecha_emision = st.date_input('Fecha de emisión', value=datetime.now(), key='fecha_emision_tab1')
    tasa_facial = st.number_input('Tasa de interés (EA%)', min_value=0.0000, value=0.0000, format='%f', key='tasa_facial_tab1')
with col2:
    fecha_vencimiento = st.date_input('Fecha de vencimiento del bono', min_value=fecha_emision + pd.Timedelta(days=365), value=fecha_emision + pd.Timedelta(days=365), key='fecha_vencimiento_tab1')
    tasa_referencia = st.number_input('Tasa de interés de referencia (EA%)', min_value=0.0000, value=0.0000, format='%f', key='tasa_referencia_tab1')
with col3:
    fecha_compra = st.date_input('Fecha compra', value=datetime.now(), key='fecha_compra_tab1',min_value=fecha_emision, max_value=fecha_vencimiento)
    valor_nominal = st.number_input('Valor nominal del bono', min_value=0, value=0, format='%i', key='valor_nominal_tab1')
tabla, duracion,convexidad, tabla_convexidad = generar_tabla_bono_con_cupon(fecha_emision,fecha_compra,fecha_vencimiento,tasa_facial, valor_nominal,tasa_referencia)
st.dataframe(tabla)
col1, col2 = st.columns(2)
with col1:
    st.metric('Convexidad', convexidad, 'S/.')
with col2:
    st.metric('duracion', duracion, 'S/.')
#st.dataframe(tabla_convexidad)