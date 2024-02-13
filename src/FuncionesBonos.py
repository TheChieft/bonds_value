import numpy as np
from datetime import datetime

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