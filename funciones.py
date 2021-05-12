class Funciones:
    def __init__(self):
        self.top = -1
        self.arrayOperandos = []
        self.outputPostfix = []
        self.precedencia = {'+': 1, '-': 1, }
        self.stack2 = []
        self.top2 = -1
        self.concatenado = ''

    def is_op(self, a):
        if a == '+' or a == '-':
            return True
        return False

    def isEmpty(self):
        return True if self.top == -1 else False

    def peekTopOfStack(self):
        return self.arrayOperandos[-1]

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.arrayOperandos.pop()
        else:
            return "$"

    def pop2(self):
        if self.top2 == -1:
            return
        else:
            self.top2 -= 1
            return self.stack2.pop()

    def push2(self, i):
        self.top2 += 1
        self.stack2.append(i)

    def push(self, op):
        self.top += 1
        self.arrayOperandos.append(op)

    def isOperando(self, ch):
        if ch != '+' and ch != '-':
            return True
        return False

    def mayorPrecedencia(self, i):
        try:
            a = self.precedencia[i]
            b = self.precedencia[self.peekTopOfStack()]
            return True if a <= b else False
        except KeyError:
            return False

    def infixToPostfix(self, exp):
        exp = exp.replace(" ", "")

        for i in exp:
            if self.isOperando(i):
                self.concatenado = str(self.concatenado+i)
            elif self.is_op(i):
                if(self.concatenado != ''):
                    self.outputPostfix.append(self.concatenado)
                    self.concatenado = ''
                while len(self.arrayOperandos) > 0 and self.arrayOperandos[-1] != '(' and self.mayorPrecedencia(i):
                    top = self.pop()
                    self.outputPostfix.append(top)
                self.push(i)
            elif i == '(':
                self.push(i)
            elif i == ')':
                if(self.concatenado != ''):
                    self.outputPostfix.append(self.concatenado)
                    self.concatenado = ''
                while((not self.isEmpty()) and self.peekTopOfStack() != '('):
                    a = self.pop()
                    self.outputPostfix.append(a)
                    if len(a) == 0:
                        print("No hay signo de cerrado de paréntesis")
                        return -1
                if (not self.isEmpty() and self.peekTopOfStack() != '('):
                    return -1
                else:
                    self.pop()
            else:
                while(not self.isEmpty() and self.mayorPrecedencia(i)):
                    self.outputPostfix.append(self.pop())
                self.push(i)

        if(self.concatenado != ''):
            self.outputPostfix.append(self.concatenado)

        while len(self.arrayOperandos):
            caracter = self.pop()
            if caracter == "(":
                print("Hay un signo de paréntesis abierto de más")
                exit(-1)
            self.outputPostfix.append(caracter)

        resultado = " ".join(self.outputPostfix)

        if("..CHR(" in resultado):
            resultado = resultado.replace("..CHR(", " .. CHR(")

        return resultado

    def operatePostFix(self, expresion):
        arrayLocal = expresion.split(" ")

        for i in arrayLocal:
            resultado = ""
            strLocal = ""
            if(self.isOperando(i)):
                for j in i:
                    strLocal += j
                self.push2(strLocal)
            else:
                val1 = self.getStringInQuotes(self.pop2())
                val2 = self.getStringInQuotes(self.pop2())

                val1 = set(val1)
                val2 = set(val2)

                if(i == "+"):
                    resultado = val1 | val2
                elif(i == "-"):
                    resultado = val2 - val1

                self.push2(resultado)

        operacion = self.pop2()

        return operacion

    def getStringInQuotes(self, exp):
        contSimples = 0
        contDobles = 0
        for i in exp:
            if(i == "'"):
                contSimples += 1
            elif(i == '"'):
                contDobles += 1

        if(contDobles >= 2 and contSimples < 2):
            exp = exp.replace('"', "")
        elif(contSimples >= 2 and contDobles < 2):
            exp = exp.replace("'", '')

        return exp

    def getIfString(self, exp):
        contSimples = 0
        contDobles = 0
        isString = False

        if(isinstance(exp, str)):
            for i in exp:
                if(i == "'"):
                    contSimples += 1
                elif(i == '"'):
                    contDobles += 1

            if(contDobles == 2 and contSimples <= 1):
                isString = True
            elif(contSimples == 2 and contDobles <= 1):
                isString = True

        return isString