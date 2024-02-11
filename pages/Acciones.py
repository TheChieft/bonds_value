import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from scipy.stats import linregress

# Obtener la lista de símbolos de las empresas que cotizan en el NYSE
nyse_symbols = pd.read_csv('data/db/nasdaq_screener.csv', header=0)

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5*365)


def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date, interval='1mo')
    return data['Adj Close']


def get_stock_cumulative_returns(ticker, start_date, end_date):
    stock_prices = get_stock_data(ticker, start_date, end_date)
    stock_returns = stock_prices.pct_change().dropna()
    stock_cumulative_returns = (1 + stock_returns).cumprod() - 1
    return stock_cumulative_returns


def calculate_capm(ticker, market_ticker, start_date, end_date):
    stock_returns = get_stock_data(
        ticker, start_date, end_date).pct_change().dropna()
    market_returns = get_stock_data(
        market_ticker, start_date, end_date).pct_change().dropna()

    slope, intercept, r_value, p_value, std_err = linregress(
        market_returns, stock_returns)

    expected_return = intercept + slope * market_returns.mean()
    beta = slope

    return expected_return, beta


# Mapeo de siglas a nombres completos
index_mapping = {
    "^GSPC": "S&P 500",
    "^DJI": "Dow Jones Industrial Average",
    "^IXIC": "Nasdaq Composite",
    "^RUT": "Russell 2000"
}

# Streamlit app
st.title("Modelo CAPM")

st.header("Parámetros")
# Crear columnas para organizar el diseño
col1, col2 = st.columns([1, 2])

# Input form en la columna de la derecha
with col1:
    # Menú desplegable para seleccionar las empresas
    selected_tickers = st.multiselect(
        "Select Stock Tickers (Max 4):", nyse_symbols['Symbol'].to_list(), default=["AAPL"]
    )

    if len(selected_tickers) > 4:
        st.warning("Por favor, selecciona un máximo de 4 activos.")
        st.stop()

with col2:
    # Menú desplegable para seleccionar el índice del mercado
    market_ticker_options = list(index_mapping.values())
    selected_index_name = st.selectbox(
        "Select Market Index:", market_ticker_options)

    # Obtener la sigla correspondiente al índice seleccionado
    market_ticker = [key for key, value in index_mapping.items(
    ) if value == selected_index_name][0]

# Obtener datos de precios de las acciones seleccionadas
stock_prices = [get_stock_data(ticker, start_date, end_date)
                for ticker in selected_tickers]

stock_returns = [get_stock_cumulative_returns(ticker, start_date, end_date)
                 for ticker in selected_tickers]
# --- Menú gráficos ---

selected_chart = st.selectbox("Gráfico:", [
                              "Precios", "Retornos acumulados"])

# ---- Gráfico precios ----

if selected_chart == 'Precios':

    fig = go.Figure()

    # Agregar las líneas de precios de acciones
    for i, stock_price in enumerate(stock_prices):
        fig.add_trace(go.Scatter(x=stock_price.index, y=stock_price,
                                 mode='lines', name=f'{selected_tickers[i]}'))

    # Configurar el diseño del gráfico
    fig.update_xaxes(tickcolor='white', tickfont=dict(color='white'), title=dict(
        text='Fecha', font=dict(color='white')))
    fig.update_yaxes(tickcolor='white', tickfont=dict(color='white'), title=dict(
        text='Precio de cierre', font=dict(color='white')))

    # Ajustar el título general
    fig.update_layout(
        title=dict(
            text='Precios de acciones',
            font=dict(color='white', size=20),
            x=0.35,
            y=0.9
        ),
        showlegend=True,
        legend=dict(font=dict(color='white')),
        width=700,
        height=400
    )

    # Ajustar el diseño financiero
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del papel transparente
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_ticks='outside',
        yaxis_ticks='outside',
        xaxis_linecolor='white',
        yaxis_linecolor='white',
        showlegend=True,
        # Color de la cuadrícula del eje x con alpha
        xaxis_gridcolor='rgba(255, 255, 255, 0.1)',
        # Color de la cuadrícula del eje x con alpha
        yaxis_gridcolor='rgba(255, 255, 255, 0.1)'
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

# ---- Gráfico retornos ----
if selected_chart == 'Retornos acumulados':
    fig = go.Figure()

    # Agregar las líneas de precios de acciones
    for i, stock_returns in enumerate(stock_returns):
        fig.add_trace(go.Scatter(x=stock_returns.index, y=stock_returns,
                                 mode='lines', name=f'{selected_tickers[i]}'))

    # Configurar el diseño del gráfico
    fig.update_xaxes(tickcolor='white', tickfont=dict(color='white'), title=dict(
        text='Fecha', font=dict(color='white')))
    fig.update_yaxes(tickcolor='white', tickfont=dict(color='white'), title=dict(
        text='Retorno', font=dict(color='white')))

    # Ajustar el título general
    fig.update_layout(
        title=dict(
            text='Retornos Acumulados',
            font=dict(color='white', size=20),
            x=0.35,
            y=0.9
        ),
        showlegend=True,
        legend=dict(font=dict(color='white')),
        width=700,
        height=400
    )

    # Ajustar el diseño financiero
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del papel transparente
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_ticks='outside',
        yaxis_ticks='outside',
        xaxis_linecolor='white',
        yaxis_linecolor='white',
        showlegend=True,
        # Color de la cuadrícula del eje x con alpha
        xaxis_gridcolor='rgba(255, 255, 255, 0.1)',
        # Color de la cuadrícula del eje x con alpha
        yaxis_gridcolor='rgba(255, 255, 255, 0.1)'
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

# Calculate CAPM for each selected stock
for ticker in selected_tickers:
    expected_return, beta = calculate_capm(
        ticker, market_ticker, start_date, end_date)

    # Display results for each stock en la columna de la izquierda

    st.subheader(f"Resultados para {ticker} en {selected_index_name}:")
    st.write(f"Market Ticker: {market_ticker}")
    st.write(f"Expected Return: {expected_return:.4%}")
    st.write(f"Beta: {beta:.4}")
    st.write("----")

# Additional charts or information can be added as needed
