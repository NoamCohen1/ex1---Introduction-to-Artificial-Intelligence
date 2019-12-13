'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple, Counter
from ways import load_map_from_csv


def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    return {
        'Number of junctions': len(roads),
        'Number of links': len(list(roads.iterlinks())),
        'Outgoing branching factor': Stat(max=max(len(roads[junction].links) for junction in roads),
                                          min=min(len(roads[junction].links) for junction in roads),
                                          avg=len(list(roads.iterlinks())) / len(roads)),
        'Link distance': Stat(max=max(link.distance for link in roads.iterlinks()),
                              min=min(link.distance for link in roads.iterlinks()),
                              avg=sum(link.distance for link in roads.iterlinks()) / len(list(roads.iterlinks()))),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram': Counter(link.highway_type for link in roads.iterlinks()),
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))


if __name__ == '__main__':
    from sys import argv

    assert len(argv) == 1
    print_stats()
