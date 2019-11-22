import requests
from pandas import DataFrame
from os import path
import sqlite3
#import json


def get_line(game,provider):
    for one_provider in game:
        if one_provider['provider'] == provider:
            return one_provider['spread']

fc_url = 'https://api.collegefootballdata.com/lines?year=2019&seasonType=regular'

resp = requests.get(fc_url)

df = DataFrame(resp.json())

df = df[['id','homeTeam','awayTeam','lines']]

df['line'] = [get_line(x,'consensus') for x in df['lines']]
df['line'] = df['line'].astype(float)


df = df.query('line.notnull()',engine='python')[['id','homeTeam','awayTeam','line']]
df=df.set_index('id')

df.head()

DATA_DIR = '/Users/kr406045/ltcwff/data'

# create connection
conn = sqlite3.connect(path.join(DATA_DIR, 's_and_p.sqlite'))

df.to_sql("lines", conn, if_exists='replace', index=True)

