from objects import RaceEntry, Session, Race

session = Session()

def get_previous_entry(race_entry):
    entry2 = (session.query(RaceEntry)
            .join(Race)
            .filter(RaceEntry.horse == race_entry.horse)
            .filter(Race.date < race_entry.race.date)).first()

    return entry2

for race in session.query(Race):
    print(race)
    for entry in race.entries:
        print(entry.result)
        print(race.result)

        if entry.result.quick_pos:
            pos = entry.result.quick_pos
