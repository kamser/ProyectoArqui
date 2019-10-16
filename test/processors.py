import threading
import time
from structureModules.contexMatrix import contexMatrix
from structureModules.MainMemory import MainMemory
from structureModules.dataCache import dataCache
from structureModules.instructionsCache import instructionsCache

testBarrier = threading.Barrier(2)
class processors():
    contextMat = contexMatrix(7)
    mainMemory = MainMemory()

    def __init__(self):
        littlethreadList = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
        mainMemory_InstruSection = []
        listaAxu = []
        directionInstrucSec = 384
        for littleThreadItem in littlethreadList:
            archivo = open(littleThreadItem, "r")
            for line in archivo.readlines():
                listaAxu = list(map(int, line.split()))     #Pasa lista de isntruccion de string a int
                self.mainMemory.putInMainMemoryInstSec(listaAxu, directionInstrucSec)
                directionInstrucSec = directionInstrucSec + 4

        archivo.close()

        self.mainMemory.showMainMemory()

    def processor(self):
        data_Cache = dataCache()
        instr_Cache = instructionsCache()

def main():
    pru = processors()

if __name__ == "__main__":
    main()
