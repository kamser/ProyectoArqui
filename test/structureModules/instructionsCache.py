class instructionsCache():

    def __init__(self):
        self.instrucCacheMatrix = []
        self.auxilirListForColums = []
        self.auxiliarListForWords = []
        for rows in range(0, 5):
            for colums in range(0, 4):
                for word in range(4):
                    self.auxiliarListForWords.append(colums - 1)
                self.auxilirListForColums.append(self.auxiliarListForWords)
                self.auxiliarListForWords = []
            self.instrucCacheMatrix.append(self.auxilirListForColums)
            self.auxilirListForColums = []

        self.instrucCacheMatrix[4][0] = [-1, "C"]   #B: # de bloque en memoria. C: condición del bloque.
        self.instrucCacheMatrix[4][1] = [-1, "C"]
        self.instrucCacheMatrix[4][2] = [-1, "C"]
        self.instrucCacheMatrix[4][3] = [-1, "C"]


    def showInstructionSectionMatrix(self):
        print("\t   Bloque_0\t\t\t  Bloque_1\t\t\t  Bloque_2\t\t\t  Bloque_3")
        for row in range(0, 4):
            for colum in range(0, 4):
                print("\t" + str(self.instrucCacheMatrix[row][colum]) + "\t", end='')
            print()

        for row in range(4, 5):
            for colum in range(0, 4):
                print("\t\t" + str(self.instrucCacheMatrix[row][colum]) + "\t", end='')
            print()

    def getBlockNumber(self, block):
        return self.instrucCacheMatrix[4][block][0]

    def getWordFromCache(self, numberWordInBlock, numberOfBlock):
        directionInCache = numberOfBlock%4
        word = -1
        if numberOfBlock == self.instrucCacheMatrix[4][directionInCache][0]:
            word = self.instrucCacheMatrix[numberWordInBlock][directionInCache]
        return word

    def isInInstrucCache(self, blockNumber):
        isInCache = False
        for colums in range(0, 4):
            for word in range(2):
                if self.instrucCacheMatrix[4][colums][0] == blockNumber:       #Se posicióna directamente en la fila 5 y revisa las primeras posiciones de las columnas
                    isInCache = True
        return isInCache

    def setBlock(self, blockNumberInMemory, blockContent):
        indexForBlockContent = 0
        positionInCache = int(blockNumberInMemory % 4)
        for rows in range(0, 4):
            for colums in range(0, 4):
                if colums == positionInCache:
                    for word in range(4):
                        self.instrucCacheMatrix[rows][colums][word] = blockContent[indexForBlockContent]
                        indexForBlockContent = indexForBlockContent + 1
        self.instrucCacheMatrix[4][positionInCache % 4][0] = blockNumberInMemory
        self.instrucCacheMatrix[4][positionInCache % 4][1] = "C"

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
    pru = instructionsCache()

    pru.showInstructionSectionMatrix()

    print(str(432/16))

    print(str(27%4))

    pru.setBlock(24, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])

    pru.showInstructionSectionMatrix()

    print(str(pru.getNumberOfWordInBlock(404)))

    print(pru.isInInstrucCache(10))

    print(pru.getBlockNumber(1))

    print(pru.getBlockNumber(1))

    print(pru.getWordFromCache(1, 27))

if __name__ == "__main__":
    main()