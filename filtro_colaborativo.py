import pandas as pd
import numpy as np

def agregar_usuario_y_normalizar(ratings_matrix, usuario_nuevo):
    # Convertir el diccionario del usuario nuevo a un DataFrame
    usuario_nuevo_df = pd.DataFrame(usuario).T
    
    # Alinear las columnas con la matriz de ratings original
    usuario_nuevo_df = usuario_nuevo_df.reindex(columns=ratings_matrix.columns).fillna(0)
    
    # Calcular la media de ratings
    avg_ratings = usuario_nuevo_df.mean(axis=1).values
     
    # Normalizar la matriz de ratings
    ratings_usuario_nuevo = usuario_nuevo_df.sub(avg_ratings[0])

    #ratings_matrix_normalized = pd.concat([ratings_matrix_normalized, ratings_usuario_nuevo], ignore_index=True)
    
    return ratings_usuario_nuevo


def recomendacion_knn(idx, ratings_matrix_normalized, ratings_matrix, knn_model, n_recommendations=10):
  if type(idx) is not int:
    ratings_usuario_nuevo = agregar_usuario_y_normalizar(ratings_matrix_normalized, idx)
    distances, indices = knn_model.kneighbors(ratings_usuario_nuevo.values.reshape(1,-1), n_neighbors=n_recommendations + 1)
    peliculas_vistas = usuario.index.tolist()

  else:
    distances, indices = knn_model.kneighbors(ratings_matrix_normalized.loc[idx].values.reshape(1,-1), n_neighbors=n_recommendations + 1)
    peliculas_vistas = ratings_matrix.columns[ratings_matrix.loc[idx].values != 0].tolist()

  distances = distances.flatten()[1:]
  indices = indices.flatten()[1:]
  similar_users = ratings_matrix_normalized.iloc[indices]
  mean_ratings = similar_users.T.dot(distances) / np.sum(distances)
  mean_ratings_df = pd.DataFrame(mean_ratings, index=ratings_matrix_normalized.columns, columns=['mean_rating'])
  # Eliminamos las películas que el usuario ya haya visto
  mean_ratings_df = mean_ratings.drop(peliculas_vistas, axis=0)
  mean_ratings_df = mean_ratings_df.dropna()
  return mean_ratings_df

