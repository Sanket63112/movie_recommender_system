import time
import streamlit as st
import pickle
import pandas as pd
import requests
import http.client
import json


def fetch_poster(movie_name):
    conn = http.client.HTTPSConnection("imdb-movies-web-series-etc-search.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "5bd8075399msh0af3b0a0396c03bp1d6003jsn13ddeefe90d5",
        'x-rapidapi-host': "imdb-movies-web-series-etc-search.p.rapidapi.com"
    }
    mov_list = movie_name.split(" ")[:]

    movie_var = "".join(mov_list)

    url1 = "/{}.json".format(movie_var)
    print(url1)
    conn.request("GET", url=url1, headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    # print(data)

    d = data['d']
    # q = data['q']
    # v = data['v']
    img = ""
    for items in d:
        img = items['i']['imageUrl']
        break
    return img


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    with st.spinner(text="In progress"):
        time.sleep(3)
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_name = movies.iloc[i[0]].title
        #fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_name))


    return recommended_movies, recommended_movies_posters


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Enter the movie name which you would like to search',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.subheader(names[0])
        st.image(posters[0])
    with col2:
        st.subheader(names[1])
        st.image(posters[1])
    with col3:
        st.subheader(names[2])
        st.image(posters[2])
    with col4:
        st.subheader(names[3])
        st.image(posters[3])
    with col5:
        st.subheader(names[4])
        st.image(posters[4])

st.link_button("Github", "https://docs.streamlit.io/develop/quick-reference/cheat-sheet#display-text")
