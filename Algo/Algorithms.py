import sys
import math
from ways import graph
from Algo import Node, PriorityQueue
from .Node import Node
from .PriorityQueue import PriorityQueue
from ways.info import SPEED_RANGES
from ways import tools

roads = graph.load_map_from_csv(filename='israel.csv', start=0, count=sys.maxsize)


# write the results to a file
def write_to_file(file_name, source, target):
    est_cost = h_idastar(source, target.state)
    file = open(file_name, 'a')
    if file_name == 'results/AStarRuns.txt' or file_name == 'results/IDAStarRuns.txt':
        file.write(str(est_cost) + ',')
    file.write(str(target.path_cost) + '\n')
    file.close()


# compute the distance between to junctions
def h_idastar(source, target):
    return (tools.compute_distance(roads[target].lat, roads[target].lon,
                                   roads[source].lat, roads[source].lon) /
            max(max(SPEED_RANGES)))


# compute the distance between to junctions
def h(link, target):
    return (tools.compute_distance(roads[target].lat, roads[target].lon,
                                   roads[link.target].lat, roads[link.target].lon) /
            max(max(SPEED_RANGES)))


# compute the distance between to junctions
def g(link, target):
    # distance / speed (the higher one) = time
    return (link.distance / 1000) / max(SPEED_RANGES[link.highway_type])


# go over the different links from the node and compute the time to go
# between them, and return a list of all the targets from the node
def expand(node, target, f):
    nodes = []
    for link in roads[node.state].links:
        cost_g_h = node.path_cost + f(link, target)
        cost = node.path_cost + g(link, target)
        nodes.append(Node(link.target, node, None, cost, cost_g_h))
    return nodes


def DFS_contour(node, target, f_limit, f):
    # if the heuristic cost is bigger than the f_limit
    if node.path_cost_g_h > f_limit:
        return None, node.path_cost_g_h
    # if we found the target
    if node.state == target:
        return node, f_limit
    next_f_limit = math.inf
    # go over all the targets from the node
    for child in expand(node, target, f):
        target_node, new_f_limit = DFS_contour(child, target, f_limit, f)
        if target_node:
            return target_node, f_limit
        next_f_limit = min(next_f_limit, new_f_limit)
    return None, next_f_limit


# IDA*
def idastar(file_name, source, target, f):
    f_limit = h_idastar(source, target)
    node = Node(source, None, None, 0, f_limit)
    while True:
        solution_node, f_limit = DFS_contour(node, target, f_limit, f)
        if solution_node:
            #write_to_file(file_name, source, solution_node)
            return solution_node.solution()
        if f_limit == math.inf:
            return None


# for UCS and A*
def best_first_graph_search(file_name, source, target, f):
    node = Node(source)
    frontier = PriorityQueue(lambda n: n.path_cost_g_h)  # Priority Queue
    frontier.append(node)
    closed_list = set()
    while frontier:
        node = frontier.pop()
        if node.state == target:
            #write_to_file(file_name, source, node)
            return node.solution()
        closed_list.add(node.state)
        for child in expand(node, target, f):
            if child.state not in closed_list and child not in frontier:
                frontier.append(child)
            elif child in frontier and child.path_cost_g_h < frontier[child]:
                del frontier[child]
                frontier.append(child)
    return None


# f = g:
def uniform_cost_search(source, target):
    return best_first_graph_search('results/UCSRuns.txt', source, target, f=g)


# f = g + h
def astar_search(source, target):
    return best_first_graph_search('results/AStarRuns.txt', source, target,
                                   f=lambda node, goal: g(node, goal) + h(node, goal))


# f = g + h
def idastar_search(source, target):
    return idastar('results/IDAStarRuns.txt', source, target,
                   f=lambda node, goal: g(node, goal) + h(node, goal))
