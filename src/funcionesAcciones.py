import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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

def CAPM_model_con_grafiquita(rendimientos_mensuales, Rf, Rm):
    beta, alpha = dict()
    fig = plt.figure(figsize=(10, 6), dpi=80)
    # Estimar CAPM: rendimiento_stock ~ alpha + beta * rendimiento_benchmark
    for i, stock in enumerate(rendimientos_mensuales):
        rendimientos_mensuales.plot(kind="scatter", x=)
    

    

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=beta_values, y=SML_values, mode='lines', line=dict(color='red' if B<0 or Rf>Rm else 'green', width=4), name='SML'))
    # Agrega el punto de corte
    fig.add_trace(go.Scatter(x=[B], y=[Rf + B * (Rm - Rf)], mode='markers', marker=dict(color='blue' if B<0 or Rf>Rm else 'red', size=10), name='Rentabilidad Esperada'))

    fig.update_xaxes(tickcolor='white', tickfont=dict(color='white'),
                     title=dict(text='Beta (Riesgo Sistemático)', font=dict(color='white')), dtick=0.4)
    fig.update_yaxes(tickcolor='white', tickfont=dict(color='white'),
                     title=dict(text='Rentabilidad Esperada', font=dict(color='white')), dtick= 0.02 if Rf!=Rm else 0.4 )

    # Ajusta el título general
    fig.update_layout(
        title=dict(
            text='CAPM - Capital Asset Pricing Model',
            font=dict(color='white', size=20),
            x=0.41,
            y=0.9
        ),
        showlegend=True,
        legend=dict(font=dict(color='white')),
        width=700,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del papel transparente
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_ticks='outside',
        yaxis_ticks='outside',
        xaxis_linecolor='white',
        yaxis_linecolor='white',
        showlegend=True,
        xaxis_gridcolor='rgba(255, 255, 255, 0.1)',  # Color de la cuadrícula del eje x con alpha
        yaxis_gridcolor='rgba(255, 255, 255, 0.1)'  # Color de la cuadrícula del eje x con alpha
    )

    fig.show()