import csv
import timeit

import matplotlib.pyplot as plt
from Algo import Algorithms
from ways import graph
import sys

roads = graph.load_map_from_csv(filename='israel.csv', start=0, count=sys.maxsize)


def read_from_file(fileName):
    with open(fileName, 'r') as csvFile:
        reader = csv.reader(csvFile)
        sum_time = 0
        for row in reader:
            #start_time = timeit.default_timer()
            path = Algorithms.astar_search(int(row[0]), int(row[1]))
            flons, tolons, flats, tolats = [], [], [], []
            for s, t in zip(path[:-1], path[1:]):
                ps, pt = roads[s], roads[t]
                flons.append(ps.lon)
                tolons.append(pt.lon)
                flats.append(ps.lat)
                tolats.append(pt.lat)
            plt.plot(flons, flats, tolons, tolats, 'g')
            plt.show()
            #end_time = timeit.default_timer()
    csvFile.close()
    #sum_time += (end_time - start_time)
    #print(str(sum_time / 100))

    # x = []
    # y = []
    # with open('results/IDAStarRuns.txt', 'r') as solFile:
    #     reader = csv.reader(solFile)
    #     for row in reader:
    #         x.append(float(row[0]))
    #         y.append(float(row[1]))
    # solFile.close()
    #
    # plt.xlabel('heuristic travel time')
    # plt.ylabel('actual travel time')
    # plt.plot(x, y, 'ro')
    # plt.show()


if __name__ == '__main__':
    read_from_file('problems.csv')