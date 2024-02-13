import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import numpy as np
import datetime
import plotly.graph_objects as go
from scipy.stats import linregress
import statsmodels.api as sm
from streamlit_extras.metric_cards import style_metric_cards
from src.funcionesAcciones import get_stock_data, get_stock_cumulative_returns, calculate_capm, calculate_stock_returns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

# -------------------------------------------------------------
# Configuraciones de la página
st.set_page_config(layout="wide", page_title="Fondos & Modelos CAPM", page_icon="📈")

# -------------------------------------------------------------
# Streamlit app
st.title("Modelo CAPM")

st.markdown(
    '''Como representación de mercado de Estados Unidos se utiliza en la práctica un índice bursátil representativo de 
    las acciones o fondos que en él cotizan, tales como el Dow Jones, S&P 500, Nasdaq Composite y Russell 2000, por defecto se toma el S&P 500
    y se recomienda porque incluye 500 de las empresas más grandes y representativas cotizadas en las bolsas de valores de EE.UU. 
    Estas empresas provienen de diversos sectores, lo que lo convierte en un buen indicador de la salud general del mercado estadounidense.
    ''')
# -------------------------------------------------------------

nyse_symbols = [
    "VIVAX", "NAESX", "VIMSX", "VEIEX", "VISVX", "VFINX", 
    "VWELX", "VWNDX", "VEXPX", "VWUSX", "VQNPX", # Fondos iniciales
    "0P00006AEG.TW", "BPTIX", "INPSX", "0P00006AH3.TW", "INPIX", 
    "0P0001DFU6.TW", "0P00006AKS.TW", "0P00006A9Z.TW", "RYELX", "RYSIX" # Fondos adicionales
]
# -------------------------------------------------------------

# Fechas de inicio y fin
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5*365)

# -------------------------------------------------------------

# Mapeo de siglas a nombres completos
index_mapping = {
    "^GSPC": "S&P 500",
    "^DJI": "Dow Jones",
    "^IXIC": "Nasdaq Composite",
    "^RUT": "Russell 2000"
}

# -------------------------------------------------------------
# Sidebar

# Input form in the sidebar
st.sidebar.title("Parámetros")

# Menú desplegable para seleccionar las empresas
selected_tickers = st.sidebar.multiselect(
    "Select Stock Tickers:", nyse_symbols, default=["VIVAX"],
)

if not selected_tickers:
    st.warning("Por favor, selecciona al menos una acción.")
    st.stop()


# Menú desplegable para seleccionar el índice del mercado
market_ticker_options = list(index_mapping.values())
selected_index_name = st.sidebar.selectbox(
    "Select Market Index:", market_ticker_options)

# Obtener la sigla correspondiente al índice seleccionado
market_ticker = [key for key, value in index_mapping.items(
) if value == selected_index_name][0]

# Obtener datos de precios de las acciones seleccionadas
stock_prices = [get_stock_data(ticker, start_date, end_date)
                for ticker in selected_tickers]

stock_returns = [get_stock_cumulative_returns(ticker, start_date, end_date)
                 for ticker in selected_tickers]

# Convertir listas a DataFrames
df_stock_prices = pd.concat(stock_prices, axis=1)
df_stock_returns = pd.concat(stock_returns, axis=1)


# -------------------------------------------------------------
# Configuraciones para la tabla
# Ajusta según la cantidad de activos
table_height = 400
table_width = 400

with st.expander("Precios"):
    col1, col2 = st.columns(2)
    with col1:
        # Mostrar tabla de precios
        st.subheader("Precios")
        st.dataframe(df_stock_prices, height=table_height, width=table_width)
    with col2:
        precios = go.Figure()
        for i, stock_prices_df in enumerate(stock_prices):
            precios.add_trace(go.Scatter(x=stock_prices_df.index, y=stock_prices_df.iloc[:, 0],  # Utilizamos iloc para seleccionar la columna
                                        mode='lines', name=f'{selected_tickers[i]}'))
        precios.update_xaxes(tickcolor='white', tickfont=dict(color='white'), title=dict(text='Fecha', font=dict(color='white')))
        precios.update_yaxes(tickcolor='white', tickfont=dict(color='white'), title=dict(text='Precio de cierre', font=dict(color='white')))
        precios.update_layout(
            autosize=True,
            title=dict(
                text='Precios de Fondos',
                font=dict(color='white', size=20),
                x=0.35,
                y=0.9
            ),
            legend=dict(font=dict(color='white')),
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
            yaxis_gridcolor='rgba(255, 255, 255, 0.1)',
            margin=dict(l=0, r=50, b=50, t=50),
        )
        
        st.plotly_chart(precios)

