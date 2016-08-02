'''
Created on Aug 1, 2016

@author: Matt
'''

import json, os, time

from bs4 import BeautifulSoup
import mechanize


DEBUG = True
TOP_PLAYERS_PER_CAT = 200

PLAYER_FILE = '../Outputs/players.json'
CREDENTIALS_FILE = '../scraper_credentials.json'

YEARS = [ '2015', '2014', '2013' ]
SORT_COLUMNS = {    'AR': 'Rank', 
                    '5': 'PIM',
                    '11': 'SHP',
                    '16': 'Face-offs',
                    '31': 'Hits',
                    '32': 'Blocks',
                    '4': 'Plus/Minus',
                    '8': 'PPP',
                    '14': 'Shots',
                    'OR': 'O-Rank'}

username = ''
password = ''

start_time = time.time()

if os.path.isfile(CREDENTIALS_FILE):
    print 'Login credentials found.'
    with open(CREDENTIALS_FILE) as data_file:    
        d = json.load(data_file)
        username = d.get('username')
        password = d.get('password')
else:
    print 'No login credentials found.'
    d = {}
    username = raw_input('Please enter Yahoo username: ')
    password = raw_input('Please enter Yahoo password: ')
    d['username'] = username
    d['password'] = password
    
    with open(CREDENTIALS_FILE,'w') as data_file:    
        data_file.write(json.dumps(d))
        print 'Yahoo login credentials saved for future use.'
    
print 'Authenticating to Yahoo server as \'%s\'' % username
cookies = mechanize.CookieJar()
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
br.set_cookiejar(cookies)
br.open("https://login.yahoo.com/config/login_verify2?&.src=ym&.intl=ca")
br.select_form(nr=0)
br.form["username"] = username
br.submit()
br.select_form(nr=0)
br.form["passwd"] = password
br.submit()
print 'Successfully logged in.'
print ''

players = {}

for year in YEARS:
    print 'Polling data for year %s' % year
    for sort in SORT_COLUMNS.keys():
        print '\tCollecting data for top %s players in category \'%s\'' % (TOP_PLAYERS_PER_CAT, SORT_COLUMNS.get(sort))
        page = 0
        while page < TOP_PLAYERS_PER_CAT:
            paging_url = '' if page is 0 else '&count=' + str(page)
            print '\t\tProcessing players %s to %s' % ( page, page+25 )
            page += 25
            url = 'https://hockey.fantasysports.yahoo.com/hockey/4138/players?status=ALL&pos=P&cut_type=33&stat1=S_S_{{YEAR}}&myteam=0&sort={{SORT}}&sdir=1{{PAGE}}'
            url = url.replace('{{YEAR}}', year).replace('{{SORT}}', sort).replace('{{PAGE}}', paging_url)
            soup = BeautifulSoup(br.open(url), 'html5lib')
            
            for row in soup.find('div', {'class': 'players'}).find('tbody').findChildren('tr'):
                d = {}
                cells = row.findChildren('td')
                name = cells[1].findAll('a')[1].contents[0].decode("utf-8")
                if players.get(name) and players.get(name).get(year): continue
                    
                d['name'] = name
                d['team'] = cells[1].findAll('span', {'class': 'Fz-xxs'})[0].string.split(' - ')[0]
                d['positions'] = cells[1].findAll('span', {'class': 'Fz-xxs'})[0].string.split(' - ')[1]
                d['games_played'] = cells[5].find('div').string
                d['orank'] = cells[6].find('div').string
                d['rank'] = cells[7].find('div').string
                d['G'] = cells[10].find('div').string
                d['A'] = cells[11].find('div').string
                d['P'] = cells[12].find('div').string
                d['plus_min'] = cells[13].find('div').string
                d['PIM'] = cells[14].find('div').string
                d['PPP'] = cells[15].find('div').string
                d['SHP'] = cells[16].find('div').string
                d['GWG'] = cells[17].find('div').string
                d['SOG'] = cells[18].find('div').string
                d['FW'] = cells[19].find('div').string
                d['HIT'] = cells[20].find('div').string
                d['BLK'] = cells[21].find('div').string
                
                new_entry = players.get(name) if players.get(name) else {}
                new_entry[year] = d
                players[name] = new_entry
    print 'Data collection finished for %s' % year
    print ''

print 'Data collection and processing finished - it took %s minutes.' % str(round((time.time() - start_time)/60,2))
print 'Statistics found for %s unique players.' % len(players.keys())
with open(PLAYER_FILE, 'w') as outfile:
        json.dump(players, outfile, sort_keys = True, indent = 4)
        print 'Player data saved to %s' % PLAYER_FILE
