import streamlit as st
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Función bono valor presente
def valor_presente(te, tn, vb, t, fc, T): # te: tasa emisión, tn:tasa negociación
    T = (T-t).days
    fc = (fc - t).days 
    c = convertion_rate(te)                # t : fecha emision, fc: fecha compra T:tasa vencimiento
    r = convertion_rate(tn)
    basic = (1+r)**(T-fc)
    part2 = 100/basic
    valor_m = (basic-1)/(basic*r)
    valor = c*(valor_m)+part2
    total = valor * vb / 100
    return(total)

# Función que convertirá la tasa anual a tasa diaria
def convertion_rate(taa): # ta: tasa anual actual
    tda = (1+taa)**(1/365)-1  # tda : tasa diaria actual
    return(tda)

# función que generadora del flujo de caja 

#vb: valor bono
#fcb: tasa cupon valor bono
#vpfcb : valor por decha cupon bono
#tvpfcb : valor por decha cupon bono por tiempo
#ttvpfcb : valor por decha cupon bono por dos veces el tiempo
#fa : fecha actual
#fcbu : tasa cupon valor unidad
#vbu : valor bono unidad
#tda : tasa diaria

def flujo_caja(tc, vb,fe,fv, tda):
    fechas = [fe]
    fcb = [0]
    vpfcb = [0]
    tvpfcb = [0]
    ttvpfcb = [0]
    for fecha in range(fe.year+1,fv.year+1):
        fa = datetime(fecha, fe.month, fe.day)
        fa = fa.date()
        if fecha == fv.year: # si la fecha del bono es igual a la de vencimiento se retorna el bono y el cupon
            fcbu = (1+tc)*vb
            vbu = fcbu / ((1+tda)**((fa-fe).days))
            vpfcb.append(vbu)
            fcb.append(fcbu)
            fechas.append(fa)
        else:
            fcbu = tc*vb
            vbu = fcbu / ((1+tda)**((fa-fe).days))
            vpfcb.append(vbu)
            fcb.append(fcbu)
            fechas.append(fa)
    flujo_de_caja = {'Fecha':fechas, 'FCB': fcb, 'VPFCB':vpfcb}
    flujo_de_caja = pd.DataFrame(flujo_de_caja)
    flujo_de_caja['t*VPFCB'] = flujo_de_caja.index * flujo_de_caja['VPFCB']
    flujo_de_caja['t*t*VPFCB'] = flujo_de_caja.index * flujo_de_caja['t*VPFCB']
    return(flujo_de_caja)

fecha_actual = datetime.now()

fecha_mayor = fecha_actual + timedelta(days=36500)

st.title("Calculadora avanzada de Bonos con cupón")

tab1, tab2, tab3 = st.tabs(["Bonos sin cupón", "Bono con cupon", "Valor presente bono con cupon"])
with tab1:
    st.write('Proximamente')
with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        fe = st.date_input("Fecha de emisión: ", min_value=fecha_actual, max_value=fecha_mayor) # fe : fecha emisión
        tc = st.number_input('Ingrese la tasa de emisión: ', format="%f")# tc : tasa cupon
    with col2:
        fv = st.date_input("Fecha de vencimiento:", min_value=fecha_actual, max_value=fecha_mayor)
        tn = st.number_input('Ingrese la tasa de negociación: ', format="%f") # tn : tasa de negociación
    with col3:
        fc = st.date_input("Fecha de compra: ", min_value=fe, max_value=fv) # fc : fecha compra
        if fc < fe or fc > fv:
            st.warning('Ingrese una fecha válida')
        vb = st.number_input('Ingrese el valor del bono: ')

    tda = convertion_rate(tn)
    df = flujo_caja(tc, vb, fe,fv, tda)
    st.dataframe(df)
    total = round(sum(df['VPFCB']),3)
    total_t = round(sum(df['t*VPFCB']),3)
    total_t_t = round(sum(df['t*t*VPFCB']),3)
    if total_t_t == 0 or  total_t == 0 or total == 0:
        rendimiento = 0
        duracion = 0
        convexidad = 0
    else: 

        rendimiento = round(total_t_t / total_t, 3)
        duracion = round(total_t / total,3)
        convexidad = round(1/total*((1+tda)**2) * total_t_t,3)
    duracion_mod = round(duracion/(1+tda), 3)
    col1, col2, col3 = st.columns(3)
    col1.metric("VPFCB", value = total)
    col2.metric("t*VPFCB", value = total_t)
    col3.metric("t* t * VPFCB", value = total_t_t)
    col1.metric("Convexidad", value = convexidad)
    col2.metric("Duración", value = duracion)
    col3.metric("Rendimiento", value = rendimiento)
    col1.metric('Duración módificada', value= duracion_mod)

    # calcular la convexida

    num = np.arange(-0.1, 0.1, 0.001)
    #conv = list(map(lambda x: (-duracion * x + (0.5 * convexidad * x**2)), num))
    #dura = list(map(lambda x: x * -duracion, num))
    var_dura =  -duracion_mod * num #variación precio bono respecto a la duración
    precio_dura = vb * (1+ var_dura)
    var_total =  var_dura + ( 0.5 * convexidad * (num**2))  # variacion total
    precio_con = vb * (1 + var_total)


    # grafico convexidad
    st.button("Volver", type="primary")
    if st.button('Mostrar convexidad'):
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=num, y=precio_con, mode='lines', name='Convexidad'))
        fig.add_trace(go.Scatter(x=num, y=precio_dura, mode='lines', name='Duración'))

        fig.update_layout(title='Variación del precio del bono en función de cambios en la Tasa de negociación',
                        xaxis_title='Tasa de negociación',
                        yaxis_title='Precio del bono')
        st.plotly_chart(fig, use_container_width=True)



with tab3:
    col1, col2, col3 = st.columns(3)
    with col1:
        t = st.date_input("Fecha de emisión", min_value=fecha_actual, max_value=fecha_mayor) # fe : fecha emisión
        c = st.number_input('Ingrese la tasa de emisión : ', format="%f")# tc : tasa cupon
    with col2:
        T = st.date_input("Fecha de vencimiento", min_value=fecha_actual, max_value=fecha_mayor)
        r = st.number_input('Ingrese la tasa de negociación : ', format="%f") # tn : tasa de negociación
    with col3:
        f_c = st.date_input("Fecha de compra", min_value=t, max_value=T) # fc : fecha compra
        valor_bond = st.number_input('Ingrese el valor del bono : ')
    
    #st.write('El valor presente del bono es:', valor_presente(c,r,valor_bond,t,f_c,T))
    col1,col2 = st.columns(2)
    col1.metric('Valor bono', value = valor_presente(c,r,valor_bond,t,f_c,T), delta =valor_presente(c,r,valor_bond,t,f_c,T)- valor_bond)