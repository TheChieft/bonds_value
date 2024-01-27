import pandas as pd
import time

def read_bonds_info():
    #dia y hora de hoy
    now = time.localtime()
    now = time.strftime("%Y-%m-%d", now)
    
    keywords = ["Tasa apertura\n", "Última tasa\n", "Tasa Máxima\n", "Tasa Mínima\n", "Cantidad\n", "Volumen*\n", "Nemotécnico\n","Base\n", "Fecha de emisión\n","Fecha de vencimiento\n","Tipo de tasa*\n"]

    df = pd.DataFrame(columns = ['Dia scraping','Tasa apertura','Última tasa','Tasa Máxima', 'Tasa Mínima', 'Cantidad', 'Volumen*', "Nemotécnico", 'Base', 'Fecha de emisión','Fecha de vencimiento','Tipo de tasa*'])
    l = [now]
    with open("test.txt", "r") as file:
        print("Leyendo archivo")
        data = file.readlines()
        for line in data:
            if line in keywords: # no entra aquí
                l.append(data[data.index(line) + 1].replace('\n', ''))
        df.loc[len(df)]= l
    return df

df = read_bonds_info()
# escribir en csv
df.to_csv('data/db/bonds.csv', mode='a', index=False)       

