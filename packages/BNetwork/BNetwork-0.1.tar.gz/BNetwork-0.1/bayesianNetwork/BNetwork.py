import itertools
import copy
#Genera la tabla de verdad para la relacion de nodos y coloca los solicitados por el usuario. Se ingresa BC, devuelve BC, B-C, -BC, -B-C
def generateTableNodes(letters):
        boleanos = []
        structure = []
        res = []

        for l in letters:
            boleanos.append([True, False])

        for element in itertools.product(*boleanos):
            structure.append(element)

        for x in structure:
            change = 0
            newStructure = ""
            for t in x:
                if t == True:
                    newStructure+= letters[change]
                else:
                    newStructure+= "-"+letters[change]
                change+=1
            res.append(newStructure)
        return res

class BNetwork:

    bnet = {}

    def __init__(self):
        self.bnet = {}

    #Genera la red bayesiana
    def createBNetwork(self, matrix):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        red = {}
        negred = {}
        baynet = {}

        for x in range(len(matrix)):
            val = ''
            count = 0
            for y in matrix:
                if y[len(matrix) - x - 1] == 1:
                    val = val + letters[count] 
                count+=1
            red['{}'.format(letters[len(matrix) - x - 1])]= {val:0}

        for j in red.keys():
            firstKey = list(red.get(j).keys())[0]
            if firstKey != '':
                tableNodes = generateTableNodes(firstKey)
            else:
                red[j] = 0
                continue
            for node in tableNodes:
                red[j].update({node: 0})
        
        for node in red.keys():
            negred["-"+node] = red.get(node)

        baynet['Pos'] = red
        baynet['Neg'] = negred

        self.bnet = baynet

    #Genera la representación compacta de la red bayesiana
    def showCompactRepresentation(self):
        bayesianNetwork = self.bnet['Pos']
        listados = list(bayesianNetwork.keys())
        res = []
        compact = ""
        for l in listados:
            if type(bayesianNetwork.get(l)) == dict:
                val = list(bayesianNetwork.get(l))[0]
                res.append('P('+l + '|' + val+')')
            else:
                res.append('P('+l+')')
        for p in res:
            compact+=p + ' '

        compact = "\nForma compacta:\n" + compact + "\n"
        return compact

    #Función para ingresar probabilidad de un nodo específico
    def insertProbability(self, inf, prob):
        pos = copy.deepcopy(self.bnet.get('Pos'))
        neg = copy.deepcopy(self.bnet.get('Neg'))
        res = {}

        try:
            if len(inf) !=1:
                letters = list(inf.partition('|'))
                letters.remove('|')
                if letters[1] in pos.get(letters[0]):
                    pos[letters[0]].update({letters[1]: prob})
                    res['Pos'] = pos
                    neg["-"+letters[0]].update({letters[1]: 1-prob})
                    res['Neg'] = neg
                else:
                    print('No se encuentra la relacion dada')
                    res = self.bnet
            else:
                if inf in pos:
                    pos[inf] = (prob)
                    res['Pos'] = pos
                    neg["-"+inf] = (1-prob)
                    res['Neg'] = neg
                else:
                    print('No se encuentra la relacion dada')
                    res = self.bnet
        except:
            print('No se encuentra la relacion dada')
            res = self.bnet

        self.bnet = res
    
    #Función para verificar que la Red se encuentre correctamente descrita (Valores distintos de 0)
    def descriptionCheck(self):
        pos = self.bnet.get('Pos')
        faltantes = ""
    
        for k in pos.keys():
            if type(pos.get(k)) == dict:
                for kk in pos.get(k).keys():
                    if pos[k][kk] == 0:
                        faltantes+=(k + '|' + kk + '\n')                

        if faltantes != "":
            faltantes = "\nProbabilidades faltantes de ingresar:\n" + faltantes
        else:
            faltantes = "\nLa red se encuentra completamente descrita\n"
        return faltantes
    
    def test():
        return "Hola mundo"
    
    def __str__(self): 
        return "\nMatriz:\n" + str(self.bnet) + "\n"


matriz = [
    #A B C D E
    [0,1,1,0,0],    #A                  [A]
    [0,0,0,1,1],    #B                 /   \
    [0,0,0,0,1],    #C              [B]     [C]
    [0,0,0,0,0],    #D             /   \
    [0,0,0,0,0]     #E          [D]     [E]
]

# BayesianNetwork = BNetwork()
# BayesianNetwork.createBNetwork(matriz)

# BayesianNetwork.insertProbability('A',0.24)     #A
# BayesianNetwork.insertProbability('B|A',0.15)   #B
# BayesianNetwork.insertProbability('B|-A',0.19)
# BayesianNetwork.insertProbability('C|A',0.24)   #C
# BayesianNetwork.insertProbability('C|-A',0.31)
# BayesianNetwork.insertProbability('D|B',0.12)   #D
# BayesianNetwork.insertProbability('D|-B',0.25)
# BayesianNetwork.insertProbability('E|BC',0.12)  #E
# BayesianNetwork.insertProbability('E|B-C',0.08)
# BayesianNetwork.insertProbability('E|-BC',0.31)
# BayesianNetwork.insertProbability('E|-B-C',0.14)

# print(BayesianNetwork.descriptionCheck())
# print(BayesianNetwork.showCompactRepresentation())
# print(BayesianNetwork)



