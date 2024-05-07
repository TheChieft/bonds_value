import streamlit as st


class text:

    def __init__(self, titulo: str, nivel: int):

        self.titulo = titulo
        self.nivel = nivel

    def text(self, texto: str):

        return st.markdown(
            f"""<h{self.nivel} style="font-family: 'arial', serif; color: #FFFFFF; margin-bottom: 8px; ">{self.titulo}</h>
                <p style="font-family: 'arial', serif; color: #FFFFFF; text-indent: 30px; margin-top: 20px; margin-left: 10px; text-align: justify; width: 97%;">{texto}</p>""",
            unsafe_allow_html=True)
