class mainMemoryIntructSection():
    instrucSectionMatrix = []
    auxilirListForColums = []
    auxiliarListForWords = []

    def __init__(self):
        for rows in range(0, 10):
            for colums in range(0, 16):
                for word in range(4):
                    self.auxiliarListForWords.append(colums)
                self.auxilirListForColums.append(self.auxiliarListForWords)
                self.auxiliarListForWords = []
            self.instrucSectionMatrix.append(self.auxilirListForColums)
            self.auxilirListForColums = []

    def showInstructionSectionMatrix(self):
        for row in range(0, 10):
            print(str(self.instrucSectionMatrix[row]))

    def getBlockOfInstrucSection(self, directionInMemory):
        block = []
        positionInMemory = int(directionInMemory/16)
        currentBlock = 24
        itemstoChangeBlock = 0
        for rows in range(0, 10):
            for colums in range(0, 16):
                if itemstoChangeBlock == 3:
                    itemstoChangeBlock = 0
                    currentBlock = currentBlock + 1
                    if currentBlock == positionInMemory:
                        #cada bloque está compuesto por 4 instrucciones, cada instrucción está compuesta por 4 elementos
                        amountOfBlocks = 4
                        #Para posicionarme en la columna donde inicia el bloque y después recorrer las otras columans que quedan
                        auxiliarColums = colums
                        for item in range(amountOfBlocks):
                            block.append(self.instrucSectionMatrix[rows][auxiliarColums + (item + 1)])   #al item se le suma 1 por estar en posición atrasada.
                else:
                    itemstoChangeBlock = itemstoChangeBlock + 1

        return block



def main():
    pru = mainMemoryIntructSection()
    pru.showInstructionSectionMatrix()
    print(pru.getBlockOfInstrucSection(412)[:])


if __name__ == "__main__":
    main()