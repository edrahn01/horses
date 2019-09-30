import re
from datetime import datetime
from fractions import Fraction

def lift_regex(regex, string, *args):
    m = re.search(regex, string, *args)
    string = re.sub(regex, '', string, 1, *args)

    return m, string

class NoMatch(Exception):
    pass

class Info:
    race = None

    def match(self, race):
        # Track name, date and race number
        m, race = lift_regex(r'^(.*?) \- (.*?) \- Race (\d+)\n', race)
        track_name = None
        if m:
            # Whitespace in tracks
            with open('./tracks.csv', 'r') as csvfile:
                rows = csvfile.read().split('\n')

                for r in rows:
                    if r:
                        r = r.split(',')
                        if r[2].replace(' ', '') == m.group(1).replace(' ', ''):
                            track_name = r[2]


            
            track_date = datetime.strptime(m.group(2), "%B %d, %Y").date()
            track_race_number = int(m.group(3))
        else:
            raise NoMatch
       
        self.race = race

        return {'track_name': track_name, 
                'date': track_date, 
                'race_number': track_race_number}




class Type:
    RACE_TYPE = {'ALLOWANCE OPTIONAL CLAIMING': 0,
            'CLAIMING': 1,
            'MAIDEN CLAIMING': 2,
            'STAKES': 3,
            'STAKE': 3,
            'STARTER ALLOWANCE': 4,
            'MAIDEN SPECIAL WEIGHT': 5,
            'ALLOWANCE': 6,
            'TRIAL': 7,
            'STARTER HANDICAP': 8,
            'MAIDENS': 9,
            }

    def match(self, race):
        # Race type
        m, race = lift_regex(r'(%s) (.*?)\- ([A-Za-z]+)\s*'%('|'.join(self.RACE_TYPE.keys())), race)

        if m:
            race_type = self.RACE_TYPE[m.group(1)]
            stakes_name = m.group(2).strip() or None
            race_for = m.group(3)
        else:
            race_type = None
            race_for = None
            stakes_name = None
#            raise NoMatch

        self.race = race

        return {'race_type': race_type, 'race_for': race_for, 'stakes_name': stakes_name}



class Registered:
    """ Do we really need to differentiate registered and
    registered_state """
    def match(self, race):
        m, race = lift_regex(r' REGISTERED (.*?) BRED', race)
        if m:
            registered = True
            registered_state = m.group(1)
        else:
            registered = False
            registered_state = None

        self.race = race

        return {'registered': registered,
                'registered_state': registered_state}


class Sex:
    SEX = {'FILLIES AND MARES': 0}
    def match(self, race):
        m, race = lift_regex(r' (%s)'%('|'.join(self.SEX.keys())), race)
        if m:
            sex = self.SEX[m.group(1)]
        else:
            sex = None
#            raise NoMatch
        
        self.race = race

        return {'sex': sex}

class Age:
    AGE = { 'TWO YEARS OLD': 0,
            'TWO YEAR OLDS': 0,
            'TWO YEAR OLD': 0,
            'TWO-YEAR-OLDS': 0,
            'TWO-YEAR-OLD': 0,
            'TWO-YEAR-': 0,
            'TWO-YEARS-OLD': 0,
            'THREE YEAR OLDS AND UPWARD': 2,
            'THREE YEARS OLD AND UPWARD': 2,
            'THREE-YEAR-OLDS AND UPWARD': 2,
            'THREE-YEARS-OLD AND UPWARD': 2,
            'THREE-YEAR OLDS AND UPWARD': 2,
            'THREE YEAR OLDS': 1,
            'THREE YEARS OLD': 1,
            'THREE-YEAR-OLD': 1,
            'THREE YEAR OLD': 1,
            'THREE-YEARS-OLD': 1,
            'THREE AND FOUR YEAR OLDS': 3,
            'THREE AND FOUR-YEAR-OLD': 3,
            'THREE YEAR OLDS OR FOUR YEAR OLDS AND UPWARD': 4,
            'THREE, FOUR, AND FIVE YEARS OLD': 5,
            'FOUR YEAR OLDS AND UPWARD': 6,
            'FOUR YEARS OLD AND UPWARD': 6,
            'THREE, FOUR, FIVE, AND SIX YEARS OLD': 7}
            
    def match(self, race):
        AGES = {}
        for k, v in self.AGE.items():
            k = k.replace(' ', '\s+')
            AGES[k] = v
        m, race = lift_regex(r'(%s)'%('|'.join(AGES.keys())), race, re.M)
        if m:
            AGE = re.sub('\s+', ' ', m.group(1))
            age = self.AGE[AGE]
        else:
            age = None
