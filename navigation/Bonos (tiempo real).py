import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime
from streamlit_option_menu import option_menu

# CONSTANTS
DATAFRAME = pd.read_csv('data/db/bonds_public.csv', sep=',')
INFO_DATAFRAME = pd.read_csv('data/db/info_bonds_public.csv', sep=',')

# FUNCTIONS ----------------------------------
# Filtrar DATAFRAME por Nemotécnico lo que tienen FTIT y TCO
def filtro_nemotecnico (df):
    filtro = df['Nemotécnico'].str.startswith('TFIT') | df['Nemotécnico'].str.startswith('TCO')
    return(df[filtro])

DATAFRAME = filtro_nemotecnico(DATAFRAME)

def qualifying_bcon (df):
    filtro = df['Nemotécnico'].str.startswith('TFIT')
    return(df[filtro])

df_cupon = qualifying_bcon(INFO_DATAFRAME)

def qualifying_bsin (df):
    filtro = df['Nemotécnico'].str.startswith('TCO')
    return(df[filtro])

df_sin_cupon = qualifying_bsin(INFO_DATAFRAME)

def precio_bono_sin_cupon(F, r, n, t):
    return F / (1 + r/n)**(n*t)

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
            
            st.dataframe(df_cupon)
            # Agregar un menú desplegable para seleccionar el Nemotécnico
            selected_nemotecnico = st.selectbox(
                label='Selecciona un Nemotécnico',
                options=df_cupon['Nemotécnico'].tolist(),
                index=0  # o puedes omitir el índice para que seleccione el primero por defecto
            )

            try:
                # Filtrar el DataFrame basado en el Nemotécnico seleccionado
                selected_row = df_cupon[df_cupon['Nemotécnico'] == selected_nemotecnico].iloc[0]

                # Acciones específicas para el Nemotécnico seleccionado
                FCB = selected_row['Tasa facial']
                base = selected_row['Base']
                fecha_emision = pd.to_datetime(selected_row['Fecha de emisión'])
                fecha_vencimiento = pd.to_datetime(selected_row['Fecha de vencimiento'])

            except IndexError:
                st.warning('Nemotécnico no encontrado o DataFrame vacío.')

            tasa_anual = st.text_input('Ingresa la tasa de referencia:') #Ingresa la tasa de referencia

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
            st.markdown("<h1 style='display: flex; font-size: 30px; text-align: left;'>Valuación de Bonos Sin Cupón</h1>",
                        unsafe_allow_html=True)
            
            # Mostrar el DataFrame de bonos sin cupón
            st.dataframe(df_sin_cupon, width=2000, height=100)
            
            # Agregar un menú desplegable para seleccionar el Nemotécnico
            selected_nemotecnico_sin_cupon = st.selectbox(
                label='Selecciona un Nemotécnico',
                options=df_sin_cupon['Nemotécnico'].tolist(),
                index=0
            )

            try:
                # Filtrar el DataFrame basado en el Nemotécnico seleccionado
                selected_row_sin_cupon = df_sin_cupon[df_sin_cupon['Nemotécnico'] == selected_nemotecnico_sin_cupon].iloc[0]

                # Acciones específicas para el Nemotécnico seleccionado
                valor_nominal_sin_cupon = selected_row_sin_cupon['Valor Nominal']
                plazo_sin_cupon = selected_row_sin_cupon['Plazo (en períodos)']

            except IndexError:
                st.warning('Nemotécnico no encontrado o DataFrame vacío para bonos sin cupón.')

            if valor_nominal_sin_cupon and plazo_sin_cupon:

                # Convertir los valores a números
                valor_nominal_sin_cupon = float(valor_nominal_sin_cupon)
                plazo_sin_cupon = int(plazo_sin_cupon)

                # Crear una lista de períodos hasta el vencimiento
                periodos_sin_cupon = list(range(1, plazo_sin_cupon + 1))

                # Calcular los precios de los bonos sin cupón utilizando la fórmula del número de Euler
                precios_sin_cupon = [precio_bono_sin_cupon(valor_nominal_sin_cupon, tasa_diaria, 2, periodo/2) for periodo in periodos_sin_cupon]

                # Crear un DataFrame con los resultados
                df_valuacion_sin_cupon = pd.DataFrame({
                    'Período': periodos_sin_cupon,
                    'Precio Bono Sin Cupón': precios_sin_cupon
                })

                # Mostrar la tabla de valuación
                st.dataframe(df_valuacion_sin_cupon, width=800, height=400)

            else:
                st.warning('Por favor, ingrese valores válidos para el valor nominal y el plazo del bono sin cupón.')


        
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
            
            