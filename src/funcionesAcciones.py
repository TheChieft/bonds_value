import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
import datetime
import statsmodels.api as sm
from urllib3.exceptions import MaxRetryError, NewConnectionError

# Funciones para obtener datos de precios de acciones


def get_symbols(market):
    nyse_symbols = pd.read_csv(f'././data/db/{market}.csv', header=0)
    return nyse_symbols


def get_stock_data(ticker, start_date, end_date, max_retries=3):
    for _ in range(max_retries):
        try:
            data = yf.download(ticker, start=start_date,
                               end=end_date, interval='1mo')['Adj Close']
            data_df = pd.DataFrame(data)
            # Asignar el nombre de la columna como una lista
            data_df.columns = [ticker]
            return data_df
        except (MaxRetryError, NewConnectionError) as e:
            print(f"Error de conexión: {e}")
            print("Reintentando...")
    raise Exception(
        f"No se pudo descargar los datos después de {max_retries} intentos")


def get_stock_cumulative_returns(ticker, start_date, end_date):
    stock_prices = get_stock_data(ticker, start_date, end_date)
    if stock_prices.empty or len(stock_prices) == 1:
        # La secuencia está vacía o tiene solo un elemento, no se pueden calcular los retornos
        return pd.Series(index=stock_prices.index, data=0.0)
    stock_returns = stock_prices.pct_change().dropna()
    stock_cumulative_returns = (1 + stock_returns).cumprod() - 1
    return stock_cumulative_returns


def descargar_datos(ticker, start_date, end_date, max_retries=3):
    for _ in range(max_retries):
        try:
            data = yf.download(ticker, start=start_date, end=end_date, interval='1mo')[
                'Adj Close'].reset_index()
            return data
        except (MaxRetryError, NewConnectionError) as e:
            print(f"Error de conexión: {e}")
            print("Reintentando...")
    raise Exception(
        f"No se pudo descargar los datos después de {max_retries} intentos")


def calcular_alpha_beta(start_date, end_date, acciones_ticker, mercado_ticker=['^GSPC'], bono_ticker='^TNX'):
    resultados_dict = {}
    mercado_data = descargar_datos(mercado_ticker, start_date, end_date)
    bono_data = descargar_datos(bono_ticker, start_date, end_date)

    for accion_ticker in acciones_ticker:
        try:
            # Descargar datos de Yahoo Finance
            accion_data = descargar_datos(accion_ticker, start_date, end_date)

        # Resto del código para procesar los datos...

        except (MaxRetryError, NewConnectionError) as e:
            st.warning(f"Error de conexión para {accion_ticker}: {e}")
            st.warning("Por favor, recarga la página e intenta nuevamente.")
            st.stop()  # Detiene la ejecución de la aplicación de Streamlit

        except Exception as e:
            st.warning(f"Error al procesar {accion_ticker}: {e}")
            st.warning("Por favor, recarga la página e intenta nuevamente.")
            st.stop()  # Detiene la ejecución de la aplicación de Streamlit

        # Calcular rendimientos logarítmicos
        rendimientos_accion = np.log(
            accion_data['Adj Close'] / accion_data['Adj Close'].shift(1)).dropna()
        rendimientos_mercado = np.log(
            mercado_data['Adj Close'] / mercado_data['Adj Close'].shift(1)).dropna()

        # Calcular tasa mensual para el bono
        def tasa_mensual(x):
            return (1 + (x / 100)) ** (1 / 12) - 1

        tasa_libre_riesgo = pd.DataFrame(
            {'tasa_mensual': bono_data['Adj Close'].iloc[1:].apply(tasa_mensual)})

        # Calcular excesos de retornos
        accion_er = rendimientos_accion - tasa_libre_riesgo['tasa_mensual']
        marcado_er = rendimientos_mercado - tasa_libre_riesgo['tasa_mensual']

        # Concatenar las series de excesos de retornos
        df_excesos = pd.concat([accion_er, marcado_er], axis=1).dropna()
        df_excesos.columns = ['accion_er', 'marcado_er']

        # Agregar una columna de unos para representar el intercepto
        df_excesos['intercepto'] = 1
        # Ajustar el modelo de regresión lineal
        modelo = sm.OLS(df_excesos['accion_er'],
                        df_excesos[['marcado_er', 'intercepto']])

        resultados = modelo.fit()

        # Obtener los coeficientes del modelo
        coeficientes = resultados.params
        alpha, beta = coeficientes['intercepto'], coeficientes['marcado_er']

        resultados_dict[accion_ticker] = {'alpha': alpha, 'beta': beta}

    fig = go.Figure()

    colores_pastel = ['rgb(255, 223, 186)', 'rgb(173, 216, 230)',
                      'rgb(144, 238, 144)', 'rgb(221, 160, 221)', 'rgb(255, 165, 0)']

    for accion_ticker, valores in resultados_dict.items():
        # Valores de beta para trazar la línea
        beta_values = np.linspace(0, max(valores['beta'], 4), 100)

        # Calcula la línea CAPM
        SML_values = valores['alpha'] + beta_values * \
            (rendimientos_mercado.mean() -
             tasa_libre_riesgo['tasa_mensual'].mean())

        # Usa el operador de módulo para obtener el índice correcto del color
        selected_color = colores_pastel[len(fig.data) % len(colores_pastel)]

        # Agrega la línea CAPM
        fig.add_trace(go.Scatter(x=beta_values, y=SML_values, mode='lines', line=dict(
            color=selected_color, width=2), name=f'{accion_ticker} - SML', hoverlabel=dict(font=dict(color='white')), hovertext=[f'{accion_ticker} - SML']*len(beta_values)))

        # Agrega el punto de intersección (alpha) sin leyenda
        fig.add_trace(go.Scatter(x=[valores['beta']], y=[valores['alpha'] + valores['beta'] * (rendimientos_mercado.mean() - tasa_libre_riesgo['tasa_mensual'].mean())],
                                 mode='markers', marker=dict(color='blue' if valores['alpha'] < 0 else 'red', size=8), name=f'{accion_ticker} - Rentabilidad Esperada', hoverlabel=dict(font=dict(color='white'))))

        # Ajusta los ejes x e y
        fig.update_xaxes(tickcolor='white', tickfont=dict(
            color='white'), title=dict(text='Beta (Riesgo Sistemático)', font=dict(color='white')), dtick=0.4)
        fig.update_yaxes(tickcolor='white', tickfont=dict(
            color='white'), title=dict(text='Rentabilidad Esperada', font=dict(color='white')), dtick=0.02)

        # Ajusta el título general
        fig.update_layout(
            title=dict(
                text='CAPM - Capital Asset Pricing Model',
                font=dict(color='white', size=20),
                x=0.1,
                y=0.9  # Ajusta la posición del título
            ),
            # showlegend=True,
            legend=dict(font=dict(color='white')),
            width=600,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',  # Fondo del papel transparente
            plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
            xaxis_showgrid=True,
            yaxis_showgrid=True,
            xaxis_ticks='outside',
            yaxis_ticks='outside',
            xaxis_linecolor='white',
            yaxis_linecolor='white',
            # showlegend=True,
            # Color de la cuadrícula del eje x con alpha
            xaxis_gridcolor='rgba(255, 255, 255, 0.1)',
            # Color de la cuadrícula del eje x con alpha
            yaxis_gridcolor='rgba(255, 255, 255, 0.1)',
            margin=dict(l=0, r=0, b=0, t=70),
        )

    return resultados_dict, fig
