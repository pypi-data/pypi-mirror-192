'''
This module contains the base classes used in the book.

'''

class Node:
    # using __slots__ for optimization
    __slots__ = ['node', 'distance', 'parent', 'osmid', 'G']
    # constructor for each node
    def __init__(self ,graph , osmid, distance = 0, parent = None):
        # the dictionary of each node as in networkx graph --- still needed for internal usage
        self.node = graph[osmid]
        
        # the distance from the parent node --- edge length
        self.distance = distance
        
        # the parent node
        self.parent = parent
        
        # unique identifier for each node so we don't use the dictionary returned from osmnx
        self.osmid = osmid
        
        # the graph
        self.G = graph
    
    # retrieve the osmid
    def get_id(self):
        return self.osmid
    
    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance

    def set_parent(self, parent):
        self.parent = parent
        
    # returning all the nodes adjacent to the node
    def expand(self, reverse=False, attr_name='length'):
        children = []
        if not reverse:
            # Look at outbound edges
            for id, child in self.G.out_edges(self.osmid):
                try:
                    dist = self.G[id][child][0][attr_name]
                except:
                    dist = self.G[id][child][attr_name]
                children.append(Node(graph = self.G, osmid = child, distance = dist, parent = self))    
        else:
            # Look at inbound edges
            for child, id in self.G.in_edges(self.osmid):
                try:
                    dist = self.G[child][id][0][attr_name]
                except:
                    dist = self.G[child][id][attr_name]
                children.append(Node(graph = self.G, osmid = child, distance = dist, parent = self))      
        return children
    
    # returns the path from that node to the origin as a list and the length of that path
    def path(self):
        node = self
        path = []
        while node:
            path.append(node.osmid)
            node = node.parent
        return path[::-1]
    
    # the following two methods are for dictating how comparison works

    def __eq__(self, other):
        try:
            return self.osmid == other.osmid
        except:
            return self.osmid == other
            
    
    def __hash__(self):
        return hash(self.osmid)


class Solution:
    def __init__(self, result, time, space, explored):
        self.result = result
        self.time = time
        self.space = space
        self.explored = explored

        