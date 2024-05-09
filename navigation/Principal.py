import datetime
import pandas as pd
import streamlit as st

from components.text import text


def Principal():


    # Encabezado
    st.title("¡Bienvenidos a nuestra aplicación DeFi!")

    # Mensaje de bienvenida
    st.write("""
    ¡Hola a todos!

    ¡Bienvenidos a nuestra aplicación DeFi! Estamos emocionados de tenerlos aquí para explorar todas las herramientas y recursos que hemos creado para ayudarlos en el mundo de las finanzas descentralizadas.
    """)

    # Sección: ¿Qué encontrarás aquí?
    st.header("¿Qué encontrarás aquí?")
    st.write("""
    En esta aplicación, encontrarás una variedad de herramientas útiles para tus actividades en DeFi:

    - **Calculadoras:** Realiza cálculos rápidos y precisos para tus estrategias de inversión.
    - **Valoración de activos financieros:** Accede a instrumentos para valorar activos y tomar decisiones informadas.
    - **Modelos:** Explora modelos financieros avanzados para comprender mejor los conceptos financieros.
    """)

    # Sección: Conoce al equipo detrás de la aplicación
    st.header("Conoce al equipo detrás de la aplicación")

    # Datos del equipo
    equipo = [
        {"nombre": "Jorfan Vargas", "github": "Jorfanv"},
        {"nombre": "Andrés Yañez", "github": "TheChieft"},
        {"nombre": "Juan David", "github": "juan1031"}
    ]

    # Mostrar el equipo
    for miembro in equipo:
        st.write(f"- **{miembro['nombre']}** [![GitHub](https://img.shields.io/badge/GitHub-{miembro['github']}-blue?style=flat&logo=github)](https://github.com/{miembro['github']})")
