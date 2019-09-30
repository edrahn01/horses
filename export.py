import sys
import csv
from parse import format_file, open_text_file, all_files, html_file, FileNotExist, text_file
from charts import Desc, Type, Registered, Sex, Age, Info, CommentDesc,Desc2, Info2, Purse, Plus, EntriesHTML, FractionalTime, SplitTimes, FinalTime


if __name__ == '__main__':
    with open(sys.argv[1], "wt") as f:
        writer = csv.writer(f)
        writer.writerow(('track',
            'date',
            'race_number',
            'race_type',
            'race_for',
            'sex',
            'age',
            'race_desc',
            'comment_desc',
            'desc2',
            'distance',
            'surface',
            'purse',
            'purse_plus',
            'fracts',
            'final',
            'Horse',
            'Jockey',
            'Pgm',
            'weight',
            'm_e',
            'pp',
            'start',
            'quart',
            'half',
            'last_quart',
            'str',
            'fin',
            'odds',
            'comments'))

    for file_name in all_files('texts'):
#        file_name = 'charts/texts/IND081719USA.txt' 
        print(file_name)

        chart = format_file(str(file_name))
        races = open_text_file(text_file(chart))

        html_race_num = 0
        for race in races:
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
                try:
                    html_chart = html_file(chart, html_race_num)
                except FileNotExist:
                    print(f"Couldn't find HTML file {chart}-{html_race_num}.html")
                    break

                f = open(html_chart, 'r')
                html_entries = EntriesHTML().match(f.read())

                info = {}
                parsers = [Info(),
                        Type(),
                        Registered(),
                        Sex(),
                        Age(),
                        Desc(),
                        CommentDesc(),
                        Desc2(),
                        Info2(),
                        Purse(),
                        Plus(),
                        FractionalTime(),
                        SplitTimes(),
                        FinalTime()]

                for p in parsers:
                    info.update(p.match(race))
                    race = p.race

                info['entries'] = html_entries

                for entry in info['entries']:
                    del info['entries']
                    print(info)
            except:
                print("Failed parseing")
