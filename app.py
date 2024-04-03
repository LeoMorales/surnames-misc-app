import streamlit as st
import pandas as pd
import numpy as np


if not "surname" in st.session_state:
    
    st.title("¿Cuál es tu apellido?")

    st.text_input("Tu apellido", key="surname")


else:
    
    st.write(f'Apellido "{st.session_state.surname}"')
    
    st.write(f'¿Sabías que en el país hay 24753 personas que también se llaman como vos?')
    
    st.write(f'¿Sabías que tu apellido es de origen español?')
    
    st.write(f'¿Sabías que la mayoría de la gente que tiene tu mismo apellido vive en Entre Rios?')
