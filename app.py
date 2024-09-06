from filtro_colaborativo import recomendacion_knn
from content_based import similitud_coseno
from bayesian import calcular_top_items_bayesian
from sklearn.neighbors import NearestNeighbors
import streamlit as st
import pandas as pd
import gdown
import numpy as np
import requests

# Configurar la página para modo ancho
st.set_page_config(layout="wide")

# Botón de login
#if 'logged_in' not in st.session_state:
#    st.session_state.logged_in = False

# Crear el botón de login en la parte superior
st.markdown("<h1 style='text-align: center;'>🎬 XPERIENCE PLAY 🍿</h1>", unsafe_allow_html=True)

if st.button("Login"):
    # Solicitar al usuario que ingrese un número
    user_number = st.number_input("Please enter your number to login:", min_value=0, step=1)
    
    if user_number > 0:
        st.success(f"Logged in successfully! Your number is {user_number}")
        #st.session_state.logged_in = True
        

# URL directa de la imagen en GitHub
img_url = 'https://raw.githubusercontent.com/santiiferrero/movie-recommender/main/8d7970_9a0ca002a61144d19b6ed5ea34107bab%7Emv2.webp'

# Configura la imagen de fondo usando HTML y CSS
page_bg_img = f'''
<style>
.stApp {{
    background-image: url("{img_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)


# Cargar bases de datos
url_final = 'https://raw.githubusercontent.com/santiiferrero/movie-recommender/main/df_final.csv'
df_final = pd.read_csv(url_final)

url_vectorizer = 'https://raw.githubusercontent.com/santiiferrero/movie-recommender/main/df_vectorizer.csv'
df_vectorizer = pd.read_csv(url_vectorizer)

url_cosine = 'https://drive.google.com/file/d/1tdplDRklLoWigx4V5bDfbU-ZO0r8nZ72/view?usp=drive_link'
output_cosine = 'array.npy'
gdown.download(url_cosine, output_cosine, fuzzy=True, quiet=False)
data = np.load(output_cosine)
cosine = data['arr']


            ##########  MÉTODO BAYESIANO  ##########
##########  DETERMINAMOS LAS PELÍCULAS MÁS POPULARES  ##########

top_10_bayesian_recomendaciones = calcular_top_items_bayesian(df_final)
st.subheader('**MOST POPULAR MOVIES:** ')

## Consiguiendo los posters de las películas más populares
poster_populares = []
tmdbId_bayesian = []
for i, valor in enumerate(top_10_bayesian_recomendaciones['tmdbId'].tolist()):
    api_key = '53881244403c42cb58048b62e1d8fa71'
    url = f'https://api.themoviedb.org/3/movie/{valor}?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        movie_data_1 = response.json()
    else:
        print("Error en la solicitud:", response.status_code)
    poster_url_1 = 'https://image.tmdb.org/t/p/w500' + movie_data_1['poster_path']
    poster_populares.append(poster_url_1)
    tmdbId_bayesian.append(valor)


# Centrar contenido y ajustar el tamaño
img_width = 140  # Tamaño uniforme para las imágenes

# Creamos una fila con varias columnas
cols_bayesian = st.columns(len(poster_populares))

# Iteramos sobre cada película y su respectiva columna
for i, (tmdb_id,url) in enumerate(zip(tmdbId_bayesian, poster_populares)):


    with cols_bayesian[i]:

        # URL del endpoint de videos
        video_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos?api_key={api_key}&language=en-US"

        # Realizar la solicitud GET
        response = requests.get(video_url)
        data = response.json()

        # Obtener el primer tráiler (si está disponible)
        if 'results' in data and len(data['results']) > 0:
            trailer = next((video for video in data['results'] if video['type'] == 'Trailer'), None)
            if trailer:
                trailer_url = f"https://www.youtube.com/watch?v={trailer['key']}"

        st.link_button("Trailer", trailer_url, use_container_width=True)
        st.image(url, width=img_width)
        st.link_button("See more", f"https://www.themoviedb.org/movie/{tmdb_id}", use_container_width=True)
        # st.page_link(trailer_url, label="Trailer", icon="📺")
        

# Línea de separación
st.markdown("---")

# Selectbox para seleccionar películas
df = df_final.groupby('title')['title'].first()
option = st.selectbox("CHOOSE A MOVIE:", df.tolist())
rating = 0
# Mostrar datos de la película seleccionada
if option:
    df_title_tmdbId = df_final.groupby('title')['tmdbId'].first().reset_index()
    api_key = '53881244403c42cb58048b62e1d8fa71'
    tmdb_id = df_title_tmdbId[df_title_tmdbId['title'] == f"{option}"]['tmdbId'].tolist()[0]
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        movie_data = response.json()

        col1, col2 = st.columns([1, 3], vertical_alignment="center")

        with col1:
            poster_url = 'https://image.tmdb.org/t/p/w500' + movie_data['poster_path']
            st.image(poster_url, width=200)

        with col2:
            st.link_button(f"**TITLE:** {df_final[df_final['tmdbId'] == tmdb_id]['title'].tolist()[0]}", 
                           f"https://www.themoviedb.org/movie/{tmdb_id}", use_container_width=True)
            st.write(f"**GENRES:** {df_final[df_final['tmdbId'] == tmdb_id]['genres'].tolist()[0]}")
            st.write(f"**OVERVIEW:** {movie_data['overview']}")
            st.write(f"**RELEASE DATE:** {movie_data['release_date']}")
            st.write(f"**DURATION:** {movie_data['runtime']} min")
            st.write(f"**RANKING:** ⭐({movie_data['popularity']})")

        # Añadir la opción de puntuación con estrellas
        st.write("Rate this movie:")
        rating = st.radio("", [1, 2, 3, 4, 5], format_func=lambda x: '⭐' * x, horizontal=True)
        st.write(f"Your rating: {'⭐' * rating}")

    else:
        st.write("Error en la solicitud:", response.status_code)
else:
    st.write('*** Selecciona una película ***')

# Línea de separación
st.markdown("---")


if rating > 3:
                           
              ##########  SIMILITUD DE COSENO  ##########
    ##########  DETERMINAMOS LAS PELÍCULAS RECOMENDADAS  ##########
    
    ## Mostrando la similitud de coseno de la película especifica
    df_similitud_coseno = similitud_coseno(option, df_vectorizer, cosine)
    st.subheader('**WHY YOU LIKED:** ' + option)
    
    ## Consiguiendo los títulos y posters de las películas recomendadas
    poster_recomendadas = []
    tmdbId_coseno = []
    for i, valor in enumerate(df_similitud_coseno['tmdbId'].tolist()):
        api_key = '53881244403c42cb58048b62e1d8fa71'
        url = f'https://api.themoviedb.org/3/movie/{valor}?api_key={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            movie_data_2 = response.json()
        else:
            print("Error en la solicitud:", response.status_code)
        poster_url_2 = 'https://image.tmdb.org/t/p/w500' + movie_data_2['poster_path']
        poster_recomendadas.append(poster_url_2)
        tmdbId_coseno.append(valor)
    
    # Centrar contenido y ajustar el tamaño
    img_width = 140  # Tamaño uniforme para las imágenes
    
    # Creamos una fila con varias columnas
    cols_cosine = st.columns(len(poster_recomendadas))
    
    # Iteramos sobre cada película y su respectiva columna
    for i, (tmdb_id, url) in enumerate(zip(tmdbId_coseno, poster_recomendadas)):
    
        # URL del endpoint de videos
        video_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos?api_key={api_key}&language=en-US"
    
        # Realizar la solicitud GET
        response = requests.get(video_url)
        data = response.json()
    
        # Obtener el primer tráiler (si está disponible)
        if 'results' in data and len(data['results']) > 0:
            trailer = next((video for video in data['results'] if video['type'] == 'Trailer'), None)
            if trailer:
                trailer_url = f"https://www.youtube.com/watch?v={trailer['key']}"
    
        with cols_cosine[i]:
            st.link_button("Trailer", trailer_url, use_container_width=True)
            st.image(url, width=img_width)
            st.link_button("See more", f"https://www.themoviedb.org/movie/{tmdb_id}", use_container_width=True)
    
            # if st.button('Ver más', key=f'ver_mas_{i+10}', use_container_width=True):
            #     st.write(f'Detalles de {url}')


#if st.session_state.logged_in:
#    st.subheader('**User:** ' + user_number)
    #FILTRO COLABORATIVO


##########  DETERMINAMOS LAS PELÍCULAS RECOMENDADAS  POR FILTRO COLABORATIVO##########
df = df_final.groupby('userId')['userId'].first()
user_number = st.selectbox(
    "Escoge un usuario:", df.tolist())

if user_number:    
    st.subheader('**Películas Recomendadas Por Filtro Colaborativo:** ')
    
    ratings_matrix = df_final.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    avg_ratings = ratings_matrix.mean(axis=1)
    ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0)
    
    knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
    knn_model.fit(ratings_matrix_normalized.values)
    
    recomendaciones = recomendacion_knn(user_number, ratings_matrix_normalized, ratings_matrix, knn_model)
    df_filtro_col = recomendaciones.sort_values(ascending=False).reset_index().head(10)
    
    
    df_filtrado = df_final[df_final['movieId'].isin(df_filtro_col['movieId'])][['movieId','title','tmdbId']].drop_duplicates()
    
    
    ## Consiguiendo los títulos y posters de las películas recomendadas
    original_title = []
    poster_recomendadas = []
    for i, valor in enumerate(df_filtrado['tmdbId'].values.tolist()):
        api_key = '53881244403c42cb58048b62e1d8fa71'
        url = f'https://api.themoviedb.org/3/movie/{valor}?api_key={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            movie_data_2 = response.json()
            poster_url_2 = 'https://image.tmdb.org/t/p/w500' + movie_data_2['poster_path']
            original_title.append(movie_data_2['original_title'])
            poster_recomendadas.append(poster_url_2)
        else:
            print("Error en la solicitud:", response.status_code)
    
    
    # Primera fila de 5 columnas
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    # Centrar contenido y ajustar el tamaño
    img_width = 140  # Tamaño uniforme para las imágenes
    
    with col1:
        with st.container():
            st.markdown(f"<h4 style='text-align: center; font-size: 16px;'>{original_title[0]}</h4>", unsafe_allow_html=True)
            st.image(poster_recomendadas[0], width=img_width)
    
    with col2:
        with st.container():
            st.markdown(f"<h4 style='text-align: center; font-size: 16px;'>{original_title[1]}</h4>", unsafe_allow_html=True)
            st.image(poster_recomendadas[1], width=img_width)
    
    with col3:
        with st.container():
            st.markdown(f"<h4 style='text-align: center; font-size: 16px;'>{original_title[2]}</h4>", unsafe_allow_html=True)
            st.image(poster_recomendadas[2], width=img_width)
    
    with col4:
        with st.container():
            st.markdown(f"<h4 style='text-align: center; font-size: 16px;'>{original_title[3]}</h4>", unsafe_allow_html=True)
            st.image(poster_recomendadas[3], width=img_width)
    
    with col5:
        with st.container():
            st.markdown(f"<h4 style='text-align: center; font-size: 16px;'>{original_title[4]}</h4>", unsafe_allow_html=True)
            st.image(poster_recomendadas[4], width=img_width)


    
