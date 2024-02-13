import pandas as pd
import numpy as np

def calcular_precio_bono_sin_cupon(fecha_compra, fecha_final, tasa_interes, valor):
    """
    Calcula el precio de un bono sin cupón.

    Parámetros:
    fecha_compra (datetime): Fecha de compra del bono.
    fecha_final (datetime): Fecha de vencimiento del bono.
    tasa_interes (float): Tasa de interés del bono.
    valor (float): Valor esperado del bono.

    Retorna:
    float: Precio del bono.
    """
    # Calcula el precio del bono
    precio_bono = valor / (1 + tasa_interes) ** ((fecha_final - fecha_compra).days / 365)
    
    return precio_bono

def calcular_bono_con_cupon(plazo, tasa_cupon, valor_nominal, tasa_interes_mercado):
    # Calcular los flujos de efectivo de los cupones
    flujos_cupon = [tasa_cupon * valor_nominal] * int(plazo)

    # Agregar el flujo de efectivo del valor nominal al final del plazo
    flujos_cupon[-1] += valor_nominal

    # Calcular el valor presente de cada flujo de efectivo
    vp_flujos_cupon = [flujo / (1 + tasa_interes_mercado) ** (i + 1) for i, flujo in enumerate(flujos_cupon)]

    # Calcular T*VPFCB
    T_VPFCB = sum([(i + 1) * vp for i, vp in enumerate(vp_flujos_cupon)])

    # Calcular T²*VPFCB
    T_cuadrado_VPFCB = sum([(i + 1) ** 2 * vp for i, vp in enumerate(vp_flujos_cupon)])

    # Calcular VPFCB
    VPFCB = sum(vp_flujos_cupon)

    # Calcular T²VPFCB/TVPFCB
    T_cuadrado_VPFCB_TVPFCB = T_cuadrado_VPFCB / VPFCB

    # Calcular la duración
    duracion = T_VPFCB / VPFCB

    # Calcular la convexidad
    convexidad = sum([((i + 1) ** 2 * vp) / ((1 + tasa_interes_mercado) ** (i + 1)) for i, vp in enumerate(vp_flujos_cupon)]) / VPFCB

    return VPFCB, T_VPFCB, T_cuadrado_VPFCB, T_cuadrado_VPFCB_TVPFCB, duracion, convexidad

def generar_tabla_bono_con_cupon(fecha_inicial, fecha_final, tasa_cupon, valor_nominal, tasa_interes_mercado):
    # Calcular el plazo en años
    plazo = (fecha_final - fecha_inicial).days // 365

    # Crear las fechas de vencimiento para cada flujo de efectivo
    fechas = pd.date_range(start=fecha_inicial, end=fecha_final, freq="Y")
    
    # Crear la tabla de flujos de efectivo
    tabla = pd.DataFrame(columns=["t", "Fecha", "Tasa Facial", "VPFCB", "t*VPFCB", "t*t*VPFCB"])

    # Inicializar t y los valores de VPFCB, T_VPFCB, y T_cuadrado_VPFCB
    t = None
    VPFCB = np.nan
    T_VPFCB = np.nan
    T_cuadrado_VPFCB = np.nan

    # Agregar los flujos de efectivo a la tabla
    for i, fecha in enumerate(fechas):
        
        # Ajustar la última fila correspondiente a la tasa facial
        if i == plazo - 1:
            tasa_facial_ajustada = 1 + tasa_cupon
        elif i == 0:
            tasa_facial_ajustada = np.nan
        else:
            tasa_facial_ajustada = tasa_cupon
            t = i
            fecha_actual = fechas[i]
            fecha_inicial = pd.to_datetime(fecha_inicial)  # Convert fecha_inicial to datetime
            dias_transcurridos = (fecha_actual - fecha_inicial).days
            VPFCB = tasa_cupon / ((1 + tasa_interes_mercado) ** dias_transcurridos)
            T_VPFCB = t * VPFCB
            T_cuadrado_VPFCB = T_VPFCB * t
        tabla.loc[i] = [t, fecha, tasa_facial_ajustada, VPFCB, T_VPFCB, T_cuadrado_VPFCB]
    # tabla con el index columna t
    tabla.set_index('t', inplace=True)
    
    return tabla

def generar_tabla_bono_con_cupon2(fecha_inicial, fecha_final, tasa_cupon, valor_nominal, tasa_interes_mercado):
    tasa_interes_mercado_diaria = (1 + tasa_interes_mercado) ** (1 / 365) - 1
    plazo = (fecha_final - fecha_inicial).days // 365
    fechas = pd.date_range(start=fecha_inicial, end=fecha_final, freq="Y")
    tabla = pd.DataFrame(columns=["t", "Fecha", "Tasa Facial", "VPFCB", "t*VPFCB", "t*t*VPFCB"])
    fila = [0, fecha_inicial, np.nan, np.nan, np.nan, np.nan]
    tabla.loc[0] = fila
    for i in range(1, plazo):
        print(fechas[i])
        VPFCB = tasa_cupon / ((1 + tasa_interes_mercado_diaria) ** (fecha_inicial - pd.Timestamp(fechas[i])).days)
        T_VPFCB = i * VPFCB
        T_cuadrado_VPFCB = T_VPFCB * i
        fila = [i, fechas[i], tasa_cupon, VPFCB, T_VPFCB, T_cuadrado_VPFCB]
        tabla.loc[i] = fila
    ultima_fila = [plazo, fecha_final, 1 + tasa_cupon, valor_nominal / ((1 + tasa_interes_mercado) ** (plazo * 365)), plazo * valor_nominal / ((1 + tasa_interes_mercado) ** (plazo * 365)), plazo * plazo * valor_nominal / ((1 + tasa_interes_mercado) ** (plazo * 365))]
    tabla.loc[plazo] = ultima_fila
    return tabla
            

