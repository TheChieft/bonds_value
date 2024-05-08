import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from src.funciones_cripto import obtener_datos_cierre

fecha_actual = pd.Timestamp('today')
fecha_inicio = fecha_actual - pd.DateOffset(years=3)
criptomonedas = pd.read_csv('././data/db/criptomonedas.csv') # contiene simbolo de las 200 criptomonedas principales

# Función que contiene el análisis tecnico de las criptomonedas
def ana_tecnico_cripto():
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

    # Métricas criptomoneda
    
    with col1:
        st.write("""
    <h1 style='text-align: center; font-size: 25px;'>Estadísticas</h1>
""", unsafe_allow_html=True)
    with col2:
        st.write("""
    <h1 style='text-align: center; font-size: 25px;'> Precios Criptos </h1>
""", unsafe_allow_html=True)
        grafico_precios_cripto(cripto_option)
