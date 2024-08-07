# Importa las bibliotecas necesarias
import streamlit as st
import pandas as pd
from PIL import Image
from recommender import Recommender

def get_user_input():
    """
    Solicita al usuario que introduzca un ID de usuario a través de una barra de búsqueda en la parte superior de la aplicación Streamlit.
    Si el input no es un número, muestra un error, de lo contario muestra una lista con 10 recomendaciones para el usuario
    """
    user = st.text_input("Insert a user")
    if(user):
        if(not user.isdigit()):
            st.error("Input wasn't a correct Id")
        else:
            user = int(user)
            return user

def recommend_movies(user):
    """
    Crea un objeto Recommender para el usuario y utiliza este objeto para recomendar películas.
    Muestra las recomendaciones en la aplicación Streamlit.
    """
    recommender = Recommender(user)
    st.write(recommender.recommend_movies())

# Solicita al usuario que introduzca un ID de usuario
user = get_user_input()

# Si se ha introducido un ID de usuario, recomienda películas para ese usuario
if user:
    recommend_movies(user)

    
