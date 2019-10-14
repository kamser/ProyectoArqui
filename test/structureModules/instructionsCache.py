class instructionsCache():
    instrucCacheMatrix = []
    auxilirListForColums = []
    auxiliarListForWords = []

    def __init__(self):
        for rows in range(0, 5):
            for colums in range(0, 4):
                for word in range(4):
                    self.auxiliarListForWords.append(colums)
                self.auxilirListForColums.append(self.auxiliarListForWords)
                self.auxiliarListForWords = []
            self.instrucCacheMatrix.append(self.auxilirListForColums)
            self.auxilirListForColums = []

        self.instrucCacheMatrix[4][0] = [1, "C"]   #B: # de bloque en memoria. C: condición del bloque.
        self.instrucCacheMatrix[4][1] = [2, "C"]
        self.instrucCacheMatrix[4][2] = [3, "C"]
        self.instrucCacheMatrix[4][3] = [12, "C"]


    def showInstructionSectionMatrix(self):
        print("    Bloque_0      Bloque_1     Bloque_2      Bloque_3")
        for row in range(0, 5):
            print(str(self.instrucCacheMatrix[row]))

    def getBlockNumber(self, block):
        return self.instrucCacheMatrix[4][block][0]

    def getWordFromCache(self, numberWordInBlock, numberOfBlock):
        return self.instrucCacheMatrix[numberWordInBlock][numberOfBlock]

    def isInInstrucCache(self, blockNumber):
        isInCache = False
        for colums in range(0, 4):
            for word in range(2):
                if self.instrucCacheMatrix[4][colums][0] == blockNumber:       #Se posicióna directamente en la fila 5 y revisa las primeras posiciones de las columnas
                    isInCache = True
        return isInCache

    def setBlock(self, blockNumberInMemory, blockContent):
        indexForBlockContent = 0
        positionInCache = blockNumberInMemory % 4
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

    pru.setBlock(27, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])

    pru.showInstructionSectionMatrix()

    print(str(pru.getNumberOfWordInBlock(404)))

    print(pru.isInInstrucCache(10))

    print(pru.getBlockNumber(1))

    print(pru.getWordFromCache(3, 3))

if __name__ == "__main__":
    main()