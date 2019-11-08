class dataCache():
    dataCacheMatrix = []
    auxilirListForColums = []

    def __init__(self):
        for rows in range(0, 5):
            for colums in range(0, 4):
                self.auxilirListForColums.append(colums)
            self.dataCacheMatrix.append(self.auxilirListForColums)
            self.auxilirListForColums = []

        self.dataCacheMatrix[4][0] = [-1, "C"]   #B: # de bloque en memoria. C: condición del bloque.
        self.dataCacheMatrix[4][1] = [-1, "C"]
        self.dataCacheMatrix[4][2] = [-1, "C"]
        self.dataCacheMatrix[4][3] = [-1, "C"]


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

    #requiere que el bloque esté en caché
    def getWordFromCache(self, numberWordInBlock, numberOfBlock):
        positionInCache = numberOfBlock % 4
        return self.dataCacheMatrix[numberWordInBlock][positionInCache]

    def isInDataCache(self, directionInMemori):
        blockNumber = int(directionInMemori/16)
        positionInCache = blockNumber % 4
        isInCache = False
        if self.dataCacheMatrix[4][positionInCache][0] == blockNumber:
            isInCache = True
        return isInCache

    def setBlock(self, blockNumberInMemory, blockContent):
        indexForBlockContent = 0
        positionInCache = int(blockNumberInMemory % 4)
        #self.dataCacheMatrix[positionInCache] = blockContent
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

    def invalidBlock(self, blockNumber):
        for row in range(0, 4):
            if self.dataCacheMatrix[4][row][0] == blockNumber:
                self.dataCacheMatrix[4][row][1] = 'i'

    def isBlockValid(self, blockNumber):
        isValid = True
        for row in range(0, 4):
            if self.dataCacheMatrix[4][row][0] == blockNumber:
                if self.dataCacheMatrix[4][row][1] == 'i':
                    isValid = True
        return isValid

    def putWordInDataCache(self, wordValue, directionInMemory):
        targetBlock = int(directionInMemory/16)
        blockInCache = targetBlock%4
        self.dataCacheMatrix[self.getNumberOfWordInBlock(directionInMemory)][blockInCache] = wordValue

def main():
    pru = dataCache()

    pru.showDataSectionMatrix("1")

    #print(str(432/16))

    #print(str(2%4))

    pru.setBlock(27, [10, 20, 30, 40])

    #pru.showDataSectionMatrix("1")

    print(str(pru.getNumberOfWordInBlock(296)))

    print(pru.isInDataCache(48))

    print(pru.getBlockNumber(3))

    print(pru.getWordFromCache(3, 3))

    #print(pru.getWordFromCache(3, 3))

    #pru.invalidBlock(27)

    pru.showDataSectionMatrix("1")

    #print(pru.isBlockInvalid(1))

    #pru.putWordInDataCache(-1, 24)

    #pru.showDataSectionMatrix("1")

if __name__ == "__main__":
    main()