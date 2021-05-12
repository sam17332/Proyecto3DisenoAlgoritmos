from graphviz import Digraph
from nodoD import *
import time
import pickle5 as pickle

class Directo:
    def __init__(self, postfixTokens):
        self.postfix = postfixTokens
        self.lenguaje = []
        self.diccioFinal = {}
        self.diccioSiguientePos = {}
        self.diccioAceptacion = {}
        self.contador1 = 1
        self.contador2 = 0
        self.pila = []
        self.pilaFinal = []
        self.Destados = []
        self.DestadosGlobal = []
        self.cadena = "ab"

    """
    Función para obtener el lenguaje del postfix.
    """
    def getLenguaje(self, postfix):
        newLenguaje = []
        arrayLocal = []
        for tokensDef in postfix:
            if(tokensDef.getTipo() == "CHARACTER" or tokensDef.getTipo() == "EPSILON" or tokensDef.getTipo() == "STRING"):
                # print(arrayLocal)
                # print(tokensDef.getCharacter())
                # print(tokensDef.getValor())
                # print()
                if(tokensDef.getCharacter() not in arrayLocal):
                    arrayLocal.append(tokensDef.getCharacter())
                    newLenguaje.append(tokensDef)

        return newLenguaje

    """
    Función para saber si el caracter es un operando o un operador.
    Si es un operando, epsilon o numeral, retorna TRUE
    de lo contrario, retorna FALSE
    """
    def esOperando(self, valor):
        if valor == "CHARACTER" or valor == "STRING" or valor == "EPSILON" or valor == "ACEP":
            return True
        return False

    """
    Función para saber si el caracter es un anulable o no.
    Si el caracter es:
    EPSILON = TRUE
    OR = anulable1 or anulable2
    APPEND = anulable1 and anulable2
    KLEENE = TRUE
    operando = FALSE
    """
    def esAnulable(self, nodos, char):
        if(char == "EPSILON"):
            return True
        elif(self.esOperando(char)):
            return False
        elif (char == "OR"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            anulable1 = nodo1.getAnulable()
            anulable2 = nodo2.getAnulable()

            return (anulable1 or anulable2)
        elif(char == "APPEND"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            anulable1 = nodo1.getAnulable()
            anulable2 = nodo2.getAnulable()

            return (anulable1 and anulable2)
        elif(char == "KLEENE"):
            return True
        else:
            print("ERROR")

    """
    Función para saber la primeraPos de cada caracter
    Si el caracter es:
    EPSILON = ø -  vacio
    OR = primeraPosC1 U primeraPosC2
    APPEND = anulable(c1) ? primeraPosC1 U primeraPosC2 : primeraPosC1
    KLEENE = primeraPosC1
    operando = {id}
    """
    def primeraPos(self, nodos, char):
        if(char == "EPSILON"):
            return ""
        elif(self.esOperando(char)):
            nodo1 = nodos.pop()
            nodo1Id = nodo1.getId()

            return [nodo1Id]
        elif (char == "OR"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            primeraPos1 = nodo1.getPrimeraPos()
            primeraPos2 = nodo2.getPrimeraPos()

            if(primeraPos1 == ""):
                primeraPos1 = []
            if(primeraPos2 == ""):
                primeraPos2 = []

            arrayLocalOR = primeraPos1+primeraPos2
            arrayLocalOR = list(dict.fromkeys(arrayLocalOR))
            arrayLocalOR.sort()

            return arrayLocalOR
        elif(char == "APPEND"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            anulable1 = nodo1.getAnulable()
            primeraPos1 = nodo1.getPrimeraPos()
            primeraPos2 = nodo2.getPrimeraPos()

            if(primeraPos1 == ""):
                primeraPos1 = []
            if(primeraPos2 == ""):
                primeraPos2 = []
            if(anulable1):
                arrayLocalCAT = primeraPos1+primeraPos2
            else:
                arrayLocalCAT = primeraPos1

            arrayLocalCAT = list(dict.fromkeys(arrayLocalCAT))
            arrayLocalCAT.sort()

            return arrayLocalCAT
        elif(char == "KLEENE"):
            nodo1 = nodos.pop()
            primeraPos1 = nodo1.getPrimeraPos()

            if(primeraPos1 == ""):
                primeraPos1 = []

            arrayLocalKL = primeraPos1
            arrayLocalKL = list(dict.fromkeys(arrayLocalKL))
            arrayLocalKL.sort()

            return arrayLocalKL
        else:
            print("ERROR")

    """
    Función para saber la ultimaPos de cada caracter
    Si el caracter es:
    EPSILON = ø  "vacio"
    OR = ultimaPosC1 U ultimaPosC2
    APPEND = anulable(c2) ? ultimaPosC1 U ultimaPosC2 : ultimaPosC2
    KLEENE = ultimaPosC1
    operando = {id}
    """
    def ultimaPos(self, nodos, char):
        if(char == "EPSILON"):
            return ""
        elif(self.esOperando(char)):
            nodo1 = nodos.pop()
            nodo1Id = nodo1.getId()

            return [nodo1Id]
        elif (char == "OR"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            ultimaPos1 = nodo1.getUltimaPos()
            ultimaPosC2 = nodo2.getUltimaPos()

            if(ultimaPos1 == ""):
                ultimaPos1 = []
            if(ultimaPosC2 == ""):
                ultimaPosC2 = []

            arrayLocalOR = ultimaPos1+ultimaPosC2
            arrayLocalOR = list(dict.fromkeys(arrayLocalOR))
            arrayLocalOR.sort()

            return arrayLocalOR
        elif(char == "APPEND"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            anulableC2 = nodo2.getAnulable()
            ultimaPos1 = nodo1.getUltimaPos()
            ultimaPosC2 = nodo2.getUltimaPos()

            if(ultimaPos1 == ""):
                ultimaPos1 = []
            if(ultimaPosC2 == ""):
                ultimaPosC2 = []
            if(anulableC2):
                arrayLocalCAT = ultimaPos1+ultimaPosC2
            else:
                arrayLocalCAT = ultimaPosC2

            arrayLocalCAT = list(dict.fromkeys(arrayLocalCAT))
            arrayLocalCAT.sort()

            return arrayLocalCAT
        elif(char == "KLEENE"):
            nodo1 = nodos.pop()
            ultimaPos1 = nodo1.getUltimaPos()

            if(ultimaPos1 == ""):
                ultimaPos1 = []

            arrayLocalKL = ultimaPos1
            arrayLocalKL = list(dict.fromkeys(arrayLocalKL))
            arrayLocalKL.sort()

            return arrayLocalKL

        else:
            print("ERROR")

    """
    Función para saber la siguientePos de cada caracter
    Si el caracter es:
    APPEND = Para cada id que este en ultimaPos de C1, incerte cada id que este en primeraPos de C2
    KLEENE = Para cada id que este en primeraPos de C1, incerte cada id que este en ultimaPos de C1
    """
    def siguientePos(self, nodos, char):
        if(char == "APPEND"):
            nodo1 = nodos.pop()
            nodo2 = nodos.pop()

            ultimaPos1 = nodo1.getUltimaPos()
            primeraPos2 = nodo2.getPrimeraPos()

            if(primeraPos2 == ""):
                primeraPos2 = []
            if(ultimaPos1 == ""):
                ultimaPos1 = []

            arrayLocal = []
            for x in ultimaPos1:
                arrayLocal = self.diccioSiguientePos[int(x)]
                arrayLocal = arrayLocal+primeraPos2
                arrayLocal = list(dict.fromkeys(arrayLocal))
                arrayLocal.sort()
                self.diccioSiguientePos[int(x)] = arrayLocal

        elif(char == "KLEENE"):
            nodo1 = nodos.pop()
            ultimaPos1 = nodo1.getUltimaPos()
            primeraPosC1 = nodo1.getPrimeraPos()

            if(ultimaPos1 == ""):
                ultimaPos1 = []
            if(primeraPosC1 == ""):
                primeraPosC1 = []

            for x in ultimaPos1:
                arrayLocal = self.diccioSiguientePos[int(x)]
                arrayLocal = arrayLocal+primeraPosC1
                arrayLocal = list(dict.fromkeys(arrayLocal))
                arrayLocal.sort()
                self.diccioSiguientePos[int(x)] = arrayLocal

        else:
            print("ERROR")

    """
    Función para obtener el id de los estados finales del AFD
    """
    def getFinalNumber(self):
        arrayLocal = []
        for id, value in self.diccioSiguientePos.items():
            if len(value) == 0 and id not in arrayLocal:
                arrayLocal.append(id)

        return arrayLocal

    """
    Función para obtener el numero de estado de un estado
    """
    def getStateNumber(self, array):
        for valor in self.pilaFinal:
            if(valor[1] == array):
                return valor[0]

    """
    Función para obtener los estados finales del AFD
    """
    def getEstadosFinales(self):
        finales = []
        numeroEstadoFinal = self.getFinalNumber()
        for estado in self.pilaFinal:
            for estadoFinal in numeroEstadoFinal:
                if(str(estadoFinal) in estado[1] and estado[1] not in finales):
                    finales.append(estado[0])

        return finales

    """
    Funcion para encontrar el siguiente estado
    """
    def mover(self, estado, caracter):
        arrayMover = []
        for estados in estado:
            for transicion in self.pilaFinal:
                if(transicion[2] == caracter and len(transicion[3]) > 0 and estados == transicion[0]):
                    estadoSiguiente = self.getStateNumber(transicion[3])
                    if(estadoSiguiente not in arrayMover):
                        arrayMover.append(estadoSiguiente)

        return arrayMover

    """
    Funcion para simular el AFD
    """
    def simular(self):
        start_time = time.perf_counter()
        s = [0]
        for x in self.cadena:
            s = self.mover(s, x)
        end_time = time.perf_counter()
        idfinal = self.getEstadosFinales()

        if(len(s) > 0):
            if(s[0] in idfinal):
                print("------------------SIMULACION-------------------")
                print("La cadena ", self.cadena, " si es aceptada por el AFD")
                print("--- %s segundos ---" % (end_time - start_time))
                print("-----------------------------------------------")
                print("")

            else:
                print("------------------SIMULACION-------------------")
                print("La cadena ", self.cadena, " no es aceptada por el AFD")
                print("--- %s segundos ---" % (end_time - start_time))
                print("-----------------------------------------------")
                print("")
        else:
            print("------------------SIMULACION-------------------")
            print("La cadena ", self.cadena, " no es aceptada por el AFD")
            print("--- %s segundos ---" % (end_time - start_time))
            print("-----------------------------------------------")
            print("")

    """
    Función para graficar el AFD
    """
    def graficar(self):
        dig = Digraph()
        dig.attr(rankdir="LR", size="50")
        estadosFinales = self.getEstadosFinales()
        pickle.dump(estadosFinales, open( "estadosFinales.p", "wb" ))
        for estado in estadosFinales:
            # posicionDelFinal = self.DestadosGlobal.index(estado)
            dig.attr("node", shape="doublecircle")
            dig.node(str(estado))
        for nodo in self.pilaFinal:
            if(len(nodo[1]) > 0 and len(nodo[3]) > 0):
                estado1 = self.getStateNumber(nodo[1])
                estado2 = self.getStateNumber(nodo[3])
                dig.attr("node", shape="circle")
                dig.edge(str(estado1), str(estado2), str(nodo[2]))
            # if(nodo[3] != 'ɛ' and len(nodo[2]) > 0):
                # if(nodo[0] in self.DestadosGlobal and nodo[2] in self.DestadosGlobal):
                #     index1 = self.DestadosGlobal.index(nodo[0])
                #     index2 = self.DestadosGlobal.index(nodo[2])
                # dig.attr("node", shape="circle")
                # dig.edge(str(index1), str(index2), str(nodo[1]))

        dig.render("Automatas/Directo.gv", view=True)

    def setToString(self, caracteres):
        valor = ""
        if(isinstance(caracteres, set)):
            for char in caracteres:
                valor += str(chr(int(char)))
        elif(isinstance(caracteres, int)):
            valor = str(chr(caracteres))
        elif(isinstance(caracteres, str)):
            valor = str(chr(int(caracteres)))

        return valor

    """
    Función para obtener los diferentes id's de una letra
    """
    def getIdsLetra(self, letra):
        ids = []
        for id, nodo in self.diccioFinal.items():
            if(nodo.getChar() == letra.getCharacter()):
                ids.append(nodo.getId())

        return ids

    """
    Función para armar el arbol de caracteres.
    Se lee cada caracter y se setea id, anulable, primeraPos
    ultimaPos y siguientePos para cada nodo dependiendo del caracter
    """
    def arbolDirecto(self):
        self.lenguaje = self.getLenguaje(self.postfix)
        for char in self.postfix:
            if(char.getTipo() == "OR"):
                nodosAnulable = ""
                nodosPrimeraPos = ""
                nodosUltimaPos = ""
                nodo2 = self.pila.pop()
                nodo1 = self.pila.pop()

                nodoOR = NodoD()
                nodoOR.setChar(chr(char.getValor()))
                nodoOR.setId("")

                nodosAnulable = [nodo2, nodo1]
                nodosPrimeraPos = [nodo2, nodo1]
                nodosUltimaPos = [nodo2, nodo1]

                nodoOR.setAnulable(self.esAnulable(nodosAnulable, char.getTipo()))
                nodoOR.setPrimeraPos(self.primeraPos(nodosPrimeraPos, char.getTipo()))
                nodoOR.setUltimaPos(self.ultimaPos(nodosUltimaPos, char.getTipo()))

                self.diccioFinal[self.contador2] = nodoOR
                self.contador2 += 1
                self.pila.append(nodoOR)

            elif(char.getTipo() == "KLEENE"):
                nodosAnulable = ""
                nodosPrimeraPos = ""
                nodosUltimaPos = ""
                nodosSiguientePos = ""
                nodo = self.pila.pop()

                nodoKL = NodoD()
                nodoKL.setChar(chr(char.getValor()))
                nodoKL.setId("")

                nodosAnulable = [nodo]
                nodosPrimeraPos = [nodo]
                nodosUltimaPos = [nodo]
                nodosSiguientePos = [nodo]

                nodoKL.setAnulable(self.esAnulable(nodosAnulable, char.getTipo()))
                nodoKL.setPrimeraPos(self.primeraPos(nodosPrimeraPos, char.getTipo()))
                nodoKL.setUltimaPos(self.ultimaPos(nodosUltimaPos, char.getTipo()))
                self.siguientePos(nodosSiguientePos, char.getTipo())

                self.diccioFinal[self.contador2] = nodoKL
                self.contador2 += 1
                self.pila.append(nodoKL)

            elif(char.getTipo() == "APPEND"):
                nodosAnulable = ""
                nodosPrimeraPos = ""
                nodosUltimaPos = ""
                nodosSiguientePos = ""
                nodo2 = self.pila.pop()
                nodo1 = self.pila.pop()

                nodoCAT = NodoD()
                nodoCAT.setChar(chr(char.getValor()))
                nodoCAT.setId("")

                nodosAnulable = [nodo2, nodo1]
                nodosPrimeraPos = [nodo2, nodo1]
                nodosUltimaPos = [nodo2, nodo1]
                nodosSiguientePos = [nodo2, nodo1]

                nodoCAT.setAnulable(self.esAnulable(nodosAnulable, char.getTipo()))
                nodoCAT.setPrimeraPos(self.primeraPos(nodosPrimeraPos, char.getTipo()))
                nodoCAT.setUltimaPos(self.ultimaPos(nodosUltimaPos, char.getTipo()))
                self.siguientePos(nodosSiguientePos, char.getTipo())

                self.diccioFinal[self.contador2] = nodoCAT
                self.contador2 += 1
                self.pila.append(nodoCAT)

            elif(char.getTipo() == "EPSILON"):
                nodos = ""

                nodoEP = NodoD()
                nodoEP.setChar(chr(char.getValor()))
                nodoEP.setId("")

                nodos = [nodoEP]

                nodoEP.setAnulable(self.esAnulable(nodos, char.getTipo()))
                nodoEP.setPrimeraPos(self.primeraPos(nodos, char.getTipo()))
                nodoEP.setUltimaPos(self.ultimaPos(nodos, char.getTipo()))

                self.diccioFinal[self.contador2] = nodoEP
                self.contador2 += 1
                self.pila.append(nodoEP)

            else:
                if(char.getTipo() == "STRING" or char.getTipo() == "ACEP" or char.getTipo() == "CHARACTER"):
                    nodosAnulable = ""
                    nodosPrimeraPos = ""
                    nodosUltimaPos = ""

                    nodo = NodoD()
                    nodo.setChar(char.getCharacter())
                    nodo.setId(str(self.contador1))

                    # diccionario de aceptacion
                    if(char.getTipo() == "ACEP"):
                        self.diccioAceptacion[self.contador1] = char.getCharacter()

                    self.diccioSiguientePos[self.contador1] = []
                    self.contador1 += 1

                    nodosAnulable = [nodo]
                    nodosPrimeraPos = [nodo]
                    nodosUltimaPos = [nodo]

                    nodo.setAnulable(self.esAnulable(nodosAnulable, char.getTipo()))
                    nodo.setPrimeraPos(self.primeraPos(nodosPrimeraPos, char.getTipo()))
                    nodo.setUltimaPos(self.ultimaPos(nodosUltimaPos, char.getTipo()))

                    self.diccioFinal[self.contador2] = nodo
                    self.contador2 += 1
                    self.pila.append(nodo)

        nodoRoot = self.pila.pop()
        primerEstado = nodoRoot.getPrimeraPos()
        self.Destados.append(primerEstado)
        self.DestadosGlobal.append(primerEstado)
        cont = -1
        while(len(self.Destados) > 0):
            estado = self.Destados.pop()
            cont += 1
            for letra in self.lenguaje:
                if(letra.getTipo() != "EPSILON"):
                    idsLetra = self.getIdsLetra(letra)
                    array = []
                    for id in idsLetra:
                        if(id in estado):
                            array = array + self.diccioSiguientePos[int(id)]

                    if(array not in self.DestadosGlobal):
                        self.Destados.append(array)
                        self.DestadosGlobal.append(array)
                        # setStr = self.setToString(letra.getValor())
                        # self.pilaFinal.append([cont, estado, setStr, array])
                        self.pilaFinal.append([cont, estado, letra.getValor(), array])

                    else:
                        if(len(estado) > 0):
                            # setStr = self.setToString(letra.getValor())
                            # self.pilaFinal.append([cont, estado, setStr, array])
                            self.pilaFinal.append([cont, estado, letra.getValor(), array])

        # Se guaran los diccionario necesarios para poder simular

        # Se guarda el AFD
        file = open("pilaFinal", "wb")
        pickle.dump(self.pilaFinal, file)
        file.close()

        # Se guarda la "tabla" de aceptacion
        file = open("diccioAceptacion", "wb")
        pickle.dump(self.diccioAceptacion, file)
        file.close()

        # self.graficar()
        # self.simular()