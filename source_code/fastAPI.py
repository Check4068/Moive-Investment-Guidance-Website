import uvicorn
import pandas as pd
from fastapi import FastAPI, Query

app = FastAPI()

similar_data = pd.read_csv('similar_movie_data.csv')
predict_data = pd.read_csv('predicted_data.csv')


def check_success(df):
    df = df['success'].value_counts()
    if not 1 in df:
        return False
    if not 0 in df:
        return True
    return df[1] >= df[0]


@app.get('/')
async def index():
    return {"text": "Hello API Masters"}


@app.get('/similar/{query}')
async def get_npf(query):
    params = query.split('&')
    budget = params[0]
    length = params[1]
    genre = params[2]
    director = params[3]
    company = params[4]
    df = similar_data.loc[(similar_data[budget] == 1) & (similar_data[length] == 1) &
                          (similar_data[genre] == 1) & (similar_data[director] == 1) & (similar_data[company] == 1)]
    df_sorted = df.sort_values('release_year', ascending=False).head(5)
    df_display = df_sorted[['original_title',
                            'popularity', 'success', 'release_year']]
    df_display['success'] = df_display['success'].map(
        lambda s: 'yes' if s == 0 else 'no')

    return df_display


@app.get('/recommend/{query}')
async def get_npa(query):
    params = query.split('&')
    budget = params[0]
    length = params[1]
    genre = params[2]
    director = params[3]
    company = params[4]
    df_pre = predict_data.loc[(similar_data[budget] == 1) & (similar_data[length] == 1) &
                              (similar_data[genre] == 1) & (similar_data[director] == 1) & (similar_data[company] == 1)]
    return df_pre

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
