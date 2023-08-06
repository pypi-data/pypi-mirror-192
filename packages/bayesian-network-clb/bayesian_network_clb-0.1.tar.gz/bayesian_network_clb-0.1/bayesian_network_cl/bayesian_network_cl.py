######################################################################################
_author_ = "Cristian Fernando Laynez Bachez - 201281"
_copyright_ = "Universidad el Valle de Guatemala, Inteligencia Artifical 2023"
_status_ = "Student of Computer Science"

"""
Bayesian Network CL: Clase donde se encontrará todas las funciones de esta
librería de redes bayesianas e interferencia probabilística.
"""
######################################################################################

class BayesianNetwork():
                
    def __init__(self) -> None:         
        self.__nodes = {}
        self.__probs = {}
    
    def add_nodes(self, all_nodes : list) -> None:
        for edge_1, edge_2 in all_nodes:
            if edge_1 not in self.__nodes: self.__nodes[edge_1] = []
            if edge_2 not in self.__nodes: self.__nodes[edge_2] = []
            self.__nodes[edge_1].append(edge_2)
                    
        nodes_count = {}
        for key, value in self.__nodes.items():
            if key not in nodes_count:
                nodes_count[key] = 0
                                    
        for key, value in self.__nodes.items():
            for v in value:
                nodes_count[v] += 1

        # We are going to test something
        prepare_for_probs = {}
        for key, value in self.__nodes.items():
            for v in value:
                if v not in prepare_for_probs:
                    prepare_for_probs[v] = [key]
                else:
                    prepare_for_probs[v].append(key)
            
        for key, value in self.__nodes.items():
            if key not in  prepare_for_probs:
                prepare_for_probs[key] = []
    
        for key, value in prepare_for_probs.items():
            temp = [None for _ in range(2 ** len(value)) ]
            if key not in self.__probs:
                self.__probs[(key, True)] = temp
                self.__probs[(key, False)] = temp

    def add_probs(self, node: str, probs : list) -> None:
        if((node, True) not in self.__probs):
            print("\033[1;31;40mERROR: El nodo ingresado no existe la red bayesiana\033[0;37;40m \n")
            return
        
        if len(probs) != len(self.__probs[(node, True)]):
            print("\033[1;31;40mERROR: El tamanio de las listas no coinciden\033[0;37;40m \n")
            return
            
        self.__probs[(node, True)] = probs
        
    def show_bayesian_network(self) -> str:
        info_nodes = ''
        for key, value in self.__nodes.items():
            info_nodes += f'{key} --> {value}\n'
        return info_nodes
                
    def show_bayesian_network_and_probs(self) -> str:        
        information = []        
        for i in self.__probs.items():
            prob, array_probs = i
            if prob[1] == True:
                information.append(f'PROB: {prob} | VALUES: {array_probs}')                
        return '\n'.join(map(str, information))
            
    def inference_by_enumeration(self, **conditions) -> float:
        return 0.0
        
    def bayesian_network_complete(self) -> bool:
        for i in self.__probs.items():
            prob, array_probs = i
            if prob[1] == True:
                for p in array_probs:
                    if p == None: return False
        return True
    