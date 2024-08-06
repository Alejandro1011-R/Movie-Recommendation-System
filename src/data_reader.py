import pandas as pd

def read_data():
    """
    Lee los datos de películas y calificaciones desde archivos CSV y los preprocesa.

    Returns
    -------
    md_genres : DataFrame
        Un DataFrame con las películas y sus géneros, donde cada género es una fila separada.
    ratings : DataFrame
        Un DataFrame con las calificaciones de los usuarios para las películas.
    md : DataFrame
        Un DataFrame con las películas y sus géneros, donde los géneros están en una sola columna.
    """
    md = pd.read_csv('dataset/movies.csv')
    md[['title', 'year']] = md['title'].str.extract(r'(.*)\s\((\d{4})\)', expand=True)
    md['genres'] = md['genres'].str.split('|')
    ratings = pd.read_csv('dataset/ratings.csv')
    ratings = ratings.drop('timestamp', axis=1)
    md_genres = md.explode('genres')

    return md_genres, ratings, md
