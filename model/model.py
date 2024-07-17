import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self.graph = nx.DiGraph()

        self._listChromosome = []
        self._listConnectedGenes = []
        self._listGenes = []
        self.idMap = {}

        self.loadGenes()
        self.loadChromosome()
        self.loadConnectedGenes()


    def loadChromosome(self):
        self._listChromosome = DAO.getAllChromosomes()

    def loadConnectedGenes(self):
        self._listConnectedGenes = DAO.getAllConnectedGenes()

    def loadGenes(self):
        self._listGenes = DAO.getAllGenes()
        self.idMap = {}
        for g in self._listGenes:
            self.idMap[g.GeneID] = g.Chromosome

    def build_graph(self):
        self.graph.clear()

        for c in self._listChromosome:
            self._nodes.append(c)
        self.graph.add_nodes_from(self._nodes)

        edges = {}
        for g1, g2, corr in self._listConnectedGenes:
            if (self.idMap[g1], self.idMap[g2]) not in edges:
                edges[(self.idMap[g1], self.idMap[g2])] = float(corr)
            else:
                edges[(self.idMap[g1], self.idMap[g2])] += float(corr)
        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))
        self.graph.add_weighted_edges_from(self._edges)

    def count_edges(self, t):
        count_bigger = 0
        count_smaller = 0
        for x in self.get_edges():
            if x[2]['weight'] > t:
                count_bigger += 1
            elif x[2]['weight'] < t:
                count_smaller += 1
        return count_bigger, count_smaller

    def get_nodes(self):
        return self.graph.nodes()

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def get_num_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_num_of_edges(self):
        return self.graph.number_of_edges()

    def get_min_weight(self):
        return min([x[2]['weight'] for x in self.get_edges()])

    def get_max_weight(self):
        return max([x[2]['weight'] for x in self.get_edges()])