#            raise NoMatch

        self.race = race

        return {'age': age}

class Desc:
    def match(self, race):
        m, race = lift_regex(r'(FOR|A .*?\.) ', race, re.S|re.M)
        if m:
            race_desc = m.group(1)
            race_desc = re.sub(r'\s', ' ', race_desc)

            if race_desc == 'FOR':
                race_desc = None
        else:
            race_desc = None
        
        self.race = race

        return {'race_desc': race_desc}

class WeightInfo:
    def match(self, race):
        info = []
        race = race.replace(';', '')
        while True:
            m, race = lift_regex(r'(.*?), (\d+)[\n ]lbs\. ', race)
            if m:
                info.append({'desc': m.group(1),
                    'weight': m.group(2)})
            else:
                break

        self.race = race
 
        return {'weight_info': info}
    
class ClaimingPrice:
    def match(self, race):
        m, race = lift_regex('Claiming Price \$([0-9,]+)\. ', race)
        if m:
            claiming_price = m.group(1)
        else:
            claiming_price = None

        m, race = lift_regex('Claiming[\n ]Price: \$([0-9,]+)\n', race)

        self.race = race

        return {'claiming_price': claiming_price}


class Desc2:
    def match(self, race):
        m, race = lift_regex(r'\((.{2,10})\) \S*', race)
        if m:
            desc2 = m.group(1)
        else:
            desc2 = None

        self.race = race


        return {'desc2': desc2}

class Info2:
    DISTANCE = {'Five And One Half Furlongs': 0,
            'Six Furlongs': 1,
            'Six And One Half Furlongs': 2,
            'Mile And Seventy Yards': 3,
            'One Mile And Seventy Yards': 4}
    SURFACE = {'Dirt': 0}
    def match(self, race): 
        m, race = lift_regex(r'(%s) On The (%s) Track Record: \((.*?)\)'%('|'.join(self.DISTANCE.keys()), '|'.join(self.SURFACE.keys())), race)
        if m:
            distance = self.DISTANCE[m.group(1)]
            surface = self.SURFACE[m.group(2)]
            track_record = m.group(3)
        else:
            distance = None
            surface = None
            track_record = None

        self.race = race

        return {'distance': distance,
                'surface': surface,
                'track_record': track_record}

        
class BredClaimingPrice:
    def match(self, race):
        m, race = lift_regex(r'^(.*?)\s+Bred Claiming Price \$([0-9,]+)\.\s*', race)

        if m:
            state = m.group(1)
            price = m.group(2)
        else:
            state = None
            price = None


        self.race = race

        return {'bred_claiming_price': price, 
                'bred_claiming_state': state}

class Purse:
    def match(self, race):
        m, race = lift_regex(r'Purse: \$([0-9,]+)\n', race)

        if m:
            purse = m.group(1)
        else:
            purse = None

        self.race = race

        return {'purse': purse}

class Plus:
    def match(self, race):
        info = []
        while True:
            m, race = lift_regex(r'Plus: \$([0-9,]+) (.*?)\n', race)

            if m:
                purse = m.group(1)
                group = m.group(2)

                info.append({'purse': purse, 'group': group})
            else:
                break

        self.race = race
    
        return {'purse_plus': info}

class AvailableMoney:
    def match(self, race):
        m, race = lift_regex(r'Available Money: \$([0-9,]+)\n', race)

        if m:
            money = m.group(1)

        self.race = race

        return {'avail_money': money}

class ValueOfRace:
    def match(self, race):
        m, race = lift_regex(r'Value of Race: (\$[0-9,]+)\s*(.*?)\n(?=Weather)', race, re.S)

        value = {}
        if m:
            value['total'] = m.group(1) 
            vor = m.group(2).replace('\n', ' ')
            for v in re.split(r'\s*,\s+', vor):
                # Propbably a mistake
                v = re.sub(r'\s+\(US.*?\)', '', v)
                try:
                    n, v = v.split(' ')
                    m = re.match(r'^\$([0-9,]+)', v)
                    value[n] = m.group(1)
                except ValueError:
                    n = '1st'
                    v = v

        self.race = race

        return {'value_of_race': value}

