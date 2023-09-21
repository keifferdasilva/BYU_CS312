#!/usr/bin/python3


from CS312Graph import *
import time
from ArrayPriorityQueue import *
from HeapPriorityQueue import *


class NetworkRoutingSolver:
    shortestPaths = {}

    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network


    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.dest]
        prev = self.shortestPaths["previous"]
        edge = prev[node]
        if edge == "":
            total_length = float('inf')
        while edge != "":
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.src
            edge = prev[node]
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        dist = {}
        prev = {}
        for node in self.network.nodes: #O(V)
            dist[node.node_id] = math.inf #Space is O(V)
            prev[node] = ""
        dist[self.source] = 0
        if use_heap == False:
            queue = ArrayPriorityQueue()
            queue.makeQueue(self.network.nodes) #O(1 or V) space is O(V)
        elif use_heap == True:
            queue = HeapPriorityQueue()
            queue.makeQueue(self.network.nodes, dist) #O(V log V), space is O(3V)
        while len(queue) > 0: #O(V)
            origin = queue.deleteMin(dist) #O(V) or O(log V)
            if origin == "":
                break
            for neighbor in origin.neighbors: #O(E) which is O(V*3)
                if dist[neighbor.dest.node_id] > dist[origin.node_id] + neighbor.length:
                    dist[neighbor.dest.node_id] = dist[origin.node_id] + neighbor.length
                    prev[neighbor.dest] = neighbor #Space is O(V)
                    queue.decreaseKey(neighbor.dest, dist[origin.node_id] + neighbor.length) #O(1) or O(log V)
        self.shortestPaths = {"distances": dist, "previous": prev}
        t2 = time.time()
        return (t2-t1)