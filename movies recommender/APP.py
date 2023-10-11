import streamlit as st
import pickle as pkl
import pandas as pd
import requests


movies1=pkl.load(open('movies.pkl','rb'))
movies=pd.DataFrame(movies1)
similarity=pkl.load(open('similarity.pkl','rb'))


def get_poster(movie_id):
    api_key = '499d6df71f5b7e2273d9de859e153278'

    url=f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=images'
    response=requests.get(url)
    if response.status_code==200:
        movie_data=response.json()
        image1=movie_data.get('poster_path')
        return 'http://image.tmdb.org/t/p/w185'+image1


def recommend(a):
    index=movies[movies['title']==a].index[0]
    #movie_id=movies[movies['title']==a]['movie_id'][0]
    x = (-similarity[index]).argsort()[1:11]
    movie_name = []
    movie_image=[]
    for i in x:
        movie_id = movies.iloc[i]['movie_id']
        movie_name.append(movies.iloc[i]['title'])
        movie_image.append(get_poster(movie_id))
    return movie_name,movie_image


st.title('MOVIE RECOMMENDER')
selected_movie_name=st.selectbox('movie selector',movies['title'].values)
if st.button('recommend'):
    movies,poster=recommend(selected_movie_name)
    col1,col2,col3=st.columns(3)
    for i,j in zip(movies,poster):
        column=col1 if movies.index(i)%3==0 else (col2 if movies.index(i)%3==1 else col3)
        with column:
            st.image(j,use_column_width='auto')
            st.write(i)