# -- Retornos acumulados --
with st.expander("Retornos "):
    col1, col2 = st.columns(2)
    with col1:
        # Mostrar tabla de retornos
        st.subheader("Retornos")
        st.dataframe(df_stock_returns, height=table_height, width=table_width)
        

    with col2:
        fig = go.Figure()

        # Agregar las líneas de precios de acciones
        for i, stock_return_df in enumerate(stock_returns):
            fig.add_trace(go.Scatter(x=stock_return_df.index, y=stock_return_df.iloc[:, 0],  # Utilizamos iloc para seleccionar la columna
                                    mode='lines', name=f'{selected_tickers[i]}'))

        # Configurar el diseño del gráfico
        fig.update_xaxes(tickcolor='white', tickfont=dict(color='white'), title=dict(
            text='Fecha', font=dict(color='white')))
        fig.update_yaxes(tickcolor='white', tickfont=dict(color='white'), title=dict(
            text='Retorno', font=dict(color='white')))

        # Ajustar el título general
        fig.update_layout(
            autosize=True,
            title=dict(
                text='Retornos Acumulados',
                font=dict(color='white', size=20),
                x=0.35,
                y=0.9
            ),
            legend=dict(font=dict(color='white')),
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
            yaxis_gridcolor='rgba(255, 255, 255, 0.1)',
            margin=dict(l=0, r=50, b=50, t=50),
        )
        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)


# ---- Gráfico CAPM ----

# Obtén el primer ticker de la lista seleccionada
default_ticker = selected_tickers[0]

# Crea el menú desplegable inicial con el primer ticker
selected_stock = st.selectbox(
    "Seleccione una acción:",
    selected_tickers,
    index=selected_tickers.index(default_ticker),
)

# Muestra las tarjetas de métricas solo para el ticker seleccionado
# Itera sobre los tickers y muestra las tarjetas de métricas solo para el ticker seleccionado
# ---- Gráfico CAPM ----

# Itera sobre los tickers y muestra las tarjetas de métricas solo para el ticker seleccionado
for i, ticker in enumerate(selected_tickers):
    fig, betas, alphas, historic_returns = calculate_stock_returns([ticker], [market_ticker])

    # Muestra las tarjetas de métricas solo para el ticker seleccionado
    if ticker == selected_stock:
        col1, col2, col3 = st.columns(3)
        col1.metric('Market Ticker:', value=market_ticker)
        col2.metric('Alpha (Jensen):', value=round(alphas[ticker],4))
        col3.metric('Beta:', value=round(betas[ticker],4))
        style_metric_cards(background_color='rgba(0,0,0,0)', border_left_color="#003C6F",
                           border_color="#003C6F", box_shadow="blue")
        st.write("----")

        # Gráfico CAPM
        st.title("Gráfico CAPM")
        st.plotly_chart(fig)

gb, ga = st.columns(2)

with gb:
# Crear un gráfico de barras para los Betas
    fig_betas = go.Figure()

    # Iterar sobre los tickers seleccionados
    for ticker in selected_tickers:
        # Calcular los Betas
        _, betas, _, _ = calculate_stock_returns([ticker], [market_ticker])
        
        # Agregar una barra para el Beta de la acción actual
        fig_betas.add_trace(go.Bar(x=[ticker], y=[betas[ticker]], name=ticker))

    # Configurar el diseño del gráfico de Betas
    fig_betas.update_layout(
        title=dict(
                text='Betas',
                font=dict(color='white', size=20),
                x=0.4,
                y=0.9
            ),
        xaxis_title='Fondos',
        yaxis_title='Beta',
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del papel transparente
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
        xaxis=dict(tickfont=dict(color='white')),
        yaxis=dict(tickfont=dict(color='white')),
        font=dict(color='white'),
    )

    # Mostrar el gráfico de Betas en Streamlit
    st.plotly_chart(fig_betas)

with ga:
# Crear un gráfico de barras para los Betas
    fig_alphas = go.Figure()

    # Iterar sobre los tickers seleccionados
    for ticker in selected_tickers:
        # Calcular los Betas
        _, _, alphas, _ = calculate_stock_returns([ticker], [market_ticker])
        
        # Agregar una barra para el Beta de la acción actual
        fig_alphas.add_trace(go.Bar(x=[ticker], y=[alphas[ticker]], name=ticker))

    # Configurar el diseño del gráfico de Betas
    fig_alphas.update_layout(
        title=dict(
                text='Alphas',
                font=dict(color='white', size=20),
                x=0.4,
                y=0.9
            ),
        xaxis_title='Fondos',
        yaxis_title='Alpha',
        barmode='group',
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del papel transparente
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
        xaxis=dict(tickfont=dict(color='white')),
        yaxis=dict(tickfont=dict(color='white')),
        font=dict(color='white'),
    )

    # Mostrar el gráfico de Betas en Streamlit
    st.plotly_chart(fig_alphas)

