# makes a grid for scanning x,y coords in a range
# example below: make a grid that is 15 pixels across (x coord)
# by 805 pixels deep (y coord)
# you can save the output to a file typing '> grid.txt' minus the quotes
# at the end of the command

import datetime
print(datetime.time())


def run():
    for x in range(0,15,1):
        for i in range(0,805,1):
            print('(',x,',', i, ")")


run()