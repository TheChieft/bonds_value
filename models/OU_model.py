import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import streamlit as st
from src.funciones_cripto import obtener_datos_cierre

fecha_actual = pd.Timestamp('today')
fecha_inicio = fecha_actual - pd.DateOffset(years=3)
criptomonedas = pd.read_csv('././data/db/criptomonedas.csv') # contiene simbolo de las 200 criptomonedas principales

# Modelo Ornstein Uhlenbeck
def simulate_ou_process4(mu, theta, sigma, X0, n_simulations = 1000, dt=1):
    X = []
    for i in range(n_simulations):
        noise = np.random.normal()
        p = X0 * np.exp(-theta*dt) + mu * (1 - np.exp(-theta*dt)) + sigma * np.sqrt((1 - np.exp(-2*theta*dt)) / (2*theta)) * noise
        X.append(p)
    return X

def model_ou():
    # opciones cripto
    cripto_option = st.sidebar.selectbox('Selecciona una criptomoneda', (criptomonedas['Símbolo']+ '-USD')) 
    data = obtener_datos_cierre(cripto_option, fecha_inicio, fecha_actual)
    # Se resaga la data
    criptosi_1 = data.drop(data.index[-1])
    criptosi = data.drop(data.index[0])
    data_eth = {}
    data_eth['X'] = criptosi_1
    data_eth['N'] = len(criptosi_1)

    # estimación parametros modelo ou con mso
    # Calcular los parámetros de la regresión lineal
    x_data = np.array(criptosi_1 )
    y_data = np.array(criptosi)
    n = len(x_data)
    S_x = np.sum(x_data)  # Suma de todos los x, excepto el último
    S_y = np.sum(y_data)       # Suma de todos los y
    S_xx = np.sum(x_data ** 2)  # Suma de los cuadrados de todos los x, excepto el último
    S_xy = np.sum(x_data * y_data)  # Suma de los productos de x (excepto el último) con y (desde el segundo en adelante)
    S_yy = np.sum(y_data ** 2)  # Suma de los cuadrados de y
    a = (n * S_xy - S_x * S_y) / (n * S_xx - S_x ** 2)
    b = (S_y - a * S_x) / n

    # Calcular el error estándar de la estimación
    sd_e = np.sqrt((n*S_yy - S_y**2 - a*(n*S_xy - S_x*S_y)) / (n*(n - 2)))
    delta = 1 
    # Estimación3s = 1 
    lambda_eth = -np.log(a) / delta
    mu_eth = b / (1 - a)
    sigma_eth = sd_e * np.sqrt(-2 * np.log(a) / (delta * (1 - a**2)))
    estimationLSE = []
    for i in criptosi:
        simulated_data = simulate_ou_process4(mu_eth, lambda_eth, sigma_eth, i, 10000)
        estimationLSE.append(np.mean(simulated_data))
