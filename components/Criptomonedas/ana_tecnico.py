import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Función para obtener los datos de cierre de las criptomonedas seleccionadas
def obtener_datos_cierre(symbol):
    data = yf.download(symbol, start="2023-05-01", end="2024-05-01", interval="1wk")
    return data['Close'].tolist()

# Definir los símbolos de criptomonedas disponibles
criptomonedas = pd.read_csv('././data/db/criptomonedas.csv')
criptomonedas = criptomonedas['Símbolo'].tolist()

# Lista para almacenar las criptomonedas seleccionadas
seleccionadas = []

cripto_option = st.sidebar.selectbox('Selecciona un criptomoneda', criptomonedas, criptomonedas['btc'])
