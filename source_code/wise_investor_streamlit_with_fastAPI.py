import streamlit as st
import numpy as np
import pandas as pd
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from io import StringIO

url = 'http://127.0.0.1:8000'


def check_success(df):
    df = df['success'].value_counts()
    if not 1 in df:
        return False
    if not 0 in df:
        return True
    return df[1] >= df[0]


st.write("""
# Being a Wise Movie Investor
""")

st.write('Select the properties of the proposed movie')

# select box for budget
budget_list = ('Select from the dropdown list', 'VeryLowBudget', 'LowBudget', 'MedBudget',
               'HighBudget', 'VeryHighBudget')
budget_selected = st.selectbox('Select the budget range', options=list(
    range(len(budget_list))), format_func=lambda x: budget_list[x])
budget = budget_list[budget_selected]

# select box for movie length
length_list = ('Select from the dropdown list', 'ShortMovie',
               'NormalMovie', 'LongMovie')
length_selected = st.selectbox('Select the movie length range', options=list(
    range(len(length_list))), format_func=lambda x: length_list[x])
length = length_list[length_selected]

# select box for movie genre
genre_list = ('Select from the dropdown list', 'Crime',
              'Comedy', 'Action', 'Thriller', 'Documentary', 'Adventure', 'Science Fiction', 'Animation',
              'Family', 'Drama', 'Romance', 'Fantasy', 'War', 'Music', 'Western', 'Mystery', 'History',
              'Horror', 'TV Movie')
genre_selected = st.selectbox('Select the movie genre', options=list(
    range(len(genre_list))), format_func=lambda x: genre_list[x])
genre = genre_list[genre_selected]

# select box for director
director_list = ('Select from the dropdown list', 'Steven Spielberg',
                 'Clint Eastwood', 'Woody Allen', 'Martin Scorsese', 'Ridley Scott', 'Brian De Palma', 'Steven Soderbergh', 'Wes Craven',
                 'Francis Ford Coppola', 'Ron Howard', 'Other Director')
director_selected = st.selectbox('Select the movie director', options=list(
    range(len(director_list))), format_func=lambda x: director_list[x])
director = director_list[director_selected]

# select box for produce company
company_list = ('Select from the dropdown list', 'Universal Pictures',
                'Paramount', 'Columbia Pictures', 'Warner Bros. Pictures', '20th Century Fox', 'New Line Cinema', 'Walt Disney Pictures', 'Touchstone Pictures',
                'Miramax', 'Metro-Goldwyn-Mayer', 'Other Company')
company_selected = st.selectbox('Select the produce company', options=list(
    range(len(company_list))), format_func=lambda x: company_list[x])
company = company_list[company_selected]


if len(budget) != 29 and len(length) != 29 and len(genre) != 29 and len(director) != 29 and len(company) != 29:
    query = url + '/similar/' + budget + '&' + length + \
        '&' + genre + '&' + director + '&' + company
    r = requests.get(query)
    if r.status_code == 200:
        result = str(r.content, 'utf-8')
        stringfied = StringIO(result)
        df_display = pd.read_csv(stringfied)
        if df_display.empty:
            st.write('No similar movies found, please select different parameters')
        else:
            st.write('Similar movies are as follows:')
            st.write(df_display)
    else:
        st.write('No recommendation based on input information')

if len(budget) != 29 and len(length) != 29 and len(genre) != 29 and len(director) != 29 and len(company) != 29:
    query = url + '/recommend/' + budget + '&' + length + \
        '&' + genre + '&' + director + '&' + company
    r = requests.get(query)
    if r.status_code == 200:
        result = str(r.content, 'utf-8')
        stringfied = StringIO(result)
        df_pre = pd.read_csv(stringfied)
        if df_pre.empty:
            st.write(
                'Very few similar movies has been invested before, the movie is not recommended to invest.')
            elif check_success(df_pre):
                st.write('The Movie is recommended to invest.')
            else:
                st.write('The Movie is not recommended to invest.')
