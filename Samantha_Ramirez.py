disps = ['I', 'D', 'S']
blank = '~'

class Transition:
    def __init__(self, id, fromState, toState, readInString, writeInString, disp):
        self._id = id
        self._fromState = fromState
        self._toState = toState
        self._readInString = readInString
        self._writeInString = writeInString
        self._disp = disp if disp in disps else 'S'

class TestCase:
    def __init__(self, id, N, T):
        self._id = id
        self._tape = list()
        self._currentPositionInTape = 0
        self._currentState = 0
        self._finalState = N - 1
        self._N = N if N >= 1 else 1 # cantidad de estados
        self._T = T if T >= 0 else 0 # cantidad de transiciones
        self._symbols = list()
        self._transitions = dict()
        self._string = ''
    
    def getCurrentPositionInTape(self): return self._currentPositionInTape

    def getTape(self): return self._tape
    
    def getSymbols(self): return self._symbols

    def getString(self): return self._string
    
    def getTransitions(self): return self._transitions
    
    def getCurrentState(self): return self._currentState

    def getFinalState(self): return self._finalState

    def setState(self, state): self._currentState = state if state < self._N else self._currentState
    
    def setCurrentPositionInTape(self, disp):
        if disp == 'D':
            # si se mueve a la derecha
            ## append ~
            ## mover index
            if not self.isCurrentPositionValid(self.getCurrentPositionInTape() + 1):
                self.getTape().append(blank)
            self._currentPositionInTape = self.getCurrentPositionInTape() + 1
                
        elif disp == 'I':
            # si se mueve a la izquierda 
            if self.isCurrentPositionValid(self.getCurrentPositionInTape() - 1):
                self._currentPositionInTape = self.getCurrentPositionInTape() - 1
            else:
                ## insert ~ de primero
                ## no mover index
                self.getTape().insert(0, blank)

        # else es S / disp no valido / posicion no valida
    
    def setCharInCurrentPositionInTape(self, writeInString):
        self.getTape()[self.getCurrentPositionInTape()] = writeInString
    
    def initTape(self):
        for i in self.getString():
            self.getTape().append(i)
        
        self.printCurrentTape()

    def isCurrentPositionValid(self, pos):
        if pos >= 0 and pos < len(self.getTape()):
            return True
        return False

    def isStringAccepted(self):
        if self.getCurrentState() == self.getFinalState():
            print("Aceptada")
        else:
            print("Rechazada")
    
    def addSymbol(self, symbol):
        self.getSymbols().append(symbol)

    def addTransitions(self, id, fromState, toState, readInString, writeInString, disp):
        transition = Transition(id, fromState, toState, readInString, writeInString, disp)
        self.getTransitions().update({transition._id:transition})

    def useTransition(self, transition):
        # cambiar estado
        self.setState(transition._toState)

        # cambiar caracter
        self.setCharInCurrentPositionInTape(transition._writeInString)

        # cambiar cabecera 
        self.setCurrentPositionInTape(transition._disp)

        # imprimir resultado
        self.printCurrentTape()
    
    def searchTransition(self):
        for key, value in self.getTransitions().items():
            if value._fromState == self.getCurrentState() and value._readInString == self.getTape()[self.getCurrentPositionInTape()]:
                return value
        return False
    
    def evaluateString(self):
        # cinta inicial es cadena
        self.initTape()

        # obtener transition
        transition = self.searchTransition()

        while transition:
            # usar transicion
            self.useTransition(transition)

            # obtener transicion
            transition = self.searchTransition()
        
        # imprimir Aceptada o Rechazada
        self.isStringAccepted()        
        
    def printCurrentTape(self):
        for i in self.getTape():
            if i != blank:
                print(i, end="")
        print("")
        
    def printSolution(self):
        print("Caso " + str(self._id) + ":")
        self.evaluateString()
        print("")

class TuringMachine:
    def __init__(self):
        self._numTestCases = 0
        self._testCases = dict()
    
    def getTestCases(self): return self._testCases
    
    def getInput(self): 
        # numero C de casos prueba
        text = input()
        self._numTestCases = int(text[0])

        for i in range(1, self._numTestCases+1):
           
            # cantidad N de estados 
            # cantidad T de transiciones
            text = input().split(" ")
            # crear Caso prueba           
            Test = TestCase(i, int(text[0]), int(text[1]))

            # simbolos de cinta separados por espacio
            text = input().split(" ")
            for i in range(0, len(text)):
                # agregar simbolo
                Test.addSymbol(text[i])

            # T transiciones OFLED 
            for i in range(0, Test._T):
                text = input().split(" ")
                Test.addTransitions(i, int(text[0]), int(text[1]), text[2], text[3], text[4])
            
            # cadena a evaluar
            text = input()
            Test._string = text
            
            # agregar caso a MT
            self.addTestCase(Test)

    def addTestCase(self, Test):
        self._testCases.update({Test._id:Test})

    def printSolution(self):
        for key, i in self.getTestCases().items():
            i.printSolution()
    
Machine = TuringMachine()
Machine.getInput()
Machine.printSolution()