class Weather:
    def match(self, race):
        m, race = lift_regex(r'Weather: (.*?) ', race)

        if m:
            weather = m.group(1)

        self.race = race

        return {'weather': weather}

class TrackSpeed:
    def match(self, race):
        m, race = lift_regex(r'Track: (.*?)\n', race)

        if m:
            speed = m.group(1)

        self.race = race

        return {'track_speed': speed}

class OffAt:
    def match(self, race):
        m, race = lift_regex(r'Off at: ([0-9:]+) ', race)

        if m:
            off_at = m.group(1)
            off_at = datetime.strptime(off_at, "%M:%S").time()

        self.race = race

        return {'off_at': off_at}

class Start:
    def match(self, race):
        m, race = lift_regex(r'Start: (.*?)\n', race)

        if m:
            start = m.group(1)

        self.race = race

        return {'start_condition': start}

class Cleanup:
    def match(self, race):
        m, race = lift_regex(r'[<\[/]\n\n', race)
        m, race = lift_regex(r'Video Race Replay\n\n', race)
        m, race = lift_regex(r'^[ ]\n', race)

        self.race = race

        return {}

class FinalTime:
    def match(self, race):
        m, race = lift_regex(r'Final Time: ([0-9:\.]+)\n\n', race)

        if m:
            final_time = m.group(1)
        else:
            final_time = None

        self.race = race
        return {'final_time': final_time}



class LastRaced:
    def match(self, race):
        race = FixFlaw1().fix(race)
        m, race = lift_regex(r'Last Raced\n(.*?)\n\n', race, re.M|re.S)

        tracks = []
        with open('./tracks.csv', 'r') as csvfile:
            rows = csvfile.read().split('\n')
            for row in rows:
                cols = row.split(',')

                tracks.append(cols[0].strip())
        
        last_raced = {}
        if m:
            last_raced_str = m.group(1).split('\n')
            i = 0 
            for info in last_raced_str:
                lr, tr = info.split(' ')

                m = re.match(r'(\d+)(.*?)(\d+)', lr)
                if m:
                    lr = m.groups()
                else:
                    raise NoMatch

                m = re.match(r'(\d+)(%s)(\d+)'%('|'.join(tracks)), tr)

                if m:
                    last_raced[i+1] = {'last_race': lr,
                            'last_track': m.groups()}
                    i+=1 
        else:
            raise NoMatch

        self.race = race

        FixFlaw1().place(race)
        return {'last_raced': last_raced}

class Includes:
    def match(self, race):
        m, race = lift_regex(r'Includes: \$([0-9,]+) (.*?)\n ', race)

        if m:
            includes = m.group(1)
            includes_info = m.group(2)
        else:
            includes = None
            includes_info = None

        self.race = race

        return {'includes': includes, 'includes_info': includes_info}


class CommentDesc:
    def match(self, race):
        m, race = lift_regex('\((.*?)\) ', race)

        if m:
            comment_desc = m.group(1)
        else:
            comment_desc = None

        self.race = race

        return {'comment_desc': comment_desc}


class FixFlaw1:
    flaw = 'Pgm Horse Name (Jockey)\n\n'

    def fix(self, race):
        sign = 'Last Raced\n\n'
        
        pos = race.find(sign)

        if pos != None:
            base = pos+len(sign)
            race = race[:base-1] + race[base+len(self.flaw):]

        return race

    def place(self, race):
        race = self.flaw+race

            

class Entries:
    def match(self, race):
        m, race = lift_regex(r'Pgm Horse Name \(Jockey\)\n(.*?)\n\n(.*?)\n\n', race, re.S)

        entries = {}
        if m:
            pgms = m.group(1)
            pgms = pgms.split('\n')
            entries = []
            for pgm in pgms:
                entries.append({'pgm': pgm})
        
        m, race = lift_regex(r'Wgt M/E PP Start\n\n1/4\n\n1/2\n\nStr\n\nFin\n\n(.*?)\n\n(.*?)\n\n(.*?)\n\n(.*?)\n\n(.*?)\n\n(.*?)\n\n(.*?)\n\n(.*?)\n\n', race, re.S)

        def def_entries(entry_infos, entries, name):
            entry_infos = entry_infos.split('\n')
            for e, i in zip(entries, entry_infos):
                e[name] = i

        if m:
            def_entries(m.group(1), entries, 'weight')
            def_entries(m.group(2), entries, 'quarter')
            def_entries(m.group(3), entries, 'half')
            def_entries(m.group(4), entries, 'str')
            def_entries(m.group(5), entries, 'fin')
            def_entries(m.group(6), entries, 'me')
            def_entries(m.group(7), entries, 'pp')
            def_entries(m.group(8), entries, 'start')

        m, race = lift_regex(r'Odds Comments\n(.*?)\n\n(.*?)\n\n', race, re.S)
        if m:
            def_entries(m.group(1), entries, 'odds')
            def_entries(m.group(2), entries, 'comments')

        self.race = race

        return {'entries': entries}

