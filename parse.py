#!/usr/bin/python

import re
import sys
import csv
import os
from pathlib import Path
from datetime import datetime
from charts import *


def format_file(argv_file):
    paths = argv_file[:-4].split('/')
    chart = paths[-1]

    return chart

def text_file(chart):
    return '/'.join(['charts', 'texts', chart])+'.txt'

def open_text_file(file_name):
    f = open(file_name,  'r')
    t = f.read()
    races = t.split('\x0c')

    return races

class FileNotExist(Exception):
    pass


def html_path(chart=None):
    p = Path('charts')
    if chart:
        return p / 'htmls' / chart
    else:
        return p / 'htmls'

def html_file(chart, num):
    html_file = f'{chart}-{num}.html'
    html_file = html_path(html_file)
    print(html_file)
    if not os.path.exists(html_file):
        raise FileNotExist
    else:
        return html_file

def all_files(what=None):
    if what == None:
        # Get pdf files
        for pdf_file in Path('charts').iterdir():
            if pdf_file == Path('charts/htmls'):
                continue
            if pdf_file == Path('charts/texts'):
                continue
            yield pdf_file

    if what == 'htmls':
        for html_file in (Path('charts') / 'htmls').iterdir():
            yield html_file
    
    if what == 'texts':
        for text_file in (Path('charts') / 'texts').iterdir():
            yield text_file



def chart(file_name):
    print(file_name)
    chart = format_file(str(file_name))
    races = open_text_file(text_file(chart))

    html_race_num = 0
    info = []
    i = 0
    for race in races:
        try:
            html_race_num += 1
            if not race:
                continue
            if 'Thoroughbred' not in race:
                continue
            if 'Hurdle' in race:
                continue
            if len(race) < 4000:
                continue

            try:
                html_chart = html_file(chart, html_race_num)
            except FileNotExist:
                print(f"Couldn't find HTML file {chart}-{html_race_num}.html")
                break

            f = open(html_chart, 'r')
            html_entries = EntriesHTML().match(f.read())

            parsers = [Info(),
                Type(),
                Registered(),
                Sex(),
                Age(),
                Desc(),
                CommentDesc(),
                WeightInfo(),
                ClaimingPrice(),
                Desc2(),
                Info2(),
                BredClaimingPrice(),
                Purse(),
                Plus(),
                AvailableMoney(),
                ValueOfRace(),
                Weather(),
                TrackSpeed(),
                OffAt(),
                Start(),
                Cleanup(),
    #            LastRaced(),
                Includes(),
                FractionalTime(),
                SplitTimes(),
                RunUp(),
    #            Entries(),
                FinalTime(),
                Winner(),

                ]

            race_info = {}
            for parse in parsers:
                race_info.update(parse.match(race))
                race = parse.race

            race_info['entries'] = html_entries

            yield race_info
        except:
            print(f"Failed parseing {file_name}-{i}")
#            raise
        else:
            i += 1

