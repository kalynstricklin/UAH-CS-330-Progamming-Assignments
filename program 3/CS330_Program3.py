#
# Project: CS 330
# Program Assignment 3: A* Pathfinding Algorithm
# Purpose: Example of A* Implementation
# Author: Kalyn Stricklin
# Created: 2023-10-22
#


import numpy as np
import math
# initalize constansts used by pathfinding algorithms

INFINITY = float("inf")
UNDEFINED = 0
UNVISITED = 1
OPEN = 2
CLOSED = 3

#initalize
STATUS = 3      # Status of node; UNVISITED, OPEN, or CLOSED
COSTSOFAR = 4   # Cost of shortest path found so far to this node
HEURISTIC = 5   #Estimated heuristic cost
TOTAL = 6       # Estimated total cost
PREVIOUS = 7    # Previous node in path from start to this node
LOC_X = 8       # Location (position) x coordinate    
LOC_Z = 9       # Location (position) z coordinate     

# initialize constants used for graph connections data structure
CONNECTION_NUM = 2 
FROM_NODE = 3   # connection from node number
TO_NODE = 4     # connection to node number
COST = 5        # connection cost

class NodeRecord:
    def __init__(self, fromNode, toNode, cost):
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost
class Node:
    def __init__(self, node_number, status, costsofar, heuristic, total, previous, x, z):
        self.node_number = node_number
        self.status = status
        self.costsofar = costsofar
        self.heuristic = heuristic
        self.total = total
        self.previous = previous
        self.x = x
        self.z = z

    def __str__(self):
        return f'{self.node_number}, {self.status}, {self.costsofar}, {self.heuristic}, {self.total}, {self.previous}, {self.x}, {self.z}'

class Graph:
    def __init__(self):
        self.nodes = {} #list of nodes
        self.connections = {} #list
    
    def addConnections(self, connectionNum, fromNode, toNode, cost):
        self.connections[connectionNum]= NodeRecord(fromNode,toNode,cost)
    
    def getNeighbors(self, nodeId):
        neighbors =[]
        for fromNode, toNode, cost in self.connections:
            neighbors.append([toNode,fromNode,cost])
        return neighbors

#def lowest(graph, openNodes):
#    total = min(graph.nodes[node]['total'] for node in openNodes) #determine the lowest total cost of all opens  nodes
#    result_index = np.where(graph.nodes[openNodes]['total'] == total) #find indexes of all opens nodes with lowest total cost
#    result = openNodes(min(result_index[0])) #find node number of lowest total cost opennodes with lowesr index
#    return result
def lowest(graph, openNodes):
    min_total = float('inf')
    min_node = None

    for node in openNodes:
        current_total = graph.nodes[node]['total']
        if current_total < min_total:
            min_total = current_total
            min_node = node

    return min_node 
def getHeuristic(graph, node1, node2):  #possible params (graph, node.1, node.2)
    '''Calc the euclidean distance between two points'''
    distance = math.sqrt((graph.nodes[node2]['x'] - graph.nodes[node1]['x'])**2 + (graph.nodes[node2]['z'] - graph.nodes[node1]['z'])**2)
    return distance

#def getConnections(graph,currentNode):
#    result= np.where(graph.connections[:,FROM_NODE] == currentNode)
#    return result
def getConnections(graph, currentNode):
    result = [i for i, connections in graph.connections.items() if connections['fromNode'] == currentNode]
    return result

graph = Graph()
# Reading in a Txt File

with open("CS 330, Pathfinding, Graph AB Connections v3.txt", "r") as f:
    for line in f:
        fields = line.strip().split(",")
        if fields[0] == '"C"':
            CONNECTION_NUM = int(fields[1])
            FROM_NODE = int(fields[2])
            TO_NODE = int(fields[3])
            COST = int(fields[4])

        connections = NodeRecord(FROM_NODE, TO_NODE, COST)
        # Add the connection to the graph
        graph.connections[CONNECTION_NUM] = {
                'fromNode': connections.fromNode,
                'toNode': connections.toNode,
                'cost': connections.cost
            }
       
        #print(f"Read connection: {CONNECTION_NUM}, {FROM_NODE}, {TO_NODE}, {COST}")

# reading a txt file for connections 
with open ("CS 330, Pathfinding, Graph AB Nodes v3.txt", 'r') as f:
    for line in f:
        fields = line.strip().split(",")
        if fields[0] == '"N"':
            NODENUMBER = int(fields[1])
            STATUS = int(fields[2])
            COSTSOFAR = float(fields[3])
            HEURISTIC = float(fields[4])
            TOTAL = float(fields[5])
            PREVIOUS = int(fields[6])
            LOC_X = float(fields[7])
            LOC_Z = float(fields[8])
        
            currentNode = Node(NODENUMBER, STATUS, COSTSOFAR, HEURISTIC, TOTAL, PREVIOUS, LOC_X, LOC_Z)

            graph.nodes[NODENUMBER] = {
                'status': currentNode.status,
                'costsofar': currentNode.costsofar,
                'heuristic': currentNode.heuristic,
                'total': currentNode.total,
                'previous': currentNode.previous,
                'x': currentNode.x,
                'z': currentNode.z
            }
         
