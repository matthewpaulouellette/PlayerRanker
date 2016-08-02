'''
Created on Aug 1, 2016

@author: Matt
'''
import json

from myql import MYQL
from yahoo_oauth import OAuth1


DEBUG = True 

def pp_json(input_json):
    print ( json.dumps(input_json, indent=4) )
    
def json_to_file(filename, data):
    with open('../Outputs/'+filename+'.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 4)

# Create/get yahoo auth
oauth = OAuth1(None, None, from_file='../api_credentials.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

yql = MYQL(format='json', oauth=oauth)

# Get league settings (stats)
response = yql.raw_query("select * from fantasysports.leagues.settings where league_key='nhl.l.4138'")
stat_categories = response.json().get('query').get('results').get('league').get('settings').get('stat_categories').get('stats').get('stat')
if DEBUG:
    pp_json ( stat_categories )
json_to_file('stat_categories', stat_categories)

# Get player stats for last year
response = yql.raw_query("select * from fantasysports.players.stats where league_key='nhl.l.4138'")
player_stats = response.json().get('query').get('results').get('player')
print (len(player_stats))
if DEBUG:
    pp_json ( player_stats )
json_to_file('player_stats', player_stats)

