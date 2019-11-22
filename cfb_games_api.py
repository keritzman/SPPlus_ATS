import requests
from pandas import DataFrame
from os import path
import sqlite3
#import json

fc_url = 'https://api.collegefootballdata.com/games?year=2019&seasonType=regular'

resp = requests.get(fc_url)

df = DataFrame(resp.json())

df = df[['id','week','neutral_site','home_team','away_team','home_points','away_points']]

df=df.query('home_points.notnull()',engine='python')

int_cols=['week','home_points','away_points']
bool_cols=['neutral_site']

df[int_cols] = df[int_cols].astype(int)
df[bool_cols] = df[bool_cols].astype(bool)

df=df.set_index('id')

df.head()

DATA_DIR = '/Users/kr406045/ltcwff/data'

# create connection
conn = sqlite3.connect(path.join(DATA_DIR, 's_and_p.sqlite'))

df.to_sql("games", conn, if_exists='replace', index=True)

