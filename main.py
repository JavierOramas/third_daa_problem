from graph import Node, Edge
import sys
greatest_k = 0
group = []

def del_node(node: Node, current_nodes: list, mask: list, dependencies: dict):
    pending_nodes = [node]
    
    while len(pending_nodes):
        n = pending_nodes.pop()
        mask[n.id] = False
        
        del_nodes = dependencies[n.id]+[i for i in n.edges if i.val < 0]
        
        pending_nodes.extend(del_nodes)
        current_nodes.remove(n)
    return current_nodes, mask, dependencies

def add_node(node: Node, current_nodes:list, mask: list, dependencies: dict):
    pending = [node]
    
    while len(pending):
        n = pending.pop()
        if mask[n.id]:
            continue
            
        mask[n.id] = True
        current_nodes.append(n)
        
        negative_nodes = [
            e.source for e in n.in_edges if e.val < 0 
        ]
        
        dependencies[n.id] = negative_nodes
        pending.extend(negative_nodes)
    return current_nodes, mask, dependencies

def backtracking(k,current_nodes, mask, dependencies):
    if len(current_nodes) > k:
        return
    
    global greatest_k
    global group
    
    if 0 <= greatest_k < len(current_nodes) <= k:
        greatest_k = len(current_nodes)
        group = [node.id for node in current_nodes]
        
    if greatest_k == k:
        return
    
    neighbors = set()
    for n in current_nodes:
        neighbors.union(n.neighbors+n.neighbors)
    
    for n in current_nodes:
        if not mask[n.id]:
            current_nodes,mask, dependencies = add_node(n, current_nodes, mask, dependencies)
            backtracking(k, current_nodes, mask, dependencies)
            current_nodes,mask,dependencies = del_node(n, current_nodes, mask, dependencies)

def brute_force_solution(nodes, k):
    global greatest_k
    global group
    
    greatest_k = 0
    group = []
    
    # mask = [False] * len(nodes)
    
    for i in nodes:
        mask = [False] * len(nodes)
        
        s_nodes, mask, dependencies = add_node(i, [], mask, {})
        
        if len(s_nodes) > k:
            continue
        
        backtracking(k,s_nodes, mask, dependencies)
        
        if greatest_k == k:
            break
    
    return greatest_k, group

def solve(persons: list, k:int, accept_blank=False):
    ids = set([p['id'] for p in persons])
    
    nodes_dict = {p['id']:Node(p['id']) for p in persons}
    nodes = list(nodes_dict.values())
    for i in range(len(nodes)):
        for j in range(len(persons[i]['edges'])):
            nodes[i].connect(nodes_dict[persons[i]['edges'][j]], -1)

    for node in nodes:
        node.fill_node(nodes)
    
    sol = brute_force_solution(nodes, k)
    
    # it is valid that some graphs may not have a valid group but we take it out because the generator very often makes a lot of cases with this output
    # call solve with accept_blank = True to alow those cases
    if accept_blank or sol[0] != 0:
        print(f"greatest_k_val: {sol[0]} group: {sol[1]}")
        
    return sol

def process_data(data_list, k):
    for data in data_list:
        id_value = data["id"]
        edges_list = data["edges"]

        
if __name__ == '__main__':
    arg_list = sys.argv[1:-1]  # Exclude the script name and the last argument
    k = int(sys.argv[-1])  # Last argument is the single integer 'k'

    # Convert the command line arguments to the desired data structure
    parsed_list = []
    for arg in arg_list:
        data_dict = {}
        parsed_data = arg.split(":")
        data_dict["id"] = int(parsed_data[0])
        try:
            data_dict["edges"] = [int(edge) for edge in parsed_data[1].split(",")] 
        except:
            data_dict["edges"] = []
        parsed_list.append(data_dict)

    solve(k=k, persons=parsed_list, accept_blank=True)