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
      user_id = self.user_id
      numerator = 0
      denominator = 0
      for neighbor, similarity in neighbors:
          neighbor_rating = ratings.loc[neighbor, item]
          neighbor_avg = ratings.loc[neighbor].mean()
          if neighbor_rating > 0:
              numerator += similarity * (neighbor_rating - neighbor_avg)
              denominator += abs(similarity)
      if denominator == 0:
          return 0
      user_avg = ratings.loc[user_id].mean()
      result = user_avg + (numerator / denominator)
      return result


    def recommend_movies(self):
        """
        Genera una lista de películas recomendadas para el usuario objetivo.

        Returns
        -------
        DataFrame
            Un DataFrame que contiene las películas recomendadas y sus calificaciones predichas.
        """
        hybrid_matrix, ratings, movies = build_matrix()
        neighbors = find_neighbors(hybrid_matrix, self.user_id)
        movies = movies[movies['movieId'].isin(ratings.columns)]

        predicted_rating = []
        for movieId in ratings.columns:
            if ratings.loc[self.user_id, movieId] == 0:
                mov = movies[movies['movieId'] == movieId]
                name = mov['title'].values[0]
                rate = round(self.predict_user_rating(ratings, movieId, neighbors), 2)
                predicted_rating.append((name, rate))

        predicted_rating = sorted(predicted_rating, key=lambda x: x[1], reverse=True)
        predicted_rating = [rating for rating in predicted_rating if rating[1] > 3]

        df = pd.DataFrame(predicted_rating, columns=['Movie', 'Rating'])

        return df[:10]

if __name__ == '__main__':
    example = Recommender(2)
    print(example.recommend_movies())
