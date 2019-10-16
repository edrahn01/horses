from objects import Session, Track

session = Session()

POINTS_OF_CALL =((0, 3), True, None, None, True, True)
                ((3.25, 4.5), .25, None, None, True, True)
                ((5, 5.25), .1875, .375, None, None, True, True) 
                (5.5, .25, .375, None, None, True, True)
                (6, 7.5), .25, .5, None, None, True, True)
                (8, 9.5), .25, .5, .75, None, True, True)

1 1/4 mi. to 1 3/8 miles 	- 	at 1/4 of a mile 	at 1/2 of a mile 	at 3/4 of a mile 	at 1 mile 	stretch finish
1 7/16 mi to 1 9/16 mi 	- 	at 1/4 of a mile 	at 1/2 of a mile 	at 1 mile 	at 1 1/4 miles 	stretch finish
1 5/8 mi. & 1 11/16 mi. 	- 	at 1/4 of a mile 	at 1/2 of a mile 	at 1 mile 	at 1 3/8 miles 	stretch finish
1 3/4 mi. to 1 7/8 mi. 	- 	at 1/2 of a mile 	at 1 mile 	at 1 1/4 miles 	at 1 1/2 miles 	stretch finish
1 15/16 miles 	- 	at 1/2 of a mile 	at 1 mile 	at 1 3/8 miles 	at 1 5/8 miles 	stretch finish
2 miles to 2 3/16 mi. 	- 	at 1/2 of a mile 	at 1 mile 	at 1 1/2 miles 	at 1 3/4 miles 	stretch finish
2 1/4 mi. to 2 1/2 mi. 	- 	at 1/2 of a mile 	at 1 mile 	at 1 1/2 miles 	at 2 miles 	stretch finish
2 5/8 mi. to 2 3/4 mi. 	- 	at 1/2 of a mile 	at 1 mile 	at 2 miles 	at 2 1/4 miles 	stretch finish
3 miles 	- 	at 1 mile 	at 1 1/2 miles 	at 2 miles 	at 2 1/2 miles 	stretch finish
3 1/4 miles 	- 	at 1 mile 	at 2 miles 	at 2 1/2 miles 	at 2 3/4 miles 	stretch finish
3 1/2 miles 	- 	at 1 mile 	at 2 miles 	at 2 1/2 miles 	at 3 miles 	stretch finish


for track in session.query(Track):
    print(track)
