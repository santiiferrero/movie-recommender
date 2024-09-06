## Funciones para determinar la similitud de coseno de películas - Top 10

def similitud_coseno(test, df_vectorizer, cosine_sim):
  index_title = df_vectorizer[df_vectorizer['title'] == test].index[0] ##Index del titulo seleccionado

  ## Consiguiendo las similitudes para el título seleccionado, con respecto al index
  sim_scores = list(enumerate(cosine_sim[index_title]))
  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
  sim_scores = sim_scores[1:11]
  sim_scores_id = [i[0] for i in sim_scores]

  ## Armando el de similaridad de coseno
  df_similarity_cosine = df_vectorizer[['movieId', 'title', 'genres', 'tmdbId']]
  df_similarity_cosine = df_similarity_cosine.iloc[sim_scores_id]
  df_similarity_cosine['similitud_coseno'] = [i[1] for i in sim_scores]
  df_similarity_cosine = df_similarity_cosine.drop(df_similarity_cosine[df_similarity_cosine['title'] == test].index)

  df_similarity_cosine.reset_index(drop=True, inplace=True)

  return df_similarity_cosine.sort_values(by='similitud_coseno', ascending=False)