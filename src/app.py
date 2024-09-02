import streamlit as st
import pandas as pd
from PIL import Image

from recommender import Recommender
from user import UserInteraction


def load_films(movies_to_display, name_tag):
    """
    Carga las películas que recibe en movies_to_display en la vista de la aplicación
    Permite buscar entre las películas del dataframe por su nombre para darles una calificación
    """

    st.markdown(
        """
        <style>
        .container {
            width: 200% !important;
        }
        .block-container {
            padding: 1rem 2rem;
            max-width: 1200px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    search_query = st.text_input("Busca una película:")
    if search_query:
        # si se hace una búsqueda se sale de las recomendaciones y se muestran todas las películas del dataset que coincidan con el criterio de búsqueda
        st.session_state.show_recommended = False
        results = st.session_state.user.merged_df[st.session_state.user.merged_df[name_tag].str.contains(search_query, case=False, na=False)].head(20)
    else:
        results = movies_to_display.head(20)

    num_results = len(results)
    rows = (num_results // 3) + (num_results % 3 > 0)

    # muestra las películas con un panel debajo para calificarlas
    with st.container():
        for row in range(rows):
            cols = st.columns(3)
            for col, idx in zip(cols, range(row * 3, min((row + 1) * 3, num_results))):
                movie = results.iloc[idx]
                img = Image.open(image_path)
                # movie_rating = int(movie['rating'])
                # print(movie_rating)
                # if movie_rating < 1:
                #     movie_rating = "-"

                movie_caption = f"{movie[name_tag]},  Año: {movie['year']}"
                col.image(img, caption=movie_caption, use_column_width=True)

                with col.form(key=f"rating_form_{idx}"):
                    rating = st.selectbox(f"Select your rating for {movie[name_tag]}", [1, 2, 3, 4, 5], key=f"rating_select_{idx}")
                    submit_button = st.form_submit_button(label="Guardar calificación")
                    if submit_button:
                        st.session_state.user.rate_movie(movie['movieId'], rating)
                        st.write(f"Rating for {movie[name_tag]}: {rating} stars")



def main():
    """
    Función main para correr la aplicación de streamlit
    Maneja las interacciones del usuario, incluyendo la creación de nuevos usuarios, recomendación y calificación de filmes
    """

    st.title("Sistema de recomendación de películas")

    if 'user' not in st.session_state:
        st.session_state.user = None
        # st.session_state.user representa la instancia del usuario
    if 'show_recommended' not in st.session_state:
        st.session_state.show_recommended = False
        # st.session_state.show_recommended representa que las películas a mostrar por ahora son las recomendadas
        # porque se presionó el botón recommend_button

    if st.session_state.user:
        st.write(f"UserId: {st.session_state.user.user_id}")

        # Añade el botón para pedir recomendaciones
        recommend_button = st.button("Recomendar Películas", key="recommend_button")

        if recommend_button:
            st.session_state.show_recommended = True
            recommended_movies = recommend_movies(st.session_state.user)
            st.session_state.recommendations = recommended_movies
            # st.session_state.recommendations representa las películas recomendadas para el usuario actual
            load_films(recommended_movies, 'title')
        else:
            if st.session_state.show_recommended:
                load_films(st.session_state.recommendations, 'title')
            else:
                load_films(st.session_state.user.merged_df, 'title')

    else:
        if 'creating_new_user' in st.session_state:
            new_user_name = st.text_input("Ingrese su nombre de usuario:")
            if new_user_name:
                user = create_user(new_user_name)
                st.session_state.user = user
                st.session_state.recommendations = recommend_movies(user)
                st.write(f"{new_user_name}, your id is: {st.session_state.user.user_id}")
                st.session_state.creating_new_user = False
                # st.session_state.creating_new_user guarda un booleano para indicar si se va a crear un nuevo usuario
                st.rerun()
        else:
            user_ids = ratings_df['userId'].unique().tolist()
            user_ids.insert(0, None)

            # Create the select component with the default value
            user_id = st.selectbox('Seleccione su ID', user_ids)

            if user_id:
                st.session_state.user = UserInteraction(str(user_id))
                st.session_state.recommendations = recommend_movies(st.session_state.user)
                st.write(f"UserId: {st.session_state.user.user_id}")
                st.rerun()
            else:
                if st.button("Crear nuevo usuario"):
                    st.session_state.creating_new_user = True
                    st.rerun()



def create_user(user_name):
    """
    Crea un objeto UserInteraction para el usuario, equivalente a una sesión
    Este objeto se utiliza para obtener las recomendaciones para ese usuario
    """
    st.write(f"Creating user: {user_name}")

    user = UserInteraction()
    return user

def recommend_movies(user):
    """
    Llama al método get_recommendations de la instancia de la clase UserInteraction
    Devuelve las películas recomendadas para el usuario
    """
    return user.get_recommendation()

if __name__ == "__main__":

    # carga el csv con ratings iniciales
    ratings_df = pd.read_csv('dataset/ratings.csv')

    # establece la dirección de la imagen que se utiliza para mostrar las películas
    image_path = './movie_icon.jpg'
    user = None
    main()