#to keep track of nodes
openNodes = set()
closedNodes = set()
visitedNodes = []

def retrievePath(graph, first, last):
    path = []
    current = last
    while current != UNDEFINED:
        path.append(current)
        current = graph.nodes[current]['previous']
    path.reverse()

    if path and path[0] == first:
        return path
    else:
        return path

# find path from start node (first) to goal node (last) using A*

def aStar(graph, first, last):
    
    # initialize node array
    for i in range(1, len(graph.nodes)+1):
        graph.nodes[i]['status'] = UNVISITED
        graph.nodes[i]['costsofar'] = INFINITY
        graph.nodes[i]['previous'] = UNDEFINED     
   
    # initalize start node (first) and show intial status before first iteration
    #print(f'first: {first}, graph.nodes = {graph.nodes}')
    graph.nodes[first]['status']= OPEN
    graph.nodes[first]['costsofar'] = 0
    iteration = 0
    openNodes = [node for node in range(1, len(graph.nodes)) if graph.nodes[node]['status'] == OPEN]
    #openNodes = [(node,i) for node in enumerate(graph.nodes) if graph.nodes[i]['status'] == OPEN]# list of nodes currently open
   
    # Main Loop: execute once for each node until path is found
    while (len(openNodes)>0):
        iteration += 1
        # select current node; end main loop if path has been found
        currentNode = lowest(graph, openNodes)
        if currentNode == last:
            break

        currentConnections = getConnections(graph, currentNode)

        for connection in currentConnections:
            # to.node is node at other end of connection from current node (which is from node of the connection).
	        # to.cost is sum of COSTSOFAR, cost from start node to to current node,  plus COST, cost of current connection.	        
            toNode = graph.connections[connection]['toNode']
            toCost = graph.nodes[currentNode]['costsofar'] + graph.connections[connection]['cost']

            # If the path to the to node via the current node is lower cost than the previous lowest cost path to the to node,
            # then update the to node's fields to reflect the newly found lower cost path.
            if(toCost < graph.nodes[toNode]['costsofar']):
                graph.nodes[toNode]['status'] = OPEN
                graph.nodes[toNode]['costsofar'] = toCost
                graph.nodes[toNode]['heuristic']= getHeuristic(graph, toNode, last)
                graph.nodes[toNode]['total'] = graph.nodes[toNode]['costsofar'] + graph.nodes[toNode]['heuristic']
                graph.nodes[toNode]['previous'] = currentNode
                openNodes.append(toNode) 
        
        path = retrievePath(graph, first, last)
        graph.nodes[currentNode]['path'] = path
        graph.nodes[currentNode]['status'] = CLOSED
        openNodes.remove(currentNode)
        #closedNodes.append(currentNode)
    
    return None


def outputDataStructure():
    with open("output_file.txt", 'w') as output_file:
        
        output_file.write("Nodes\n")
        for node_number, node_data in graph.nodes.items():
            output_line = (
                f'N {node_number} {node_data["status"]} {node_data["costsofar"]} '
                f'{node_data["heuristic"]} {node_data["total"]} {node_data["previous"]} '
                f'{node_data["x"]} {node_data["z"]}\n'
            )
            
            output_file.write(output_line)

        output_file.write("Connections\n")
        for connection, connections in graph.connections.items():
            output_line = f'C {connection} {connections["fromNode"]} {connections["toNode"]} {connections["cost"]} \n'
            #output_line = f'C {connection[0]} {FROM_NODE} {TO_NODE} {COST}\n'     
            output_file.write(output_line)
           #output_file.write(f"C {CONNECTION_NUM} {FROM_NODE} {TO_NODE} {COST}\n")


def outputPath(start, goal, path, cost):

    with open("output_file.txt", 'a') as output_file:
        output_file.write(f"Path from {start} to {goal} path = {path} cost = {cost}\n")


if __name__ == "__main__":
   
    # Test Cases for Output
    testcases = [(1, 29), (1, 38), (11, 1), (33, 66), (58, 43)]

    outputDataStructure()
    for start, goal in testcases:
        
        aStar(graph, start, goal)
        path = retrievePath(graph, start, goal)
       # print(graph.nodes[node]['path'])
        outputPath(start, goal, path, graph.nodes[goal]['costsofar'])
        # Print the path for each node
        for node_number in graph.nodes:
            if 'path' in graph.nodes[node_number]:
                print(f"Node {node_number} Path: {graph.nodes[node_number]['path']}")
