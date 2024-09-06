import numpy as np
import pandas as pd

def calcular_top_items_bayesian(df_final_2):

    df_final_2 = df_final_2.drop(columns=['genres', 'genre_set', 'content'])
    df_final_2 = df_final_2.drop_duplicates()

    mean_rating = df_final_2.groupby('title')['rating'].mean()

    df_stats = pd.DataFrame({
        'movieId': df_final_2.groupby('title')['movieId'].first(),
        'tmdbId': df_final_2.groupby('title')['tmdbId'].first(),
        'imdbId': df_final_2.groupby('title')['imdbId'].first(),
        'year': df_final_2.groupby('title')['year'].first(),
        'mean_rating': mean_rating,
        'num_votos': df_final_2['title'].value_counts()
    })

    m = df_stats['num_votos'].quantile(0.9)
    df_stats = df_stats[df_stats['num_votos'] >= m]
    c = df_stats['mean_rating'].mean()


    df_stats['weighted_rating'] = (df_stats['mean_rating'] * (df_stats['num_votos'] / (df_stats['num_votos'] + m)) +
                                   c * (m / (m + df_stats['num_votos'])))

    top_10_items = df_stats.sort_values(by='weighted_rating', ascending=False).head(10).reset_index()
    # print('Las películas recomendadas son:')
    return top_10_items