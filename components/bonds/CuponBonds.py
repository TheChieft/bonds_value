import streamlit as st
import pandas as pd
import time 
# src/WebScraping_Factorization.py

#from src.WebScraping_Factorization import do_the_scraping

def CuponBonds():
    # Boton para recargar los datos
    container = st.container(border=True)
    # Agregar un botón dentro del contenedor
    with container:
        st.title("Bonos con Cupón de la BVC")
        st.write("Antes de regargar la información de los bonos, asegúrate de tener conexión a internet. Y que sea hora de mercado. 9:00am a 4:00 pm")
        if st.button("Recargar datos"):
            #datos = do_the_scraping()
            st.write("Datos recargados")
 
    # Leer los datos del CSV en un DataFrame
    @st.cache_data 
    def cargar_datos():
        return pd.read_csv('data/db/bonds_public.csv')

    datos = cargar_datos()
    # Filtrar los bonos con cupón (Es cuando el nemotecnico tiene la palabra TFIT en el nombre)
    datos = datos[datos['Nemotécnico'].str.contains('TFIT')]
    

    # Mostrar los datos en una tabla
    st.write("Bonos con cupón de la BVC:")
    st.write(datos)

    # Mostrar los datos en una tabla y permitir al usuario seleccionar un bono
    st.title("Análisis de bonos con cupón de la BVC:")
    bono_seleccionado = st.selectbox("Seleccione un bono", options=datos['Nemotécnico'])

    # Función para calcular y mostrar detalles del bono seleccionado
    def mostrar_detalle_bono(bono):
        # Aquí puedes realizar los cálculos y visualizaciones para el bono seleccionado
        detalles_bono = datos[datos['Nemotécnico'] == bono]
        st.write(detalles_bono)

    # Llamar a la función para mostrar detalles del bono seleccionado
    mostrar_detalle_bono(bono_seleccionado)
