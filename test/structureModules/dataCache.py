class dataCache():
    dataCacheMatrix = []
    auxilirListForColums = []

    def __init__(self):
        for rows in range(0, 5):
            for colums in range(0, 4):
                self.auxilirListForColums.append(colums)
            self.dataCacheMatrix.append(self.auxilirListForColums)
            self.auxilirListForColums = []

        self.dataCacheMatrix[4][0] = [1, "C"]   #B: # de bloque en memoria. C: condición del bloque.
        self.dataCacheMatrix[4][1] = [2, "C"]
        self.dataCacheMatrix[4][2] = [3, "C"]
        self.dataCacheMatrix[4][3] = [12, "C"]


    def showDataSectionMatrix(self, threadId):
        print("\t_____________________|| Nucleo: " + threadId + "||_____________________")
        print("\tBloque_0\t\tBloque_1\t\tBloque_2\t\tBloque_3")
        for row in range(0, 4):
            for colum in range(0, 4):
                print("\t\t" + str(self.dataCacheMatrix[row][colum]) + "\t\t", end='')
            print()

        for colum in range(0, 4):
            print("\t" + str(self.dataCacheMatrix[4][colum]) + "\t", end='')

        print()

    def getBlockNumber(self, block):
        return self.dataCacheMatrix[4][block][0]

    def getWordFromCache(self, numberWordInBlock, numberOfBlock):
        return self.dataCacheMatrix[numberWordInBlock][numberOfBlock]

    def isInDataCache(self, blockNumber):
        isInCache = False
        for colums in range(0, 4):
            if self.dataCacheMatrix[4][colums][0] == blockNumber:       #Se posicióna directamente en la fila 5 y revisa las primeras posiciones de las columnas
                isInCache = True
        return isInCache

    def setBlock(self, blockNumberInMemory, blockContent):
        indexForBlockContent = 0
        positionInCache = blockNumberInMemory % 4
        for rows in range(0, 4):
            for colums in range(0, 4):
                if colums == positionInCache:
                    self.dataCacheMatrix[rows][colums] = blockContent[indexForBlockContent]
                    indexForBlockContent = indexForBlockContent + 1
        self.dataCacheMatrix[4][positionInCache % 4][0] = blockNumberInMemory
        self.dataCacheMatrix[4][positionInCache % 4][1] = "C"

    def getNumberOfWordInBlock(self, directionInMemory):
        targetBlock = int(directionInMemory/16)
        numberWord = 0
        directionForDecrement = directionInMemory
        for word in range(0, 4):
            if int(directionForDecrement/16) == targetBlock:
                numberWord = numberWord + 1
                directionForDecrement = directionForDecrement - 4
        return numberWord - 1      #debido a que la numeración va de 0 - 3

def main():
    pru = dataCache()

    pru.showDataSectionMatrix("1")

    #print(str(432/16))

    #print(str(27%4))


    pru.setBlock(27, [1, 2, 3, 4])

    pru.showDataSectionMatrix("1")

    #print(str(pru.getNumberOfWordInBlock(28)))

    #print(pru.isInInstrucCache(12))

    print(pru.getBlockNumber(3))
    #
    #print(pru.getWordFromCache(3, 3))

if __name__ == "__main__":
    main()