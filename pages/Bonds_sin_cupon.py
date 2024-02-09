import streamlit as st
from datetime import datetime
import numpy as np

def calcular_precio_bono_sin_cupon(fecha_actual, fecha_final, tasa_actual, valor_esperado, fecha_emision):
    """
    B(tiempo_actual, tiempo_final, tasa_actual) = e^(-r(fecha_final-fecha_actual))
    """
    return valor_esperado * np.exp(-tasa_actual * ((fecha_final - fecha_actual).days / (fecha_final - fecha_emision).days))
    
# Título de la página
st.title('Calculadora Avanzada de Bonos Sin Cupón')

# 2 columas
col1, col2, col3 = st.columns(3)

with col1:
    fecha_emision = st.date_input('Fecha de emision del bono:')
with col2:
    fecha_final = st.date_input('Fecha de vencimiento del bono:')
with col3:
    fecha_compra = st.date_input('Fecha compra:',min_value=fecha_emision,max_value=fecha_final)

# Entradas del usuario

col1, col2 = st.columns(2)
with col1:
    valor_esperado = int(st.number_input('Ingrese el valor esperado del bono:', min_value=0.0))
with col2:
    base = st.selectbox('Seleccione la base para el cálculo:', ['365'])

col1, col2 = st.columns(2)

with col1:
    tasa_emision = st.number_input('Ingrese la tasa de emisión:')/100
with col2:
    tasa_actual = st.number_input('Ingrese la tasa actual:')/100

# Botón para realizar el cálculo
if st.button('Calcular Precio del Bono y Evaluación de Inversión'):
    diferencia_tasa = tasa_actual - tasa_emision
    precio = calcular_precio_bono_sin_cupon(fecha_compra, fecha_final, tasa_actual, valor_esperado,fecha_emision)
    st.write(f'Valor del bono: {precio}')
    if precio >= valor_esperado:
        st.write('La inversión no es rentable')
    else:
        st.write('La inversión es rentable')
    st.write(f'La diferencia de tasas es: {diferencia_tasa}')
    