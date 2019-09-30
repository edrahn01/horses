import unittest
import parse_charts
import re

class TestParseRegistered(unittest.TestCase):
    def test_match(self):
        parse = parse_charts.ParseRegistered()
        text = 'FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON'

        result = parse.match(text)

        self.assertEqual(result['registered'], True)
        self.assertEqual(result['registered_state'], 'NEW MEXICO')
        self.assertEqual(parse.race, 'FOR FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON')

class TestParseRaceInfo(unittest.TestCase):
    def test_spaces_match(self):
        parse = parse_charts.ParseInfo()
        text = 'ALBUQUERQ UE - July 24, 2019 - Race 1'

        result = parse.match(text)

        self.assertEqual(result['track_name'], 'ALBUQUERQUE')
        self.assertEqual(result['track_date'], 'July 24, 2019')
        self.assertEqual(result['track_race_number'], 1)
        self.assertEqual(parse.race, '')

class TestParseRaceType(unittest.TestCase):
    def test_match(self):
        parse = parse_charts.ParseType()

        text = 'CLAIMING - Thoroughbred'
        result = parse.match(text)

        self.assertEqual(result['race_type'], 'CLAIMING')
        self.assertEqual(result['race_for'], 'Thoroughbred')

class TestParseSex(unittest.TestCase):
    def test_match(self):
        parse = parse_charts.ParseSex()

        text = 'FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON'
        result = parse.match(text)

        self.assertEqual(result['sex'], 'FILLIES AND MARES')
        self.assertEqual(parse.race, 'FOR REGISTERED NEW MEXICO BRED THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON')

class TestParseAge(unittest.TestCase):
    def test_match(self):
        parse = parse_charts.ParseAge()

        text = 'FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON'
        result = parse.match(text)

        self.assertEqual(result['age'], 'THREE YEAR OLDS AND UPWARD')
        self.assertEqual(parse.race, 'FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES WHICH HAVE NOT WON')

class TestParseRaceDesc(unittest.TestCase):
    def test_match(self):
        parse = parse_charts.ParseDesc()

        text = 'FOR REGISTERED NEW MEXICO BRED THREE YEAR OLDS AND UPWARD WHICH HAVE NEVER WON TWO RACES. Three'

        result = parse.match(text)

        self.assertEqual(result['race_desc'], 'FOR REGISTERED NEW MEXICO BRED THREE YEAR OLDS AND UPWARD WHICH HAVE NEVER WON TWO RACES.')
        self.assertEqual(parse.race, 'Three')

class TestParseRaceDescFull(unittest.TestCase):
    def test_match(self):
        text = """FOR REGISTERED NEW MEXICO BRED FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON 
TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES. Three Year Olds, 120 lbs.; Older, 123"""

        parse = parse_charts.ParseRegistered()
        parse.match(text)
        text = parse.race
        self.assertEqual(text, """FOR FILLIES AND MARES THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON 
TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES. Three Year Olds, 120 lbs.; Older, 123""")

        parse = parse_charts.ParseSex()
        parse.match(text)
        text = parse.race
        self.assertEqual(text, """FOR THREE YEARS OLD AND UPWARD WHICH HAVE NOT WON 
TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES. Three Year Olds, 120 lbs.; Older, 123""")

        parse = parse_charts.ParseAge()
        parse.match(text)
        text = parse.race
        self.assertEqual(text, """FOR WHICH HAVE NOT WON 
TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES. Three Year Olds, 120 lbs.; Older, 123""")

        parse = parse_charts.ParseDesc()
        result = parse.match(text)

        self.assertEqual(result['race_desc'], 'FOR WHICH HAVE NOT WON  TWO RACES SINCE JANUARY 24, 2019 OR WHICH HAVE NEVER WON FOUR RACES.')
        self.assertEqual(parse.race, """Three Year Olds, 120 lbs.; Older, 123""")

class TestParseWeightInfo(unittest.TestCase):
    def test_match(self):
        text = 'Three Year Olds, 120 lbs.; Older, 123 lbs. Claiming Price $6,250 (Maiden, Claiming, Or Starter Races'

        parse = parse_charts.ParseWeightInfo()
        result = parse.match(text)

        self.assertIn({'desc': 'Three Year Olds', 'weight': '120'}, result['weight_info'])
        self.assertIn({'desc': 'Older', 'weight': '123'}, result['weight_info'])



class LiftRegexCR(unittest.TestCase):
    def test_lift_regex_cr(self):
        text = """FIRST ONE
        SECOND. Hello"""

        r = parse_charts.lift_regex(r'^.*?\.', text, re.M|re.S)

        self.assertEqual(r[1], ' Hello')
