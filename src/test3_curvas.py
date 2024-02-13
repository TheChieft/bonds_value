# Graficar curva de rendimiento de un bono

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tasa_facial = 10.2
tasa_referencia = 5.5
base = 365
fecha_emision = '2022-01-01'
fecha_vencimiento = '2027-01-01'

# Calcular el rendimiento del bono y graficar

# Convertir las tasas a números
tasa_facial = float(tasa_facial/100)
base = float(base)
tasa_referencia = float(tasa_referencia/100)

# Calcular la tasa diaria
tasa_diaria = (1 + (tasa_referencia/100))**(1 / base) - 1

# Mostrar resultados
print('Tasa diaria: ', f'{round(tasa_diaria*100,3)}%')

# Gráfico de la curva de rendimiento
# Crear la lista de fechas de pago de cupones
cupones = []
for i in range(1, 13):
    cupones.append(f'{i}-01')
df_cupones = pd.DataFrame({'Pago_cupones': cupones})
df_cupones['Pago_cupones'] = pd.to_datetime(
df_cupones['Pago_cupones'], format='%m-%d')

VPFCB = []
T_VPFCB = []
TT_VPFCB = []

emision = pd.to_datetime(fecha_emision)
a = 1

for i in df_cupones['Pago_cupones']:
    if i.date() != pd.to_datetime(fecha_vencimiento).date():
        dias_diferencia = (i - emision).days
        VPFCB.append(
            round((tasa_facial+100/((1 + tasa_diaria)**(dias_diferencia))), 3))
        T_VPFCB.append(
            round(((tasa_facial+100/((1 + tasa_diaria)**(dias_diferencia)))*a), 3))
        TT_VPFCB.append(
            round(((tasa_facial+100/((1 + tasa_diaria)**(dias_diferencia)))*(a*a)), 3))
        a += 1
    dias_diferencia = (i - emision).days
    VPFCB.append(
        round((tasa_facial/((1 + tasa_diaria)**(dias_diferencia))), 3))
    T_VPFCB.append(
        round(((tasa_facial/((1 + tasa_diaria)**(dias_diferencia)))*a), 3))
    TT_VPFCB.append(
        round(((tasa_facial/((1 + tasa_diaria)**(dias_diferencia)))*(a*a)), 3))
    a += 1
    
VPFCB = pd.DataFrame(
    {'VPFCB': VPFCB, 'T_VPFCB': T_VPFCB, 'TT_VPFCB': TT_VPFCB})

# Graficar la curva de rendimiento
plt.figure(figsize=(10, 5))
plt.plot(VPFCB['VPFCB'], label='VPFCB')
plt.plot(VPFCB['T_VPFCB'], label='T_VPFCB')

plt.title('Curva de rendimiento')
plt.xlabel('Fecha de pago de cupón')
plt.ylabel('Valor presente')
plt.legend()
plt.show()