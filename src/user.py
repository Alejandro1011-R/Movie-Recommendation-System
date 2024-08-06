from recommender import Recommender
from data_reader import read_data
import pandas as pd

class UserInteraction:
    """
    Clase destinada a manejar la interacción del usuario con el sistema de recomendaciones,
    facilitando la evaluación de películas y la obtención de recomendaciones.

    Attributes
    ----------
    md_genres : DataFrame
        DataFrame que contiene información sobre los géneros de las películas.
    ratings : DataFrame
        DataFrame que contiene las calificaciones que los usuarios han dado a las películas.
    md : DataFrame
        DataFrame que contiene información detallada de las películas.
    user : str
        Nombre del usuario que está utilizando el sistema.
    user_id : int
        Identificador único del usuario dentro del sistema.
    recommender : Recommender
        Instancia de la clase Recommender que proporciona métodos para generar recomendaciones de películas.

    Methods
    -------
    rate_movie(movie_id, rating)
        Permite al usuario calificar una película, agregando la información al DataFrame de calificaciones.
    get_recommendation()
        Devuelve un DataFrame con las top 10 películas recomendadas para el usuario, listas para ser en la interfaz gráfica.
    """

    def __init__(self, name):
        """
        Inicializa la clase UserInteraction con los datos necesarios y prepara el sistema para un nuevo usuario.

        Parameters
        ----------
        name : str
            Nombre del usuario.
        """
        self.md_genres, self.ratings, self.md = read_data()
        self.user = name
        self.user_id = int(self.ratings['userId'].max()) + 1  # Asigna un nuevo ID único al usuario.
        self.recommender = Recommender(self.user_id)  # Crea una instancia del sistema de recomendaciones.

    def rate_movie(self, movie_id, rating):
        """
        Permite al usuario calificar una película, añadiendo esta calificación al conjunto de datos.

        Parameters
        ----------
        movie_id : int
            El ID de la película que el usuario desea calificar.
        rating : float
            La calificación otorgada por el usuario a la película.
        """
        # Crea un nuevo DataFrame con la nueva calificación y lo concatena con el DataFrame de calificaciones existente.
        new_data = pd.DataFrame([[self.user_id, movie_id, rating]], columns=self.ratings.columns)
        self.ratings = pd.concat([self.ratings, new_data], ignore_index=True)

    def get_recommendation(self):
        """
        Genera y devuelve un DataFrame con las top 10 películas recomendadas para el usuario.

        Returns
        -------
        DataFrame
            Un DataFrame que contiene las top 10 películas recomendadas, incluyendo sus detalles básicos.
        """
        # Verifica si el usuario ha calificado alguna película y obtiene recomendaciones basadas en eso.
        if self.user_id in self.ratings['userId'].unique():
            recommendation = self.recommender.recommend_movies(self.md_genres, self.ratings, self.md)
            return recommendation.head(10)
        else:
            # Si el usuario es completamente nuevo y no tiene calificaciones, devuelve las películas más populares.
            top_movies = self.ratings.groupby('movieId').rating.mean().nlargest(10).index
            top_movie_details = self.md[self.md['movieId'].isin(top_movies)]
            return top_movie_details


if __name__ == "__main__":
    user_interaction = UserInteraction("User123")
    print(f'{user_interaction.get_recommendation()}\n')
    user_interaction.rate_movie(1, 5.0)
    user_interaction.rate_movie(2, 3.0)


    recommendations = user_interaction.get_recommendation()
    print("Recomendaciones obtenidas luego de dar rating:")
    print(recommendations)
