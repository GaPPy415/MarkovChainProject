from random import choices
from data import *
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt


if __name__ == '__main__':
    modify_chain(standard_races_chain)
    modify_chain(street_races_chain)

    print("Welcome to Markov Chain Season Demo!")
    print("Simulating 1000 seasons..")
    total_points = 0
    points_list = []
    for season in range(1000):
        total_points = 0
        for x in range(len(season_input)):
            j = season_input[x]
            race_type, laps, position = int(j[0]), int(j[1]), int(j[2])
            start = position

            grid = standard_races_chain if race_type == 1 else street_races_chain

            for i in range(laps):
                position = choices(range(1, 21), weights=grid[position - 1])[0]
            to_add = points[position] if position in points.keys() else 0
            # print("Race ", x+1, ", start position: ", start, " finish position: ", position, " points: ", to_add, sep="")
            total_points += to_add
        points_list.append(total_points)
        # print("Points at end of season: ", total_points, sep='')
    points_list = np.array(points_list)
    mu, sigma = points_list.mean(), points_list.std()
    #s = np.random.normal(mu, sigma, 1000)
    points_list = sorted(points_list)
    points_list = [int(_) for _ in points_list]

    l, r = st.t.interval(0.95, len(points_list) - 1, loc=np.mean(points_list), scale=st.sem(points_list))
    print(f"\n95% Confidence interval\nLeft: {round(float(l), 2)}, Right: {round(float(r), 2)}\n")
    points_list = np.array(points_list)

    quartiles = {1:"First", 2:"Second", 3:"Third"}
    for (k,v) in quartiles.items():
        print(f"{v} quartile: {np.quantile(points_list, 0.25 * k)}")
    print(f"Interquartile range: {np.quantile(points_list, 0.75) - np.quantile(points_list, 0.25)}\n")

    print(f"99th percentile: {np.percentile(points_list, 99)}")

    count, bins, ignored = plt.hist(points_list, 30, density=True)
    plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2)), linewidth=2, color='r')
    plt.show()
    print(f"Max: {points_list.max()}, Min: {points_list.min()}, Mean: {points_list.mean()}, StDev: {round(points_list.std(), 2)}")
