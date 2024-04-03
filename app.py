import streamlit as st
import pandas as pd
import numpy as np

st.title("¿Cuál es tu apellido?")

st.text_input("Tu apellido", key="surname")

input_surname = st.session_state.surname
if input_surname:
    st.write(f'Buscando "{input_surname}"...')


# ¿Sabías que en el país hay 24753 personas que también se llaman como vos?

# ¿Sabías que tu apellido es de origen español?
# ¿Sabías que la mayoría de la gente que tiene tu mismo apellido vive en Entre Rios?
