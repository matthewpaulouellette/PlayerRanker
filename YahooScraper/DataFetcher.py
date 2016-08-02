'''
Created on Aug 1, 2016

@author: Matt
'''

import csv
import datetime
import json
import os

from bs4 import BeautifulSoup
import mechanize


DEBUG = True
OUT_DIR = '../Outputs/'
CONFIG_FILE = '../scraper_credentials.json'

username = ''
password = ''

if os.path.isfile(CONFIG_FILE):
    print('Login credentials found.')
    with open(CONFIG_FILE) as data_file:    
        d = json.load(data_file)
        username = d.get('username')
        password = d.get('password')
else:
    print('No login credentials found.')
    d = {}
    username = raw_input('Please enter Yahoo username: ')
    password = raw_input('Please enter Yahoo password: ')
    d['username'] = username
    d['password'] = password
    
    with open(CONFIG_FILE,'w') as data_file:    
        data_file.write(json.dumps(d))
        print('Yahoo login credentials saved for future use.')
    
    
    
# Login/Authenticate
print('Authenticating to Yahoo server.')
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
print('Successfully logged in to Yahoo.')

# Start scraping
url = 'https://hockey.fantasysports.yahoo.com/hockey/4138/players?&sort=OR&sdir=1&status=ALL&pos=P&stat1=S_S_2015'                                  
html = br.open(url)
soup = BeautifulSoup(html, 'html5lib')
with open(OUT_DIR+'scraped-page.html', 'w') as outfile:
    outfile.write(soup.prettify('utf-8'))
    
                   
statTable = soup.findAll('table', {'id': 'statTable0'})
print(statTable)         
headers = list()
statTable = list()
values = list()

if getHeaders :
    for th in statTableRaw.find("thead").findChildren('th'):
        headers.append(th.string)
    del headers[16:17]
    statTable.append(headers)

rows = statTableRaw.find("tbody").findChildren('tr')

for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        values.append(cell.string)
    del values[16:17]                                     
    statTable.append(values)
    values = list()
    self.result = statTable

def write_to_csv(self, csvName, writeDate):
    if writeDate:
        csvFile = csvName+datetime.date.today().strftime('%m%d%y')+'.csv'
    else:
        csvFile = csvName+'.csv'
    with open(csvFile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(self.result)