class FractionalTime:
    def match(self, race):
        m, race = lift_regex(r'Fractional Times: ([0-9.: ]+)\n', race)

        fractional_times = []
        if m:
            for fract in m.group(1).split(' '):
                fractional_times.append(fract)

        self.race = race

        return {'fract_times': fractional_times}

class SplitTimes:
    def match(self, race):
        m, race = lift_regex(r'Split Times:\s*(.*?)\n', race)

        if m:
            split = m.group(1)
            split = split.replace('(', '')
            split = split.replace(')', '')
            split = split.split(' ')

        self.race = race

        return {'split_times': split}

class RunUp:
    def match(self, race):
        m, race = lift_regex(r'Run-Up: ([0-9]+) feet\n\n', race)

        if m:
            run_up = m.group(1)
        else:
            run_up = None

        self.race = race

        return {'run_up': run_up}

class Winner:
    def match(self, race):
        m, race = lift_regex(r"Winner: (.*?), (.*?), by (.*?) out of (.*?), by (.*?). Foaled (.*?) in (.*?).\nBreeder: (.*?).\nWinning Owner: (.*?)\n", race)

        info = {}
        if m:
            info['name'] = m.group(1)
            info['stats'] = m.group(2)
            info['by'] = m.group(3)
            info['out_of'] = m.group(4)
            info['out_of_by'] = m.group(5)
            info['foaled'] = m.group(6)
            info['foaled_in'] = m.group(7)
            info['breeder'] = m.group(8)
            info['owner'] = m.group(9)
        else:
            info = None
        
        self.race = race

        return {'winner': info}

