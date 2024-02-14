import pandas as pd
import numpy as np
import math 
from datetime import date

def calcular_precio_bono(fecha_emision, fecha_compra, fecha_final, tasa_facial, tasa_referencia, valor_inicial):
    """
    Calcula el precio de un bono.

    Parámetros:
    fecha_emision (datetime): Fecha de emisión del bono.
    fecha_compra (datetime): Fecha de compra del bono.
    fecha_final (datetime): Fecha de vencimiento del bono.
    tasa_facial (float): Tasa de interés del bono.
    tasa_referencia (float): Tasa de interés de referencia.
    valor_inicial (float): Valor inicial del bono.

    Retorna:
    float: Precio del bono.
    """
    if fecha_compra == fecha_emision:
        fecha = fecha_emision.day / fecha_final.day
        precio_bono = round(math.exp(-tasa_facial * fecha),3) * valor_inicial
    else:
        fecha = (fecha_final - fecha_compra).days / 365 # Convert fecha to numeric type
        precio_bono = round(math.exp(-tasa_referencia * fecha),3)* valor_inicial
    return precio_bono

def generar_tabla_bono_con_cupon(fecha_inicial, fecha_final, tasa_cupon, valor_nominal, tasa_interes_mercado):
    tasa_cupon = tasa_cupon * 100
    tasa_interes_mercado_diaria = round((1 + tasa_interes_mercado) ** ((1 / 365)- 1),4)
    print(tasa_interes_mercado,tasa_interes_mercado_diaria)
    plazo = (fecha_final - fecha_inicial).days // 365
    fechas = pd.date_range(start=fecha_inicial, end=fecha_final, freq="YE")
    tabla = pd.DataFrame(columns=["t", "Fecha", "Tasa Facial", "VPFCB", "t*VPFCB", "t*t*VPFCB"])
    fila = [0, fecha_inicial, np.nan, np.nan, np.nan, np.nan]
    tabla.loc[0] = fila
    fechas = [fecha.date() for fecha in fechas]
    for i in range(1, plazo):
        VPFCB = tasa_cupon /(1 + tasa_interes_mercado_diaria)**((fechas[i]-fecha_inicial).days)
        T_VPFCB = i * VPFCB
        T_cuadrado_VPFCB = T_VPFCB * i
        fila = [i, fechas[i], tasa_cupon, VPFCB, T_VPFCB, T_cuadrado_VPFCB]
        tabla.loc[i] = fila
    VPFCB = (100 + tasa_cupon )/ ((1 + tasa_interes_mercado_diaria))**((fecha_final-fecha_inicial).days)
    T_VPFCB = plazo * VPFCB
    T_cuadrado_VPFCB = T_VPFCB * plazo
    ultima_fila = [plazo, fecha_final, 100 + tasa_cupon, VPFCB, T_VPFCB, T_cuadrado_VPFCB]
    tabla.loc[plazo] = ultima_fila
    return tabla
            
print(generar_tabla_bono_con_cupon(date(2021, 1, 1), date(2025, 1, 1), 0.06, 1000, 0.07))