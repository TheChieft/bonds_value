import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from src.funcionesAcciones import get_stock_data, get_stock_cumulative_returns, calcular_alpha_beta, get_symbols
from finvizfinance.quote import finvizfinance

from components.text import text

md1 = open('././markdown/capm.md').read()


def valoracion():

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

    # ------------------------------------------------------------------------------

    # Menú desplegable para seleccionar el índice del mercado
    market_ticker_options = list(index_mapping.values())
    selected_index_name = st.sidebar.selectbox(
        "Selecciona referencia de mercado:", market_ticker_options)

    # Obtener la sigla correspondiente al índice seleccionado
    market_ticker = [key for key, value in index_mapping.items(
    ) if value == selected_index_name][0]
    resultados, fig = calcular_alpha_beta(
        start_date, end_date, selected_tickers, market_ticker)
    # Verificar si hay resultados antes de iterar sobre los tickers

    # -------------------------------------------------------------
    # Gráfico CAPM
    # -------------------------------------------------------------
    st.divider()

    st.header("Modelo CAPM")

    st.markdown(
        '''
        
        Como representación de mercado de Estados Unidos se utiliza en la práctica un índice bursátil representativo de 
        las acciones que en él cotizan, tales como el Dow Jones, S&P 500, Nasdaq Composite y Russell 2000, por defecto se toma el S&P 500
        y se recomienda porque incluye 500 de las empresas más grandes y representativas cotizadas en las bolsas de valores de EE.UU. 
        Estas empresas provienen de diversos sectores, lo que lo convierte en un buen indicador de la salud general del mercado estadounidense.
        ''')

    texto = text('Modelo CAPM', 4)
    texto.text(md1)
    # -------------------------------------------------------------

    left, middle, right = st.columns((1, 8, 1))
    with middle:
        st.plotly_chart(fig)

    # -------------------------------------------------------------

    tabla, gb, ga = st.columns((2, 4, 4))

    with tabla:
        st.subheader('Resultados')
        st.dataframe(pd.DataFrame(resultados).transpose(),
                     width=200, height=300)

    with gb:
        # Crear un gráfico de barras para los Betas
        fig_betas = go.Figure()

        # Iterar sobre los tickers seleccionados
        for ticker in selected_tickers:
            # Calcular los Betas
            if ticker in resultados:
                # Agregar una barra para el Beta de la acción actual
                fig_betas.add_trace(
                    go.Bar(x=[ticker], y=[resultados[ticker]['beta']], name=ticker))
            else:
                st.warning(
                    f"No se encontraron resultados para el ticker {ticker}.")

        # Configurar el diseño del gráfico de Betas
        fig_betas.update_layout(
            title=dict(
                text='Beta',
                font=dict(color='white', size=20),
                x=0.4,
                y=0.9
            ),
            width=330,
            height=400,
            xaxis_title='Acción',
            yaxis_title='Beta',
            barmode='group',
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',  # Fondo del papel transparente
            plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
            xaxis=dict(tickfont=dict(color='white')),
            yaxis=dict(tickfont=dict(color='white')),
            font=dict(color='white'),
        )

        # Mostrar el gráfico de Betas en Streamlit
        st.plotly_chart(fig_betas)

    with ga:
        # Crear un gráfico de barras para los Alphas
        fig_alphas = go.Figure()

        # Iterar sobre los tickers seleccionados
        for ticker in selected_tickers:
            # Calcular los Alphas
            if ticker in resultados:
                # Agregar una barra para el Alpha de la acción actual
                fig_alphas.add_trace(
                    go.Bar(x=[ticker], y=[resultados[ticker]['alpha']], name=ticker))
            else:
                st.warning(
                    f"No se encontraron resultados para el ticker {ticker}.")

        # Configurar el diseño del gráfico de Alphas
        fig_alphas.update_layout(
            title=dict(
                text='Alpha',
                font=dict(color='white', size=20),
                x=0.4,
                y=0.9
            ),
            width=400,
            height=400,
            xaxis_title='Acción',
            yaxis_title='Alpha',
            barmode='group',
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',  # Fondo del papel transparente
            plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
            xaxis=dict(tickfont=dict(color='white')),
            yaxis=dict(tickfont=dict(color='white')),
            font=dict(color='white'),
        )

        # Mostrar el gráfico de Alphas en Streamlit
        st.plotly_chart(fig_alphas)
    st.divider()
