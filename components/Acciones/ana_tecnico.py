import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from src.funcionesAcciones import get_stock_data, get_stock_cumulative_returns, calcular_alpha_beta, get_symbols
from finvizfinance.quote import finvizfinance

file1 = open('././markdown/capm.md').read()


def analisis_tec():

    # ------------------Sidebar---------------------------------

    st.sidebar.subheader("Escoge un Mercado Bursatil")

    # Menú desplegable para seleccionar el índice del mercado
    market = ['NYSE', 'AMEX', 'NASDAQ']
    market_selected = st.sidebar.selectbox(
        "Selecciona una bolsa de valores de EEUU:", market)

    symbols = get_symbols(market_selected)

    # Fechas de inicio y fin
    # datetime.datetime(2024, 2, 1)  # datetime.datetime.now()
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=5*365)

    index_mapping = {
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones",
        "^IXIC": "Nasdaq Composite",
        "^RUT": "Russell 2000"
    }

    ticker_list = symbols['Symbol'].to_list()
    default_tickers = ['NVDA', 'TSLA']

    for ticker in default_tickers:
        if ticker not in ticker_list:
            ticker_list.append(ticker)

    # Create the multiselect with updated ticker list
    selected_tickers = st.sidebar.multiselect(
        "Selecciona acciones:", ticker_list, default=default_tickers)

    if not selected_tickers:
        st.warning("Por favor, selecciona al menos una acción.")
        st.stop()

    # -------------------------------------------------------------

    # Obtener datos de precios de las acciones seleccionadas
    stock_prices = [get_stock_data(ticker, start_date, end_date)
                    for ticker in selected_tickers]

    stock_returns = [get_stock_cumulative_returns(ticker, start_date, end_date)
                     for ticker in selected_tickers]

    # Convertir listas a DataFrames
    df_stock_prices = pd.concat(stock_prices, axis=1)
    df_stock_returns = pd.concat(stock_returns, axis=1)

    # ------------------------------------------------------------------------------
    selected_ticker = st.selectbox(
        "Seleccione una acción:", selected_tickers, index=0)

    # Verificar si el ticker está presente en los resultados

    if selected_ticker in selected_tickers:

        stock = finvizfinance(selected_ticker)
        stock_fundament = stock.ticker_fundament()

        style_metric_cards(background_color='rgba(0,0,0,0)',
                           border_left_color="#003C6F", border_color="#003C6F", box_shadow="blue")

        # Indicadores de valorizacion
        precio = stock_fundament['Price']
        ROA = stock_fundament['ROA']
        PER = stock_fundament['P/E']
        Quick_Ratio = stock_fundament['Quick Ratio']
        Debt_Eq = stock_fundament['Debt/Eq']
        beta = stock_fundament['Beta']

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric('Precio:', value=precio)
        col2.metric('ROA:', value=ROA)
        col3.metric('P/E Ratio:', value=PER)
        col4.metric('Quick Ratio:', value=Quick_Ratio)
        col5.metric('Debt/Eq:', value=Debt_Eq)
        col6.metric('Beta:', value=beta)

    precios = go.Figure()
    for i, stock_prices_df in enumerate(stock_prices):
        precios.add_trace(go.Scatter(
            x=stock_prices_df.index, y=stock_prices_df.iloc[:, 0].values, mode='lines', name=f'{selected_tickers[i]}'))
    precios.update_xaxes(tickcolor='white', tickfont=dict(
        color='white'), title=dict(text='Fecha', font=dict(color='white')))
    precios.update_yaxes(tickcolor='white', tickfont=dict(
        color='white'), title=dict(text='Precio de cierre', font=dict(color='white')))
    precios.update_layout(
        title=dict(
            text='Precios mensuales ultimos 5 años',
            font=dict(color='white', size=20),
            x=0.2,
            y=0.95
        ),
        width=750,
        height=400,
        legend=dict(font=dict(color='white')),
        # Fondo del papel transparente
        paper_bgcolor='rgba(0,0,0,0)',
        # Fondo del gráfico transparente
        plot_bgcolor='rgba(0,0,0,0)',
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
        title=dict(
            text='Retornos mensuales ultimos 5 años',
            font=dict(color='white', size=20),
            x=0.2,
            y=0.95
        ),
        width=750,
        height=400,
        legend=dict(font=dict(color='white')),
        # Fondo del papel transparente
        paper_bgcolor='rgba(0,0,0,0)',
        # Fondo del gráfico transparente
        plot_bgcolor='rgba(0,0,0,0)',
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

    # Botones de radio
    col1, col2, col3 = st.columns([1.5, 7, 1])
    with col1:
        st.title('')
        st.title('')
        st.title('')
        tipo_grafico = col1.radio("", ["Precios", "Retornos"])

    # Mostrar el gráfico correspondiente
    if tipo_grafico == "Precios":
        with col2:
            st.plotly_chart(precios)
    else:
        with col2:
            st.plotly_chart(fig)

    # -------------- tablas -------------------------------------

    col1, col2 = st.columns((3, 3))

    with col1:

        st.subheader("Precios")
        st.dataframe(df_stock_prices, height=300, width=450)

    with col2:
        st.subheader("Retornos")
        st.dataframe(df_stock_returns, height=300, width=450)

    # ------------------------------------------------------------
