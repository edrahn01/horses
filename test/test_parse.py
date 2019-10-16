import unittest
import parse, charts
import re

def from_file(chart):
    f = open("charts/texts/{chart}.txt", "r")
    txt = f.read()

    return txt

class TestRegistered(unittest.TestCase):
    def test_match(self):
        reg = charts.Registered()

        f = open('test/registered', "r")
        all_registered = f.read().split('\n')

        for line in all_registered:
            file_name, text = line.split(':')

            info = reg.match(text)

            self.assertTrue(info['registered'])
            self.assertIsNotNone(info['registered_state'])
    
#                self.assertEqual(result['registered'], True)
#                self.assertEqual(result['registered_state'], 'NEW MEXICO')
#                self.assertEqual(parse.race, 'FOR FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON')
#
class TestRaceInfo(unittest.TestCase):
    def test_spaces_match(self):
        parse = charts.Info()
        text = 'ALBUQUERQ UE - July 24, 2019 - Race 1'

        info = parse.match(text)

        self.assertEqual(result['track_name'], 'ALBUQUERQUE')
        self.assertEqual(result['track_date'], 'July 24, 2019')
        self.assertEqual(result['track_race_number'], 1)
        self.assertEqual(parse.race, '')

class TestRaceType(unittest.TestCase):
    def test_match(self):
        parse = charts.Type()

        text = 'CLAIMING - Thoroughbred'
        result = parse.match(text)

        self.assertEqual(result['race_type'], 1)
        self.assertEqual(result['race_for'], 'Thoroughbred')

class TestSex(unittest.TestCase):
    def test_match(self):
        parse = charts.Sex()

        text = 'FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON'
        result = parse.match(text)

        self.assertEqual(result['sex'], 0)
        self.assertEqual(parse.race, 'FOR REGISTERED NEW MEXICO BRED THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON')

class TestAge(unittest.TestCase):
    def test_match(self):
        parse = charts.Age()

        text = 'FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON'
        result = parse.match(text)

        self.assertEqual(result['age'], 2)
        self.assertEqual(parse.race, 'FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES WHICH HAVE NOT WON')

class TestRaceDesc(unittest.TestCase):
    def test_match(self):
        parse = charts.Desc()

        text = 'FOR REGISTERED NEW MEXICO BRED THREE YEAR OLDS AND UPWARD WHICH HAVE NEVER WON TWO RACES. Three'

        info = parse.match(text)

        self.assertEqual(info['race_desc'], 'FOR REGISTERED NEW MEXICO BRED THREE YEAR OLDS AND UPWARD WHICH HAVE NEVER WON TWO RACES.')
        self.assertEqual(parse.race, 'Three')

class TestRaceDescFull(unittest.TestCase):
    def test_match(self):
        text = """FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON 
TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES. Three Year Olds, 120 lbs.; Older, 123"""

        parse = charts.Registered()
        info = parse.match(text)
        print(info)
        self.assertEqual(info['registered'], True)
        text = parse.race
        self.assertEqual(text, """FOR FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON 
TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES. Three Year Olds, 120 lbs.; Older, 123""")

        parse = charts.Sex()
        parse.match(text)
        text = parse.race
        self.assertEqual(text, """FOR THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON 
TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES. Three Year Olds, 120 lbs.; Older, 123""")

        parse = charts.Age()
        parse.match(text)
        text = parse.race
        self.assertEqual(text, """FOR WHICH HAVE NOT WON 
TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES. Three Year Olds, 120 lbs.; Older, 123""")

        parse = charts.Desc()
        info = parse.match(text)

        print(info) 
        self.assertEqual(result['race_desc'], 'FOR WHICH HAVE NOT WON TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES.')
        self.assertEqual(parse.race, """Three Year Olds, 120 lbs.; Older, 123""")

class TestWeightInfo(unittest.TestCase):
    def test_match(self):
        text = 'Three Year Olds, 120 lbs.; Older, 123 lbs. Claiming Price $6,250 (Maiden, Claiming, Or Starter Races'

        parse = charts.WeightInfo()
        result = parse.match(text)

        self.assertIn({'desc': 'Three Year Olds', 'weight': '120'}, result['weight_info'])
        self.assertIn({'desc': 'Older', 'weight': '123'}, result['weight_info'])



class LiftRegexCR(unittest.TestCase):
    def test_lift_regex_cr(self):
        text = """FIRST ONE
        SECOND. Hello"""

        r = charts.lift_regex(r'^.*?\.', text, re.M|re.S)

        self.assertEqual(r[1], ' Hello')

class TestDistance(unittest.TestCase):
    def test_match(self):
        for file_name in parse.all_files(what='texts'):
            print(file_name)

            for race in parse.open_text_file(file_name):
                if not race:
                    continue
                try:
                    charts.Info()
                except charts.NoMatch:
                    continue
                if 'Hurdle' in race:
                    continue

                d = charts.Info2()
                try:
                    info = d.match(race)
                except charts.NoMatch:
                    print(race)
                
                print(info)

                self.assertIsNotNone(info['distance'])

        
