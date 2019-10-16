from objects import Session, Race


session = Session()


for race in session.query(Race):
    entry_result = repr(race.entries[0].result)
    marks = entry_result[1:-1].split(' ')

    race_result = repr(race.result)
    marks2 = race_result[1:-1].split(' ')

    if len(marks) != len(marks2):
        print(race.result)
        print(entry_result)
