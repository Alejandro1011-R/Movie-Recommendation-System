import pandas as pd
import numpy as np
from .data_reader import read_data

def build_matrix():
    """
    Crea la matriz híbrida utilizada para calcular las similitudes entre los usuarios y sus preferencias de películas.

    Returns
    -------
    hybrid_matrix : DataFrame
        Un DataFrame que representa las preferencias de los usuarios por diferentes géneros.
    user_movie_matrix : DataFrame
        Un DataFrame que representa las calificaciones de los usuarios para diferentes películas.
    md : DataFrame
        Un DataFrame con las películas y sus géneros, donde los géneros están en una sola columna.
    """
    md_genres, ratings, md = read_data()
    merged = pd.merge(ratings, md_genres, on='movieId')
    merged['rating>3'] = (merged['rating'] > 3).astype(int)

    grouped = merged.groupby(['userId', 'genres'])['rating>3'].sum().reset_index()
    grouped = grouped[grouped['genres'] != '(no genres listed)']

    pivot_table = grouped.pivot(index='userId', columns='genres', values='rating>3').fillna(0)
    total_ratings = pivot_table.sum(axis=1)
    proportions = pivot_table.div(total_ratings, axis=0)

    likes_many_X_movies = pd.DataFrame(0, index=proportions.index, columns=proportions.columns)
    likes_some_X_movies = pd.DataFrame(0, index=proportions.index, columns=proportions.columns)

    for user in proportions.index:
        sorted_genres = proportions.loc[user].sort_values(ascending=False)
        n_genres = len(sorted_genres)
        if n_genres == 0:
            continue
        first_third = int(n_genres / 3)
        second_third = int(2 * n_genres / 3)
        likes_many_X_movies.loc[user, sorted_genres.index[:first_third]] = 1
        likes_some_X_movies.loc[user, sorted_genres.index[first_third:second_third]] = 1

    likes_many_X_movies_prefixed = likes_many_X_movies.add_prefix('likes_many_')
    likes_some_X_movies_prefixed = likes_some_X_movies.add_prefix('likes_some_')
    interleaved_columns = np.array(list(zip(likes_many_X_movies_prefixed.columns, likes_some_X_movies_prefixed.columns))).flatten()
    likes_many_X_movies_prefixed = likes_many_X_movies_prefixed.reindex(columns=interleaved_columns)
    likes_some_X_movies_prefixed = likes_some_X_movies_prefixed.reindex(columns=interleaved_columns)

    hybrid_matrix = pd.DataFrame()

    for col_many, col_some in zip(likes_many_X_movies_prefixed.columns, likes_some_X_movies_prefixed.columns):
        if not likes_many_X_movies_prefixed[col_many].isna().all():
            hybrid_matrix = pd.concat([hybrid_matrix, likes_many_X_movies_prefixed[col_many]], axis=1)
        if not likes_some_X_movies_prefixed[col_some].isna().all():
            hybrid_matrix = pd.concat([hybrid_matrix, likes_some_X_movies_prefixed[col_some]], axis=1)

    user_movie_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    return hybrid_matrix, user_movie_matrix, md
