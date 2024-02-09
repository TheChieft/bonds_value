import streamlit as st
from datetime import datetime

def calcular_precio_bono_sin_cupon(valor_nominal, tasa_interes, base, fecha_actual, fecha_final):
    # Calcular el número de días entre las fechas según la base seleccionada
    if base == '30/360':
        n = (fecha_final.year - fecha_actual.year) * 360 + (fecha_final.month - fecha_actual.month) * 30 + (fecha_final.day - fecha_actual.day)
    elif base == 'Actual/365':
        n = (fecha_final - fecha_actual).days
    
    # Convertir días a años usando la base seleccionada
    if base in ['30/360']:
        años = n / 360
    elif base == 'Actual/365':
        años = n / 365
    
    precio = valor_nominal / ((1 + tasa_interes) ** años)
    return precio, años

# Título de la página
st.title('Calculadora Avanzada de Bonos Sin Cupón')

# Entradas del usuario
fecha_actual = st.date_input('Fecha actual:')
col1, col2 = st.columns(2)
with col1:
    valor_nominal = st.number_input('Ingrese el valor nominal del bono:', min_value=0.01, step=0.01)
with col2:
    base = st.selectbox('Seleccione la base para el cálculo:', ['Actual/365','30/360'])
# 2 columas
col1, col2 = st.columns(2)
with col1:
    tasa_emision = st.number_input('Ingrese la tasa de emisión', min_value=0.0, max_value=1.0, step=0.01)
with col2:
    tasa_actual = st.number_input('Ingrese la tasa actual:', min_value=0.0, max_value=1.0, step=0.01)

# 2 columas
col1, col2 = st.columns(2)
with col1:
    st.write('Fecha de emisión del bono:')
    fecha_emision = st.date_input('Fecha de emisión del bono:')
with col2:
    st.write('Fecha de vencimiento del bono:')
    fecha_final = st.date_input('Fecha de vencimiento del bono:')

# Botón para realizar el cálculo
if st.button('Calcular Precio del Bono y Evaluación de Inversión'):
    precio, años = calcular_precio_bono_sin_cupon(valor_nominal, tasa_actual, base, fecha_actual, fecha_final)
    diferencia_tasa = tasa_actual - tasa_emision
    ganancia_o_perdida = "ganancia" if diferencia_tasa > 0 else "pérdida"
    
    st.write(f'El precio del bono sin cupón, considerando una tasa actual de {tasa_actual*100:.2f}%, es: ${precio:.2f}')
    st.write(f'Con base en la diferencia de tasas de {diferencia_tasa*100:.2f}%, esto representa una {ganancia_o_perdida} potencial al invertir en este bono.')
    st.write(f'Número de años hasta el vencimiento: {años:.2f}')