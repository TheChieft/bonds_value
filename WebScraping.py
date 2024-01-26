# Webscraping to get the value of the bonds of the Colombia Government
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

import datetime
import os
import time
import sys

BONDS_PUBLIC = 'https://www.bvc.com.co/mercado-local-en-linea?tab=renta-fija_deuda-publica-segmento-publico'
BONDS_PRIVATE = 'https://www.bvc.com.co/mercado-local-en-linea?tab=renta-fija_deuda-publica-segmento-privado'
BONDS_CORPORATE = 'https://www.bvc.com.co/mercado-local-en-linea?tab=renta-fija_deuda-corporativa'
BONDS = [BONDS_PUBLIC, BONDS_PRIVATE, BONDS_CORPORATE]


# Web Scraping to get information of the bonds
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# ...

def actual_bonds(url):
    driver = webdriver.Chrome(executable_path='chromedriver-linux64/chromedriver')

    try:
        # Abrir la página con Selenium
        driver.get(url)

        # Esperar unos segundos para que la página se cargue completamente (puedes ajustar este tiempo según sea necesario)
        time.sleep(5)

        # buscar el elemento tabla
        table = driver.find_element(By.TAG_NAME, "table")  
        
        # click a las clases sc-jEACwC jXpSUu Tablestyled__StyledSelectableField-sc-1vmiaeb-6 kswwBb field--selectable


        # Verificar si la tabla se encontró correctamente
        if table:
            # Obtener todas las filas de la tabla
            rows = table.find_elements(By.TAG_NAME, 'tr')
            df = pd.DataFrame(columns = ['Emisor','Nemotécnico','Clase de titulo', 'Fecha de vencimiento'])            
            for row in rows:
                try:
                    df.loc[len(df)]= row.text.split("\n")
                except:
                    df = df.drop(index=0)
                    continue
            print(df)
    finally:
        # Cerrar el navegador de Selenium al finalizar
        driver.quit()

def get_info_bonds(codigo: str):
    pass


actual_bonds(BONDS_PUBLIC)
