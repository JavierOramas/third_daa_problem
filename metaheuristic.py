import random
from utils import add_node


class AntColony:
    def __init__(
        self,
        nodes: list,
        max_k: int,
        n_ants=10,
        taomin=0.005,
        taomax=5,
        alpha=2,
        rho=0.99,
        times=1000,
    ):
        self.nodes = nodes
        self.max_k = max_k
        self.best_sol = []
        self.n_ants = n_ants
        self.taomax = taomax
        self.taomin = taomin
        self.alpha = alpha
        self.times = times
        self.rho = rho

    def init_phreomone(self):
        for n in self.nodes:
            for e in n.edges:
                e.phreomone = self.taomax

    def create_model(self):
        initial_node = False
        nodes = []

        dependencies = {}
        best_nodes = set()

        while not initial_node:
            test_initial_node = random.sample(self.nodes, 1)[0]
            mask = [False] * (len(self.nodes)+1)
            node, mask, dependencies = add_node(test_initial_node, [], mask, {})

            if len(nodes) > self.max_k:
                continue

            initial_node = True

        nodes_in_group = set()
        for n in nodes:
            nodes_in_group.add(n)

        posible_new_nodes = set()
        for n in nodes:
            posible_new_nodes.union(n.neighbors)

        best_nodes.update(nodes_in_group)

        while len(posible_new_nodes) > 0:
            pheromone = [
                self.pheromone_factor(n, posible_new_nodes) for n in posible_new_nodes
            ]

            probs = [f / sum(pheromone) for f in pheromone]
            node_to_add = random.choices(list(posible_new_nodes), probs, k=1)[0]

            new_nodes, mask, dependencies = add_node(
                node_to_add, list(nodes_in_group), mask, dependencies
            )

            nodes_in_group = nodes_in_group.union(set(new_nodes))

            if len(nodes_in_group) > self.max_k:
                break

            posible_new_nodes = posible_new_nodes.intersection(node_to_add.neighbors)
            best_nodes.update(nodes_in_group)
        return best_nodes

    def pheromone_factor(self, node, nodes):
        return sum([e.pheromone for e in node.edges if e in nodes])

    def solve(self):
        for it in range(self.times):
            cliques = [self.create_model() for j in range(self.n_ants)]
            self.update_pheromones(cliques)

        return len(self.best_sol), self.best_sol

    def update_pheromones(self, cliques):
        best = max(cliques, key=lambda x: len(x))

        if len(best) > len(self.best_sol):
            self.best_sol = list(best)

        for node in self.nodes:
            for e in node.edges:
                e.pheromone = max(self.taomin, self.rho * e.pheromone)

        actual_best = len(self.best_sol)
        actual_k = len(best)

        for node in best:
            for e in node.edges:
                e.pheromone += min(self.taomax, (1 / (1 + actual_best - actual_k)))

