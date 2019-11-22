import requests
from pandas import DataFrame
from os import path
import sqlite3

fc_url = 'https://api.collegefootballdata.com/teams/fbs?year=2019'

resp = requests.get(fc_url)

df = DataFrame(resp.json())

df = df[['id','school','conference','division']].set_index('id')

df.head()

DATA_DIR = '/Users/kr406045/ltcwff/data'

# create connection
conn = sqlite3.connect(path.join(DATA_DIR, 's_and_p.sqlite'))

df.to_sql("teams", conn, if_exists='replace', index=True)

