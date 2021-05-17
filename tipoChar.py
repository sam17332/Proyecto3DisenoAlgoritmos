class TipoChar:
    def __init__(self):
        self.tipo = ""
        self.valor = ""
        self.character = ""
        self.keywords = ""

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getCharacter(self):
        return self.character

    def setCharacter(self, character):
        self.character = character

    def getKeywords(self):
        return self.keywords

    def setKeywords(self, keywords):
        self.keywords = keywords

    def getTipoChar(self):
        return [self.tipo, self.valor, self.character]