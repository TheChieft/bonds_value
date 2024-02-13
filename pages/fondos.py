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

fund_list = yf.FundsList()

# Muestra algunos detalles sobre los fondos (puedes ajustar según tus necesidades)
for fund_symbol in fund_list:
    fund = yf.Ticker(fund_symbol)
    print(f"Nombre del Fondo: {fund.info['longName']}")
    print(f"Símbolo: {fund_symbol}")
    print(f"Tipo de Activo: {fund.info['category']}")
    print("-----------------------------")
