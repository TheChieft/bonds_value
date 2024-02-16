import pandas as pd
import numpy as np
import math 
from datetime import date

def calcular_precio_bono(fecha_emision, fecha_compra, fecha_vencimiento, tasa_facial, tasa_referencia, valor_inicial):
    """
    Calcula el precio de un bono.

    Parámetros:
    fecha_emision (datetime): Fecha de emisión del bono.
    fecha_compra (datetime): Fecha de compra del bono.
    fecha_vencimiento (datetime): Fecha de vencimiento del bono.
    tasa_facial (float): Tasa de interés del bono.
    tasa_referencia (float): Tasa de interés de referencia.
    valor_inicial (float): Valor inicial del bono.

    Retorna:
    float: Precio del bono.
    """
    if fecha_compra == fecha_emision:
        fecha = fecha_emision.day / fecha_vencimiento.day
        precio_bono = round(math.exp(-tasa_facial * fecha),3) * valor_inicial
    else:
        fecha = (fecha_vencimiento - fecha_compra).days / 365 # Convert fecha to numeric type
        precio_bono = round(math.exp(-tasa_referencia * fecha),3)* valor_inicial
    return precio_bono

def grafica_convexidad():
    # graficar convexidad de un bono
    pass

def calcular_tasa_interes_mercado_diaria(tasa_referencia):
        return round((1 + tasa_referencia) ** ((1 / 365))-1,4)
    
def calcular_proximo_cupon(fecha_emision, fecha_compra):
    fecha = fecha_emision
    while fecha.year < fecha_compra.year:
        fecha = fecha.replace(year=fecha.year + 1)
    return fecha

def calcular_fechas_cupones(fecha_proximo_cupon, fecha_vencimiento):
    lista_fechas = [fecha_proximo_cupon]
    fecha = fecha_proximo_cupon
    while fecha.year < fecha_vencimiento.year:
        fecha = fecha.replace(year=fecha.year + 1)
        lista_fechas.append(fecha)
    return lista_fechas, len(lista_fechas)
    
def generar_tabla_bono_con_cupon(fecha_emision,fecha_compra, fecha_vencimiento, tasa_cupon, valor_nominal, tasa_referencia):
    fecha_proximo_cupon = calcular_proximo_cupon(fecha_emision, fecha_compra) # REVISADO
    tasa_interes_mercado_diaria = calcular_tasa_interes_mercado_diaria(tasa_referencia) # REVISADO
    fechas, plazo = calcular_fechas_cupones(fecha_proximo_cupon, fecha_vencimiento) # REVISADO
    tabla = pd.DataFrame(columns=["t", "Fecha", "Tasa Facial", "VPFCB", "t*VPFCB", "t*t*VPFCB"]) # REVISADO
    fila = [0, fecha_compra, np.nan, np.nan, np.nan, np.nan] # REVISADO
    tabla.loc[0] = fila # REVISADO
    # ------------------- Calculo de la tabla -------------------
    if fecha_compra == fecha_emision:
        VPFCB = tasa_cupon/((1 + tasa_interes_mercado_diaria)**((fechas[1] - fecha_compra).days))
        fecha = fecha_compra
    else:
        VPFCB = tasa_cupon/((1 + tasa_interes_mercado_diaria)**((fechas[1] - fecha_proximo_cupon).days))
        fecha = fecha_proximo_cupon
    T_VPFCB = VPFCB
    T_cuadrado_VPFCB = T_VPFCB
    fila = [0, fecha, tasa_cupon, VPFCB, T_VPFCB, T_cuadrado_VPFCB]
    tabla.loc[1] = fila
    print(tabla)
    for i in range(2, plazo):
        if fecha_compra == fecha_emision:
            VPFCB = tasa_cupon/((1 + tasa_interes_mercado_diaria)**((fechas[i - 1] - fecha_compra).days))
        else:
            VPFCB = tasa_cupon/((1 + tasa_interes_mercado_diaria)**((fechas[i - 1] - fecha_proximo_cupon).days))
        T_VPFCB = (i) * VPFCB
        T_cuadrado_VPFCB = T_VPFCB * (i)
        fila = [i, fechas[i - 1], tasa_cupon, VPFCB, T_VPFCB, T_cuadrado_VPFCB]
        tabla.loc[i] = fila
    VPFCB = (100 + tasa_cupon )/ ((1 + tasa_interes_mercado_diaria))**((fecha_vencimiento-fecha_compra).days)
    T_VPFCB = plazo * VPFCB
    T_cuadrado_VPFCB = T_VPFCB * plazo
    ultima_fila = [plazo, fecha_vencimiento, 1 + tasa_cupon, VPFCB, T_VPFCB, T_cuadrado_VPFCB]
    tabla.loc[plazo] = ultima_fila
    suma_VPFCB = tabla["VPFCB"].sum()
    suma_T_VPFCB = tabla["t*VPFCB"].sum()
    suma_T_cuadrado_VPFCB = tabla["t*t*VPFCB"].sum()
    duracion = suma_T_VPFCB / suma_VPFCB
    convexidad = (suma_T_cuadrado_VPFCB / suma_T_VPFCB)/suma_VPFCB
    ultima_ultima_fila = [np.nan, np.nan, np.nan, suma_VPFCB, suma_T_VPFCB, suma_T_cuadrado_VPFCB]
    tabla.loc[plazo + 1] = ultima_ultima_fila
    
    tabla_convexidad = grafica_convexidad()
    return tabla, duracion, convexidad, tabla_convexidad


            
print(generar_tabla_bono_con_cupon(date(2022,11,2),date(2023,3,11),date(2029, 11, 3), 0.06, 1000, 0.07))