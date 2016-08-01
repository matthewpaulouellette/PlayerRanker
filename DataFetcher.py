'''
Created on Aug 1, 2016

@author: Matt
'''

from yahoo_oauth import OAuth1
from myql import MYQL
from Utils import pp_json

# Create/get yahoo auth
oauth = OAuth1(None, None, from_file='credentials.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

yql = MYQL(format='json', oauth=oauth)

# Get league settings (stats)
response = yql.raw_query("select * from fantasysports.leagues.settings where league_key='nhl.l.4138'")
stat_categories = response.json().get('query').get('results').get('league').get('settings').get('stat_categories').get('stats').get('stat')
pp_json ( stat_categories )

