class TipoCharProd:
    def __init__(self):
        self.tipo = ""
        self.valor = ""
        self.numToken = ""
        self.parametros = ""
        self.primeraPos = []

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getNumToken(self):
        return self.numToken

    def setNumToken(self, numToken):
        self.numToken = numToken

    def getParametros(self):
        return self.parametros

    def setParametros(self, param):
        self.parametros = param

    def getPrimeraPos(self):
        return self.primeraPos

    def setPrimeraPos(self, pos):
        if(pos not in self.primeraPos):
            self.primeraPos.append(pos)

    def getTipoCharProd(self):
        return [self.tipo, self.valor, self.numToken, self.parametros, self.primeraPos]
