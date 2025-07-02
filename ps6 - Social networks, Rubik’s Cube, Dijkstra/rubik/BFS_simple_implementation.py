#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BFS simple implementation

The implementation follows the lecture notes of MIT 6.006 (week 13)
"""

def BFS(source,Adj):
    """
        Performs a breadth first search of the connected graph starting with the 
        source node.
        
        Input: 
            source: node (or any immutable object), the starting node of the search
            Adj: dict, maps a node to its connected (by edges) nodes 
        
        Returns:
            levels: dict, returns the level of each node in the BFS
            parent: dict, returns the shortest path parent of each node.
            
        
        To obtain the shortest path we just start we call parent iteratively
        starting from the destination node.
    """
    level = {source: 0}
    parent = {source: None}
    i = 1
    frontier = [source]
    while frontier:
        next = []
        for u in frontier:
            for v in Adj[u]:
                if v not in level:
                    level[v] = i
                    parent[v] = u
                    next.append(v)
        frontier = next
        i += 1
    return level, parent


## Check
"""
if __name__ == "__main__":
    nodes = list(range(6))
    
    # Building the adjecency dictionary
    Adj = {}
    tuples = [(0,1),(0,2),(1,2),(1,3),(2,5),(3,4)]
    for node in nodes:
        Adj[node] = []
    for tup in tuples:
            Adj[tup[0]].append(tup[1])
        
        
    level, parent = BFS(0,Adj)
    print('levels:')
    print(level)
    print('\n')
    print('parents:')
    print(parent)
"""    
    
    

    