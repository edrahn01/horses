from objects import Session, Race

session = Session()

for race in session.query(Race):
    for entry in race.entries:
        print(entry.weight)
        print(entry.result)
        print(entry.race.result)
