#!/usr/bin/env python3.5
from __future__ import print_function
from urllib.request import urlopen
import json
import time
import datetime
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

SPREADSHEET_ID = '1EO_tWWy8fNvSZN80x16HAEIwv7fsWQGh8M7yJkWlW8E'
RANGE_NAME = 'Рассылка!A2:C'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=RANGE_NAME).execute()
values = result.get('values', [])
d = {}
if not values:
    print('No data found.')
else:
    for row in values:
        a = [row[0], row[1]]
        try:
            d[row[2]].append(a)
        except:
            d[row[2]] = []
            d[row[2]].append(a)

resp = urlopen('https://tickets.fifa.com/API/WCachedL1/en/Availability/GetAvailabilityForAvaDemmand')
result = resp.read()
strres = result.decode("utf-8")
parsed = json.loads(strres)
data = parsed['Data']
tickets = False

keys = d.keys()
for key in keys:
    text = ''
    array = d.get(key)
    length = len(array)
    for x in range(length):
        tabl = array.pop()
        matches = tabl[0].split(',')
        cats = tabl[1].split(',')
        for i1 in range(len(matches)):
            for j1 in range(len(cats)):
                itog = int(matches[i1]) * 8 - 9 + int(cats[j1])
                if data[itog]['a'] == 1:
                    text = text + 'Match ' + data[itog]['p'] + ' ' + 'cat ' + str(data[itog]['c'] - 13) + ' '
    if text != '':
        try:
            result = urlopen('https://api.telegram.org/bot/sendMessage?chat_id=' + str(key) + '&text=' + text)
            tickets = True
        except:
            print(str(datetime.datetime.now()) + ' билеты есть, но чет не работает')
            tickets = True
if not tickets:
    print(str(datetime.datetime.now()) + ' билетов нет')
#print(data)
