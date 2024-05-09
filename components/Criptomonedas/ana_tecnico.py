import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from src.funciones_cripto import obtener_datos_cierre
from src.funciones_cripto import descargar_info_cripto

fecha_actual = pd.Timestamp('today')
fecha_inicio = fecha_actual - pd.DateOffset(years=3)
criptomonedas = pd.read_csv('././data/db/criptomonedas.csv') # contiene simbolo de las 200 criptomonedas principales

# Función que contiene el análisis tecnico de las criptomonedas
def ana_tecnico_cripto():
    st.markdown(
    """
    <style>
        /* Estilo para cambiar la fuente, el tamaño y centrar el texto */
        .custom-text {
            font-family: Arial, sans-serif; /* Cambia la fuente a Arial o cualquier otra fuente que desees */
            font-size: 17px; /* Cambia el tamaño del texto a 20px o cualquier otro tamaño que desees */
            text-align: center; /* Centra el texto horizontalmente */
        }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.divider()
    # Utiliza st.write() para mostrar texto con el estilo personalizado
    st.markdown('<p class="custom-text">En este apartado podrás elegir una canntidad determinada de criptomonedas y ver su comportamiento a lo largo del tiempo, observando las principales métricas de la primera criptomoneda seleccionada.</p>', unsafe_allow_html=True)
    # opciones cripto
    st.divider()
    cripto_option = st.sidebar.multiselect('Selecciona las criptomonedas', criptomonedas['Símbolo']+ '-USD', ['BTC-USD']) 
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
                    title={
                        'text': 'Precio de Cierre de Criptomonedas Seleccionadas',
                        'y':1,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                },
                
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
#----------------------------------------------------------------------------------------------------
    # Métricas criptomoneda
    api_key = '2a257bf9-595e-40fe-b9bd-911acadcc922'
    cripto_symbol = cripto_option[0].replace('-USD','')
    df = descargar_info_cripto(api_key, cripto_symbol)

    #-------------------------------------------------------------------------------------
    with col1:
        st.write(f"""
    <h1 style='text-align: center; font-size: 25px;'>Métricas {cripto_option[0]}</h1>
""", unsafe_allow_html=True)

                # Crear un métrico decorado
        st.markdown("""
            <style>
            .big-font {
                font-family: 'Helvetica';
                font-size:15px !important;
                color: #ffffff;
            }
            .metric-value {
                font-family: 'Helvetica';
                font-size:25px !important;
                color: #ffffff;
                margin-bottom: 70px;  # Añade un margen en la parte inferior de cada métrica
            }
            .metric-title {
                border-bottom: 2px solid #00c9ff;
                padding-bottom: 5px;
                margin-bottom: 10px;  # Espacio adicional después del título
            }
            .container {
                margin-bottom: 30px;  # Espacio entre contenedores de métricas
            }
            </style>
            """, unsafe_allow_html=True)

        # Formateo de números grandes para mejor legibilidad
        def format_large_number(value):
            if value >= 1e12:
                return f"${value / 1e12:.2f} T"
            elif value >= 1e9:
                return f"${value / 1e9:.2f} B"
            elif value >= 1e6:
                return f"${value / 1e6:.2f} M"
            else:
                return f"${value:.2f}"

        # Creación de columnas con estilo
        col1_1, col1_2 = st.columns(2)

        with col1_1:
            st.markdown('<div class="metric-title big-font">Precio</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">${:.2f}</div>'.format(df['Price'][0]), unsafe_allow_html=True)

            st.markdown('<div class="metric-title big-font">Capitalización del mercado</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">{}</div>'.format(format_large_number(df['Market Cap'][0])), unsafe_allow_html=True)

            st.markdown('<div class="metric-title big-font">24h Volumen</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">{}</div>'.format(format_large_number(df['24h Volume'][0])), unsafe_allow_html=True)

        with col1_2:
            st.markdown('<div class="metric-title big-font">Cambio % 1h</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">{:.2f}%</div>'.format(df['Percent Change 1h'][0]), unsafe_allow_html=True)

            st.markdown('<div class="metric-title big-font">Cambio % 24h</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">{:.2f}%</div>'.format(df['Percent Change 24h'][0]), unsafe_allow_html=True)

            st.markdown('<div class="metric-title big-font">Cambio % 7d</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">{:.2f}%</div>'.format(df['Percent Change 7d'][0]), unsafe_allow_html=True)

    with col2:
        st.write("""
    <h1 style='text-align: center; font-size: 25px;'> Precios Criptos </h1>
""", unsafe_allow_html=True)
        grafico_precios_cripto(cripto_option)
