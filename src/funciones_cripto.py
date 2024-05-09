import yfinance as yf
import pandas as pd
import requests
# Funcion para obtener datos de cierre 
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
# funcion para obtener métricas de la criptomoneda requerida
def descargar_info_cripto(api_key, cripto_symbol):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    parameters = {
        'symbol': cripto_symbol  # Cambiado de 'id' a 'symbol'
    }
    response = requests.get(url, headers=headers, params=parameters)
    if response.status_code == 200:
        data = response.json()
        cripto_data = data['data'][cripto_symbol]  # Acceder por el símbolo de la cripto

        # Building the dataframe with symbol included
        df = pd.DataFrame([{
            'Market Cap': cripto_data['quote']['USD']['market_cap'],
            '24h Volume': cripto_data['quote']['USD']['volume_24h'],
            'Price': cripto_data['quote']['USD']['price'],
            'Percent Change 1h': cripto_data['quote']['USD']['percent_change_1h'],
            'Percent Change 24h': cripto_data['quote']['USD']['percent_change_24h'],
            'Percent Change 7d': cripto_data['quote']['USD']['percent_change_7d'],
            'Last Updated': cripto_data['quote']['USD']['last_updated'],
            'Symbol': cripto_symbol  # Cambiado de 'Name' a 'Symbol'
        }])
        return df
    else:
        print("Error en la solicitud:", response.status_code)
        return None