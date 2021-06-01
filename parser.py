
import pickle

class Parser():
    def __init__(self):
        self.tokensScaneados = ""
        self.tokensMapeados = ""
        self.lastToken = ""
        self.lookAheadToken = ""

    def main(self):
        self.leerTokensAndMap()
        self.ParserFunc()

    def leerTokensAndMap(self):
        file = open("tokensLeidos", 'rb')
        self.tokensScaneados = pickle.load(file)
        file.close()

        file = open("diccionarioTokensLeidos", 'rb')
        self.tokensMapeados = pickle.load(file)
        file.close()

        print(self.tokensMapeados)

        for x in range(len(self.tokensScaneados)):
            if(self.tokensScaneados[x].getID() != ""):
                self.tokensScaneados.append(self.tokensScaneados[x])

    def Expect(self, tokenId):
        if(self.lookAheadToken.getID() == tokenId):
            self.GetNewToken()
        else:
            self.printERROROnScreen(tokenId)

    def GetNewToken(self):
        self.lastToken = self.lookAheadToken
        if(len(self.tokensScaneados) > 0):
            self.lookAheadToken = self.tokensScaneados.pop(0)
        else:
            self.lookAheadToken = self.lookAheadToken

    def getNumber(self):
        if(self.lookAheadToken.getValor() != "+" and self.lookAheadToken.getValor() != "-" and self.lookAheadToken.getValor() != "*" and self.lookAheadToken.getValor() != "/" and self.lookAheadToken.getValor() != ";"):
            return int(self.lastToken.getValor())
        else:
            return self.lastToken.getValor()

    def getVar(self):
        return self.lookAheadToken.getValor()

        
    def Expr (self):
        self.StatSeq()

    def StatSeq (self):
        while self.lookAheadToken.getID() == 5 or self.lookAheadToken.getID() == 2 or self.lookAheadToken.getID() == 8:
            self.Stat()
            self.Expect(3)


    def Stat (self):
        value = 0
        value = self.Expression(value)
        print("El valor final es: " + str(value))

    def Expression(self, result):
        result1 , result2 = 0, 0
        result1 = self.Term(result1)
        while self.lookAheadToken.getID() == 4 or self.lookAheadToken.getID() == 5:
            if(self.lookAheadToken.getID() == 4):
                self.Expect(4)
                result2 = self.Term(result2)
                result1 = int(result1)
                result2 = int(result2)
                result1 += result2

            elif(self.lookAheadToken.getID() == 5):
                self.Expect(5)
                result2 = self.Term(result2)
                result1 = int(result1)
                result2 = int(result2)
                result1 -= result2


        result = result1
        return result

    def Term(self, result):
        result1 , result2 = 1, 1
        result1 = self.Factor(result1)
        while self.lookAheadToken.getID() == 6 or self.lookAheadToken.getID() == 7:
            if(self.lookAheadToken.getID() == 6):
                self.Expect(6)
                result2 = self.Factor(result2)
                result1 = int(result1)
                result2 = int(result2)
                result1 *= result2

            elif(self.lookAheadToken.getID() == 7):
                self.Expect(7)
                result2 = self.Factor(result2)
                result1 = int(result1)
                result2 = int(result2)
                result1 /= result2


        result = result1
        return result

    def Factor(self, result):
        sign = 1
        if(self.lookAheadToken.getID() == 5):
            self.Expect(5)
            sign = -1

        if(self.lookAheadToken.getID() == 2):
            result = self.Number(result)
            result *= sign

        elif(self.lookAheadToken.getID() == 8):
            self.Expect(8)
            result = self.Expression(result)
            self.Expect(9)
            result *= sign

        return result

    def  Number(self, result):
        self.Expect(2)
        result = self.getNumber()
        return result


    def ParserFunc(self):
        self.GetNewToken()
        self.Expr()

    def printERROROnScreen(self, tokenId):
        for x in self.tokensScaneados:
            if(x.getID() == tokenId):
                if(x.getTipoToken() == "ERROR"):
                    errorPrint = x.getValor()
                    print(f'{errorPrint} expected')
                elif(x.getTipoToken() != "ERROR"):
                    errorPrint = x.getTipoToken()
                    print(f'{errorPrint} expected')

def menu():
    obj = Parser()
    obj.main()

menu()
        