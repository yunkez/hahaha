from collections import defaultdict
from dijkstra import *
import json
import random
import datetime

class Graph:
    def __init__(self, directional=False):
        self.nodes = set()
        self.edges = defaultdict(set)
        self.distances = {}
        self.directional = directional

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].add(to_node)
        self.distances[(from_node, to_node)] = distance
        if not self.directional:
            self.edges[to_node].add(from_node)
            self.distances[(to_node, from_node)] = distance

def build_graph1():
    with open('bus_stops.json') as f:
        data_nodes = json.load(f)
    with open('bus_routes.json') as f:
        data = json.load(f)

    g = Graph(directional=True)

    for node in data_nodes:
        g.add_node(node['BusStopCode'])

    for i in range(1, len(data)):
        if data[i]['ServiceNo'] == data[i-1]['ServiceNo'] and data[i]['Direction'] == data[i-1]['Direction']:
            g.add_edge(data[i-1]['BusStopCode'], data[i]['BusStopCode'], abs(data[i-1]['Distance']-data[i]['Distance']))
    return g

def build_graph2():
    g = Graph()

    file = open('roadNet-CA.txt', 'r')
    for line in file:
        pair = line.split()
        g.add_node(pair[0])
        g.add_node(pair[1])
        g.add_edge(pair[0], pair[1], 1)

    return g


g = build_graph2()
source = random.choice(list(g.nodes))
print("graph finished")
start = datetime.datetime.now()
print(start)
print(source)
visited, path = dijkstra_heap(g, source)
print(visited)
print(datetime.datetime.now() - start)
