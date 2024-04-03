import streamlit as st
import pandas
import numpy as np


@st.cache_data
def load_data():
    data = pandas.DataFrame({
        'surname': ["MORALES"],
        'n_arg': [100],
        'origin': ["Español"],
        'province_most_people': ["Neuquén"]
    })

    data = pandas.read_parquet("data/data.parquet")

    return data


def search_surname_and_get_dict(df, target_surname):

    target_surname = target_surname.upper()

    try:
        indice = df.index[df['surname'] == target_surname].tolist()[0]
        # Obtener la fila correspondiente al índice encontrado
        fila = df.iloc[indice]
        return fila.to_dict()

    except IndexError:
        return {}


data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done!")


if "surname" not in st.session_state:
    st.title("¿Cuál es tu apellido?")

    st.text_input("Tu apellido", key="surname")

else:
    data_load_state.text("")

    target_surname = st.session_state.surname

    data_item = search_surname_and_get_dict(data, target_surname)

    st.header(f'Apellido "{target_surname}"')

    _, col_img, col_txt, _ = st.columns([1, 1, 2, 2])
    col_img.image(
        "https://static.streamlit.io/examples/dog.jpg",
        use_column_width='auto')
    col_txt.markdown(f'''
        ### Más *{target_surname}*:gray[s]

        ¿Sabías que en el país
        **:red[hay {data_item['n_arg']}] :orange[personas]** :green[que] :blue[también]
        :violet[se] :gray[llaman] :rainbow[como vos]? :balloon:

    ''')

    st.markdown("~~~")   
    _, col_txt, col_img, _ = st.columns([2, 2, 1, 1])
    col_txt.markdown(f'''
        ### Procedencia

        ¿Sabías que tu apellido
        es de origen **:rainbow[{data_item['origin']}]**?

    ''')
    col_img.image("https://static.streamlit.io/examples/dog.jpg")

    st.markdown("~~~")
    _, col_img, col_txt, _ = st.columns([1, 1, 3, 1])
    col_img.image("https://static.streamlit.io/examples/dog.jpg")
    col_txt.markdown(f'''
        ### Regionalidad

        ¿Sabías que la mayoría de la gente que tiene tu mismo apellido
        vive en **:blue[{data_item['province_most_people']}]**?

    ''')

    st.markdown("~~~")

    _, col1 = st.columns([5, 1])

    if col1.button('Buscar otro apellido'):
        st.session_state.surname = None
