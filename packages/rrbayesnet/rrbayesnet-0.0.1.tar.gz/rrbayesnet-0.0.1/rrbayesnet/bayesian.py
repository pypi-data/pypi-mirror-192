
from itertools import product



class BayesianNetwork:
    """
    A class to map in python dictionaries a bayesian network
    author: Roberto Rios
    """

    def __init__(self, nodes) -> None:
        self.graph = {}
        for i,j in nodes.items():
            self.graph[i] = j
        self.tables = {}

    
    def __repr__(self) -> str:
        return ''.join([(f"({i}) -> {j}\n") for i,j in self.graph.items()])
    

    def dependencies(self, nodeName:str):
        if nodeName in self.graph.keys():
            f = 0
            for i in self.graph:
                for name in self.graph[i]:
                    if nodeName == name:
                        f += 1
            return f
        else:
            return "node not in graph"
        

    def setParentNodeProb(self, nodeName, probability:int):
        """
        Sets the probability of a totally independent node and its complement\n
        for example:
        Burglary: [0.8, 0.2]\n
        if the node is not dependents, returns nothing and prints a message
        """

        if self.dependencies(nodeName) == 0:
            if  0 <= probability <= 1:
                self.tables[nodeName] = [probability,1-probability]


    def setDepNodeProb(self, nodeName, probs):
            
        appearences = 0
        parents = set()
        

        for node in self.graph.values():
            if nodeName in node:
                appearences += 1
                parents = {i for i in self.graph if self.graph[i]==node}

        
        # tabla booleana para ver las combinaciones
        boolTable = list(product((True, False), repeat=len(parents)))
        
        # tabla a construir
        table = []

        if len(probs) != len(boolTable):
            raise Exception("Not enough probabilities given")
        else:
            for prob in probs:
                table.append(prob)
        
        self.tables[nodeName] = {}
        
        for i in range(len(boolTable)):
            if all([False for i in range(len(probs)) if probs[i] < 0 or probs[i] > 1 ]):
                self.tables[nodeName][boolTable[i]] = [probs[i], 1 - probs[i]]
            else:
                raise Exception("some prob is not between 0 and 1")
            
        
        # ok, ya tengo al nodo influido y a los influyentes, con las tablas



    def inference(self):
        pass


    def getCompact(self):
        copied = self.graph.copy()
        childs = copied.values()
        parents = set(self.graph.keys()).difference(set([item for sublist in childs for item in sublist]))
        res = []

        for i in childs:

            values = { j for j in copied if copied[j] == i }

            if len(i) > 1:
                for j in i:
                    if len(values) > 1:
                        res.append(f"P({j}|{values})")
                    else:
                        res.append(f"P({j}|{list(values)[0]})")

            else:
                res.append(f"P({i[0]}|{values})")


        for i in parents:
            res.append(f"P({i})")

        res = set(res)

        return '*'.join([i for i in res])
    


    def describe(self):
        f = True
        for nodeName in self.tables.keys():
            if self.dependencies(nodeName) == 0 and len(self.tables[nodeName]) == 2:
                pass
            if self.dependencies(nodeName) != 0 and not (len(self.tables[nodeName]) == 2**self.dependencies(nodeName)):
                f = False
                return f"The table from node {nodeName} is not fully described."
        if f:
            return f"\nEl grafo esta completo:\n{self}"





