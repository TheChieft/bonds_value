import streamlit as st
from datetime import datetime
import numpy as np
import pandas as pd
from src.FuncionesBonos import calcular_bono_con_cupon, generar_tabla_bono_con_cupon,generar_tabla_bono_con_cupon2

st.title('Calculadora Avanzada de Bonos con Cupón')
st.write('Esta aplicación te permite calcular el precio de un bono con cupón y evaluar la rentabilidad de la inversión.')

# Sección de pestañas
tab1, tab2, tab3 = st.tabs(['Valor por retorno','Retorno por valor','Precio del bono actual'])

with tab1:
    col1,col2 = st.columns(2)
    with col1:
        fecha_compra = st.date_input('Fecha compra', value=datetime.now(), key='fecha_compra_tab1')
        tasa_facial = st.number_input('Tasa de interés (EA%)', min_value=0.0000, value=0.0000, format='%f', key='tasa_facial_tab1')
    with col2:
        fecha_vencimiento = st.date_input('Fecha de vencimiento del bono', min_value=fecha_compra + pd.Timedelta(days=365), value=fecha_compra + pd.Timedelta(days=365), key='fecha_vencimiento_tab1')
        valor_nominal = st.number_input('Valor nominal del bono', min_value=0, value=0, format='%i', key='valor_nominal_tab1')
    tasa_referencia = st.number_input('Tasa de interés de referencia (EA%)', min_value=0.0000, value=0.0000, format='%f', key='tasa_referencia_tab1')
    años=(fecha_vencimiento-fecha_compra).days/365
    VPFCB, T_VPFCB, T_cuadrado_VPFCB, T_cuadrado_VPFCB_TVPFCB, duracion, convexidad = calcular_bono_con_cupon(años, tasa_facial, valor_nominal, tasa_referencia)
    st.dataframe(generar_tabla_bono_con_cupon(fecha_compra,fecha_vencimiento,tasa_facial, valor_nominal,tasa_referencia))
    st.dataframe(generar_tabla_bono_con_cupon2(fecha_compra,fecha_vencimiento,tasa_facial, valor_nominal,tasa_referencia))
    st.metric('Precio del bono', VPFCB, 'S/.')
    st.metric('Duración', duracion, 'años')
    st.metric('Convexidad', convexidad, 'S/.')
    st.metric('T*VPFCB', T_VPFCB, 'S/.')
    st.metric('T²*VPFCB', T_cuadrado_VPFCB, 'S/.')
    st.metric('T²*VPFCB_TVPFCB', T_cuadrado_VPFCB_TVPFCB, 'S/.')
    
with tab2:
    st.write('En construcción')
with tab3:
    st.write('En construcción')