# Universidad del valle de guatemala
# Inteligencia Artificial
# Marco Jurado 20308
# Bayesian.py

class Bayes:
    def __init__(self,nodosBayes) -> None:
        self.nodosBayes = nodosBayes

    # forma compacta de red baysiana
    def representacionCompacta(self):
        compactaSTR = "\n".join(nodoBayesiano.Describir() for nodoBayesiano in self.nodosBayes) + "\n" #.join para iterar los elementos.
        return compactaSTR

    # array de tuplas donde los elementos de la tupla son el tag y la tabla de probabilidades. 
    def factoresRedBayesiana(self):
        return [(i.tag, i.CompoundTable) for i in self.nodosBayes]

    # si los estados X estan en los values del compound table entonces la funcion all devuelve true.
    def verificarDescrita(self):
        return all(estado in X.CompoundTable[relacionSuperior] for X in self.nodosBayes for relacionSuperior in X.CompoundTable for estado in X.estados)

    # probabilidad de un evento
    def consulta(self, pregunta):
        # pregunta es un diccionario donde se tiene que dar el tag del nodo y el estado del nodo.
        retorno = 1 # default 
        for X in self.nodosBayes:
            # por cada nodo en la red.
            relSUP = (pregunta[nodoSUP.tag] for nodoSUP in X.relSuperior) # nodos superiores a X
            retorno *= X.CompoundTable.get(tuple(relSUP), X.CompoundTable)[pregunta[X.tag]] # multiplicar de acuerdo con proceso de probabilidad conj. aprendido en clase.
        return retorno

# Universidad del valle de guatemala
# Inteligencia Artificial
# Marco Jurado 20308
# Nodes.py

# Se utilizan nodos para representar los elementos de la red bayesiana como visto en clase.
class BayesNode:
    def __init__(self, estados, tag, relSuperior = None, cmpTable = None) -> None:
        self.estados = estados
        self.tag = tag

        # relación superior = nodos que afectan la probablidad del nodo en discusión.
        if relSuperior is not None:
            self.relSuperior = relSuperior
        else:
            self.relSuperior = []
 
        # key = combinación de padres  
        # value = probabilidad que toma el nodo dada la prob de los padres.
        if cmpTable is not None:
            self.CompoundTable = cmpTable
        else:
            self.CompoundTable = {}

    # agregar relaciones que afectaran al nodo
    def nuevaConexionSuperior(self, x):
        self.relSuperior.append(x)
    
    def agregarCompound(self,x,y):
        self.CompoundTable[x] = y

    def Describir(self):
        retorno = ''
        retorno += 'Nodo: ' + str(self.tag) + '\n  relaciones superiores:\n'
        for p in self.relSuperior:
            retorno += '    - ' + str(p.tag) + '\n'
        retorno += '  tabla de probabilidades del nodo:\n'
        for relSUP, Probabilidad in self.CompoundTable.items():
            retorno += '    - ' + str(relSUP) + ':' + str(Probabilidad) + '\n'

        
        return retorno

def main():
    BayesNode()
    Bayes()
if __name__ == '__main__':
    main()