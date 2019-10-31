from objects import Session, RaceEntry, POINT_OF_CALL, POS, Race
from charts import FURLONG_DISTANCE
import copy

from scipy.interpolate import interp1d

    
session = Session()

START = 0
STRETCH = -2
FINAL = -3

POINT_OF_CALL_DIST_MULT = {
            1: None,
            11: (START, .1875, .375, STRETCH, FINAL),
            12: (START, .25, .375, STRETCH, FINAL),
            13: (START, .25, .5, STRETCH, FINAL),
            14: (START, .25, .5, STRETCH, FINAL),
            15: (START, .25, .5, STRETCH, FINAL),
            16: (START, .25, .5, .75, STRETCH, FINAL),
            17: (START, .25, .5, .75, STRETCH, FINAL),
            18: (START, .25, .5, .75, STRETCH, FINAL),
            19: (START, .25, .5, .75, STRETCH, FINAL),
            20: (.25, .5, .75, 1, STRETCH, FINAL),
            21: (START, .25, .5, .75, STRETCH, FINAL),
            22: (.25, .5, 1, 1.25, STRETCH, FINAL),
            23: (START, .25, .5, .75, STRETCH, FINAL),
            24: (.25, .5, 1, 1.375, STRETCH, FINAL),
            25: (START, .25, .5, .75, STRETCH, FINAL),
            26: (.25, .5, .75, 1, STRETCH, FINAL),
            27: (.25, .5, .75, 1, STRETCH, FINAL)}


def running_time(race_entry):
    race = race_entry.race
    DISTANCE = FURLONG_DISTANCE[race.distance]
    poc_dists_mult = POINT_OF_CALL_DIST_MULT[race.distance]
    if poc_dists_mult == None:
#        print("No Distance")
        return None

    # Get winning poc
    i = 1
    x = []
    y = []
    for poc_dist in poc_dists_mult:
        if poc_dist == START:
            for cur_race_entry in race.entries:
                if cur_race_entry.result.fin_pos == 1:
                    start = race_entry.result.start
                    result = start
                    break
        elif poc_dist == STRETCH:
            #TODO - what is stretch for track
            continue
        elif poc_dist == FINAL:
            result = race.result.final_call
            poc_dist = DISTANCE/8
        else:
            attr = "%s_call"%(POINT_OF_CALL[i])
            result = getattr(race.result, attr)
            if result == None:
#                print(f"No POC, {attr}")
                continue

        furlong = poc_dist * 8

        x.append(furlong/DISTANCE)
        y.append(result)

        i+=1

#    print(x, y)
    f = interp1d(x, y, fill_value="extrapolate")

    POS_mult = {}

    for poc_name, dist in POS.items():
        dist_furlong = dist * 8
        dist = dist_furlong/DISTANCE
        if dist >= 1:
            continue

        POS_mult[poc_name] = dist

    POS_mult['fin'] = 1
#    print(POS_mult)

    for poc_name, dist in POS_mult.items():
        # Find dist in RaceEntryResult
        # Get position
        position = {}
        for cur_race_entry in race.entries:
            poc_pos = getattr(cur_race_entry.result, f'{poc_name}_pos')
            if not poc_pos:
                continue

            position[poc_pos] = cur_race_entry

#        print(poc_name, position)
        reversed(sorted(position.keys()))

        behind_total = 0
        behind = 0
        results = {}
        for key in sorted(position.keys()):
            cur_race_entry = position[key]
            if behind == None:
                behind = 0
            behind_total += behind

            feet = behind_total * 8
            dist = dist + (feet/5280)

#            print(key, f(dist))
            behind = getattr(cur_race_entry.result, f'{poc_name}_behind') 
            results[cur_race_entry] = f(dist)

    return results[race_entry]
