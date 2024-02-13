# Graficar curva de rendimiento de un bono
from datetime import datetime

def calcular_valor_presente_venta(valor_nominal, tasa_cupon, tasa_actual, fecha_vencimiento):
    # Calcular el número de días hasta el vencimiento
    hoy = datetime.now()  # Convert hoy to a datetime object
    dias_hasta_vencimiento = (fecha_vencimiento - hoy).days
    # Convertir las tasas a decimales
    tasa_cupon_decimal = tasa_cupon / 100
    tasa_actual_decimal = tasa_actual / 100
    
    # Calcular el valor presente de los pagos del cupón
    valor_presente_cupon = tasa_cupon_decimal * valor_nominal * (dias_hasta_vencimiento / 365)
    
    # Calcular el valor presente del valor nominal del bono
    valor_presente_valor_nominal = valor_nominal / ((1 + tasa_actual_decimal) ** (dias_hasta_vencimiento / 365))
    
    # Calcular el valor presente total del bono
    valor_presente_total = valor_presente_cupon + valor_presente_valor_nominal
    
    return valor_presente_total

def calcular_intereses_devengados(valor_nominal, tasa_cupon, fecha_ultimo_pago, fecha_venta):
    # Calcular el número de días desde el último pago de cupón hasta la fecha de venta
    dias_hasta_venta = (fecha_venta - fecha_ultimo_pago).days
    
    # Calcular el número de días entre pagos de cupón
    dias_entre_cupones = 365 / (tasa_cupon / 100)
    
    # Calcular el número de cupones pagados desde el último pago hasta la fecha de venta
    cupones_pagados = dias_hasta_venta // dias_entre_cupones
    
    # Calcular los intereses devengados
    intereses_devengados = cupones_pagados * valor_nominal * (tasa_cupon / 100)
    
    return intereses_devengados

def calcular_retorno_inversion_bono(valor_nominal, tasa_cupon, tasa_actual, fecha_ultimo_pago, fecha_venta):
    # Calcular la venta del bono
    valor_presente_total = calcular_valor_presente_venta(valor_nominal, tasa_cupon, tasa_actual, fecha_venta)
    
    # Calcular los intereses devengados
    intereses_devengados = calcular_intereses_devengados(valor_nominal, tasa_cupon, fecha_ultimo_pago, fecha_venta)
    
    # Calcular el retorno de la inversión
    retorno_inversion = (valor_presente_total - valor_nominal + intereses_devengados) / valor_nominal * 100
    
    return retorno_inversion

def calcular_precio_venta_bono(valor_nominal, tasa_cupon, tasa_actual, fecha_ultimo_pago, fecha_venta, retorno_desado):
    intereses = calcular_intereses_devengados(valor_nominal, tasa_cupon, fecha_ultimo_pago, fecha_venta)
    precio_venta = valor_nominal + intereses - retorno_desado
    return precio_venta

# Ejemplo de uso:
valor_nominal = 5000000  # Valor nominal del bono
tasa_cupon = 12  # Tasa del cupón (%)
tasa_actual = 14  # Tasa actual (%)
fecha_ultimo_pago = datetime(2022, 2, 13)  # Fecha del último pago de cupón
fecha_venta = datetime(2023, 2, 13)  # Fecha de venta del bono

retorno_inversion = calcular_retorno_inversion_bono(valor_nominal, tasa_cupon, tasa_actual, fecha_ultimo_pago, fecha_venta)
print("El retorno de tu inversión en el bono con cupón es:", retorno_inversion, "%")
valor_actual = calcular_valor_presente_venta(valor_nominal, tasa_cupon, tasa_actual, fecha_venta)
print("El valor actual del bono es:", valor_actual)
precio_venta = calcular_precio_venta_bono(valor_nominal, tasa_cupon, tasa_actual, fecha_ultimo_pago, fecha_venta, 4708000)
print("El precio de venta del bono es:", precio_venta)