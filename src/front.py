import streamlit as st
import pandas as pd
from PIL import Image

# Sample DataFrame
df = pd.DataFrame({
    'movie_title': ['Movie 12', 'Movie 23', 'Movie 31', 'Movie 11', 'Movie 123'],
    'image_path': ['./433459342_433833065975660_5424982865884172125_n.jpg', './433459342_433833065975660_5424982865884172125_n.jpg','./433459342_433833065975660_5424982865884172125_n.jpg', './433459342_433833065975660_5424982865884172125_n.jpg', './433459342_433833065975660_5424982865884172125_n.jpg']
})

def load_films():
    st.write("Loading films...")
    search_query = st.text_input("Search for a movie:")
    if search_query:
        results = df[df['movie_title'].str.contains(search_query, case=False)]
        num_results = len(results)
        rows = (num_results // 3) + (num_results % 3 > 0)
        
        for row in range(rows):
            cols = st.columns(3)
            for col, idx in zip(cols, range(row * 3, min((row + 1) * 3, num_results))):
                movie = results.iloc[idx]
                col.write(movie['movie_title'])
                img = Image.open(movie['image_path'])
                col.image(img, caption=movie['movie_title'], use_column_width=True)
                
                if col.button(f"Rate {movie['movie_title']}", key=f"rate_button_{idx}"):
                    with st.form(key=f"rating_form_{idx}"):
                        rating = st.selectbox(f"Select your rating for {movie['movie_title']}", [1, 2, 3, 4, 5], key=f"rating_select_{idx}")
                        submit_button = st.form_submit_button(label="Save Rating")
                        if submit_button:
                            df.at[idx, 'ratings'] = rating
                            st.write(f"Rating for {movie['movie_title']}: {rating} stars")

def create_user(user_name):
    # Placeholder for creating a new user
    st.write(f"Creating user: {user_name}")
    # Simulate user ID creation
    return user_name + "_id"

def main():
    st.title("Movie Recommendation System")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.user_id:
        st.write(f"UserId: {st.session_state.user_id}")
        load_films()
    else:
        user_name = st.text_input("Enter your user name:")
        if user_name:
            st.session_state.user_id = user_name + "_id"
            st.write(f"UserId: {st.session_state.user_id}")
            load_films()
        else:
            if st.button("Create New User"):
                new_user_name = st.text_input("Enter your new user name:")
                if new_user_name:
                    st.session_state.user_id = create_user(new_user_name)
                    st.write(f"UserId: {st.session_state.user_id}")
                    load_films()

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

    
