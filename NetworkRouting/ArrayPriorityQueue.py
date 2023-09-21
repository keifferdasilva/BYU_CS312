import math

class ArrayPriorityQueue:
    queue = []
    def __init__( self):
        pass

    def __len__(self):
        return len(self.queue)

    def makeQueue(self, nodes): #O(1)
        self.queue = nodes.copy() #getting the nodes list is O(n)
        return self.queue

    def decreaseKey(self, node, newDist): #O(1) distance just changed
        pass

    def deleteMin(self, dist): 
        minDistance = math.inf
        smallestNode = ""
        for node in self.queue: #O(V)
            if dist[node.node_id] < minDistance:
                minDistance = dist[node.node_id]
                smallestNode = node
        if smallestNode != "":
            self.queue.remove(smallestNode)
        return smallestNode

    def insert(self, node): #O(1)
        self.queue.append(node)