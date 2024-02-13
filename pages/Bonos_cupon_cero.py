import streamlit as st
from datetime import datetime
import numpy as np
from src.FuncionesBonos import calcular_precio_bono_sin_cupon
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Valuación de instrumentos financieros",
    page_icon=":moneybag:"
)        

st.title('Calculadora Avanzada de Bonos Sin Cupón')
st.write('Esta aplic ación te permite calcular el precio de un bono sin cupón y evaluar la rentabilidad de la inversión.')
# Sección de pestañas
tab1, tab2 ,tab3 = st.tabs(['Valor por retorno','Retorno por valor', 'Precio del bono actual'])

# Pestaña 1 - Calcular Rentabilidad de la Inversión
# ¿Cuanto tengo que pagar para tener x cantidad de dinero en el futuro?

with tab1:
    st.write('Ingresa los datos del bono para calcular el precio de la inversión y la rentabilidad esperada.')
    col1, col2 = st.columns(2)
    with col1:
        fecha_compra = st.date_input('Fecha compra', value=datetime.now())
        tasa_facial = st.number_input('Tasa de interés (EA%)', min_value=0.0000, value=0.0000, format='%f')
    with col2:
        fecha_vencimiento = st.date_input('Fecha de vencimiento del bono', min_value=fecha_compra + pd.Timedelta(days=365), value=fecha_compra + pd.Timedelta(days=365))
        valor_esperado = st.number_input('Valor esperado del bono', min_value=0, value=0, format='%i')
    precio_bono = calcular_precio_bono_sin_cupon(fecha_compra, fecha_vencimiento, tasa_facial, valor_esperado)
    precio_bono_formatted = "{:,.2f}".format(precio_bono)
    st.write(f'La inversión en el bono debe ser de: {precio_bono_formatted}')
with tab2:
    st.write('Ingresa los datos del bono para calcular el rendimiento esperado de la inversión.')
    col1, col2 = st.columns(2)
    with col1:
        fecha_compra = st.date_input('Fecha compra', value=datetime.now(), key='fecha_compra_tab2')
        tasa_facial = st.number_input('Tasa de interés (EA%)', min_value=0.0000, value=0.0000, format='%f', key='tasa_facial_tab2')
    with col2:
        fecha_vencimiento = st.date_input('Fecha de vencimiento del bono', min_value=fecha_compra + pd.Timedelta(days=365), value=fecha_compra + pd.Timedelta(days=365),key='fecha_vencimiento_tab2')
        valor_bono = st.number_input('Valor inicial de la inversión', min_value=0, value=1000000, format='%i', key='valor_bono_tab2')
    retorno_inversion = calcular_precio_bono_sin_cupon(fecha_compra, fecha_vencimiento, tasa_facial, valor_bono)
    st.write(f'El retorno de la inversión es: {retorno_inversion:.2f}', f'lo que representa un retorno total de: {retorno_inversion + valor_bono }%')
with tab3:
    
    col1, col2 = st.columns(2)
    with col1:
        tasa_facial = st.number_input('Tasa de facial (EA%)', min_value=0.0000, value=0.0000, format='%f', key='tasa_facial')
        tasa_mercado = st.number_input('Tasa actual del mercado', min_value=0.0000, value=0.0000, format='%f', key='tasa_mercado')
    with col2:
        fecha_compra = st.date_input('Fecha compra', value=datetime.now(), min_value=datetime.now(), key='fecha_compra')
        fecha_vencimiento = st.date_input('Fecha de vencimiento del bono', min_value=fecha_compra + pd.Timedelta(days=365), value=fecha_compra + pd.Timedelta(days=365), key='fecha_vencimiento')
    valor_inicial = st.number_input('Valor inicial de la inversión', min_value=0, value=1000000, format='%i', key='valor_inicial')
    precio_bono = calcular_precio_bono_sin_cupon(fecha_compra, fecha_vencimiento, tasa_facial, valor_inicial)
    precio_bono_formatted = "{:,.2f}".format(precio_bono)
    st.write(f'Valor actual del bono: {precio_bono_formatted}, el precio del bono se redujo un {((valor_inicial - precio_bono) / valor_inicial) * 100:.2f}%')
