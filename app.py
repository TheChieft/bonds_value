import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime
from streamlit_option_menu import option_menu
import pandas as pd

# CONSTANTS
DATAFRAME = pd.read_csv('data/db/bonds_public.csv')
INFO_DATAFRAME = pd.read_csv('data/db/info_bonds_public.csv',encoding='windows-1252')

tfi = INFO_DATAFRAME[INFO_DATAFRAME['Nemotécnico'].str.startswith('TFI')]

# FUNCTIONS ----------------------------------
def qualifying_bcon (df):
    filtro = df['Nemotécnico'].str.startswith('TFIT')
    return(df[filtro])

def qualifying_bsin (df):
    filtro = df['Nemotécnico'].str.startswith('TCO')
    return(df[filtro])

df_cupon = qualifying_bcon(DATAFRAME)
df_sin_cupon = qualifying_bsin(DATAFRAME)

st.set_page_config(layout="wide", page_title='Valuación de Instrumentos Financieros', page_icon=':dollar:', initial_sidebar_state='auto')

# MAIN ---------------------------------------
with st.sidebar:
    st.markdown("<h1 style='font-size: 50px; text-align: left;'>Valuación de Instrumentos Financieros</h1>",
                unsafe_allow_html=True)
    selected = st.selectbox(
        label='Seleccione una opción:',
        options=['Mercado local: Análisis General', 'Renta Variable',
                 'Renta fija', 'ETFs', 'Criptomonedas'],
        index=0
    )

# if selected == 'Mercado local: Análisis General':

