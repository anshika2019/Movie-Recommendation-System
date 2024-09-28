import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=54161dffd63a1518f6bf63ad5fb2d94b')
    data = response.json()
    
    if 'poster_path' in data and data['poster_path']:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"


def recommend(movie):
    movie_ind = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_ind]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_mov = []
    recommended_posters = []
    
    for i in movie_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # Use the correct column name for movie ID
        recommended_mov.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_mov, recommended_posters

# Load data
movie_dct = pickle.load(open('movies_dct.pkl', 'rb'))
movies = pd.DataFrame(movie_dct)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title("Movie Recommendation System")

selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(len(names))  # Create as many columns as there are movies
    
    for idx, (name, poster) in enumerate(zip(names, posters)):
        with cols[idx]:
            st.text(name)
            st.image(poster)

