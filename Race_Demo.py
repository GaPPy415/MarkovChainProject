from random import choices
from data import *

if __name__ == '__main__':
    modify_chain(standard_races_chain)
    modify_chain(street_races_chain)

    print("Welcome to Markov Chain Demo!")
    print("Enter number of laps: ")
    laps = int(input())
    print("Enter type of race: 0 (street) / 1 (standard)")
    race_type = int(input())
    print("Enter starting position: ")
    position = int(input())

    grid = standard_races_chain if race_type == 1 else street_races_chain

    for i in range(laps):
        position = choices(range(1, 21), weights=grid[position - 1])[0]
        print("End of Lap " + str(i + 1) + ": " + str(position))
    print("You won", points[position], "points")