if selected == 'Renta fija':
    with st.sidebar:
        selected = st.selectbox(
            label='Tipo de déuda:',
            options=['Deuda pública'],
            index=0
        )

    if selected == 'Deuda pública':

        with st.sidebar:
            selected = option_menu(
                menu_title='',
                options=['Cupón', 'Sin cupón', 'General'],  #
                default_index=0,
            )

        if selected == 'Cupón':

            # Agregar un menú desplegable para seleccionar el Nemotécnico
            selected_nemotecnico = st.selectbox(
                label='Selecciona un Nemotécnico',
                options=tfi['Nemotécnico'].tolist(),
                index=0
            )

            # Filtrar el DataFrame basado en el Nemotécnico seleccionado
            selected_row = tfi[tfi['Nemotécnico'] == selected_nemotecnico].iloc[0]

            # Acciones específicas para el Nemotécnico seleccionado
            FCB = selected_row['Tasa facial']
            base = selected_row['Base']
            fecha_emision = pd.to_datetime(selected_row['Fecha de emisión'])
            fecha_vencimiento = pd.to_datetime(selected_row['Fecha de vencimiento'])

            tasa_anual = st.text_input() #Ingresa la tasa de referencia

            if tasa_anual and FCB and base:

                # Convertir las tasas a números
                FCB = float(FCB)
                base = float(base)
                tasa_anual = float(tasa_anual)

                # Calcular la tasa diaria
                tasa_diaria = (1 + (tasa_anual/100))**(1 / base) - 1

                # Mostrar resultados
                st.write('Tasa diaria: ', f'{round(tasa_diaria*100,3)}%')
                if fecha_emision and fecha_vencimiento:

                    # Obtener el año de emisión y vencimiento
                    año_emision = fecha_emision.year
                    año_vencimiento = fecha_vencimiento.year
                    mes_dia_vencimiento = fecha_vencimiento.strftime(
                        '%m-%d')

                    # Crear la lista de fechas de pago de cupones

                    cupones = []
                    for i in range(int(año_vencimiento)-int(año_emision)+1):
                        cupones.append(
                            f'{int(año_emision)+i}-{mes_dia_vencimiento}')

                    df_cupones = pd.DataFrame({'Pago_cupones': cupones})
                    df_cupones['Pago_cupones'] = pd.to_datetime(
                        df_cupones['Pago_cupones'], format='%Y-%m-%d')

                    VPFCB = []
                    T_VPFCB = []
                    TT_VPFCB = []

                    emision = pd.to_datetime(fecha_emision)
                    a = 1
                    for i in df_cupones['Pago_cupones']:
                        if i.date() == fecha_vencimiento:
                            dias_diferencia = (i - emision).days
                            VPFCB.append(
                                round((FCB+100/((1 + tasa_diaria)**(dias_diferencia))), 3))
                            T_VPFCB.append(
                                round(((FCB+100/((1 + tasa_diaria)**(dias_diferencia)))*a), 3))
                            TT_VPFCB.append(
                                round(((FCB+100/((1 + tasa_diaria)**(dias_diferencia)))*(a*a)), 3))
                            a += 1

                        dias_diferencia = (i - emision).days
                        VPFCB.append(
                            round((FCB/((1 + tasa_diaria)**(dias_diferencia))), 3))
                        T_VPFCB.append(
                            round(((FCB/((1 + tasa_diaria)**(dias_diferencia)))*a), 3))
                        TT_VPFCB.append(
                            round(((FCB/((1 + tasa_diaria)**(dias_diferencia)))*(a*a)), 3))
                        a += 1

                    VPFCB = pd.DataFrame(
                        {'VPFCB': VPFCB, 'T_VPFCB': T_VPFCB, 'TT_VPFCB': TT_VPFCB})

                    valuacion = pd.merge(
                        df_cupones, VPFCB, left_index=True, right_index=True)
                    st.dataframe(valuacion, width=2000, height=400)
                else:
                    st.warning(
                        'Por favor, ingrese fechas válidas de emisión y vencimiento.')

                col1, col2, col3, col4 = st.columns(4)

                sum_VPFCB = round(sum(valuacion['VPFCB']), 3)
                sum_T_VPFCB = round(sum(valuacion['T_VPFCB']), 3)
                sum_TT_VPFCB = round(sum(valuacion['TT_VPFCB']), 3)
                TT_VPFCBT_VPFCB = round(sum_TT_VPFCB/sum_T_VPFCB, 3)

                with col1:
                    st.write('VPFCB: ', sum_VPFCB)
                with col2:
                    st.write('T*VPFCB: ', sum_T_VPFCB)
                with col3:
                    st.write('T²*VPFCB: ', sum_TT_VPFCB)
                with col4:
                    st.write('T²*VPFCB/T*VPFCB: ', TT_VPFCBT_VPFCB)

                col_1, col_2, col_3, col_4 = st.columns(4)

                duracion = round((sum_T_VPFCB/sum_VPFCB), 3)
                convexidad = round((TT_VPFCBT_VPFCB/sum_VPFCB), 3)
                puntos_basicos = 0.0025
                delB = (-duracion*0.0025+0.5*convexidad*(0.0025)**2)

                with col_1:
                    st.write('Duración: ', duracion)
                with col_2:
                    st.write('Convexidad: ', convexidad)
                with col_3:
                    st.write('Puntos básicos: ', puntos_basicos)
                with col_4:
                    st.write('DelB(t,T): ', delB)

            else:
                st.warning(
                    'Por favor, ingrese valores válidos para la tasa.')
            
        # Sin cupón
        if selected == 'Sin cupón':
            # Titulo sección
            st.markdown("<h1 style='display: flex; font-size: 30px; text-align: left;'>Valuación de Bonos</h1>",
                        unsafe_allow_html=True)
            
            st.dataframe(df_sin_cupon, width=2000, height=100)
        
        if selected == 'General':
            # Titulo sección
            st.markdown("<h1 style='display: flex; font-size: 30px; text-align: left;'>Valuación de Bonos</h1>",
                        unsafe_allow_html=True)
            col1, col2 = st.columns(2)  # Create two columns
            # Base de datos
            with col1:
                # Titulo sección
                
                st.dataframe(DATAFRAME, width=2000, height=700)
            
            with col2:
                st.markdown("<h1 style='display: flex; font-size:20px; text-align: left;'>Principales Emisores</h1>",
                        unsafe_allow_html=True)
                st.dataframe(DATAFRAME['Emisor'].value_counts())  
            
            