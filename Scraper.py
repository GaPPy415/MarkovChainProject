from functools import reduce
from data import scrape_input as races
import requests
from bs4 import BeautifulSoup


def update(grid, pos, ra):
    for i in range(1, len(pos)):
        grid[pos[i - 1] - 1][pos[i] - 1] += 1
    # print("update after ", ra)
    # for i in grid:
    #     print(i)


if __name__ == '__main__':

    street_races = {"saudi arabia", "australia", "azerbaijan", "monaco", "hungary", "las vegas", "miami", "singapore"}

    streetChain = [[0 for i in range(20)] for j in range(20)]
    stdChain = [[0 for i in range(20)] for j in range(20)]

    for race in races:
        r = requests.get('https://en.mclarenf-1.com/2023/gp/' + races[race] + '/lap_times/239-842/')
        soup = BeautifulSoup(r.content, 'html.parser')
        inputTag = soup.find_all('small')

        for i in inputTag:
            if i.get_text().__contains__("position in the"):
                inputTag.remove(i)

        positions = []
        target = len(inputTag)

        if race == "mexico":
            target = 149
        elif race == "united states":
            target = 154

        for i in range(1, target):
            if inputTag[i - 1].get_text() == "lap":
                positions.append(int(inputTag[i].get_text()[1:]))
        print(race, positions)
        update(streetChain, positions, race) if race in street_races else update(stdChain, positions, race)

    print("Street races chain: ")
    laps = 0
    for i in streetChain:
        print(i, ", ")
        laps += reduce(lambda a, b: a + b, i)
    print("Standard races chain: ")
    for i in stdChain:
        print(i, ",")
        laps += reduce(lambda a, b: a + b, i)
    print("Total sum: ", laps)
