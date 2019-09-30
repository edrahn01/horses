from objects import RaceEntry, Session

session = Session()

for race_entry in session.query(RaceEntry):
    print(race_entry.race, race_entry)
