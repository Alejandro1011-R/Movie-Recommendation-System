import pandas as pd
from matrix_builder import *
from neighbor_finder import *

class Recommender:
    """
    Una clase utilizada para recomendar películas a un usuario basado en sus preferencias y calificaciones.

    Attributes
    ----------
    user_id : int
        El ID del usuario para el cual se generarán recomendaciones.

    Methods
    -------
    recommend_movies()
        Genera una lista de películas recomendadas para el usuario objetivo.
    """

    def __init__(self, user_id):
        """
        Inicializa la clase de recomendaciones con el ID del usuario.

        Parameters
        ----------
        user_id : int
            El ID del usuario para el cual se generarán recomendaciones.
        """
        self.user_id = user_id

    def predict_user_rating(self, ratings, item, neighbors):
        """
        Predice la calificación que un usuario podría dar a una película específica basada en las calificaciones de sus vecinos.

        Parameters
        ----------
        ratings : DataFrame
            Un DataFrame que representa las calificaciones de los usuarios para diferentes películas.
        item : int
            El ID de la película para la cual se quiere predecir la calificación.
        neighbors : list of tuples
            Una lista de tuplas que representan los vecinos más cercanos y sus puntajes de similitud.
        user_id : int
            El ID del usuario para el cual se quiere predecir la calificación.

        Returns
        -------
        float
            La calificación predicha para la película especificada.
        """

        neighbor_ratings = ratings.loc[[n for n, _ in neighbors], item]
        neighbor_avgs = ratings.loc[[n for n, _ in neighbors]].mean(axis=1)
        similarities = pd.Series([sim for _, sim in neighbors], index=[n for n, _ in neighbors])

        valid_neighbors = neighbor_ratings > 0
        if valid_neighbors.any():
            diffs = (neighbor_ratings[valid_neighbors] - neighbor_avgs[valid_neighbors])
            weighted_diffs = diffs.multiply(similarities[valid_neighbors], axis=0)

            numerator = weighted_diffs.sum()
            denominator = similarities[valid_neighbors].abs().sum()

            user_avg = ratings.loc[self.user_id].mean()
            result = user_avg + (numerator / denominator if denominator != 0 else 0)
            return result
        return 0


    def recommend_movies(self,md_genres, rates, md):
        """
        Genera una lista de películas recomendadas para el usuario objetivo.

        Returns
        -------
        DataFrame
            Un DataFrame que contiene las películas recomendadas y sus calificaciones predichas.
        """
        hybrid_matrix, ratings, movies = build_matrix(md_genres, rates, md)
        neighbors = find_neighbors(hybrid_matrix, self.user_id)
        movies = movies[movies['movieId'].isin(ratings.columns)]

        predicted_rating = []
        for movieId in ratings.columns:
            if ratings.loc[self.user_id, movieId] == 0:
                mov = movies[movies['movieId'] == movieId]
                name = mov['title'].values[0]
                genres = mov['genres'].values[0]
                year = mov['year'].values[0]
                rate = round(self.predict_user_rating(ratings, movieId, neighbors), 2)
                predicted_rating.append((movieId, name, genres, year, rate))

        predicted_rating = sorted(predicted_rating, key=lambda x: x[4], reverse=True)
        predicted_rating = [rating for rating in predicted_rating if rating[4] > 3]

        rec = pd.DataFrame(predicted_rating, columns=['movieId', 'name', 'genres', 'year', 'rate'])
        rec = rec.drop('rate', axis=1)
        return rec

    def recommend_movies_for_test(self, test_data, md_genres, rates, md):
        """
        Genera una lista de películas recomendadas para los usuarios de prueba.

        Returns
        -------
        DataFrame
            Un DataFrame que contiene las películas recomendadas y sus calificaciones predichas.
        """
        results = []
        hybrid_matrix, ratings, movies = build_matrix(md_genres, rates, md)


        for user_id in test_data['userId'].unique():
            self.user_id = user_id
            neighbors = find_neighbors(hybrid_matrix, user_id)
            predicted_rating = []
            user_rows = test_data.loc[(test_data['userId'] == user_id)]

            for movieId in user_rows['movieId']:
                rate = round(self.predict_user_rating(ratings, movieId, neighbors), 1)
                if(rate):
                    predicted_rating.append((user_id,movieId, rate))


            results.append(predicted_rating)

        return results
