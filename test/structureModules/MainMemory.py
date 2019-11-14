class MainMemory():
    instructionMemory = []*(64*10)
    dataMemory = []*96  # 24*4

    def __init__(self):
        # se inicializan los vectores
        i = 0
        for x in range(0, 96):
            self.dataMemory.append(i)
            i = i + 4

        changeIndexValue = 0
        for x in range(0, 64*10):
            self.instructionMemory.append(i)
            if changeIndexValue == 3:
                i = i+4
                changeIndexValue = -1
            changeIndexValue = changeIndexValue + 1

    def showMainMemory(self):
        indexGuide = 0
        indexBlock = 0
        print("\t\t\t\t\t\tData Section")
        for rows in range(0, 6):
            print("____________________________BLOQUE_" + str(indexBlock) + "____________________________________||", end='')
            indexBlock = indexBlock + 1
            print("________________________________BLOQUE_" + str(indexBlock) + "____________________________________||", end='')
            indexBlock = indexBlock + 1
            print("__________________________________BLOQUE_" + str(indexBlock) + "____________________________________||", end='')
            indexBlock = indexBlock + 1
            print("___________________________________BLOQUE_" + str(indexBlock) + "____________________________________||")
            indexBlock = indexBlock + 1
            for colum in range(0, 16):
                print(str(self.dataMemory[indexGuide]) + "\t\t\t\t\t", end='')
                indexGuide = indexGuide + 1
            print()
        print()
        #Descomentar para ver la sección de instruccion en memoria principal
        '''indexGuide = 0
        indexToChangeWord = 0
        print("\t\t\t\t\t\tInstructions Section")
        for rows in range(0, 10):
            for colum in range(0, 64):
                print(str(self.instructionMemory[indexGuide]) + "\t", end='')
                if indexToChangeWord == 3:
                    print("\t", end='')
                    indexToChangeWord = -1
                indexGuide = indexGuide + 1
                indexToChangeWord = indexToChangeWord + 1
            print()'''

    def getDataBlock(self, numBlock):
        if 0 <= numBlock < 24:
            numBlock = (numBlock*4)
            block = []
            for x in range(0, 4):
                block.append(self.dataMemory[numBlock+x])
            return block
        else:
            return 0

    def writeOnDataMemory(self, blockNumber, newBlock):
        if 0 <= blockNumber < 24:
            blockNumber = (blockNumber * 4)
            for x in range(0, 4):
                self.dataMemory[blockNumber+x] = newBlock[x]

    def getInstructionBlock(self, numBlock):
        fisicBlock = numBlock - 24
        if 24 <= numBlock < 63:
            block = []
            indexInInstrSeccion = fisicBlock*16
            for word in range(0, 16):
                block.append(self.instructionMemory[indexInInstrSeccion])
                indexInInstrSeccion = indexInInstrSeccion + 1
            return block
        else:
            return []

    def putInMainMemoryInstSec(self, wordValue, direction):
        directionTraslateInInstrSec = direction - 384       #Por desplazamiento lógico al dividir la memoria en 2 seciones
        for item in range(0, 4):
            self.instructionMemory[directionTraslateInInstrSec] = wordValue[item]
            directionTraslateInInstrSec = directionTraslateInInstrSec + 1

    def putInMainMemoryDataSec(self, wordValue, direction):
        fisicDirection = int(direction/4)
        self.dataMemory[fisicDirection] = wordValue



if __name__ == "__main__":
    mm = MainMemory()
    '''print(mm.getDataBlock(0))
    mm.writeOnDataMemory(23, (1,2,3,4))'''
    print(mm.getDataBlock(0))
    print(mm.getDataBlock(1))
    print(mm.getDataBlock(23))
    #print(mm.getInstructionBlock(39))
    #mm.writeOnInstructionMemory(39, ([1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]))
    print(mm.getInstructionBlock(50))
    #mm.putInMainMemoryInstSec([1, 2, 3, 4], 384)

    mm.putInMainMemoryDataSec(8, 128)
    #mm.putInMainMemoryInstSec(7, 15)
    mm.showMainMemory()
    print(mm.getDataBlock(23))