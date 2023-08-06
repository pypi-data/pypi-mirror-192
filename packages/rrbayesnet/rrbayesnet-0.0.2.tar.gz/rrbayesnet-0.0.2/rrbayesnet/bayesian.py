
from itertools import product



class BayesianNetwork:
    """
    A class to map with python native dictionaries a bayesian network
    author: Roberto Rios
    """

    def __init__(self, nodes:dict[list:str]) -> None:
        """
        constructor
        """
        self.graph = {}
        for i,j in nodes.items():
            self.graph[i] = j
        self.tables = {}

    
    def __repr__(self) -> str:
        """
        Override to print pretty nodes
        """
        return ''.join([(f"({i}) -> {j}\n") for i,j in self.graph.items()])
    

    def dependencies(self, nodeName:str):
        """
        returns the quantity of parents given the name of the node
        """
        if nodeName in self.graph.keys():
            f = 0
            for i in self.graph:
                for name in self.graph[i]:
                    if nodeName == name:
                        f += 1
            return f
        else:
            return "node not in graph"
        

    def setParentNodeProb(self, nodeName:str, probability:int):
        """
        Sets the probability of a totally independent node and its complement\n
        for example:
        Burglary: [0.8, 0.2]\n
        if the node is not dependents, returns nothing and prints a message
        """

        if self.dependencies(nodeName) == 0:
            if  0 <= probability <= 1:
                self.tables[nodeName] = [probability,1-probability]


    def setDepNodeProb(self, nodeName: str, probs: list[int]):
        """
        Sets the probability of a node that has at least one parent,
        for example, let A be a child of B and C,
        then probs needs to be a list like this:\n
        probs = [0.1,0.2,0.3,0.5]\n
        this is an abstracction of:\n
        {
            [True, True]: [0.1,0.9],
            [True, False]: [0.2,0.8],
            [False, True]: [0.3,0.7],
            [False, False]: [0.5,0.5],
        }
        """
        
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
            



    def inference(self):
        """
        Tries to guess the most probable event within the nodes.
        """
        pass


    def getCompact(self):
        """
        returns the compact version of the the probabilities of the graph
        """
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
                try:
                    res.append(f"P({i[0]}|{values})")
                except IndexError:
                    pass

        for i in parents:
            res.append(f"P({i})")

        res = set(res)

        return '\nCompacta:\n' + '*'.join([i for i in res])
    


    def describe(self):
        """
        returns all the nodes which are not completed
        """

        incompletes = []
        childs = self.graph.values()
        childs = set([item for sublist in childs for item in sublist])
        parents = set(self.graph.keys()).difference(set([item for sublist in childs for item in sublist]))


        for node in parents:
            if self.dependencies(node) == 0 and len(self.tables[node]) == 2:
                pass
            else:
                incompletes.append(node)
            
        for node in childs:
            if len(self.tables[node]) != 2**self.dependencies(node):
                incompletes.append(node)

        if len(self.tables) != 0:
                return f"\nEl grafo esta completo:\n{self}"
        else:
            return f"El grafo esta incompleto en: {incompletes}"


    def factors(self):
        """
        Shows the factors in the network
        """
        return f"\nFactores:\n{self}" + "\nTables:\n" + "\n".join([str(self.tables[i]) for i in self.tables])



