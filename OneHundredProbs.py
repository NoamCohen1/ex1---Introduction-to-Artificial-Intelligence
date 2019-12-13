import random
import collections
from ways import load_map_from_csv
import csv

'''
The BFS function gets graph, start node and limit and visit nodes
using BFS algorithm
and return target node
input: graph, start node (as int), limit (int)
output: vertex target (as int)
'''
def bfs(graph, start, lim):
    visited, queue = set(), collections.deque([start])
    iter = 0
    vertex = 0
    while queue and iter < lim:
        vertex = queue.popleft()
        visited.add(vertex)
        ver_links = graph[vertex].links
        num_of_links = len(ver_links)
        if num_of_links:
            for i in range (0,num_of_links):
                if ver_links[i].target not in visited:
                    visited.add(ver_links[i].target)
                    queue.append(ver_links[i].target)
        iter +=1
    return graph[vertex].links[0].target

'''
The function create_problems gets road and open csv file
and write to it 100 problems
'''
def create_problems(roads):
    with open('problems.csv', mode='w', newline='') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0,100):
            s_node = random.randint(5,len(roads)-1)
            lim = random.randint(2,100)
            t_node = bfs(roads,s_node,lim)
            file_writer.writerow([str(s_node), str(t_node)])

'''
The main function load map and create problems
'''
if __name__ == '__main__':
    roads = load_map_from_csv()
    create_problems(roads)