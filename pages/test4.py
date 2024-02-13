import numpy as np
import matplotlib.pyplot as plt

def calcular_ganancias_mensuales(tasa_interes, inversion_inicial, duracion_en_meses):
    """
    Calcula las ganancias mensuales con una tasa de interés efectiva anual.
    
    Parámetros:
    tasa_interes (float): Tasa de interés efectiva anual.
    inversion_inicial (float): Inversión inicial.
    duracion_en_meses (int): Duración en meses.
    
    Retorna:
    list: Lista de ganancias mensuales.
    """
    ganancias_mensuales = []
    saldo = inversion_inicial
    for _ in range(duracion_en_meses):
        saldo *= 1 + tasa_interes / 12  # Se divide la tasa anual por 12 para obtener la tasa mensual
        ganancia = saldo - inversion_inicial
        ganancias_mensuales.append(ganancia)
    return ganancias_mensuales

# Parámetros
tasa_interes_anual = 0.05  # Tasa de interés efectiva anual
inversion_inicial = 1000  # Inversión inicial
duracion_en_meses = 12  # Duración en meses

# Calcula las ganancias mensuales
ganancias = calcular_ganancias_mensuales(tasa_interes_anual, inversion_inicial, duracion_en_meses)

# Grafica las ganancias mensuales
meses = np.arange(1, duracion_en_meses + 1)
plt.plot(meses, ganancias, marker='o')
plt.title('Ganancias Mensuales')
plt.xlabel('Mes')
plt.ylabel('Ganancia')
plt.grid(True)
plt.show()
