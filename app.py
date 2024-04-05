import streamlit as st
import pandas


ARG_TOTAL_POP = 34_328_954


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

    try:
        indice = df.index[df['surname'] == target_surname].tolist()[0]
        # Obtener la fila correspondiente al índice encontrado
        fila = df.iloc[indice]
        return fila.to_dict()

    except IndexError:
        return {}


def show_surname_n_block(target_surname, n_surname):
    "Muestra el bloque con el resumen de cantidades del apellido"

    surname_pop_percentage = n_surname * 100 / ARG_TOTAL_POP

    col_img, col_txt = st.columns([2, 2])
    col_img.image(
        "static/same-surname.jpg",
        use_column_width='auto')
    txt = f'''
        ### Más *{target_surname}*:gray[s]

        ¿Sabías que en el país
        **:red[hay {n_surname:,}] :orange[personas]** :green[que]
        :blue[también] :violet[se] :gray[llaman] :rainbow[como vos]?
        :balloon:

    '''
    col_txt.markdown(txt)

    if surname_pop_percentage < 0.001:
        txt = ''':gray[Este número, representa un porcentaje *muy* bajito de
        la de la población argentina (menos de 0.001%).]'''
    else:
        txt = f'''
            Este número, representa el **{surname_pop_percentage:0.2}%**
            de la población argentina.
        '''
    col_txt.markdown(txt)


def show_surname_origin_block(surname_origin):
    "Muestra el bloque con el resumen del origen"

    col_txt, col_img = st.columns([2, 2])

    if surname_origin == '-':
        col_txt.markdown('''
            ### Procedencia

            No hemos encontrado el origen de tu apellido en
            nuestras bases de datos.

            Estas listas están confeccionadas con diversas fuentes 
            geolinguísticas y se actualizan año a año!

        ''')
    else:
        col_txt.markdown(f'''
            ### Procedencia

            ¿Sabías que tu apellido
            es de origen **:rainbow[{surname_origin}]**?

        ''')

    col_img.image("static/procedence.jpg")


def show_surname_incidence_block(
        province_most_people,
        province_most_people_value,
        province_most_surname_incidence,
        province_most_surname_incidence_value,
):
    "Muestra el bloque con el resumen de incidencia del apellido"

    incidence_value = round(province_most_surname_incidence_value * 1_000)

    _, col_img, col_txt = st.columns([1, 1, 2])
    col_img.image("static/provinces.jpg")
    col_txt.markdown(f'''
        ### Regionalidad

        ¿Sabías que la mayoría de la gente que tiene tu mismo apellido
        vive en **:blue[{province_most_people}]**?
        *:grey[({province_most_people_value:,} personas)]*

    ''')
    if incidence_value == 0:
        return

    if province_most_people_value == province_most_surname_incidence:
        col_txt.markdown(f'''

            *:grey[({incidence_value} de cada 1000 personas)]*

        ''')
    else:
        col_txt.markdown(f'''

            Sin embargo, la provincia en la que tu apellido tiene mayor
            incidencia es :orange[{province_most_surname_incidence}]
            *:grey[({incidence_value} de cada 1000 personas)]*

        ''')


data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")


if "surname" not in st.session_state:
    st.title("¿Cuál es tu apellido?")

    st.text_input("Tu apellido", key="surname")

else:
    data_load_state.text("")

    target_surname = st.session_state.surname
    target_surname = target_surname.strip()
    target_surname = target_surname.upper()

    data_item = search_surname_and_get_dict(data, target_surname)

    if data_item:


        st.header(f'Apellido "{target_surname}"')

        show_surname_n_block(target_surname, data_item['n_arg'])

        st.markdown("~~~")

        show_surname_origin_block(data_item['origin'])

        st.markdown("~~~")

        show_surname_incidence_block(
            data_item['province_most_people'],
            data_item['province_most_people_value'],
            data_item['province_most_surname_incidence'],
            data_item['province_most_surname_incidence_value'],
        )

        st.markdown("~~~")

    else:
        st.markdown(
            """
            ### :(

            No encontramos tu apellido en nuestra base de datos.

            Lo buscamos en el padrón electoral del año 2021.

            Existe la posibilidad de que hayamos perdido el apellido debido
            a nuestro proceso de limpieza de datos.

        """)

    _, col1 = st.columns([5, 1])

    if col1.button('Buscar otro apellido'):
        st.session_state.surname = None
