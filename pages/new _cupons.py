import streamlit as st
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('Calculadora Avanzada de Bonos con Cupón')
st.write('Esta aplicación te permite calcular el precio de un bono con cupón y evaluar la rentabilidad de la inversión.')

# Calculo del bono por año 
def cupon_bond (c, r, t0, t, T,VB):

    base = 365
    rd = ((1+r)**(1/base))-1
    bond = c*((((1+rd)**(T.days()-t.days()))-1)/((1+rd)**(T.days()-t.days()))*r) + 100/(1+rd)**(T.days()-t.days())
    result = (bond * VB)/100
    return(result)

col1, col2, col3 = st.columns(3)
with col1:
    fecha_emision = st.date_input('Ingresa la fecha de emisión: ')
    c = st.number_input('Ingrese la tasa de emisión: ')
with col2:
    fecha_vencimiento = st.date_input('Ingresa fecha de vencimiento: ')
    r = st.number_input('Ingrese la tasa de negociación: ')
with col3:
    fecha_compra = st.date_input('Ingresa la fecha de compra: ')
    if fecha_compra < fecha_emision or fecha_compra > fecha_vencimiento:
        st.warning('Ingrese una fecha válida')



