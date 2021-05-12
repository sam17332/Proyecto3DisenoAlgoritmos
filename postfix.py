from tipoChar import *

class Postfix:
    def __init__(self):
        self.precedencia = {'OR': 1,'APPEND': 2, 'KLEENE': 3}  # Diccionario de precedencia
        self.top = -1 # Contador
        self.operadores = ["OR", "APPEND", "KLEENE", "PARENTESIS_INICIAL", "PARENTESIS_FINAL"]  # Diccionario operadores
        self.opeArr = [] # Array usado como pila
        self.pstFx = [] # Array donde se van concatenando
        self.concat = '' # String donde se va concatenando

    def vacio(self):
        return True if self.top == -1 else False

    # Funcion para verificar si el caracter es un operador
    def isOperador(self, ope):
        if ope.getTipo() == 'OR' or ope.getTipo() == 'APPEND' or ope.getTipo() == 'KLEENE':
            return True
        return False

    # Se agrega el elemnento
    def push(self, op):
        self.top += 1
        self.opeArr.append(op)

    # Funcion para verificar que el caracter no sea un operador
    def notOperador(self, char):
        if char.getTipo() == 'CHARACTER' or char.getTipo() == 'EPSILON' or char.getTipo() == 'ACEP' or char.getTipo() == 'STRING':
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
        # Iteramos la exprecion
        for i in exp:
            if self.notOperador(i):
                self.pstFx.append(i)
            elif self.isOperador(i):
                while len(self.opeArr) > 0 and self.opeArr[-1].getTipo() != 'PARENTESIS_INICIAL' and self.masPrecedencia(i):
                    top = self.pop()
                    self.pstFx.append(top)
                self.push(i)
            elif i.getTipo() == 'PARENTESIS_INICIAL':
                self.push(i)
            # Si i es un ")"
            elif i.getTipo() == 'PARENTESIS_FINAL':
                if(self.concat != ''):
                    self.pstFx.append(self.concat)
                    self.concat = ''
                # Mientras no esté vacío y sea diferente a "("
                while((not self.vacio()) and self.stack().getTipo() != 'PARENTESIS_INICIAL'):
                    a = self.pop()
                    self.pstFx.append(a)
                    if(a == ""):
                        print("No hay signo de cerrado de paréntesis")

                        return -1
                # Si no está vacío y es diferente a "("
                if (not self.vacio() and self.stack().getTipo() != 'PARENTESIS_INICIAL'):
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
            if caracter == "PARENTESIS_INICIAL":
                print("Hace falta un ')'")
            self.pstFx.append(caracter)

        return self.pstFx
