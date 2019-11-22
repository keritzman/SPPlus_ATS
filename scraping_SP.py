from bs4 import BeautifulSoup as Soup
import requests
import pandas as pd
from pandas import DataFrame
from os import path
import sqlite3
import numpy as np

# put it in a function
def parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in row.find_all('td')]

def parse_sp_rank(str_in):
    return str_in[0:str_in.find(".")]
    
def parse_wins(str_in):
    return str_in[str_in.rfind("(")+1:str_in.rfind("-")]

def parse_losses(str_in):
    return str_in[str_in.rfind("-")+1:str_in.rfind(")")]
        
def parse_team_name(str_in):
    return str_in[str_in.find(".") + 2 : str_in.rfind("(")-1]

def parse_rating(str_in):
    return str_in[0:str_in.find("(")]

def parse_rank(str_in):
    return str_in[str_in.find("(") + 1 : str_in.find(")")]

def load_sp_week(week, url):
    ffc_response = requests.get(url)
    adp_soup = Soup(ffc_response.text)

    # adp_soup is a nested tag, so call find_all on it
    tables = adp_soup.find_all('table')

    # get the adp table out of it
    sp_table = tables[0]
    rows = sp_table.find_all('tr')

    # call function
    list_of_parsed_rows = [parse_row(row) for row in rows[1:]]

    # put it in a dataframe
    df = DataFrame(list_of_parsed_rows)
    df['week'] = week
    
    if week==1:
        df.columns = ['sp_rank','team','conf','rating','week']
        df['sp_rank'] = [ x[0:x.find(".")] for x in df['sp_rank']]
        df.drop('conf', axis=1, inplace=True)
        
    else:
        if week>2:
            df.columns = ['team', 'rating', 'o_rating', 'd_rating', 'st_rating','week']
        else:
            df.columns = ['team', 'rating', 'o_rating', 'd_rating','week']

        df['sp_rank'] = df['team'].apply(parse_sp_rank)
        df['wins'] = df['team'].apply(parse_wins)
        df['losses'] = df['team'].apply(parse_losses)
        df['team'] = df['team'].apply(parse_team_name)
        df['o_rank'] = df['o_rating'].apply(parse_rank)
        df['o_rating'] = df['o_rating'].apply(parse_rating)
        df['d_rank'] = df['d_rating'].apply(parse_rank)
        df['d_rating'] = df['d_rating'].apply(parse_rating)
        if week>2:
            df['st_rank'] = df['st_rating'].apply(parse_rank)
            df['st_rating'] = df['st_rating'].apply(parse_rating)
        else:
            df['st_rank'] = 0
            df['st_rating'] = np.nan

        float_cols =['rating', 'o_rating','d_rating','st_rating']
        int_cols =['sp_rank', 'wins', 'losses','o_rank','d_rank','st_rank', 'week']
        
        df[float_cols] = df[float_cols].astype(float)
        df[int_cols] = df[int_cols].astype(int)

    df.to_sql("weekly_sp", conn, if_exists='append', index=False)
    


DATA_DIR = '/Users/kr406045/ltcwff/data'

# create connection
conn = sqlite3.connect(path.join(DATA_DIR, 's_and_p.sqlite'))

sp_links = pd.read_csv(path.join(DATA_DIR, 'sp_links.csv'))


[load_sp_week(week,url) for week,url in sp_links[['week','link']].values]







