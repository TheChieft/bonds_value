import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
import datetime

# Funciones para obtener datos de precios de acciones
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date,
                       end=end_date, interval='1mo')['Adj Close']
    data_df = pd.DataFrame(data)
    # Asignar el nombre de la columna como una lista
    data_df.columns = [ticker]
    return data_df

def get_stock_cumulative_returns(ticker, start_date, end_date):
    stock_prices = get_stock_data(ticker, start_date, end_date)
    if stock_prices.empty or len(stock_prices) == 1:
        # La secuencia está vacía o tiene solo un elemento, no se pueden calcular los retornos
        return pd.Series(index=stock_prices.index, data=0.0)
    stock_returns = stock_prices.pct_change().dropna()
    stock_cumulative_returns = (1 + stock_returns).cumprod() - 1
    return stock_cumulative_returns


def calculate_capm(ticker, market_ticker, start_date, end_date):

    stock_returns = get_stock_data(ticker, start_date, end_date)
    market_returns = get_stock_data(market_ticker, start_date, end_date)

    # Calcular rendimientos logarítmicos
    stock_returns = np.log(stock_returns / stock_returns.shift(1))
    market_returns = np.log(market_returns / market_returns.shift(1))

    alpha_jensen = None
    beta_value = None
    regression_data = None

    X = market_returns[1:]  # Excluir el primer NaN
    y = stock_returns[ticker][1:]  # Excluir el primer NaN
    X = sm.add_constant(X)  # Añadir constante para el término alpha

    # Estimar CAPM: rendimiento_stock ~ alpha + beta * rendimiento_benchmark
    model = sm.OLS(y, X, missing='drop').fit()
    alpha_jensen = model.params[0]  # Alpha de Jensen
    beta_value = model.params[1]   # Beta

    # Almacenar datos de la regresión para la gráfica
    regression_data = {
        'X': X['const'].tolist(), 'y': model.fittedvalues.tolist()}

    return alpha_jensen, beta_value, regression_data, model.summary()

def calculate_stock_returns(stocks_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'], indice = ['^GSPC']):
    # Getting the stock data from yfinance
    data = yf.download(stocks_list + indice, period='5y',interval='1mo')['Adj Close']
    indice = indice[0]
    # Calculating Daily % change in stock prices
    daily_returns = data.pct_change()
    daily_returns.iloc[0,:] = 0

    # Boxplot of daily returns (in %)
    #daily_returns.boxplot(figsize=(6, 5), grid=False)

    # Initializing empty dictionaries to save results

    beta,alpha = dict(), dict()

    # Make a subplot

    # fig, axes = plt.subplots(1,3, dpi=150, figsize=(15,8))

    # axes = axes.flatten()

    # for idx, stock in enumerate(daily_returns.columns.values[:-1]):

        # scatter plot between stocks and the NSE

    #    daily_returns.plot(kind = "scatter", x = indice[0], y = stock, ax=axes[idx])

        # Fit a line (regression using polyfit of degree 1)

    #    b_, a_ = np.polyfit(daily_returns[indice[0]], daily_returns[stock], 1)

    #    regression_line = b_ * daily_returns[indice[0]] + a_

    #    axes[idx].plot(daily_returns[indice[0]], regression_line, "-", color = "r")

        # save the regression coeeficient for the current stock

    #    beta[stock] = b_
    #    alpha[stock] = a_

    # plt.show()

    # ----------------- PRUEBA CON GO ------------------------------

    fig = go.Figure()

    for idx, stock in enumerate(daily_returns.columns.values[:-1]):
        # Scatter plot entre las acciones y el índice
        fig.add_trace(go.Scatter(x=daily_returns[indice], y=daily_returns[stock],
                                 mode='markers', name=stock))

        # Ajustar una línea de regresión (usando polyfit de grado 1)
        b_, a_ = np.polyfit(daily_returns[indice], daily_returns[stock], 1)
        regression_line = b_ * daily_returns[indice] + a_

        # Añadir la línea de regresión
        fig.add_trace(go.Scatter(x=daily_returns[indice], y=regression_line,
                                 mode='lines', name=f'Regresión - {stock}', line=dict(color='red')))

        # Guardar los coeficientes de regresión para la acción actual
        beta[stock] = b_
        alpha[stock] = a_

    # Configurar el diseño de la figura
    fig.update_layout(
        autosize=True,
        title=dict(
            text='Retornos Acumulados',
            font=dict(color='white', size=20),
            x=0.35,
            y=0.9
        ),
        legend=dict(font=dict(color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_ticks='outside',
        yaxis_ticks='outside',
        xaxis_linecolor='white',
        yaxis_linecolor='white',
        showlegend=True,
        xaxis_gridcolor='rgba(255, 255, 255, 0.1)',
        yaxis_gridcolor='rgba(255, 255, 255, 0.1)',
        margin=dict(l=0, r=50, b=50, t=50),
    )

    # Mostrar el gráfico interactivo en Streamlit
    #st.plotly_chart(fig)

    keys = list(beta.keys()) # list of stock names

    beta_3 = dict()

    for k in keys:
        beta_3[k] = [daily_returns[[k,indice]].cov()/daily_returns[indice].var()][0].iloc[0,1]
        print(f"el beta de {k}: {beta[k]}")

    ER = dict()

    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=5*365)

    rf_data = yf.download('^TNX', start=start_date, end=end_date)
    # Calcular el rendimiento promedio de los bonos del Tesoro a 10 años
    rf = rf_data['Adj Close'].pct_change().mean() * 250  # Suponiendo 250 días de trading al año

    trading_days = 250

    # Estimate the expected return of the market using the daily returns

    rm = daily_returns[indice].mean() * trading_days

    for k in keys:

        # Calculate return for every security using CAPM

        ER[k] = rf + beta[k] * (rm-rf)

    for k in keys:

        print("Expected return based on CAPM model for {} is {}%".format(k, round(ER[k], 2)))

    # Calculating historic returns

    for k in keys:

        print('Return based on historical data for {} is {}%'.format(k, round(daily_returns[k].mean() * trading_days, 2)))

    historic_returns = {k: round(daily_returns[k].mean() * trading_days, 2) for k in keys}

    return fig, beta, alpha, historic_returns
