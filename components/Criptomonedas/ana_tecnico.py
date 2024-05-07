import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Función para obtener los datos de cierre de las criptomonedas seleccionadas
def obtener_datos_cierre(symbol):
    data = yf.download(symbol, start="2023-05-01", end="2024-05-01", interval="1wk")
    return data['Close']

# Definir los símbolos de criptomonedas disponibles
criptomonedas = pd.read_csv('/home/jorfan/Universidad/Defi/APP2.0/bonds_value/data/db/criptomonedas.csv')

# Lista para almacenar las criptomonedas seleccionadas
seleccionadas = []

# Desplegable para seleccionar hasta 5 opciones
for i in range(5):
    seleccion = st.selectbox(f'Selecciona la criptomoneda {i+1}', criptomonedas, key=i)
    if seleccion not in seleccionadas:
        seleccionadas.append(seleccion)

# Obtener los datos de cierre de las criptomonedas seleccionadas
datos = []
for cripto in seleccionadas:
    datos.append(obtener_datos_cierre(cripto))

# Graficar los datos
fig = go.Figure()
for i in range(len(datos)):
    fig.add_trace(go.Scatter(x=datos[i].index, y=datos[i], mode='lines', name=seleccionadas[i]))

# Personalizar el diseño del gráfico
fig.update_layout(title='Precios de cierre de criptomonedas seleccionadas',
                  xaxis_title='Fecha',
                  yaxis_title='Precio de cierre (USD)')

# Mostrar el gráfico
st.plotly_chart(fig)
