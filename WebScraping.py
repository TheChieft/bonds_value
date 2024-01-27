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

BOND_INFO_URL_PUBLIC = 'https://www.bvc.com.co/renta-fija-deuda-publica-segmento-publico/'
BOND_INFO_URL_PRIVATE = 'https://www.bvc.com.co/renta-fija-deuda-publica-segmento-privado/'
BOND_INFO_URL_CORPORATE = 'https://www.bvc.com.co/renta-fija-deuda-corporativa/'


# Web Scraping to get information of the bonds
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys




def actual_bonds(url):
    driver = webdriver.Chrome()

    try:
        # Abrir la página con Selenium
        driver.get(url)

        # Esperar unos segundos para que la página se cargue completamente (puedes ajustar este tiempo según sea necesario)
        time.sleep(5)

        # buscar el elemento tabla
        table = driver.find_element(By.TAG_NAME, "table")  
        
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
        return df
    
def read_bonds_info(codigo: str):
    #dia y hora de hoy
    now = time.localtime()
    now = time.strftime("%Y-%m-%d %H:%M:%S", now)
    
    keywords = ["Tasa apertura\n", "Última tasa\n", "Tasa Máxima\n", "Tasa Mínima\n", "Cantidad\n", "Volumen*\n", "Nemotécnico\n","Base\n", "Fecha de emisión\n","Fecha de vencimiento\n","Tipo de tasa*\n"]

    df = pd.DataFrame(columns = ['Dia scraping','Tasa apertura','Última tasa','Tasa Máxima', 'Tasa Mínima', 'Cantidad', 'Volumen*', "Nemotécnico", 'Base', 'Fecha de emisión','Fecha de vencimiento','Tipo de tasa*'])
    l = [codigo,now]
    with open("test.txt", "r") as file:
        print("Leyendo archivo")
        data = file.readlines()
        for line in data:
            if line in keywords: # no entra aquí
                l.append(data[data.index(line) + 1].replace('\n', ''))
        df.loc[len(df)]= l
    return df


def get_info_bonds(codigo: str, url: str):
    driver = webdriver.Chrome()
    url = url + codigo + "?tab=resumen"
    
    try:
        # Abrir la página con Selenium
        driver.get(url)      
        # Esperar unos segundos para que la página se cargue completamente (puedes ajustar este tiempo según sea necesario)
        time.sleep(5)
        # Datos de tablas 
        try:
            # buscar clase "sc-bXCLTC hetshd"
            content = driver.find_element(By.CLASS_NAME, "Summarystyled__StyledSummary-sc-1ougflf-0")
            # guardar archivo en txt
            with open("data/raw/test.txt", "w") as file:
                file.write(content.text)
        except:
            print("Doesn't info in this page")
    except:
        print("DOESN'T WORK the link")
    finally:
        # Analisis  txt
        df_= read_bonds_info()
        # escribir linea en csv
        df_.to_csv("data/raw/bonds.csv", mode='a', header=False)
        # Cerrar el navegador de Selenium al finalizar
        driver.quit()
        

#get_info_bonds("TFIT21280542", BOND_INFO_URL_PUBLIC)
actual_bonds(BONDS_PUBLIC)
