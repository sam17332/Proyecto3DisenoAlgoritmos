class NodoD:
    def __init__(self):
        self.nodoId = ""
        self.anulable = True
        self.primeraPos = []
        self.ultimaPos = []
        self.caracter = ""
        self.siguientePos = ""

    def getId(self):
        return self.nodoId

    def setId(self, nodoId):
        self.nodoId = nodoId

    def getAnulable(self):
        return self.anulable

    def setAnulable(self, anulable):
        self.anulable = anulable

    def getPrimeraPos(self):
        return self.primeraPos

    def setPrimeraPos(self, primeraPos):
        self.primeraPos = primeraPos

    def getUltimaPos(self):
        return self.ultimaPos

    def setUltimaPos(self, ultimaPos):
        self.ultimaPos = ultimaPos

    def getChar(self):
        return self.caracter

    def setChar(self, caracter):
        self.caracter = caracter

    def getSiguientePos(self):
        return self.siguientePos

    def setSiguientePos(self, siguientePos):
        self.siguientePos = siguientePos

    def getNodo(self):
        return [self.nodoId, self.anulable, self.primeraPos, self.ultimaPos, self.caracter]