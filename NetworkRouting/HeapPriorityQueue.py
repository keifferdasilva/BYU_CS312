import math

class HeapPriorityQueue:
    heap = []
    pointers = {}
    distances = {}
    def __init__( self):
        pass

    def __len__(self):
        return len(self.heap)

    def makeQueue(self, nodes, dist): #O(v log v)
        self.distances = dist.copy()
        for node in nodes:
            self.insert(node)
        return self.heap

    def switchNodeWithParent(self, node): #O(log V)
        while True:
            parentIndex = math.floor((self.pointers[node] - 1) / 2)
            if parentIndex >= 0:
                parentNode = self.heap[parentIndex]
            else:
                break
            if self.distances[node.node_id] >= self.distances[parentNode.node_id]:
                break
            else:
                parentIndex = self.pointers[parentNode]
                nodeIndex = self.pointers[node]
                self.heap[parentIndex] = node
                self.heap[nodeIndex] = parentNode
                self.pointers[node] = parentIndex
                self.pointers[parentNode] = nodeIndex
    
    
    def decreaseKey(self, node, newDist):
        if self.pointers.get(node) != None:
            self.distances[node.node_id] = newDist
            self.switchNodeWithParent(node) #O(log V)

    def deleteMin(self, dist):
        minNode = self.heap[0]
        self.pointers.pop(minNode)
        self.heap[0] = self.heap[-1]
        self.heap.pop(-1)
        if len(self.heap) == 0:
            return minNode
        index = 0
        node = self.heap[0]
        self.pointers[node] = 0
        #O(1)
        while True: #O(log V)
            smallestDistance = self.distances[node.node_id]
            if len(self.heap) > (index * 2) + 1:
                firstChild = self.heap[(index * 2) + 1]
            else:
                break
            if len(self.heap) > (index * 2) + 2:
                secondChild = self.heap[(index * 2) + 2]
            else:
                secondChild = ""
            nodeToSwitch = ""
            if(self.distances[firstChild.node_id] < smallestDistance):
                smallestDistance = self.distances[firstChild.node_id]
                nodeToSwitch = firstChild
            if secondChild != "":
                if(self.distances[secondChild.node_id] < smallestDistance):
                    smallestDistance = self.distances[secondChild.node_id]
                    nodeToSwitch = secondChild
            if nodeToSwitch != "":
                parentIndex = self.pointers[node]
                childIndex = self.pointers[nodeToSwitch]
                self.heap[parentIndex] = nodeToSwitch
                self.heap[childIndex] = node
                self.pointers[node] = childIndex
                self.pointers[nodeToSwitch] = parentIndex
            else:
                break
            index = self.pointers[node]
        return minNode


    def insert(self, node): #O(log V)
        self.heap.append(node)
        self.pointers[node] = len(self.heap) - 1
        if len(self.heap) > 1:
            self.switchNodeWithParent(node) #O(log V)
