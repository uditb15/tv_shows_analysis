import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from analysis.functions import barplot, scatterplot

df = pd.read_csv('data/df.csv')

# App
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title(":blue[TV Show Database]")
st.write('Created by: Udit Bhandari')
URL = "https://www.kaggle.com/datasets/denizbilginn/tv-shows"
st.write("Click Here to View Data: [Kaggle](%s)"%URL)

# sidebar
st.sidebar.header('Choose your Options')
opt1 = st.sidebar.multiselect("Select Genre", df['genre_name'].unique())

opt2 = st.sidebar.selectbox(
    "Select Minimum Seasons", df['number_of_seasons'].sort_values(
        ascending=True).unique()
)

opt3 = st.sidebar.multiselect(
    "Show Status", options=df['status_name'].unique(), default=df['status_name'].unique()
)

opt4 = st.sidebar.slider("Select Minimum Show Rating", np.round(df['vote_average'].min(), 1),
                         np.round(df['vote_average'].max(), 1), 7.0)

opt5 = st.sidebar.multiselect("Select Network",
                              options=df['network_name'].unique().tolist(),
                              default=['Netflix']
                              )

opt6 = st.sidebar.multiselect("Select Languages",
                              options=df.query("spoken_language_name!='No Language'")
                              ['spoken_language_name'].unique().tolist(),
                              default=['English']
                              )

shows = df.query(
    "genre_name==@opt1&number_of_seasons>=@opt2&status_name==@opt3&vote_average>=@opt4&network_name==@opt5&spoken_language_name==@opt6"
    )

genre_count = shows.groupby('genre_name', as_index=False).agg(
    {"show_id": "nunique"}).sort_values(by='show_id', ascending=False)

# metrics
unique_shows = shows['show_id'].nunique()
unique_genres = genre_count['genre_name'].nunique()
avg_rating = np.round(shows['vote_average'].mean(), 1)
avg_votes = np.round(shows['vote_count'].mean(), 0)

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Unique Shows", unique_shows)
col2.metric("Unique Genres", unique_genres)
col3.metric("Average Rating", avg_rating)
col4.metric("Average Number of Votes", avg_votes)

with st.expander(f"Your Selections yielded {shows['show_id'].nunique()} shows. Click here to see raw data"):
    st.dataframe(shows, use_container_width=True)

# Top 20 Shows by Popularity
popularity = shows[['name', 'popularity']].sort_values(by='popularity', 
                                                    ascending=False).drop_duplicates(['name', 'popularity'])[:20]
popularity['popularity'] = popularity['popularity'].round(2)

popularity_bar = px.bar(popularity, x='name', y='popularity', labels='popularity',
                        height=800, width=600, text='popularity', title='Top 20 Shows by Popularity')

popularity_bar.update_layout(
    title=dict(
        font=dict(size=24)
    ),
    xaxis_tickangle=90,
    title_x=0.5,
)
st.plotly_chart(popularity_bar, use_container_width=True)

fig2 = px.box(shows, x='genre_name', y='vote_average',
              title="Avg Rating Distribution by Genre")
fig2.update_traces(width=0.8)
fig2.update_layout(uniformtext_minsize=11, xaxis_tickangle=90, xaxis=dict(tickfont=dict(size=12)), yaxis=dict(tickfont=dict(size=12)), font_family="Times New Roman",
                   xaxis_title="Genre", title={'font': dict(size=22), 'y': 0.9, 'x': 0.5, "xanchor": 'center', 'yanchor': 'top', 'automargin': True}, width=1100, height=600, margin={'t': 5})

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(barplot(genre_count, 'genre_name', 'show_id', 'Number of Shows By Genre',
                    'show_id'), theme="streamlit", use_container_width=True)
with col4:
    col4 = st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

# Networks
networks = shows[['network_name', 'show_id']].groupby('network_name', as_index=False).agg(
    {'show_id': "nunique"}).sort_values(by='show_id', ascending=False)

st.plotly_chart(barplot(networks[:20], x='network_name', y='show_id', text='show_id',
                title="Network Count"), theme="streamlit", use_container_width=True)


# Scatter Plot
scatter = shows[shows['vote_count'] != 0]

st.plotly_chart(scatterplot(scatter, x='vote_count', y='vote_average',
                color='genre_name', title="Number of Votes and Average Rating", xaxis_title='Number of Votes', yaxis_title="Average Rating"), theme="streamlit", use_container_width=True)

languages = shows[['spoken_language_name', 'show_id']].dropna().\
    groupby('spoken_language_name', as_index=False).\
    agg({'show_id': 'nunique'}).rename(columns={'show_id': 'count'}
                                       ).sort_values(by='count', ascending=False)

st.plotly_chart(
    barplot(languages, x='spoken_language_name', y='count',
            title="TV Shows by Language", text='count'),
    use_container_width=True
)

# Strip Plot Showing Rating Distribution by Language
data_filtered = shows[(shows['vote_average'] != 0)
                      & (shows['vote_count'] != 0)]
data = pd.DataFrame(
    data_filtered.groupby('show_id', as_index=False)[['spoken_language_name', 'vote_average']].agg(
        {
            "vote_average": 'mean',
            'spoken_language_name': "unique"
        }
    )
)

data = data.explode("spoken_language_name").sort_values(by='vote_average', ascending=False)
data = pd.merge(data, df[['show_id', 'name']], how='left', on='show_id')

violin = px.violin(data, x='spoken_language_name', 
                   y='vote_average', color='spoken_language_name',
                   box=True, title='Rating Distribution by Language')

violin.update_layout(
    title=dict(
        font=dict(size=24),
        xanchor='center',
        yanchor='top'
    ),
    title_x=0.5
)

st.plotly_chart(
    violin,
    use_container_width=True
)

# histogram of Ratings by Genre
valid_ratings = shows.query('vote_average!=0&vote_count!=0')
hist = px.histogram(valid_ratings, x='vote_average', nbins=20, color='genre_name', height=600, width=1000,
                    title='Rating Distribution by Genre')
hist.update_layout(
    title=dict(
        font=dict(size=24),
        xanchor='center',
        yanchor='top'
        ),
    title_x=0.5,
)
st.plotly_chart(hist, use_container_width=True)
