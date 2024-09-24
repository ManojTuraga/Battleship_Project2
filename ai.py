from random import choice

HIT_STATE = False
SUNK_STATE = False
ALL_COORDINATES = []
HIT_COORDINATES = []

def level_one():
    while True:
        rand_col = choice(list("ABCDEFJHIJ"))
        rand_row = choice(range(1, 11))

        if (rand_col, rand_row) not in ALL_COORDINATES:
            ALL_COORDINATES.append( (rand_col, rand_row) )
            return rand_col, rand_row

def level_two():
    previous_coord = None

    if len( HIT_COORDINATES ) > 0:
        previous_coord = HIT_COORDINATES[ -1 ]

    while True:
        if not HIT_STATE or SUNK_STATE:
            rand_col = choice(list("ABCDEFJHIJ"))
            rand_row = choice(range(1, 11))

            if (rand_col, rand_row) not in ALL_COORDINATES:
                ALL_COORDINATES.append( (rand_col, rand_row) )
                return rand_col, rand_row
            
        else:
            coord = transform_coord( previous_coord[ 0 ], previous_coord[ 1 ] )
            if coord == (None, None):
                previous_coord.pop()
                previous_coord = HIT_COORDINATES[-1]
            else:
                return coord


def transform_coord( column, row ):
    columns = list("ABCDEFJHIJ")
    rows = [ str( i ) for i in range(1, 11) ]

    curr_col = columns.index( str( column ) )
    curr_row = rows.index( str( row ) )

    new_coord = ( None, None )

    if curr_col > 0 and (columns[ curr_col - 1 ], int( rows[ curr_row ] )) not in ALL_COORDINATES:
        new_coord = (columns[ curr_col - 1 ], int( rows[ curr_row ] ))

    elif curr_row < len(rows) - 1 and (columns[ curr_col ], int( rows[ curr_row + 1 ] )) not in ALL_COORDINATES:
        new_coord = (columns[ curr_col ], int( rows[ curr_row + 1 ] ))

    elif curr_col < len(columns) - 1 and (columns[ curr_col + 1 ], int(rows[ curr_row ])) not in ALL_COORDINATES:
        new_coord = (columns[ curr_col + 1 ], int(rows[ curr_row ]))

    elif curr_row > 0 and (columns[ curr_col ], int(rows[ curr_row - 1 ])) not in ALL_COORDINATES:
        new_coord = (columns[ curr_col ], int(rows[ curr_row - 1 ]))

    return new_coord


def level_three():
    pass