class EntriesHTML:
    def match(self, race):
        # Avoid overflow races, make sure page has Race info on it.
        if not 'Race' in race:
            return {}

        if 'Quarter&#160;Horse' in race:
            print("Quarter Horse")
            return {}

        def cleanup_spaces(text):
            return text.replace('&#160;', ' ')


        found = False
        r = race.split('\n')
        i = 0
        for l in r:
            if 'Odds' in l:
                break

            i += 1

        entries = []
        h = 0
        while True:
            if 'Last&#160;Raced' in race:
                i += 1
                m = re.match(r'<p .*?>(.*?)</p>', r[i])
                
                if m:
                    if m.group(1) == '---':
                        info = {'last_raced': None,
                                'track_raced': None}
                    else:
                        info = {'last_raced': m.group(1)}

                        tr = []
                        for j in range(1, 4):
                            i += 1
                            m = re.match(r'<p .*?>(.*?)</p>', r[i])
                            if m:
                                tr.append(m.group(1))


                        info = {'track_raced': tuple(tr), **info}

                
            if 'Pgm&#160;Horse&#160;Name&#160;(Jockey)' in race:
                i += 1
                m = re.match(r'<p .*?>(.*?)</p>', r[i])

                if m:
                    entries.append({'pgm': m.group(1)})

                i += 1
                m = re.match(r'<p .*?>(.*?)</p>', r[i])

                if m:
                    horse = m.group(1)
                    # I have no idea what this is..
                    if not '&#160;(' in horse:
                        i += 1
                        m = re.match(r'<p .*?>(.*?)</p>', r[i])
                        print(f"Horse skipped by {horse} {m.group(1)}")
                        horse = m.group(1)

                    m = re.search(r'(\([A-Z]+\))', horse)
                    if m:
                        horse = horse.replace(m.group(1), '')
                        entries[h]['horse_country'] = m.group(1)[1:-1]
                    else:
                        entries[h]['horse_country'] = None
                    horse, jockey = horse.split('&#160;(')
                    jockey = jockey[:-1]
                    entries[h]['horse_name'] = cleanup_spaces(horse)
                    entries[h]['jockey_name'] = cleanup_spaces(jockey)
                    
            if 'Wgt&#160;M/E&#160;' in race:
                i += 1
                m = re.match(r'<p .*?>(.*?)</p>', r[i])

                if m:
                    tmp = m.group(1)
                    tmp = cleanup_spaces(tmp)
                    tmp = tmp.split(' ')
                    wght = tmp[0]
                    m_e = ''.join(tmp[1:]).strip()

                    if not m_e:
                        i += 1
                        m = re.match(r'<p .*?>(.*?)</p>', r[i])
                        if m:
                            m_e = m.group(1)
                            if m_e in ['»', '½', '¶']:
                                i += 1
                                m = re.match(r'<p .*?>(.*?)</p>', r[i])
                                if m:
                                    m_e = m.group(1)


                    entries[h]['weight'] = wght
                    entries[h]['m_e'] = m_e

            pp_scrap = None
            if 'PP' in race:
                i += 1
                m = re.match(r'<p .*?>(.*?)</p>', r[i])

                if m:
                    pp_scrap = m.group(1)
                    pp_scrap = cleanup_spaces(pp_scrap)
                    pp_scrap = pp_scrap.split(' ')
                    pp = pp_scrap[0]

                    entries[h]['pp'] = pp


            frth = None
            if 'PP&#160;1/4' in race:
                frth = pp_scrap[1]
            else:
                start = pp_scrap[1]
                entries[h]['start'] = start


            def get_behind(behind):
                if behind:
                    behind = behind.replace('Head', ' 1/2')
                    behind = behind.replace('Neck', ' 1/4')
                    behind = behind.replace('Nose', ' 1/8')
                    return float(sum(Fraction(s) for s in behind.split()))

            def get_position(r, i, name, info):
                i += 1
                pos = None
                behind = None

                if name == 'quart' and frth:
                    ft = 1
                    pos = frth

                    i += 1
                    m = re.match(r'<p .*? class=\"(ft\d+)\">(.*?)</p>', r[i])

                    if m:
                        ft2 = m.group(1)
                        if ft != ft2:
                            behind = cleanup_spaces(m.group(2))
                        else:
                            # They equal the same.... This happens 
                            # when a horse is last and has no one
                            # behind them.
                            i -= 1

                    info[name] = (pos, get_behind(behind))
                else:
                    m = re.match(r'<p .*? class=\"(ft\d+)\">(.*?)</p>', r[i])
                    if m:
                        ft = m.group(1)
                        pos = m.group(2)

                        if pos == '---':
                            pos = None

                        i += 1
                        m = re.match(r'<p .*? class=\"(ft\d+)\">(.*?)</p>', r[i])

                        if m:
                            ft2 = m.group(1)
                            if ft != ft2:
                                behind = cleanup_spaces(m.group(2))
                            else:
                                # They equal the same.... This happens 
                                # when a horse is last and has no one
                                # behind them.
                                i -= 1

                        info[name] = (pos, get_behind(behind))
                    else:
                        raise NoMatch(r[i])

                return i
            
            def find_offset(r, name):
                for l in r:
                    if 'ft00' in l and f"<b>{name}</b>" in l:
                        return True

                return False
                
            if find_offset(r, '3/16'):
                i = get_position(r, i, 'quick', info)
            if find_offset(r, '1/4'):
                i = get_position(r, i, 'quart', info)
            if find_offset(r, '3/8'):
                i = get_position(r, i, 'quack', info)
            if find_offset(r, '1/2'):
                i = get_position(r, i, 'half', info)
            if find_offset(r, '3/4'):
                i = get_position(r, i, 'last_quart', info)
            if find_offset(r, '1m'):
                i = get_position(r, i, 'mile', info)
            if find_offset(r, '11/4'):
                i = get_position(r, i, 'mile_frth', info)
            if find_offset(r, 'Str'):
                i = get_position(r, i, 'str', info)
            if find_offset(r, 'Fin'):
                i = get_position(r, i, 'fin', info)
            
            i += 1
            m = re.match(r'<p .*?>(.*?)</p>', r[i])
            if m:
                tmp = m.group(1)
                tmp = cleanup_spaces(tmp).split(' ')
                odds = tmp[0]
                comments = ' '.join(tmp[1:])

            info['odds'] = odds
            info['comments'] = comments

            entries[h].update(info)
            h += 1

            if 'ft00' in r[i+1]: #or '---' in r[i+1]:
                break

        return entries
