class contexMatrix():

    mainMatix = []
    auxiliarList = []
    AmountOfLittleThreads = 0
    nextThreat = 0

    def __init__(self, totalNumberThreads):
        self.AmountOfLittleThreads = totalNumberThreads
        for rows in range(self.AmountOfLittleThreads):
            #Se llenan 35 espacios que son: la direccion de memoria, los 32 registros, el identificador del hilo y el estado del hilo
            for colums in range(35):
                self.auxiliarList.append(0)
            self.mainMatix.append(self.auxiliarList)
            self.auxiliarList = []

    def showContextMatrix(self):
        print(" Dir  R0 R1 R2 R3 R4 R5 R6 R7 R8 R9 R0 R1 R2 R3 R4 R5 R6 R7 R8 R9 R0 R1 R2 R3 R4 R5 R6 R7 R8 R9 R0 R1 Thr stat")
        for row in range(self.AmountOfLittleThreads):
            print(str(self.mainMatix[row]))

    def getInstrDirectInMemory(self, thread):
        directionInMem = 0
        for i in range(self.AmountOfLittleThreads):
            #La posición 33 de todas las filas contiene el identificador del hilo
            if self.mainMatix[i][33] == thread:
                #La posición 1 de todas las filas contiene la dirección en memoria del hilillo.
                directionInMem = self.mainMatix[i][0]
        return directionInMem

    def setConditionOfLittleThread(self, thread, condition):
        for i in range(self.AmountOfLittleThreads):
            #La posición 33 de todas las filas contiene el identificador del hilo
            if self.mainMatix[i][33] == thread:
                #La posición 34 de todas las filas contiene la dirección en memoria del hilillo.
                 self.mainMatix[i][34] = condition

    def setDirect_Id_Condition(self, directionThread, idThread, conditionThread):
        self.mainMatix[idThread][0] = directionThread
        self.mainMatix[idThread][33] = idThread
        self.mainMatix[idThread][34] = conditionThread

    def changeThreadToExecute(self):
        self.nextThreat = self.nextThreat + 1

    def getNextThreadToExecute(self):
        return self.nextThreat

def main():
    pru = contexMatrix(7)
    pru.setDirect_Id_Condition(384, 0, "i")
    pru.setDirect_Id_Condition(384, 1, "i")
    pru.setDirect_Id_Condition(400, 2, "i")
    pru.setDirect_Id_Condition(500, 3, "i")
    pru.setDirect_Id_Condition(600, 4, "i")
    pru.setDirect_Id_Condition(700, 5, "i")
    pru.setDirect_Id_Condition(800, 6, "i")
    pru.showContextMatrix()


if __name__ == "__main__":
    main()
