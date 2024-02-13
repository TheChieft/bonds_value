#importing required libraries
import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import scipy.stats as stats
import plotly.graph_objects as go

#getting historic stock data from yfinance

def calculate_stock_returns(stocks_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'], index = ['^GSPC']):
    # Getting the stock data from yfinance
    data = yf.download(stocks_list + index, period='5y',interval='1mo')['Adj Close']

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

    #    daily_returns.plot(kind = "scatter", x = index[0], y = stock, ax=axes[idx])

        # Fit a line (regression using polyfit of degree 1)

    #    b_, a_ = np.polyfit(daily_returns[index[0]], daily_returns[stock], 1)

    #    regression_line = b_ * daily_returns[index[0]] + a_

    #    axes[idx].plot(daily_returns[index[0]], regression_line, "-", color = "r")

        # save the regression coeeficient for the current stock

    #    beta[stock] = b_
    #    alpha[stock] = a_

    # plt.show()

    # ----------------- PRUEBA CON GO ------------------------------

    fig = go.Figure()

    for idx, stock in enumerate(daily_returns.columns.values[:-1]):
        # Scatter plot entre las acciones y el índice
        fig.add_trace(go.Scatter(x=daily_returns[index[0]], y=daily_returns[stock],
                                 mode='markers', name=stock))

        # Ajustar una línea de regresión (usando polyfit de grado 1)
        b_, a_ = np.polyfit(daily_returns[index[0]], daily_returns[stock], 1)
        regression_line = b_ * daily_returns[index[0]] + a_

        # Añadir la línea de regresión
        fig.add_trace(go.Scatter(x=daily_returns[index[0]], y=regression_line,
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
    st.plotly_chart(fig)

    keys = list(beta.keys()) # list of stock names

    beta_3 = dict()

    for k in keys:
        beta_3[k] = [daily_returns[[k,'^GSPC']].cov()/daily_returns['^GSPC'].var()][0].iloc[0,1]
        print(f"el beta de {k}: {beta[k]}")

    ER = dict()

    rf = 0.0733

    trading_days = 250

    # Estimate the expected return of the market using the daily returns

    rm = daily_returns[index[0]].mean() * trading_days

    for k in keys:

        # Calculate return for every security using CAPM

        ER[k] = rf + beta[k] * (rm-rf)

    for k in keys:

        print("Expected return based on CAPM model for {} is {}%".format(k, round(ER[k], 2)))

    # Calculating historic returns

    for k in keys:

        print('Return based on historical data for {} is {}%'.format(k, round(daily_returns[k].mean() * trading_days, 2)))


calculate_stock_returns()
