from tipoChar import *

class PostfixProd:
    def __init__(self):
        self.precedencia = {'OR': 1,'APPEND': 2}  # Diccionario de precedencia
        self.top = -1 # Contador
        self.operadores = ["OR", "APPEND", "LENCERRADOL", "RENCERRADOL", "LOR", "ROR", "LENCERRADOC", "RENCERRADOC"]  # Diccionario operadores
        self.opeArr = [] # Array usado como pila
        self.pstFx = [] # Array donde se van concatenando
        self.concat = '' # String donde se va concatenando

    def vacio(self):
        return True if self.top == -1 else False

    # Funcion para verificar si el caracter es un operador
    def isOperador(self, ope):
        if ope.getTipo() == 'OR' or ope.getTipo() == 'APPEND':
            return True
        return False

    # Se agrega el elemnento
    def push(self, op):
        self.top += 1
        self.opeArr.append(op)

    # Funcion para verificar que el caracter no sea un operador
    def notOperador(self, char):
        if char.getTipo() == 'NOTERMINAL' or char.getTipo() == 'TERMINAL' or char.getTipo() == 'ACTION':
            return True
        return False

    # Retorna el valor de hasta arriba de la pila
    def stack(self):
        return self.opeArr[-1]

    # Hace pop de el ultimo elemento de la pila
    def pop(self):
        if not self.vacio():
            self.top -= 1
            return self.opeArr.pop()
        else:
            return "$"

     # Funcion para obtener que caracter tiene mas precedencia
    def masPrecedencia(self, i):
        a = self.precedencia[i.getTipo()]
        b = self.precedencia[self.stack().getTipo()]

        return True if a <= b else False

     # Funcion para armar el postfix
    def toPostfix(self, exp):
        for i in exp:
            # print(i.getTipo())
            if i.getTipo() == "NOMBRE":
                self.pstFx.append(i)
            elif self.notOperador(i):
                self.pstFx.append(i)
            elif self.isOperador(i):
                while len(self.opeArr) > 0 and self.opeArr[-1].getTipo() != 'LENCERRADOL' and self.opeArr[-1].getTipo() != 'LOR' and self.opeArr[-1].getTipo() != 'LENCERRADOC' and self.masPrecedencia(i):
                    top = self.pop()
                    self.pstFx.append(top)
                self.push(i)
            elif(i.getTipo() == "LENCERRADOL"
                    or i.getTipo() == "LOR"
                    or i.getTipo() == "LENCERRADOC"
                ):
                self.pstFx.append(i)
                self.push(i)
            # Si i es un ")"
            elif(i.getTipo() == "RENCERRADOL"
                    or i.getTipo() == "ROR"
                    or i.getTipo() == "RENCERRADOC"
                ):
                if(self.concat != ''):
                    self.pstFx.append(self.concat)
                    self.concat = ''
                # Mientras no esté vacío y sea diferente a "("
                while((not self.vacio()) and self.stack().getTipo() != 'LENCERRADOL' and self.opeArr[-1].getTipo() != 'LOR' and self.opeArr[-1].getTipo() != 'LENCERRADOC'):
                    a = self.pop()
                    self.pstFx.append(a)
                    if(a == ""):
                        print("No hay signo de cerrado de paréntesis")

                        return -1
                self.pstFx.append(i)
                # Si no está vacío y es diferente a "("
                if (not self.vacio() and self.stack().getTipo() != 'LENCERRADOL'  and self.opeArr[-1].getTipo() != 'LOR' and self.opeArr[-1].getTipo() != 'LENCERRADOC'):
                    return -1
                else:
                    self.pop()
            else:
                while(not self.vacio() and self.masPrecedencia(i)):
                    self.pstFx.append(self.pop())
                self.push(i)
        if(self.concat != ''):
            self.pstFx.append(self.concat)

        while len(self.opeArr):
            caracter = self.pop()
            if caracter == "LENCERRADOL" or caracter == "LOR" or caracter == "LENCERRADOC" :
                print("Hace falta un ')'")
            self.pstFx.append(caracter)

        return self.pstFx
