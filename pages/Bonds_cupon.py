import streamlit as st
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards

# TUTV con cupón 
# TFIT sin cupón 

df = pd.read_csv('data/db/DeudaPublica_20240209.csv', delimiter= ';', index_col= False)
#df = pd.read_csv('data/db/bonds_public.csv', sep=',')
#INFO_DATAFRAME = pd.read_csv('data/db/info_bonds_public.csv', sep=',')


def qualifying_bcon (df):
    filtro = df['Nemotécnico'].str.startswith('TFIT')
    return(df[filtro])

df_cupon = qualifying_bcon(df)

estilo_recuadro = """
    <style>
        .recuadro {
            padding: 20px;
            background-color: #f0f0f0;
            border-radius: 10px;
            border: 2px solid #ccc;
            color: black;
        }
    </style>
"""    

st.title("Calculadora avanzada de Bonos con cupón")

tab1, tab2, tab3 = st.tabs(["Base de datos", "Calculo de Bono", "Gráficos"])

with tab1:
   st.header("Renta fija")
   st.dataframe(df)

with tab2:
    st.header("Cálculo bono")
    option = st.selectbox('¿Qué prefieres?', ('','Conservar el Bono', 'Vender el Bono'))
    st.write('Elegió: ', option)
    if option == 'Conservar el Bono':
        col1, col2 = st.columns(2)
        with col1:
        # Acciones específicas para el Nemotécnico seleccionado
            fecha_emision = st.date_input('Ingresa la fecha de compra: ', datetime.now())
            FCB = st.slider('Ingresa la tasa facial', min_value=0.0,max_value=100.0,step=0.1) #Ingresa la tasa facial
        with col2:
            fecha_vencimiento = st.date_input('Ingresa fecha de vencimiento: ', min_value=datetime.now() )
            tasa_anual = st.slider('Ingresa la tasa de referencia', min_value=0.0,max_value=100.0,step=0.1) #Ingresa la tasa de referencia
        base = 365
        if tasa_anual and FCB and base:

            # Convertir las tasas a números
            FCB = float(FCB/100)
            base = float(base)
            tasa_anual = float(tasa_anual/100)

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
                    if i.date() != fecha_vencimiento:
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

            style_metric_cards(background_color='rgba(0,0,0,0)', border_left_color="#003C6F",
                           border_color="#003C6F", box_shadow="blue")  
            
            with col1:
                text1 = 'VPFCB: '
                st.markdown(estilo_recuadro, unsafe_allow_html=True)
                st.metric(label=text1, value=sum_VPFCB, delta_color="inverse")              
            with col2:
                text2 = 'T*VPFCB: '
                st.markdown(estilo_recuadro, unsafe_allow_html=True)
                st.metric(label=text2, value=sum_T_VPFCB, delta_color="inverse")               
            with col3:
                text3 = 'T²*VPFCB: '
                st.markdown(estilo_recuadro, unsafe_allow_html=True)
                st.metric(label=text3, value=sum_TT_VPFCB, delta_color="inverse")               
            with col4:
                text4 = 'T²*VPFCB/T*VPFCB: '
                st.markdown(estilo_recuadro, unsafe_allow_html=True)
                st.metric(label=text4, value=TT_VPFCBT_VPFCB, delta_color="inverse")               

            col_1, col_2, col_3, col_4 = st.columns(4)
            
            conv_list = [VPFCB['TT_VPFCB']/VPFCB['T_VPFCB']]
            dur_list = [VPFCB['T_VPFCB']/VPFCB['VPFCB']]

            duracion = round((sum_T_VPFCB/sum_VPFCB), 3)
            convexidad = round((TT_VPFCBT_VPFCB/sum_VPFCB), 3)
            puntos_basicos = 0.0025
            delB = (-duracion*0.0025+0.5*convexidad*(0.0025)**2)

            with col_1:
                text1 = 'Duración: '
                st.markdown(estilo_recuadro, unsafe_allow_html=True)
                st.metric(label=text1, value=duracion, delta_color="inverse")
            with col_2:
                text2 = 'Convexidad: '
                st.markdown(estilo_recuadro, unsafe_allow_html=True)
                st.metric(label=text2, value=convexidad, delta_color="inverse")
            with col_3:
                text3 = 'Puntos básicos: '
                st.markdown(estilo_recuadro, unsafe_allow_html=True)
                st.metric(label=text3, value=puntos_basicos, delta_color="inverse")
            with col_4:
                text4 = 'DelB(t,T): '
                st.markdown(estilo_recuadro, unsafe_allow_html=True)
                st.metric(label=text4, value=delB, delta_color="inverse")        

        else:
            st.warning(
                'Por favor, ingrese valores válidos para la tasa.')

        
with tab3:
    
    if option == 'Conservar el Bono':
        st.header('Gráficos')

        # Plot Duración
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(dur_list)),dur_list, label='Duración', marker='o', color='blue')
        plt.title('Duración del Bono')
        plt.xlabel('Período')
        plt.ylabel('Valor')
        plt.xticks(range(len(dur_list)), ['Actual'])
        plt.legend()
        plt.grid(True)

        # Mostrar el gráfico de duración
        st.subheader('Gráfico de Duración')
        st.pyplot(plt)

        # Graficar Convexidad
        plt.figure(figsize=(10, 6))
        
        plt.plot(dur_list,conv_list, label='Convexidad', marker='o', color='green')
        plt.title('Convexidad del Bono')
        plt.xlabel('Duración')
        plt.ylabel('Valor')
        plt.legend()
        plt.grid(True)
        

        # Mostrar el gráfico de convexidad
        st.subheader('Gráfico de Convexidad')
        st.pyplot(plt)
    else:
        st.warning('Por favor, seleccione la opción "Conservar el Bono" para visualizar los gráficos.')
    





