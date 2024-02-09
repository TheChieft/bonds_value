import streamlit as st
# icono
st.set_page_config(page_title="Valuación de instrumentos financieros", page_icon=":moneybag:")

# Titulo
# icono encima del titulo
st.markdown("<h2 style='font-size: 80px; text-align: Center; padding: 0px'>💰</h2>"
            "<h1 style='font-size: 50px; text-align: Center;'>Una manera sencilla de valorar los instrumentos financieros</h1>"
            "<p style='text-align: Center; font-size: 25px'>Esta aplicación te permite valorar los instrumentos financieros de manera sencilla y rápida.</p>"
            "<hr>"
            "<h3 style='text-align: Center;'>Instrumentos financieros</h3>"
            "<ul style='text-align: Center; display:flex; justify-content: Center; list-style: None;'>"
            "<li style='font-size: 25px'> ♦️ Bonos </li>"
            "<li style='font-size: 25px'> 💸 Acciones </li>"
            "<li style='font-size: 25px'> Divisas </li>"
            "<li style='font-size: 25px'> Futuros </li>"
            "<li style='font-size: 25px'> Opciones </li>"
            "</ul>",
            unsafe_allow_html=True)

# Explicacion de cada instrumento financiero
html_string = "<div class='container' style='border-radius:20px; opacity:0.8;padding: 5px 20px; text-align: Left; font-size: 25px; background-color:#ffff'><h2 style='text-align: Left; color:black'>¿Qué es un bono?</h2><p style='font-size:18px; color:black'>Los bonos son instrumentos financieros de deuda utilizados por entidades privadas y públicas para financiarse. Los bonos son instrumentos de renta fija, lo que significa que el emisor del bono paga un interés fijo a los tenedores de los bonos. Los bonos son una forma de inversión a largo plazo, ya que suelen tener vencimientos de entre 1 y 30 años.</p></div>"
# Explicacion de bonos
st.markdown(html_string, unsafe_allow_html=True)