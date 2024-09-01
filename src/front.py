import streamlit as st
import pandas as pd
from PIL import Image

from recommender import Recommender
from user import UserInteraction

# Read the CSV file
df = pd.read_csv('dataset/movies.csv')
ratings_df = pd.read_csv('dataset/ratings.csv')
user_ids = ratings_df['userId'].unique()


movies = df[['movieId', 'title']]
image_path = './movie_icon.jpg'
user = None


def load_films(movies_to_display):
    search_query = st.text_input("Search for a movie:")
    if search_query:
        results = movies_to_display[movies_to_display['title'].str.contains(search_query, case=False)].head(20)
    else:
        results = movies_to_display.head(20)

    num_results = len(results)
    rows = (num_results // 3) + (num_results % 3 > 0)
    
    for row in range(rows):
        cols = st.columns(3)
        for col, idx in zip(cols, range(row * 3, min((row + 1) * 3, num_results))):
            movie = results.iloc[idx]
            img = Image.open(image_path)
            col.image(img, caption=movie['title'], use_column_width=True)
            
            if col.button(f"Rate {movie['title']}", key=f"rate_button_{idx}"):
                with st.form(key=f"rating_form_{idx}"):
                    rating = st.selectbox(f"Select your rating for {movie['title']}", [1, 2, 3, 4, 5], key=f"rating_select_{idx}")
                    st.write(movie['movieId'])
                    submit_button = st.form_submit_button(label="Save Rating")
                    if submit_button:
                        st.session_state.user.rate_movie(movie['movieId'], rating)
                        st.write(f"Rating for {movie['title']}: {rating} stars")

def create_user(user_name):
    # Placeholder for creating a new user
    st.write(f"Creating user: {user_name}")
    # Simulate user ID creation
    user = UserInteraction()
    return user

def recommend_movies(user):
    """
    Crea un objeto Recommender para el usuario y utiliza este objeto para recomendar películas.
    Muestra las recomendaciones en la aplicación Streamlit.
    """
    return user.get_recommendation()

def main():
    st.title("Movie Recommendation System")

    if 'user' in st.session_state:
        st.write(f"UserId: {st.session_state.user.user_id}")
        
        # Add the "Recommend Movies" button at the top right corner
        recommend_button = st.button("Recommend Movies", key="recommend_button")
        
        if recommend_button:
            recommended_movies = recommend_movies(st.session_state.user)
            load_films(recommended_movies)
        else:
            load_films(movies)

    else:
        if 'creating_new_user' in st.session_state:
            new_user_name = st.text_input("Enter your new user name:")
            if new_user_name:
                user = create_user(new_user_name)
                st.session_state.user = user
                st.write(f"{new_user_name}, your id is: {st.session_state.user.user_id}")
                st.session_state.creating_new_user = False
                st.rerun()
        else:
            # user_id = st.text_input("Enter your user id:")
            # Extract unique userIds and add a default option
            user_ids = ratings_df['userId'].unique().tolist()
            user_ids.insert(0, None)

            # Create the select component with the default value
            user_id = st.selectbox('Select User ID', user_ids)

            if user_id:
                st.session_state.user = UserInteraction(user_id)
                st.write(f"UserId: {st.session_state.user.user_id}")
                st.rerun()
            else:
                if st.button("Create New User"):
                    st.session_state.creating_new_user = True
                    st.rerun()

                    # new_user_name = st.text_input("Enter your new user name:")
                    # if new_user_name:
                    #     user = create_user(new_user_name)
                    #     st.session_state.user = user
                    #     st.write(f"{new_user_name}, your id is: {st.session_state.user.user_id}")
                    #     st.session_state.creating_new_user = False
                    #     load_films(movies)
    # if 'user_id' not in st.session_state:
    #     st.session_state.user_id = None

    # if 'creating_new_user' not in st.session_state:
    #     st.session_state.creating_new_user = False

    # if st.session_state.user_id:
    #     st.write(f"UserId: {st.session_state.user_id}")
        
    #     # Add the "Recommend Movies" button at the top right corner
    #     recommend_button = st.button("Recommend Movies", key="recommend_button")
        
    #     if recommend_button:
    #         recommended_movies = recommend_movies(user)
    #         load_films(recommended_movies)
    #     else:
    #         load_films(movies)
    # else:
    #     if st.session_state.creating_new_user:
    #         new_user_name = st.text_input("Enter your new user name:")
    #         if new_user_name:
    #             user = create_user(new_user_name)
    #             st.session_state.user_id = user.user_id
    #             st.write(f"{new_user_name}, your id is: {st.session_state.user_id}")
    #             st.session_state.creating_new_user = False
    #             load_films(movies)
    #     else:
    #         user_id = st.text_input("Enter your user id:")
    #         if user_id:
    #             st.session_state.user_id = user_id
    #             user = UserInteraction(user_id)
    #             st.write(f"UserId: {st.session_state.user_id}")
    #             load_films(movies)
    #         else:
    #             if st.button("Create New User"):
    #                 st.session_state.creating_new_user = True

if __name__ == "__main__":
    main()


# def get_user_input():
#     """
#     Solicita al usuario que introduzca un ID de usuario a través de una barra de búsqueda en la parte superior de la aplicación Streamlit.
#     Si el input no es un número, muestra un error, de lo contario muestra una lista con 10 recomendaciones para el usuario
#     """
#     user = st.text_input("Insert a user")
#     if(user):
#         if(not user.isdigit()):
#             st.error("Input wasn't a correct Id")
#         else:
#             user = int(user)
#             return user

# def recommend_movies(user):
#     """
#     Crea un objeto Recommender para el usuario y utiliza este objeto para recomendar películas.
#     Muestra las recomendaciones en la aplicación Streamlit.
#     """
#     recommender = Recommender(user)
#     st.write(recommender.recommend_movies())

# # Solicita al usuario que introduzca un ID de usuario
# user = get_user_input()

# # Si se ha introducido un ID de usuario, recomienda películas para ese usuario
# if user:
#     recommend_movies(user)

    

