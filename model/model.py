import copy

import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._graph = nx.Graph()
        self._idMapActors = {}
        self._mapEdges = {}
        actors = DAO.getAllActors()
        for act in actors:
            self._idMapActors[act.id] = act
        self._bestPath = []
        self._bestLun = 0

    def bestPath(self):
        self._bestPath = []
        self._bestLun = 0
        parziale = []
        for node in self._graph.nodes:
            parziale.append(node)
            self._ricorsione(parziale)
            parziale.pop()
        if len(self._bestPath) > 0:
            return self._bestPath, self._bestLun
        return None, None

    def _ricorsione(self, parziale):
        # Condizione di ottimalità
        if len(parziale) > self._bestLun:
            self._bestLun = len(parziale)
            self._bestPath = copy.deepcopy(parziale)

        # Ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            if parziale[-1].date_of_birth < v.date_of_birth and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    @staticmethod
    def getAllRatings():
        return DAO.getAllRatings()

    def buildGraph(self, vMin, vMax):
        self._graph.clear()
        nodes = DAO.getAllActorsByRatings(vMin, vMax)
        self._graph.add_nodes_from(nodes)
        self._mapEdges = {}
        edges = DAO.getAllEdges(vMin, vMax)
        for edge in edges:
            if '$' in edge[2]:
                income = float(edge[2].replace('$', '').strip())
            else:
                income = ""
                for car in edge[2]:
                    if car.isdigit():
                        income += car
                income = float(income)
            if (edge[0], edge[1]) in self._mapEdges.keys():
                self._mapEdges[(edge[0], edge[1])] += income
            else:
                self._mapEdges[(edge[0], edge[1])] = income
        for (act1Id, act2Id) in self._mapEdges.keys():
            act1 = self._idMapActors[act1Id]
            act2 = self._idMapActors[act2Id]
            peso = self._mapEdges[(act1Id, act2Id)]
            self._graph.add_edge(act1, act2, weight=peso)

    def graphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Edges(self):
        archi = self._graph.edges(data=True)
        return sorted(archi, key=lambda x: x[2]['weight'], reverse=True)[:5]

    def getConnectedComponents(self):
        numConnComp = len(list(nx.connected_components(self._graph)))
        maxCompConn = list(max(nx.connected_components(self._graph), key=len))
        return numConnComp, maxCompConn

    def isGraphOk(self):
        return len(self._graph.nodes) > 0 and len(self._graph.edges) > 0