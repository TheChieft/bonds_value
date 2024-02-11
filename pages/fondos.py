import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from scipy.stats import linregress
from streamlit_extras.metric_cards import style_metric_cards

fund_list = yf.FundsList()

# Muestra algunos detalles sobre los fondos (puedes ajustar según tus necesidades)
for fund_symbol in fund_list:
    fund = yf.Ticker(fund_symbol)
    print(f"Nombre del Fondo: {fund.info['longName']}")
    print(f"Símbolo: {fund_symbol}")
    print(f"Tipo de Activo: {fund.info['category']}")
    print("-----------------------------")

    # Muestra las tarjetas de métricas solo para el ticker seleccionado
    if ticker == selected_stock:
        # st.header(f'{ticker}')
        col1, col2, col3 = st.columns(3)
        col1.metric('Market Ticker:', value=market_ticker)
        col2.metric('Expected Return:', value=expected_return)
        col3.metric('Beta', value=beta)
        style_metric_cards(background_color='rgba(0,0,0,0)', border_left_color="#003C6F",
                           border_color="#003C6F", box_shadow="blue")
        st.write("----")
