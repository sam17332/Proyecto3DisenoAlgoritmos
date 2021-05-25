class TokenScanner:
    def __init__(self):
        self.tipo = ""
        self.valor = ""
        self.id = ""

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getTokenScanner(self):
        return [self.tipo, self.valor, self.id]
