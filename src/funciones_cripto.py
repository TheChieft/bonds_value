import yfinance as yf
import pandas as pd

def obtener_datos_cierre(symbols, c_start, c_end, intentos_maximos=3, intervalo = "1wk"):
    """
    Función que descarga datos de cierre de criptomonedas de Yahoo Finance.

    Argumentos:
        symbols: Lista de símbolos de criptomonedas (ej: ["BTC-USD", "ETH-USD"]).
        c_start: Fecha de inicio en formato YYYY-MM-DD.
        c_end: Fecha de finalización en formato YYYY-MM-DD.
        intentos_maximos: Número máximo de intentos de descarga (por defecto 3).

    Retorno:
        DataFrame de Pandas con los datos de cierre
    """

    for intento in range(intentos_maximos):
        try:
        # Descargaa datos 
            data = yf.download(symbols, start=c_start, end=c_end, interval= intervalo)
            return data['Close']
        except Exception as e: 
            print(f"Intento {intento+1}: Error al descargar datos: {e}")
            if intento == intentos_maximos - 1: 
                print(f"Descarga fallida después de {intentos_maximos} intentos.")
                return pd.DataFrame()