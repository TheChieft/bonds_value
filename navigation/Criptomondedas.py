import streamlit as st
import hydralit_components as hc


def Criptomonedas():
    a = 'Análisis Técnico'
    b = 'Modelos'

    tabs = [
        a,
        b
    ]

    option_data = [
        {'icon': "", 'label': a},
        {'icon': "", 'label': b},
    ]

    # Define el tema para el NavBar
    theme = {
        'menu_background': '#000020',  # Color de fondo del menú
        'txc_inactive': '#999999',  # Color del texto de las pestañas inactivas
        'txc_active': 'white',  # Color del texto de la pestaña activa
        'option_active': '#183E88'  # Color de la pestaña activa
    }

    # Crea el NavBar con los datos y el tema especificados
    # -------------------------------------------------------------

    chosen_tab = hc.option_bar(
        option_definition=option_data,
        title='',
        key='PrimaryOptionx2',
        override_theme=theme,
        horizontal_orientation=True)

    if chosen_tab == a:
        pass

    elif chosen_tab == b:
        pass

    import streamlit as st
    import yfinance as yf
    import plotly.graph_objs as go
    import pandas as pd

    # Función para obtener los datos de cierre de las criptomonedas seleccionadas
    fecha_actual = pd.Timestamp('today')
    fecha_inicio = fecha_actual - pd.DateOffset(years=3)

    def obtener_datos_cierre(symbols, c_start, c_end, intentos_maximos=3):
        """
        Función que descarga datos de cierre de criptomonedas de Yahoo Finance.

        Argumentos:
            symbols: Lista de símbolos de criptomonedas (ej: ["BTC-USD", "ETH-USD"]).
            c_start: Fecha de inicio en formato YYYY-MM-DD.
            c_end: Fecha de finalización en formato YYYY-MM-DD.
            intentos_maximos: Número máximo de intentos de descarga (por defecto 3).

        Retorno:
            DataFrame de Pandas con los datos de cierre
        """

        for intento in range(intentos_maximos):
            try:
            # Descargar datos con yfinance
                data = yf.download(symbols, start=c_start, end=c_end, interval="1wk")
                return data['Close']
            except Exception as e: 
                print(f"Intento {intento+1}: Error al descargar datos: {e}")
                if intento == intentos_maximos - 1:  # Último intento
                    print(f"Descarga fallida después de {intentos_maximos} intentos.")
                    return pd.DataFrame()  # Devolver DataFrame vacío
                
    # Símbolos de criptomonedas (son 200)
    criptomonedas = pd.read_csv('././data/db/criptomonedas.csv')
    cripto_option = st.sidebar.multiselect('Selecciona una criptomoneda', criptomonedas['Símbolo']+ '-USD', ['BTC-USD']) 
    # Función Grafico
    def grafico_precios_cripto(cripto_seleccionadas):
        if cripto_seleccionadas:
            datos = obtener_datos_cierre(cripto_seleccionadas, fecha_inicio, fecha_actual)
            fig = go.Figure()
            # Determinar el uso del eje y secundario basado en la variación de precios
            max_values = datos.max()
            scale_diff = max_values.max() / max_values.min()
            use_secondary_axis = scale_diff > 10
            # Títulos dinámicos para los ejes basados en el valor máximo
            primary_axis_label = secondary_axis_label = ""
            for cripto in cripto_seleccionadas:
                # Cuando solo es una variable 
                if isinstance(datos, pd.Series):
                        if use_secondary_axis and (max_values[cripto] < max_values.max() / 10):
                            secondary_axis_label = cripto if not secondary_axis_label else secondary_axis_label
                            fig.add_trace(go.Scatter(x=datos.index, y=datos, mode='lines', name=cripto, yaxis='y2'))
                        else:
                            primary_axis_label = cripto if not primary_axis_label else primary_axis_label
                            fig.add_trace(go.Scatter(x=datos.index, y=datos, mode='lines', name=cripto))
                else:    
                    if cripto in datos.columns:
                        if use_secondary_axis and (max_values[cripto] < max_values.max() / 10):
                            secondary_axis_label = cripto if not secondary_axis_label else secondary_axis_label
                            fig.add_trace(go.Scatter(x=datos.index, y=datos[cripto], mode='lines', name=cripto, yaxis='y2'))
                        else:
                            primary_axis_label = cripto if not primary_axis_label else primary_axis_label
                            fig.add_trace(go.Scatter(x=datos.index, y=datos[cripto], mode='lines', name=cripto))

            # Configuración de ejes y layout con el nuevo estilo
            fig.update_xaxes(
                tickcolor='white', tickfont=dict(color='white'),
                title=dict(text='Fecha', font=dict(color='white')),
                showgrid=True,
                ticks='outside',
                linecolor='white',
                gridcolor='rgba(255, 255, 255, 0.1)'
            )
            fig.update_yaxes(
                tickcolor='white', tickfont=dict(color='white'),
                title=dict(text='Precio de cierre', font=dict(color='white')),
                showgrid=True,
                ticks='outside',
                linecolor='white',
                gridcolor='rgba(255, 255, 255, 0.1)'
            )
            yaxis_config = dict(title=f'Precio ({primary_axis_label})') if primary_axis_label else {}
            yaxis2_config = dict(title=f'Precio ({secondary_axis_label})', overlaying='y', side='right') if secondary_axis_label else {}

            fig.update_layout(
                title='Precio de Cierre de Criptomonedas Seleccionadas',
                xaxis_title='Fecha',
                xaxis=dict(range=range_x),
                yaxis=yaxis_config,
                yaxis2=yaxis2_config,
                margin=dict(l=20, r=50, t=20, b=20),
                # Fondo del papel transparente
                paper_bgcolor='rgba(0,0,0,0)',
                # Fondo del gráfico transparente
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(font=dict(color='white')),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Por favor, selecciona al menos una criptomoneda para visualizar los datos.")

    range_x = [fecha_actual - pd.DateOffset(years=1), fecha_actual]
    col1, col2 = st.columns([250,500])

    # Métricas criptomoneda
    
    with col1:
        st.header('Estadísticas')
    with col2:
        st.header('Precios Criptomonedas')
        grafico_precios_cripto(cripto_option)





