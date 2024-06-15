import pandas as pd

def read_data():
    """
    Reads the movie and ratings data from CSV files and preprocesses them.

    Returns
    -------
    md_genres : DataFrame
        A DataFrame with movies and their genres, where each genre is a separate row.
    ratings : DataFrame
        A DataFrame with user ratings for movies.
    md : DataFrame
        A DataFrame with movies and their genres, where genres are in a single column.
    """
    md = pd.read_csv('movies.csv')
    md[['title', 'year']] = md['title'].str.extract(r'(.*)\s\((\d{4})\)', expand=True)
    md['genres'] = md['genres'].str.split('|')
    ratings = pd.read_csv('ratings.csv')
    md_genres = md.explode('genres')

    return md_genres, ratings, md
