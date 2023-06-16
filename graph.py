class Node:
    def __init__(self, id: int):
        self.id = id
        self.edges = []
        self.in_edges = []
        self.out_neighbors = []
        self.neighbors = []
        
    def connect(self, dest:'Node', val:int):
        e = Edge(self, dest, val)
        self.edges.append(e)
        self.neighbors.append(dest.id)
        dest.in_edges.append(e)
        dest.out_neighbors.append(self.id)
        
    def fill_node(self, nodes: list):
        for p in nodes:
            if not p.id in self.neighbors:
                self.connect(p,0)
    
    def __eq__(self, o):
        return self.id == o.ip
    
    def __hash__(self):
        return hash(self.id)
    
class Edge:
    def __init__(self,source:'Node', dest:'Node', val:int):
        self.source = source
        self.dest = dest
        self.val = val
        self.pheromone = 0

