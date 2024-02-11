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
