# Lab 2 IA

__init__(self, nodes, edges): el constructor de la clase. Recibe una lista de nodos y un diccionario de bordes, donde las claves son los nombres de los nodos y los valores son listas de los nombres de los nodos padre. 

is_fully_described(self): comprueba si se han definido los factores de probabilidad de todos los nodos de la red. Devuelve true si estoe es cierto y false si no 

compact(self): devuelve una cadena que representa la red bayesiana de forma compacta. 


representation(self): devuelve una cadena que representa la red bayesiana de forma detallada. Incluye la tabla de probabilidad de cada nodo dada la probabilidad condicional de sus padres.

compute_factor(self, node, evidence={}): calcula el factor de probabilidad del nodo node dado un diccionario de evidencia. 

compute_conditional_probability(self, node, parent_state): calcula la probabilidad condicional del nodo node dada la evidencia en el diccionario parent_state.