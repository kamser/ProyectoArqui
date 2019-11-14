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
        print("\t\t\tDir\t\t\tX0\t\t\tX1\t\t\tX2\t\t\tX3\t\t\tX4\t\t\tX5\t\t\tX6\t\t\tX7\t\t\tX8\t\t\tX9\t\t\tX10\t\t\tX11\t\t\tX12\t\t\tX13\t\t\tX14\t\t\tX15\t\t\tX16\t\t\tX17\t\t\tX18\t\t\tX19\t\t\tX20\t\t\tX21\t\t\tX22\t\t\tX23\t\t\tX24\t\t\tX25\t\t\tX26\t\t\tX27\t\t\tX28\t\t\tX29\t\t\tX30\t\t\tX31\t\t\tT-ID\t\tstat")
        for row in range(self.AmountOfLittleThreads):
            for colum in range(0, 35):
                print("\t\t\t" + str(self.mainMatix[row][colum]),  end='')
            print()

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

    def updateRegisterLittleThread(self, registerFromMainMemory, threadId):
        for reg in range(0, 32):
            self.mainMatix[threadId][reg + 1] = registerFromMainMemory[reg]

    def getRegisterVector(self, littleThreadId):
        auxRegisterVector = []
        for reg in range(0, 32):
            auxRegisterVector.append(self.mainMatix[littleThreadId][reg + 1])
        return auxRegisterVector

    def getLittleThreadCondition(self, littleThread):
        condition = -1
        for i in range(self.AmountOfLittleThreads):
            #La posición 33 de todas las filas contiene el identificador del hilo
            if self.mainMatix[i][33] == littleThread:
                #La posición 34 de todas las filas contiene la dirección en memoria del hilillo.
                 condition = self.mainMatix[i][34]
        return condition

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
    pru.updateRegisterLittleThread([4, 5, 19, 90, 41, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], 1)
    pru.showContextMatrix()
    print(pru.getNextThreadToExecute())
    pru.setConditionOfLittleThread(4, "f")
    pru.showContextMatrix()
    print(pru.getRegisterVector(2)[:])
    print("La condición es: " + pru.getLittleThreadCondition(4))

if __name__ == "__main__":
    main()
