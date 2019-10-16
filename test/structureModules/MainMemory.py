class MainMemory:
    instructionMemory = []*(64*10)
    dataMemory = []*96  # 24*4

    def __init__(self):
        # se inicializan los vectores
        i = 0
        for x in range(0, 96):
            self.dataMemory.append(i)
            i = i + 4

        auxiliarListItem = []
        for x in range(0, 40*4):
            for items in range(0, 4):
                auxiliarListItem.append(i)
            self.instructionMemory.append(auxiliarListItem)
            auxiliarListItem = []
            i = i+4

    def showMainMemory(self):
        indexGuide = 0
        print("\t\t\t\t\t\tData Section")
        for rows in range(0, 6):
            for colum in range(0, 16):
                print(str(self.dataMemory[indexGuide]) + "\t", end='')
                indexGuide = indexGuide + 1
            print()
        print()
        indexGuide = 0
        print("\t\t\t\t\t\tInstructions Section")
        for rows in range(0, 10):
            for colum in range(0, 16):
                print(str(self.instructionMemory[indexGuide]) + "\t", end='')
                indexGuide = indexGuide + 1
            print()

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
        if 0 <= numBlock < 40:
            numBlock = (numBlock*4)
            block = []
            for x in range(0, 4):
                block.append(self.instructionMemory[numBlock+x])
            return block
        else:
            return 0

    def writeOnInstructionMemory(self, numBlock, newBlock):
        fisicBlock = numBlock - 24
        if 0 <= fisicBlock < 40:
            fisicBlock = (fisicBlock*4)
            for x in range(0, 4):
                self.instructionMemory[fisicBlock+x] = newBlock[x]


if __name__ == "__main__":
    mm = MainMemory()
    '''print(mm.getDataBlock(0))
    mm.writeOnDataMemory(23, (1,2,3,4))
    print(mm.getDataBlock(0))
    print(mm.getDataBlock(1))
    print(mm.getDataBlock(23))'''
    print(mm.getInstructionBlock(39))
    mm.writeOnInstructionMemory(39, ([1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]))
    print(mm.getInstructionBlock(39))
    mm.showMainMemory()