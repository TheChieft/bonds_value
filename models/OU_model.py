import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import plotly.graph_objects as go
import streamlit as st
from src.funciones_cripto import obtener_datos_cierre


fecha_actual = pd.Timestamp('today')
fecha_inicio = fecha_actual - pd.DateOffset(weeks=1)
# contiene simbolo de las 200 criptomonedas principales
criptomonedas = pd.read_csv('././data/db/criptomonedas.csv')
# inrervalo de tiempo para visualizar la predicción
range_x = [fecha_actual - pd.DateOffset(days=1), fecha_actual]

# Modelo Ornstein Uhlenbeck


def simulate_ou_process4(mu, theta, sigma, X0, n_simulations=1000, dt=1):
    X = []
    for i in range(n_simulations):
        noise = np.random.normal()
        p = X0 * np.exp(-theta*dt) + mu * (1 - np.exp(-theta*dt)) + \
            sigma * np.sqrt((1 - np.exp(-2*theta*dt)) / (2*theta)) * noise
        X.append(p)
    return X


def model_ou():
    @st.cache_resource
    def grafico():
        return st.plotly_chart(fig, use_container_width=False)

    st.markdown(
        """
    <style>
        /* Estilo para cambiar la fuente, el tamaño y centrar el texto */
        .custom-text {
            font-family: Arial, sans-serif; /* Cambia la fuente a Arial o cualquier otra fuente que desees */
            font-size: 17px; /* Cambia el tamaño del texto a 20px o cualquier otro tamaño que desees */
            text-align: center; /* Centra el texto horizontalmente */
        }
    </style>
    """,
        unsafe_allow_html=True
    )
    st.divider()
    # Utiliza st.write() para mostrar texto con el estilo personalizado
    st.markdown('<p class="custom-text">El modelo de Ornstein-Uhlenbeck es usado en el ámbito de la estadística y la teoría de probabilidad para modelar la evolución de un proceso estocástico en el tiempo. Este modelo describe cómo una variable aleatoria (el precio de un activo) cambia con el tiempo, mostrando una tendencia hacia un cierto valor central o de equilibrio, al mismo tiempo que experimenta fluctuaciones aleatorias.</p>', unsafe_allow_html=True)
    # opciones cripto
    st.divider()
    cripto_option = st.sidebar.selectbox(
        'Selecciona una criptomoneda', (criptomonedas['Símbolo'] + '-USD'))
    data = obtener_datos_cierre(
        cripto_option, fecha_inicio, fecha_actual, intervalo="5m")
    # Se resaga la data
    criptosi_1 = data.drop(data.index[-1])
    criptosi = data.drop(data.index[0])
    criptosi_future = criptosi.index + pd.DateOffset(minutes=5)
    data_eth = {}
    data_eth['X'] = criptosi_1
    data_eth['N'] = len(criptosi_1)

    # estimación parametros modelo ou con mso
    # Calcular los parámetros de la regresión lineal
    x_data = np.array(criptosi_1)
    y_data = np.array(criptosi)
    n = len(x_data)
    S_x = np.sum(x_data)  # Suma de todos los x, excepto el último
    S_y = np.sum(y_data)       # Suma de todos los y
    # Suma de los cuadrados de todos los x, excepto el último
    S_xx = np.sum(x_data ** 2)
    # Suma de los productos de x (excepto el último) con y (desde el segundo en adelante)
    S_xy = np.sum(x_data * y_data)
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
    # lista que contiene las estimaciones
    estimationLSE = []
    for i in criptosi:
        simulated_data = simulate_ou_process4(mu_eth, lambda_eth, sigma_eth, i)
        estimationLSE.append(np.mean(simulated_data))

    # Grafico
    # def grafico():
    trace1 = go.Scatter(
        x=criptosi.index,
        y=criptosi,
        mode='lines',
        name='Precios reales',
        # line=dict( width=1),
        opacity=0.9
    )

    trace2 = go.Scatter(
        x=criptosi_future,
        y=estimationLSE,
        mode='lines',
        name='Precios predichos',
        # line=dict(width=1),
        opacity=0.9
    )

    # Create the figure
    fig = go.Figure(data=[trace1, trace2])

    # Update layout with desired styling
    fig.update_layout(
        width=1000,
        height=450,
        xaxis=dict(
            tickcolor='white',
            tickfont=dict(color='white'),
            title=dict(text='TIempo', font=dict(color='white')),
            showgrid=True,
            ticks='outside',
            linecolor='white',
            gridcolor='rgba(255, 255, 255, 0.1)', range=range_x
        ),
        yaxis=dict(
            tickcolor='white',
            tickfont=dict(color='white'),
            title=dict(text='Precio', font=dict(color='white')),
            showgrid=True,
            ticks='outside',
            linecolor='white',
            gridcolor='rgba(255, 255, 255, 0.1)',
        ),
        title=dict(
            text=f'Ornstein-Uhlenbeck Process Simulation {cripto_option}',
            y=1,
            x=0.5,
            xanchor='center',
            yanchor='top',
        ),
        legend=dict(font=dict(color='white')),
        margin=dict(l=20, r=50, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'


    )

    mitad, _ = st.columns([8, 1])
    with mitad:
        grafico()
    st.divider()
    # RMSE
    LSEsse = []
    for i, j in zip(y_data[1:], estimationLSE[:-1]):
        LSEsse.append((i-j)**2)
    LSE_MSE = sum(LSEsse)/len(LSEsse)
    LSE_RMSE = np.sqrt(LSE_MSE)
    LSE_RMSE = round(LSE_RMSE, 2)
    # R²

    def r_squared(y_true, y_pred):
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        return round(r2, 3)
    r_squared(criptosi[1:], estimationLSE[:-1])
    col01, col02 = st.columns([400, 600])
    with col02:
        col1, col2, col3 = st.columns(3)
        col1.metric('Precio siguiente',
                    f'{round(estimationLSE[-1],2)}', f'{round(criptosi[-1]-estimationLSE[-1],2)}')
        col2.metric('RMSE', f'{LSE_RMSE}')
        col3.metric('R²', f'{r_squared(criptosi,estimationLSE)}')
    with col01:
        # crear dataframe con los resultados
        resultados = pd.DataFrame()
        resultados['Precios Reales'] = criptosi
        resultados['Precios Predichos'] = estimationLSE
        st.dataframe(resultados, width=450, height=520)
