import sys

from csv import DictReader

import parse

from objects import Race, Track, Session, setup_db, RaceEntry, RaceEntryResult



if __name__ == '__main__':
#    setup_db()
    session = Session()

    if 'tracks' in sys.argv:
        with open('tracks.csv') as csvfile:
            rows = DictReader(csvfile)

            for track in rows:
                print(track['name'])
                track_db = Track(name=track['name'],
                        country=track['country'].strip(), 
                        abv=track['abv'].strip())
                session.add(track_db)
                session.commit()

    if 'charts' in sys.argv:
        try:
            files = [sys.argv[2]]
        except IndexError:
            files = parse.all_files()

        for file_name in files:
            races = parse.chart(file_name)
            for race in races:
                track = session.query(Track).filter(Track.name==race['track_name']).one()
                race_db = Race(date=race['date'],
                        race_number=race['race_number'],
                        race_type=race['race_type'],
                        track=track,
                        registered=race['registered_state'],
                        sex=race['sex'],
                        age=race['age'],
                        surface=race['surface'],
                        desc=race['race_desc'],
                        code=race['desc2'],
                        claiming_price=race['claiming_price'],
                        purse=race['purse'],
                        plus=race['purse_plus'],
                        available_money=race['avail_money'],
                        value_of_race=race['value_of_race'],
                        weather=race['weather'],
                        track_speed=race['track_speed'],
                        off_at=race['off_at'])
#                        start=race['start'])
                session.add(race_db)
                session.commit()

                for entry in race['entries']:
                    print(entry)
                    try:
                        horse = Horse(name=entry['horse_name'],
                                country=entry['horse_country'])
                        session.add(horse)
                        session.commit()
                    except:
                        horse = (session.query(Horse)
                                .filter_by(name=entry['horse_name'],
                                    country=entry['horse_country'])
                                .one())
                        print(horse)
                        raise

                    entry_db = RaceEntry(race=race_db,
                            last_raced=entry['last_raced'],
                            track_raced=entry['track_raced'],
                            pgmn=entry['pgm'],
                            horse_name=entry['horse_name'],
                            horse_country=entry['horse_country'],
                            jockey_name=entry['jockey_name'],
                            weight=entry['weight'],
                            m_e=entry['m_e'],
                            pp=entry['pp'])
                    session.add(entry_db)
                    session.commit()

                    entry_result_db = RaceEntryResult(race_entry=entry_db,
                            start=entry['start'])

                    def fill_pos(db_obj, entry, name):
                        if name in entry:
                            setattr(db_obj, '%s_pos'%name, entry[name][0])
                            setattr(db_obj, '%s_behind'%name, entry[name][1])


                    fill_pos(entry_result_db, entry, 'quick') 
                    fill_pos(entry_result_db, entry, 'quart') 
                    fill_pos(entry_result_db, entry, 'quack') 
                    fill_pos(entry_result_db, entry, 'half') 
                    fill_pos(entry_result_db, entry, 'last_quart') 
                    fill_pos(entry_result_db, entry, 'mile') 
                    fill_pos(entry_result_db, entry, 'mile_frth') 
                    fill_pos(entry_result_db, entry, 'str') 
                    fill_pos(entry_result_db, entry, 'fin') 

                    session.add(entry_result_db)
                    session.commit()

