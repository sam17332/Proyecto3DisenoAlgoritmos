# Proyecto 2 - Diseño de lenguajes
# Rodrigo Samayoa Morales - 17332
# source proyecto3/bin/activate

import pprint
from funciones import *
from tipoChar import *
from tipoCharProd import *
from postfix import *
from postfixProd import *
from directo import *

class Main:
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo
        self.json = {}
        self.characters = []
        self.print = pprint.PrettyPrinter()
        self.lineasBloqueadas = []
        self.tokens = []
        self.producciones = []
        self.posBloqueadasTemp = []
        self.diccionarioProdFinal = {}
        self.primeraPos = {}

    def main(self):
        self.lectura()

        # Convertir strings a sets
        diccionarioCHR = self.json["CHARACTERS"]
        for char in self.characters:
            valor = diccionarioCHR[char]
            if(isinstance(valor, str)):
                funciones = Funciones()
                valor = funciones.getStringInQuotes(valor)
                if(valor[0] == "{" and valor[len(valor)-1] == "}"):
                    if("{" not in valor[1:len(valor)-1]):
                        valor = valor.replace("{", "")

                    if("}" not in valor[0:len(valor)-2]):
                        valor = valor.replace("}", "")
                valor = set(valor)
                diccionarioCHR[char] = valor

        # print("----------------------------------------------------------------------------------------------------")
        # print("------------------------------------------------JSON------------------------------------------------")
        # print("----------------------------------------------------------------------------------------------------")
        # self.print.pprint(self.json)
        # print()
        # print()
        # print()

        self.construccionTokens()
        self.construccionProducciones()
    '''
        tokensLen = len(self.json["TOKENS"])

        # Se crea un array con todos los tokens separando cada token por un "OR"
        arrayAcumuladoTokens = []
        cont = 0
        for key1, definicion in self.json["TOKENS"].items():
            cont += 1
            for key2, valor in definicion.items():
                arrayAcumuladoTokens.append(valor)
            if(cont < tokensLen):
                tipoChar = TipoChar()
                tipoChar.setTipo("OR")
                tipoChar.setValor(ord("|"))
                arrayAcumuladoTokens.append(tipoChar)

        postfixInst = Postfix()
        postfix = postfixInst.toPostfix(arrayAcumuladoTokens)
        cont = 0
        # print("-----------------------------------------------------------------------------------------------------")
        # print("-----------------------------------------------POSTFIX-----------------------------------------------")
        # print("-----------------------------------------------------------------------------------------------------")
        # for token in postfix:
        #     print(cont)
        #     print(token.getTipoChar())
        #     print(type(token.getValor()))
        #     print()
        #     cont +=1
        # print()
        # print()
        # print()

        directoInst = Directo(postfix)
        directoInst.arbolDirecto()

        self.escribirScanner()


        cont = 0
        for key, produccion in self.diccionarioProdFinal.items():
            cont += 1
            print(key)
            # print(produccion)
            postfixInstProd = PostfixProd()
            postfixProd = postfixInstProd.toPostfix(produccion)
            # print(postfixProd)
            for index in postfixProd:
                print(index.getTipoCharProd())
            print()
            print()
            print()
            print()
            # if(cont == 4):
            #     break
    '''

    def lectura(self):
        char = False
        key = False
        tokens = False
        produc = False
        path = str("cocols/" + self.nombreArchivo)
        archivo = open(path, "r+")
        contador = 1
        for linea in archivo.readlines():
            linea = linea.replace("\n", "")
            if(linea[0:8] == "COMPILER"):
                nombre = linea[8:len(linea)]
                self.json[linea[0:8]] = nombre
            elif(linea[0:10] == "IGNORECASE"):
                self.json[linea[0:10]] = {}
                char = False
                key = False
                tokens = False
                produc = False
            elif(linea[0:10] == "CHARACTERS"):
                self.json[linea[0:10]] = {}
                char = True
                key = False
                tokens = False
                produc = False
            elif(linea[0:8] == "KEYWORDS"):
                self.json[linea[0:8]] = {}
                char = False
                key = True
                tokens = False
                produc = False
            elif(linea[0:6] == "TOKENS"):
                self.json[linea[0:6]] = {}
                char = False
                key = False
                tokens = True
                produc = False
            elif(linea[0:11] == "PRODUCTIONS"):
                self.json[linea[0:11]] = {}
                char = False
                key = False
                tokens = False
                produc = True
            elif(linea[0:7] == "PRAGMAS"):
                self.json[linea[0:7]] = {}
                char = False
                key = False
                tokens = False
                produc = False

            if(char):
                arrayChar = linea.split("=")
                if(len(arrayChar) >1):
                    diccionarioChar = self.json["CHARACTERS"]
                    resultado = arrayChar[1]
                    key = str(arrayChar[0].replace(" ", ""))
                    self.characters.append(str(key))
                    if(resultado[len(resultado)-1] == "."):
                        resultado = resultado[0:len(resultado)-1]

                    funciones = Funciones()
                    # Mandar a ordenar independientemente si hay un + o - en la linea
                    resultado = funciones.infixToPostfix(resultado)

                    # Se itera en los characters que ya existen
                    for character in self.characters:
                        # Si es character esta en la linea se sustituye
                        if(character in resultado):
                            if(isinstance(diccionarioChar[character], set)):
                                stringOfSet = ""
                                for char in diccionarioChar[character]:
                                    stringOfSet += char
                                resultado = resultado.replace(character, str(stringOfSet))
                            elif(isinstance(diccionarioChar[character], str)):
                                resultado = resultado.replace(character, diccionarioChar[character])

                    # Si tiene ANY
                    if('ANY' in resultado):
                        strChars = ""
                        for char in range(0, 256):
                            strChars += chr(char)
                        resultado = resultado.replace("ANY", strChars)

                    # Si hay un CHR
                    if("CHR(" in resultado):
                        funciones = Funciones()
                        # verificar si hay + o - y sustituir CHR
                        if("+" in resultado or "-" in resultado):
                            resultado = self.obtenerCHR(resultado)
                            resultado = funciones.operatePostFix(resultado)
                        else:
                            resultado = self.obtenerCHR(resultado)

                    # Si tiene + o -
                    elif("+" in resultado or "-" in resultado):
                        funciones = Funciones()
                        resultado = funciones.operatePostFix(resultado)

                    # Si tiene ..
                    if(".." in resultado):
                        resultado = self.obtenerRangoLetras(resultado)

                    diccionarioChar[key] = resultado

            elif(key):
                arrayKey = linea.split("=")
                if(len(arrayKey) >1):
                    diccionarioKey = self.json["KEYWORDS"]
                    resultado = arrayKey[1].replace(".", "")
                    resultado = resultado.replace('"', "")
                    resultado = resultado.replace(" ", "")
                    var = str(arrayKey[0].replace(" ", ""))
                    diccionarioKey[var] = str(resultado)

            elif(tokens):
                linea = linea.replace(" ", "")
                arrayToken = linea.split("=")
                if(len(arrayToken) >1):
                    diccionarioToken = self.json["TOKENS"]
                    var = str(arrayToken[0].replace(" ", ""))
                    self.tokens.append(var)
                    resultado = arrayToken[1]
                    if(resultado[len(resultado)-1] != "."):
                        resultado = self.defMultiLineaTokens(contador)
                        diccionarioToken[var] = str(resultado)
                    else:
                        diccionarioToken[var] = str(resultado)

            elif(produc and contador not in self.lineasBloqueadas):
                arrayProduc = linea.split("=", 1)
                if(len(arrayProduc) > 1):
                    diccionarioProduc = self.json["PRODUCTIONS"]
                    var = str(arrayProduc[0])
                    var = var.replace("  ", "")
                    varFinal = ""
                    if("<" in var and ">" in var):
                        acumulado = ""
                        for i in var:
                            if(i != "<"):
                                acumulado += i
                            else:
                                varFinal = acumulado.replace(" ", "")
                                self.producciones.append(acumulado.replace(" ", ""))
                                break
                    else:
                        varFinal = var.replace(" ", "")
                        self.producciones.append(var.replace(" ", ""))
                    resultado = arrayProduc[1]
                    if(resultado[len(resultado)-1] != "."):
                        self.lineasBloqueadas.append(contador)
                        resultado = self.defMultiLineaProd(contador)
                    resultado = resultado.replace("  ", "")
                    resultado = resultado.replace("(. ", "(.")
                    resultado = resultado.replace(" .)", ".)")
                    diccionarioProduc[varFinal] = str(resultado)

            contador += 1
        archivo.close()

    def obtenerRangoLetras(self, linea):
        arrayLinea = linea.split("..")
        nuevaLinea = ""
        arrayIntegers = []
        for letra in arrayLinea:
            for char in letra:
                if(char.isalpha()):
                    arrayIntegers.append(ord(char))
                    break

        for char in range(arrayIntegers[0], arrayIntegers[1]+1):
            nuevaLinea += chr(char)

        return nuevaLinea

    def obtenerCHR(self, linea):
        arrayLinea = linea.split(" ")
        arrayPuntos = []
        i = 0

        if(".." in arrayLinea):
            for pos in arrayLinea:
                if(".." in pos):
                    arrayPuntos.append(i)
                i += 1

            for i in arrayPuntos:
                if("CHR(" in arrayLinea[i-1] and "CHR(" in arrayLinea[i+1]):
                    val1 = arrayLinea[i-1].replace("CHR(", "")
                    val1 = val1.replace(")", "")
                    val2 = arrayLinea[i+1].replace("CHR(", "")
                    val2 = val2.replace(")", "")
                    setChars = str(set(chr(char) for char in range (int(val1), int(val2))))
                    setChars = setChars.replace(" ", "")
                    sustituto = "CHR(" + str(val1) + ")" + " .. " + "CHR(" + str(val2) + ")"
                    linea = linea.replace(sustituto, setChars)

        while "CHR(" in linea:
            if("CHR(" in linea):
                pos1 = linea.find("CHR(")
                subStr = linea[pos1:len(linea)]
                pos2 = subStr.find(")")
                val1 = int(subStr[4:pos2])
                strChar = chr(val1)
                sustituto = "CHR(" + str(val1) + ")"
                linea = linea.replace(sustituto, strChar)

        return linea

    def defMultiLineaTokens(self, numeroLinea):
        path = str("cocols/" + self.nombreArchivo)
        archivo = open(path, "r")
        contador = 1
        resultadoToken = ""
        multiLinea = False
        for linea in archivo.readlines():
            linea = linea.replace(" ", "")
            linea = linea.replace("\n", "")
            if(multiLinea):
                if(linea[len(linea)-1] != "."):
                    resultadoToken += linea
                else:
                    resultadoToken += linea
                    break

            if(multiLinea == False and contador == numeroLinea and linea[len(linea)-1] != "."):
                array = linea.split("=")
                resultadoToken += array[1]
                multiLinea = True

            contador += 1

        archivo.close()

        return resultadoToken

    def defMultiLineaProd(self, numeroLinea):
        path = str("cocols/" + self.nombreArchivo)
        archivo = open(path, "r")
        contador = 1
        resultadoProd = ""
        multiLinea = False
        for linea in archivo.readlines():
            linea = linea.replace("\n", "")
            if(multiLinea):
                self.lineasBloqueadas.append(contador)
                if(linea[len(linea)-1] != "."):
                    resultadoProd += linea
                else:
                    resultadoProd += linea
                    break

            if(multiLinea == False and contador == numeroLinea and linea[len(linea)-1] != "."):
                array = linea.split("=", 1)
                resultadoProd += array[1]
                multiLinea = True

            contador += 1

        archivo.close()

        return resultadoProd

    def leerString(self, expresion, diccionario, contador):
        posiAct = 0
        tamanio = len(expresion)
        for char in expresion:
            tipoChar = TipoChar()
            tipoChar.setTipo("STRING")
            valor = {ord(char)}
            tipoChar.setCharacter(valor)
            tipoChar.setValor({ord(char)})
            diccionario[contador] = tipoChar
            contador += 1
            if(posiAct != tamanio-1):
                tipoChar = TipoChar()
                tipoChar.setTipo("APPEND")
                tipoChar.setValor(ord("."))
                diccionario[contador] = tipoChar
                contador += 1
            posiAct += 1

        return diccionario, contador

    def obtenerProduccionCompuesta(self, linea, index, prodSimple):
        produccion = prodSimple
        cont = 0
        for i in linea:
            if(int(cont) > int(index)):
                if(i.isalpha()):
                    self.posBloqueadasTemp.append(cont)
                    produccion += i
                else:
                    break
            cont += 1

        return produccion

    def replaceProduccion(self, acumulado):
        acumulado = acumulado.replace(" ", "")
        acumulado = acumulado.replace(")", "")

        return acumulado

    def primera(self):
        for x in reversed(self.producciones):
            # print(x)
            # print("----")
            soyOR = False
            yaEntreNT = False
            yaEntreT = False
            for index in range(len(self.diccionarioProdFinal[x])):
                # print(index)
                llave = self.diccionarioProdFinal[x][index]
                # print(llave.getTipoCharProd())
                arrayTemp = []
                if llave.getTipo() == "NOTERMINAL":
                    self.primeraPos[x] = self.primeraPos[llave.getValor()]
                    break
                elif llave.getTipo() == "TERMINAL":
                    indexLlave = llave.getValor()
                    # print("indexLlave: " + indexLlave)
                    arrayTemp.append(llave.getValor())
                    self.primeraPos[x] = arrayTemp
                    for i in range(index+1, len(self.diccionarioProdFinal[x])):
                        # print("i actual")
                        # print(self.diccionarioProdFinal[x][i].getTipoCharProd())
                        llave2 = self.diccionarioProdFinal[x][i]
                        if(soyOR and llave2.getTipo() != "ROR"):
                            if(llave2.getTipo() == "NOTERMINAL" and yaEntreNT == False):
                                yaEntreNT = True
                                for primPos in self.primeraPos[llave2.getValor()]:
                                    arrayTemp.append(primPos)
                                    self.primeraPos[x] = arrayTemp
                            if(llave2.getTipo() == "TERMINAL" and yaEntreT == False):
                                yaEntreT = True
                                arrayTemp.append(llave2.getValor())
                                self.primeraPos[x] = arrayTemp
                        elif(llave2.getTipo() == "LOR"):
                            soyOR = True
                        elif(llave2.getTipo() == "ROR"):
                            soyOR = False
                    break
            # print()
            # print()
            # print()
            # print()
        # print(self.primeraPos)


    def construccionProducciones(self):
        diccionarioProd = self.json["PRODUCTIONS"]
        # print(self.producciones)
        # print(self.tokens)
        for key in diccionarioProd:
            # print("key")
            # print(key)
            # print('---')
            definicion = diccionarioProd[key]
            # print(definicion)
            arrayProd = []
            esSintax = False
            esToken = False
            conParams = False
            sintax = ""
            exprecion = ""
            token = ""
            params = ""
            acumulado = ""
            arrayProdTemp = []
            self.posBloqueadasTemp = []
            if("<" in key and ">" in key):
                index1 = key.find("<")
                index2 = key.find(">")
                keyLimpio = key[0:index1]
                parametros = key[index1+1:index2]
                tipoCharProd = TipoCharProd()
                tipoCharProd.setTipo("NOMBRE")
                tipoCharProd.setValor(keyLimpio)
                tipoCharProd.setParametros(parametros)
                arrayProdTemp.append(tipoCharProd)
            else:
                tipoCharProd = TipoCharProd()
                tipoCharProd.setTipo("NOMBRE")
                tipoCharProd.setValor(key)
                arrayProdTemp.append(tipoCharProd)
            for index in range(len(definicion)-1):
                if(index not in self.posBloqueadasTemp):
                    acumulado += definicion[index]
                    # print(acumulado)
                    actual = definicion[index]
                    futuro = definicion[index+1]
                    if(actual == "(" and futuro == "."):
                        self.posBloqueadasTemp.append(index)
                        self.posBloqueadasTemp.append(index+1)
                        esSintax = True
                    elif(actual == "." and futuro == ")"):
                        # print("sintax")
                        # print(sintax)
                        self.posBloqueadasTemp.append(index)
                        self.posBloqueadasTemp.append(index+1)
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("ACTION")
                        tipoCharProd.setValor(sintax)
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(sintax)
                        sintax = ""
                        esSintax = False
                        acumulado = ""
                    elif(esSintax):
                        sintax += definicion[index]
                    elif(actual == "(" and futuro == "$"):
                        self.posBloqueadasTemp.append(index)
                        self.posBloqueadasTemp.append(index+1)
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("LOR")
                        tipoCharProd.setValor("($")
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append("($")
                        acumulado = ""
                    elif(actual == "$" and futuro == ")"):
                        # print("sintax")
                        # print(sintax)
                        self.posBloqueadasTemp.append(index)
                        self.posBloqueadasTemp.append(index+1)
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("ROR")
                        tipoCharProd.setValor("$)")
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append("$)")
                        acumulado = ""
                    elif(actual == "'" or actual == '"'):
                        acumulado = ""
                        if(esToken == False):
                            esToken = True
                        else:
                            # print(token)
                            if(token in self.tokens):
                                numToken = self.tokens.index(token) + 1
                            else:
                                self.tokens.append(token)
                                numToken = len(self.tokens)
                            tipoCharProd = TipoCharProd()
                            tipoCharProd.setTipo("TERMINAL")
                            tipoCharProd.setPrimeraPos(token)
                            tipoCharProd.setValor(token)
                            # print("token: ", token)
                            tipoCharProd.setNumToken(numToken)
                            arrayProdTemp.append(tipoCharProd)
                            token = ""
                            esToken = False
                    elif(esToken):
                        token += definicion[index]
                    elif(conParams == True and actual == ">"):
                        tipoCharProd.setParametros(params)
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(params)
                        conParams = False
                        acumulado = ""
                        params = ""
                    elif(conParams):
                        if(actual != ">" and actual != "<"):
                            params += definicion[index]
                    elif(self.replaceProduccion(acumulado) in self.producciones and not(futuro.isalpha())):
                        acumNuevo = self.replaceProduccion(acumulado)
                        # print(acumNuevo)
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("NOTERMINAL")
                        tipoCharProd.setValor(acumNuevo)
                        if(futuro == "<"):
                            conParams = True
                        else:
                            arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(acumNuevo)
                        acumulado = ""
                    elif(self.replaceProduccion(acumulado) in self.producciones):
                        produccion = self.obtenerProduccionCompuesta(definicion, index, acumulado)
                        produccion = self.replaceProduccion(produccion)
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("NOTERMINAL")
                        tipoCharProd.setValor(produccion)
                        indexProd = definicion.find(produccion)
                        acum = ""
                        contLocal = 0
                        boolLocal = False
                        definicionLocal = definicion[indexProd:len(definicion)]
                        for i in definicionLocal:
                            acum += i
                            contLocal += 1
                            if(acum == produccion):
                                if(definicionLocal[contLocal] == "<"):
                                    conParams = True
                                    boolLocal = True
                        if(boolLocal == False):
                            arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(produccion)
                        acumulado = ""
                    elif(self.replaceProduccion(acumulado) in self.tokens and not(futuro.isalpha())):
                        # print("token")
                        # print(acumulado)
                        acumuladoNuevo = self.replaceProduccion(acumulado)
                        if(acumuladoNuevo in self.tokens):
                            numToken = self.tokens.index(acumuladoNuevo) + 1
                        else:
                            self.tokens.append(acumuladoNuevo)
                            numToken = len(self.tokens)
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("TERMINAL")
                        tipoCharProd.setValor(acumuladoNuevo)
                        tipoCharProd.setPrimeraPos(acumuladoNuevo)
                        # print("token: ", acumulado)
                        tipoCharProd.setNumToken(numToken)
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(acumuladoNuevo)
                        acumulado = ""
                    elif(actual == "["):
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("LENCERRADOC")
                        tipoCharProd.setValor("[")
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(actual)
                        acumulado = ""
                    elif(actual == "]"):
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("RENCERRADOC")
                        tipoCharProd.setValor("]")
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(actual)
                        acumulado = ""
                    elif(actual == "{"):
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("LENCERRADOL")
                        tipoCharProd.setValor("{")
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(actual)
                        acumulado = ""
                    elif(actual == "}"):
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("RENCERRADOL")
                        tipoCharProd.setValor("}")
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(actual)
                        acumulado = ""
                    elif(actual == "|"):
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("OR")
                        tipoCharProd.setValor("|")
                        arrayProdTemp.append(tipoCharProd)
                        arrayProd.append(actual)
                        acumulado = ""
                    elif(actual == "#"):
                        # tipoCharProd = TipoCharProd()
                        # tipoCharProd.setTipo("APPEND")
                        # tipoCharProd.setValor("#")
                        # arrayProdTemp.append(tipoCharProd)
                        # arrayProd.append(actual)
                        acumulado = ""
            arrayLocal =[]
            for objIndex in range(len(arrayProdTemp)):
                actualLocal = arrayProdTemp[objIndex]
                if(objIndex == len(arrayProdTemp)-1):
                    futuroLocal = arrayProdTemp[objIndex]
                else:
                    futuroLocal = arrayProdTemp[objIndex+1]
                arrayLocal.append(actualLocal)
                if(not isinstance(futuroLocal,str)):
                    if(
                        (futuroLocal.getTipo() == "ACTION"
                        or futuroLocal.getTipo() == "TERMINAL"
                        or futuroLocal.getTipo() == "NOTERMINAL")
                        and actualLocal.getTipo() != "OR"
                        and actualLocal.getTipo() != "LOR"
                        and actualLocal.getTipo() != "LENCERRADOC"
                        and actualLocal.getTipo() != "LENCERRADOL"
                        and actualLocal.getTipo() != "NOMBRE"
                        and objIndex != len(arrayProdTemp)-1
                    ):
                        tipoCharProd = TipoCharProd()
                        tipoCharProd.setTipo("APPEND")
                        tipoCharProd.setValor("#")
                        arrayLocal.append(tipoCharProd)
            # print("-----FIN-----")
            # print(key)
            # print("arrayProd")
            # print(arrayProd)
            # print("arrayProdTemp")
            # print(arrayProdTemp)
            # for obj in arrayLocal:
            #     # print(obj)
            #     print(obj.getTipoCharProd())
            # print()
            # print()
            self.diccionarioProdFinal[key] = arrayLocal
        self.primera()
        self.lecturaPrimera()

    def lecturaPrimera(self):
        for key in self.diccionarioProdFinal:
            estoyOr = False
            yaAgregue = False
            definicion = self.diccionarioProdFinal[key]
            # print("key")
            # print(key)
            for objProdIndex in range(len(definicion)):
            #     print(definicion[objProdIndex].getTipoCharProd())
            # print()
            # print()
                objProdActual = definicion[objProdIndex]
                objProdFuturo = ""
                if(objProdIndex != len(definicion)-1):
                    objProdFuturo = definicion[objProdIndex+1]
                if(objProdActual.getTipo() == "LENCERRADOL" and objProdFuturo.getTipo() == "NOTERMINAL"):
                    for i in self.primeraPos[objProdFuturo.getValor()]:
                        objProdActual.setPrimeraPos(i)
                    break
                elif(objProdActual.getTipo() == "LOR" and objProdFuturo.getTipo() == "NOTERMINAL"):
                    for i in self.primeraPos[objProdFuturo.getValor()]:
                        objProdActual.setPrimeraPos(i)
                elif(objProdActual.getTipo() == "LENCERRADOL" and objProdFuturo.getTipo() == "LOR"):
                    for i in range(objProdIndex+1, len(definicion)):
                        if(estoyOr and yaAgregue == False):
                            if(definicion[i].getTipo() == "TERMINAL" or definicion[i].getTipo() == "NOTERMINAL"):
                                yaAgregue == True
                                if(definicion[i].getTipo() == "TERMINAL"):
                                    defi = definicion[i].getPrimeraPos()
                                    for defiPos in defi:
                                        objProdActual.setPrimeraPos(defiPos)
                        elif(definicion[i].getTipo() == "LOR"):
                            estoyOr = True
                        elif(definicion[i].getTipo() == "ROR"):
                            estoyOr = False

                        if(objProdActual.getTipo() == "RENCERRADOL"):
                            break
                elif(objProdActual.getTipo() == "LOR" and objProdFuturo.getTipo() == "TERMINAL"):
                    for i in objProdFuturo.getPrimeraPos():
                        objProdActual.setPrimeraPos(i)
                elif(objProdActual.getTipo() == "LENCERRADOC" and objProdFuturo.getTipo() == "TERMINAL"):
                    for i in objProdFuturo.getPrimeraPos():
                        objProdActual.setPrimeraPos(i)
        # for i, proddd in self.diccionarioProdFinal.items():
        #     print(i)
        #     for prodobj in proddd:
        #         print(prodobj.getTipoCharProd())
        #     print()
        #     print()
        #     print()
        #     print()

    def construccionTokens(self):
        diccionarioToken = self.json["TOKENS"]
        diccionarioCharacters = self.json["CHARACTERS"]
        if("KEYWORDS" in self.json):
            diccionarioKey = self.json["KEYWORDS"]
        esString1 = False
        esString2 = False
        for key in diccionarioToken:
            definicion = diccionarioToken[key]
            keyInterno = ""
            cont = 0
            posicionActual = 0
            nuevoDiccionarioToken = {}
            stringConcat = ""
            finalLinea = 0
            keywords = False

            tipoChar = TipoChar()
            tipoChar.setTipo("PARENTESIS_INICIAL")
            tipoChar.setValor(ord("("))
            nuevoDiccionarioToken[cont] = tipoChar
            cont += 1

            if("EXCEPTKEYWORDS" in definicion.upper()):
                keywords = True
                finalLinea = definicion.upper().find("EXCEPTKEYWORDS")

            for char in definicion:
                if(char != " "):
                    keyInterno += char

                    if(char == '"' and esString2 == False):
                        keyInterno = ""
                        if(esString1 == True):
                            nuevoDiccionarioToken, cont = self.leerString(stringConcat, nuevoDiccionarioToken, cont)
                            if(posicionActual != len(definicion)-1
                                and definicion[posicionActual+1] != "."
                                and definicion[posicionActual+1] != "|"
                                and definicion[posicionActual+1] != "]"
                                and definicion[posicionActual+1] != "}"
                                and definicion[posicionActual+1] != ")"
                                and (posicionActual+1 < finalLinea
                                or finalLinea == 0)
                            ):
                                tipoChar = TipoChar()
                                tipoChar.setTipo("APPEND")
                                tipoChar.setValor(ord("."))
                                nuevoDiccionarioToken[cont] = tipoChar
                                cont += 1
                            stringConcat = ""
                            esString1 = False
                        else:
                            esString1 = True
                    elif(char == "'" and esString1 == False):
                        keyInterno = ""
                        if(esString2 == True):
                            nuevoDiccionarioToken, cont = self.leerString(stringConcat, nuevoDiccionarioToken, cont)
                            if(posicionActual != len(definicion)-1
                                and definicion[posicionActual+1] != "."
                                and definicion[posicionActual+1] != "|"
                                and definicion[posicionActual+1] != "]"
                                and definicion[posicionActual+1] != "}"
                                and definicion[posicionActual+1] != ")"
                                and (posicionActual+1 < finalLinea
                                or finalLinea == 0)
                            ):
                                tipoChar = TipoChar()
                                tipoChar.setTipo("APPEND")
                                tipoChar.setValor(ord("."))
                                nuevoDiccionarioToken[cont] = tipoChar
                                cont += 1
                            stringConcat = ""
                            esString2 = False
                        else:
                            esString2 = True
                    elif(str(keyInterno) in self.characters):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("CHARACTER")
                        setChar = diccionarioCharacters[keyInterno]
                        if(isinstance(diccionarioCharacters[keyInterno], set)):
                            setChar = set(ord(str(char)) for char in diccionarioCharacters[keyInterno])
                        tipoChar.setValor(setChar)
                        tipoChar.setCharacter(keyInterno)
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                        if(posicionActual != len(definicion)-1
                            and definicion[posicionActual+1] != "."
                            and definicion[posicionActual+1] != "|"
                            and definicion[posicionActual+1] != "}"
                            and definicion[posicionActual+1] != ")"
                            and definicion[posicionActual+1] != "]"
                            and (posicionActual+1 < finalLinea
                            or finalLinea == 0)
                        ):
                            tipoChar = TipoChar()
                            tipoChar.setTipo("APPEND")
                            tipoChar.setValor(ord("."))
                            nuevoDiccionarioToken[cont] = tipoChar
                            cont += 1
                    elif(esString1 or esString2):
                        keyInterno = ""
                        stringConcat += char
                    elif(char == "{"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_INICIAL")
                        tipoChar.setValor(ord("("))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                    elif(char == "}"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_FINAL")
                        tipoChar.setValor(ord(char))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        tipoChar = TipoChar()
                        tipoChar.setTipo("KLEENE")
                        tipoChar.setValor(ord(")"))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        if(posicionActual != len(definicion)-1
                            and definicion[posicionActual+1] != "."
                            and definicion[posicionActual+1] != "|"
                            and definicion[posicionActual+1] != "]"
                            and definicion[posicionActual+1] != ")"
                            and definicion[posicionActual+1] != "}"
                            and (posicionActual+1 < finalLinea
                            or finalLinea == 0)
                        ):
                            tipoChar = TipoChar()
                            tipoChar.setTipo("APPEND")
                            tipoChar.setValor(ord("."))
                            nuevoDiccionarioToken[cont] = tipoChar
                            cont += 1
                        keyInterno = ""
                    elif(char == "("):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_INICIAL")
                        tipoChar.setValor(ord(char))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                    elif(char == ")"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_FINAL")
                        tipoChar.setValor(ord(char))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        if(posicionActual != len(definicion)-1
                            and definicion[posicionActual+1] != "."
                            and definicion[posicionActual+1] != "|"
                            and definicion[posicionActual+1] != "]"
                            and definicion[posicionActual+1] != ")"
                            and definicion[posicionActual+1] != "}"
                            and (posicionActual+1 < finalLinea
                            or finalLinea == 0)
                        ):
                            tipoChar = TipoChar()
                            tipoChar.setTipo("APPEND")
                            tipoChar.setValor(ord("."))
                            nuevoDiccionarioToken[cont] = tipoChar
                            cont += 1
                        keyInterno = ""
                    elif(char == "["):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_INICIAL")
                        tipoChar.setValor(ord("("))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                    elif(char == "]"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("OR")
                        tipoChar.setValor(ord("|"))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        tipoChar = TipoChar()
                        tipoChar.setTipo("EPSILON")
                        valor = {ord("ɛ")}
                        tipoChar.setCharacter(valor)
                        # tipoChar.setCharacter(set(str(ord("ɛ"))))
                        tipoChar.setValor(ord("ɛ"))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        tipoChar = TipoChar()
                        tipoChar.setTipo("PARENTESIS_FINAL")
                        tipoChar.setValor(ord(")"))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        if(posicionActual != len(definicion)-1
                            and definicion[posicionActual+1] != "."
                            and definicion[posicionActual+1] != "|"
                            and definicion[posicionActual+1] != "]"
                            and definicion[posicionActual+1] != ")"
                            and definicion[posicionActual+1] != "}"
                            and (posicionActual+1 < finalLinea
                            or finalLinea == 0)
                        ):
                            tipoChar = TipoChar()
                            tipoChar.setTipo("APPEND")
                            tipoChar.setValor(ord("."))
                            nuevoDiccionarioToken[cont] = tipoChar
                            cont += 1
                        keyInterno = ""
                    elif(char == "|"):
                        tipoChar = TipoChar()
                        tipoChar.setTipo("OR")
                        tipoChar.setValor(ord(char))
                        nuevoDiccionarioToken[cont] = tipoChar
                        cont += 1
                        keyInterno = ""
                posicionActual += 1
            tipoChar = TipoChar()
            tipoChar.setTipo("APPEND")
            tipoChar.setValor(ord("."))
            nuevoDiccionarioToken[cont] = tipoChar
            cont += 1
            tipoChar = TipoChar()
            tipoChar.setTipo("ACEP")
            tipoChar.setCharacter(key)
            tipoChar.setValor(ord("#"))
            if(keywords):
                tipoChar.setKeywords(diccionarioKey)
            nuevoDiccionarioToken[cont] = tipoChar
            cont += 1
            tipoChar = TipoChar()
            tipoChar.setTipo("PARENTESIS_FINAL")
            tipoChar.setValor(ord(")"))
            nuevoDiccionarioToken[cont] = tipoChar
            cont += 1
            diccionarioToken[key] = nuevoDiccionarioToken

            # print("----------------------------------------------------------------------------------------------------")
            # print("-----------------------------------------------Tokens-----------------------------------------------")
            # print("----------------------------------------------------------------------------------------------------")
            # print(key)
            # print(diccionarioToken[key])
            # for id, tipo in diccionarioToken[key].items():
            #     print(id)
            #     print(tipo.getTipoChar())
            #     print(type(tipo.getValor()))
            # print()
            # print()
            # print()

    def escribirScanner(self):
        f = open("scanner.py", "w", encoding="utf8")
        f.write(
            """

import pickle5 as pickle
import pprint
from tokenScanner import *

class Scanner:
    def __init__(self, documentoALeer):
        self.diccioAceptacion = {}
        self.pilaFinal = []
        self.cadenaALeer = ""
        self.nombreDocALeer = documentoALeer
        self.print = pprint.PrettyPrinter()
        self.tokensLeidos = []

    def main(self):
        self.openFiles()

        with open(self.nombreDocALeer, "r") as f:
            self.cadenaALeer = f.read()
        f.close()

        self.simular()

        file = open("tokensLeidos", 'wb')
        pickle.dump(self.tokensLeidos, file)
        file.close()

    def openFiles(self):
        file = open("pilaFinal", "rb")
        self.pilaFinal = pickle.load(file)
        file.close()

        file = open("diccioAceptacion", "rb")
        self.diccioAceptacion = pickle.load(file)
        file.close()


    def getStateNumber(self, array):
        for valor in self.pilaFinal:
            if(valor[1] == array):
                return valor[0]

    def mover(self, estados, caracter):
        array = []
        for estado in estados:
            for transicion in self.pilaFinal:
                for i in transicion[2]:
                    if(
                        ord(caracter) == i
                        and len(transicion[3]) > 0
                        and estado == transicion[0]
                    ):
                        estadoSiguiente = self.getStateNumber(transicion[3])
                        if(estadoSiguiente not in array):
                            array.append(estadoSiguiente)

        return array

    def getToken(self, estados, acumulado):
        token = ""
        for transicion in self.pilaFinal:
            for estado in estados:
                if(estado == transicion[0]):
                    for estadoInd in transicion[1]:
                        for key, valor in self.diccioAceptacion.items():
                            if(int(estadoInd) == int(key)):
                                if(len(valor) > 1):
                                    for key2, valor2, in valor[1].items():
                                        if(str(acumulado) == str(key2)):
                                            token = valor2
                                            break
                                        else:
                                            token = valor[0]
                                else:
                                    token = valor[0]

                                return token

        return token

    def simular(self):
        cadena = []
        s = [0]
        s2 = [0]
        cont = 0
        tokenDef = ""
        for i in self.cadenaALeer:
            cadena.append(i)
        cadena.append(" ")

        while len(cadena) > 0:
            # Si no se esta en el ultimo caracter de la cadena
            if(cont == len(self.cadenaALeer)-1):
                char = self.cadenaALeer[cont]
                tokenDef += char
                s = self.mover(s, char)
                token = self.getToken(s, tokenDef)
                if(len(token) == 0):
                    self.print.pprint("La cadena ---" + str(tokenDef) + "--- es un token invalido!")
                    break
                self.print.pprint("El token es: --" + str(token) + "-- para la cadena: " + str(tokenDef))
                tokenScanner = TokenScanner()
                tokenScanner.setTipo(token)
                tokenScanner.setValor(tokenDef)
                self.tokensLeidos.append(tokenScanner)
                break

            char1 = self.cadenaALeer[cont]
            char2 = self.cadenaALeer[cont+1]
            tokenDef += char1
            s = self.mover(s, char1)
            s2 = self.mover(s, char2)

            # Si el caracter siguiente no tiene transicion,
            # pero el caracter  actual si
            if(len(s2) == 0 and len(s) > 0):
                token = self.getToken(s, tokenDef)
                # Si se encontro un token
                if(len(token) == 0):
                    self.print.pprint("La cadena ---" + tokenDef + "--- es un token invalido!")
                    s = [0]
                    s2 = [0]
                    tokenDef = ""
                    cont -= 1
                else:
                    self.print.pprint("El token es: --" + str(token) + "-- para la cadena: " + str(tokenDef))
                    tokenScanner = TokenScanner()
                    tokenScanner.setTipo(token)
                    tokenScanner.setTipo(setValor)
                    self.tokensLeidos.append(tokenScanner)
                    s = [0]
                    s2 = [0]
                    tokenDef = ""
            # Si no hay transicion
            elif(len(s) == 0):
                self.print.pprint("La cadena ---" + tokenDef + "--- es un token invalido!")
                s = [0]
                s2 = [0]
                tokenDef = ""

            cont += 1
            cadena.pop()

def menu():
    nombre = str(input("Ingrese el nombre del archivo que desea leer: "))

    main = Scanner(nombre)
    main.main()

menu()
            """
        )


def menu():
    # nombre = str(input("Ingrese el nombre del archivo Cocol que desea leer: "))

    main = Main("Expr.ATG")
    main.main()

menu()