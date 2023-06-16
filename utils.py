def del_node(node, current_nodes: list, mask: list, dependencies: dict):
    pending_nodes = [node]

    while len(pending_nodes):
        n = pending_nodes.pop()
        mask[n.id] = False

        del_nodes = dependencies[n.id] + [i for i in n.edges if i.val < 0]

        pending_nodes.extend(del_nodes)
        current_nodes.remove(n)
    return current_nodes, mask, dependencies


def add_node(node, current_nodes: list, mask: list, dependencies: dict):
    pending = [node]

    while len(pending):
        n = pending.pop()
        if mask[n.id]:
            continue

        mask[n.id] = True
        current_nodes.append(n)

        negative_nodes = [e.source for e in n.in_edges if e.val < 0]

        dependencies[n.id] = negative_nodes
        pending.extend(negative_nodes)
    return current_nodes, mask, dependencies
