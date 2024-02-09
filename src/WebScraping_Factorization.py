# Libraries to run de code
import time 
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# CONSTANTS
BONDS_PUBLIC = 'https://www.bvc.com.co/mercado-local-en-linea?tab=renta-fija_deuda-publica-segmento-publico'
BONDS_PRIVATE = 'https://www.bvc.com.co/mercado-local-en-linea?tab=renta-fija_deuda-publica-segmento-privado'
BONDS_CORPORATE = 'https://www.bvc.com.co/mercado-local-en-linea?tab=renta-fija_deuda-corporativa'
BONDS = [BONDS_PUBLIC, BONDS_PRIVATE, BONDS_CORPORATE]

BOND_INFO_URL_PUBLIC = 'https://www.bvc.com.co/mercado-local-en-linea?tab=renta-fija_deuda-publica-segmento-publico'
BOND_INFO_URL_PRIVATE = 'https://www.bvc.com.co/renta-fija-deuda-publica-segmento-privado/'
BOND_INFO_URL_CORPORATE = 'https://www.bvc.com.co/renta-fija-deuda-corporativa/'

# Web Scraping drivers
OPTS = webdriver.ChromeOptions()
OPTS.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36")
OPTS.add_argument("--headless")
DRIVER = webdriver.Chrome(ChromeDriverManager().install(), options=OPTS)

# FUNCTIONS ----------------------------------

def download_public():
    now = time.localtime()
    now = time.strftime("%Y%m%d", now)
    try:
        DRIVER.get(BOND_INFO_URL_PUBLIC)
        WebDriverWait(DRIVER, 2).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="sc-gEvEer jlIRBY button-download"]')))
        download_button = DRIVER.find_element(
            By.XPATH, '//button[@class="sc-gEvEer jlIRBY button-download"]')
        download_button.click()
        try:
            os.rename(f"DeudaPublica_{now}.csv", "data/db/bonds_public.csv")
        except:
            print("No hay bonos publicos")
    except:
        print(f"No se pudo completar la acción")
    finally:
        DRIVER.quit()

def get_info_bonds(codigo: str, url: str):
    url = url + codigo + "?tab=resumen"
    print(url)
    DRIVER.get(url)      
    print("get_info_bonds")
    time.sleep(5)
    content = DRIVER.find_element(By.CLASS_NAME, "Summarystyled__StyledSummary-sc-1ougflf-0")
    now = time.localtime()
    now = time.strftime("%Y-%m-%d %H:%M:%S", now)
    keywords = ["Nemotécnico","Tasa apertura", "Última tasa",
                "Tasa Máxima", "Tasa Mínima", "Cantidad", "Volumen*",
                "Base", "Fecha de emisión","Fecha de vencimiento","Tasa facial","Tipo de tasa*"]
    content = content.text.split("\n")
    cont = []
    for item in content:
        if item in keywords:
            cont.append(content[content.index(item) + 1].replace('\n', ''))
    # insertar en info_bonds_public.csv
    with open("data/db/info_bonds_public.csv", "a") as file:
        print(f"{now},{codigo},{','.join(cont)}\n")
        file.write(f"{now},{codigo},{','.join(cont)}\n")
        
def arreglar_df(df):
    # read csv sin la primera fila y agregarle los nombres de las coolumnasmnas
    columnas = ['Nemotécnico','Emisor','Clase de título','Fecha de vencimiento','Cantidad','Volúmenes','Tipo','Codigo Raro']
    df = pd.read_csv('data/db/bonds_public.csv', skiprows=1, sep=';', names=columnas)
    # eliminar columnas que no se usan como tipo y codigo raro
    df = df.drop(['Tipo','Codigo Raro'], axis=1)
    # Reescribir bonds_public.csv
    df.to_csv('data/db/bonds_public.csv', index=False)
    return df

def do_the_scraping():
    download_public()
    public = pd.read_csv('data/db/bonds_public.csv')
    public = arreglar_df(public)
    # Leer bien la tabla de bonos publicos
    print(public)
    try:
        for codigo in public['Nemotécnico']:
            if "TFIT" in codigo or "TCO" in codigo:
                print(codigo)
                get_info_bonds(codigo, BOND_INFO_URL_PUBLIC)
    except:
        print("No hay bonos publicos")
        
    DRIVER.quit()
    
do_the_scraping()