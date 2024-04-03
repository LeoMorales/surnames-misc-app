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
    target_surname = target_surname.strip()

    data_item = search_surname_and_get_dict(data, target_surname)

    if data_item:
        st.header(f'Apellido "{target_surname}"')

        col_img, col_txt, _ = st.columns([2, 2, 2])
        col_img.image(
            "static/same-surname.jpg",
            use_column_width='auto')
        col_txt.markdown(f'''
            ### Más *{target_surname}*:gray[s]

            ¿Sabías que en el país
            **:red[hay {data_item['n_arg']:,}] :orange[personas]** :green[que] :blue[también]
            :violet[se] :gray[llaman] :rainbow[como vos]? :balloon:

        ''')

        st.markdown("~~~")   
        _, col_txt, col_img = st.columns([2, 2, 2])
        col_txt.markdown(f'''
            ### Procedencia

            ¿Sabías que tu apellido
            es de origen **:rainbow[{data_item['origin']}]**?

        ''')
        col_img.image("static/procedence.jpg")

        st.markdown("~~~")
        _, col_img, col_txt, _ = st.columns([1, 1, 3, 1])
        col_img.image("static/provinces.jpg")
        col_txt.markdown(f'''
            ### Regionalidad

            ¿Sabías que la mayoría de la gente que tiene tu mismo apellido
            vive en **:blue[{data_item['province_most_people']}]**?

        ''')

        st.markdown("~~~")

    else:
        st.markdown(
            """
            ### :(

            No encontramos tu apellido en nuestra base de datos.

            Lo buscamos en el padrón electoral del año 2021.

            Existe la posibilidad de que hayamos perdido el apellido debido a nuestro proceso de limpieza de datos.

        """)

    _, col1 = st.columns([5, 1])

    if col1.button('Buscar otro apellido'):
        st.session_state.surname = None
