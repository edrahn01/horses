#!/usr/bin/python3

import requests
import random
import time
import re
from datetime import date
import csv
import sys

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}

today = date.today()

cur_year = int(today.strftime('%Y'))
#cur_mon = int(today.strftime('%m'))
#cur_date = int(today.strftime('%d'))

year = cur_year

def get_track(abv):
    with open('tracks.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['abv'] == abv:
                return row

def get_paded_int(_int):
    return "%02i"%(_int)

def get_static_chart(track, current, country):
    mon = get_paded_int(current.month)
    day = get_paded_int(current.day)
    year = current.year

    headers['referrer'] = 'http://www.equibase.com/premium/chartEmb.cfm?track=%s&raceDate=%s/%s/%s&cy=%s'%(track, mon, day, year, country)

    r = requests.get('http://www.equibase.com/static/chart/pdf/%s%s%s%s%s.pdf'%(track, mon, day, str(year)[2:], country), headers=headers)

    if r.status_code == 200:
        f = open('charts/%s%s%s%s%s.pdf'%(track.strip(), mon, day, str(year)[2:], country), 'wb')
        f.write(r.content)
    
    print("%s-%s-%s %s - %s"%(year, mon, day, track, r.status_code))

    sec = random.randrange(2, 5)
    time.sleep(sec)

if 'today' in sys.argv:
    track_abv = sys.argv[2]
    row = get_track(track_abv)
    get_static_chart(row['abv'], today, row['country'])

if 'all' in sys.argv:
    for mon in range(12, 0, -1):
        mon = "%02i"%(mon)
        for day in range(31, 0, -1):
            day = "%02i"%(day)

            try:
                current = date(year, int(mon), int(day))
                mark = date(year, int(mon), int(day))
                mark2 = date(year, int(mon)-1, int(day))
            except ValueError:
                continue

            with open('tracks.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    track = row['abv'].strip()
                    country = row['country']

                    if mark <= today and today >= mark2:
                        get_static_chart(track, current, country)



