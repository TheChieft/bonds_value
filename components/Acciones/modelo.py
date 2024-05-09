import datetime
import time
import yfinance as yf
import streamlit as st

from components.text import text
from src.funcionesAcciones import get_symbols
from components.backtesting_pred import data, graph

md1 = open('././markdown/hn_model.md').read()


@st.cache_resource
def grafico(ts):
    grafico = graph(data(ts))
    return grafico


def model():

    # ------------------Sidebar---------------------------------

    st.sidebar.subheader("Escoge una acción a predecir")

    # Menú desplegable para seleccionar el índice del mercado
    market = ['NYSE', 'AMEX', 'NASDAQ']
    market_selected = st.sidebar.selectbox(
        "Selecciona una bolsa de valores de EEUU:", market)

    symbols = get_symbols(market_selected)

    ticker_list = symbols['Symbol'].to_list()
    default_tickers = 'IBM'

    # Obtener el índice del valor predeterminado en la lista de símbolos
    default_index = ticker_list.index(default_tickers)

    selected_ticker = st.sidebar.selectbox(
        "Selecciona una acción:", ticker_list, index=default_index)

    start_date = datetime.datetime(2023, 5, 9)
    end_date = datetime.datetime(2024, 5, 9)
    # end_date = datetime.datetime.now()
    # start_date = end_date - datetime.timedelta(days=1*365)

    # Añadir widgets de fecha
    col1, col2 = st.columns([2, 2])
    with col1:
        start_date = st.date_input("Fecha de inicio", value=start_date)
        st.write("Inicio:", start_date)
    with col2:
        end_date = st.date_input("Fecha de fin", value=end_date)
        st.write("Fin:", end_date)

    # Mostrar las fechas seleccionadas

    ts = yf.download(selected_ticker, start=start_date,
                     end=end_date)['Adj Close']

    texto = text('HN-Model', 4)
    texto.text(md1)

    modelo = grafico(ts)

    mitad, _ = st.columns([7, 1])

    with mitad:

        st.subheader(f'HN-Model de {selected_ticker}')
        st.plotly_chart(modelo)
