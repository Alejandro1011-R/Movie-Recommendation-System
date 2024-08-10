from recommender import Recommender
from data_reader import read_data
import pandas as pd

class UserInteraction:
    """
    Clase destinada a manejar la interacción del usuario con el sistema de recomendaciones,
    facilitando la evaluación de películas y la obtención de recomendaciones.
    """

    _recommendation_cache = {}  # Cache para guardar las recomendaciones de los usuarios

    def __init__(self, idx=None):
        """
        Inicializa la clase UserInteraction con los datos necesarios y prepara el sistema para un nuevo usuario.

        Parameters
        ----------
        idx : int
            id del usuario.
        """
        self.md_genres, self.ratings, self.md = read_data()
        if not idx:
            self.user_id = int(self.ratings['userId'].max()) + 1  # Asigna un nuevo ID único al usuario.
        else:
            self.user_id = idx
        self.recommender = Recommender(self.user_id)  # Crea una instancia del sistema de recomendaciones.

    def rate_movie(self, movie_id, rating):
        """
        Permite al usuario calificar una película, añadiendo o actualizando esta calificación en el conjunto de datos.

        Parameters
        ----------
        movie_id : int
            El ID de la película que el usuario desea calificar.
        rating : float
            La calificación otorgada por el usuario a la película.
        """
        if ((self.ratings['userId'] == self.user_id) & (self.ratings['movieId'] == movie_id)).any():
            # Actualiza la calificación si el usuario calificó la película
            self.ratings.loc[(self.ratings['userId'] == self.user_id) & (self.ratings['movieId'] == movie_id), 'rating'] = rating
        else:
            # Añade una nueva fila si el usuario no calificó la película
            new_data = pd.DataFrame([[self.user_id, movie_id, rating]], columns=['userId', 'movieId', 'rating'])
            self.ratings = pd.concat([self.ratings, new_data], ignore_index=True)

        # Invalida la cache al usuario calificar una nueva película
        if self.user_id in self._recommendation_cache:
            del self._recommendation_cache[self.user_id]

    def get_recommendation(self):
        """
        Genera y devuelve un DataFrame con las top 10 películas recomendadas para el usuario.

        Returns
        -------
        DataFrame
            Un DataFrame que contiene las top 10 películas recomendadas, incluyendo sus detalles básicos.
        """
        # Verifica si las recomendaciones estan en la cache
        if self.user_id in self._recommendation_cache:
            return self._recommendation_cache[self.user_id]

        # Verifica si el usuario ha calificado alguna película y obtiene recomendaciones basadas en eso.
        if self.user_id in self.ratings['userId'].unique():
            recommendation = self.recommender.recommend_movies(self.md_genres, self.ratings, self.md)
            self._recommendation_cache[self.user_id] = recommendation.head(10)
        else:
            # Si el usuario es completamente nuevo y no tiene calificaciones, devuelve las películas más populares.
            top_movies = self.ratings.groupby('movieId').rating.mean().nlargest(10).index
            top_movie_details = self.md[self.md['movieId'].isin(top_movies)]
            self._recommendation_cache[self.user_id] = top_movie_details

        return self._recommendation_cache[self.user_id]


if __name__ == "__main__":
    user_interaction = UserInteraction("User123")
    print(f'{user_interaction.get_recommendation()}\n')
    user_interaction.rate_movie(1, 5.0)
    user_interaction.rate_movie(1, 3.0)
    user_interaction.rate_movie(1, 4.0)

    recommendations = user_interaction.get_recommendation()
    print("Recomendaciones obtenidas luego de dar rating:")
    print(recommendations)