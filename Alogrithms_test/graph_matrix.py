"""
Create and initalise an adjacency matrix of a graph

Expects a graph in form of a dictionary and creates a matrix
with a size corresponding with the number of nodes +1 row and
column to hold the node labels. Adds the node labels to the first
row and first column and returns the matrix
"""
        
def init_matrix(graph: dict) -> list:
    
    graph_nodes=list(graph.keys())
    size=len(graph_nodes) + 1
    matrix=[["" for x in range(size)] for y in range(size)]

    for x in range(1, size):
        matrix[0][x]=graph_nodes[x-1]
        matrix[x][0]=graph_nodes[x-1]

    return matrix

"""
Populate the adjacency matrix of graph

A graph and its connections is represented by a dictionary,
with the graph labels as keys and a list of node labels that
the given node (key) has a connection with as values.

The function checks if the matrix is a 2D list if it matches the size
corresponds with the number of graph nodes. Looks for the 
presence of the label of a node in another node's connections. If
the node label is present in another node's list of connections,
the connection is represented with 1. If there is no connection, the
value is 0.
"""

def populate_matrix(matrix: list[list], graph:dict) -> None:
    nodes=list(graph.keys())
    if any(isinstance(item, list) for item in matrix) and len(matrix) == len(nodes) + 1:
        
        for x in range(1, len(matrix)):
            for y in range(1, len(matrix)):
                if nodes[y-1] in graph[nodes[x-1]]:
                    matrix[x][y]=1
                else:
                    matrix[x][y]=0


    
   


        
        
