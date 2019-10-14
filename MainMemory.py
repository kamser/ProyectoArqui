class MainMemory:
    instructionMemory = []*(40*4)
    dataMemory = []*96  # 24*4

    def __init__(self):
        # se inicializan los vectores
        i = 0
        for x in range(0, 96):
            self.dataMemory.append(i)
            i = i + 4
        print(self.dataMemory)

        for x in range(0, 40*4):
            self.instructionMemory.append(i)
            i = i+4
        print(self.instructionMemory)

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
        if 0 <= numBlock < 40:
            numBlock = (numBlock*4)
            for x in range(0, 4):
                self.instructionMemory[numBlock+x] = newBlock[x]


if __name__ == "__main__":
    mm = MainMemory()
    '''print(mm.getDataBlock(0))
    mm.writeOnDataMemory(23, (1,2,3,4))
    print(mm.getDataBlock(0))
    print(mm.getDataBlock(1))
    print(mm.getDataBlock(23))'''
    print(mm.getInstructionBlock(39))
    mm.writeOnInstructionMemory(39, (1,2,3,4))
    print(mm.getInstructionBlock(39))


