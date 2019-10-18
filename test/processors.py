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
    #Vectores de registros de cada núcleo
    registerVector_P1 = []*32
    registerVector_P2 = []*32
    contextMatrix_lock = 0                  #mutex para sincronización en matriz de contexto

    def __init__(self):
        littlethreadList = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
        mainMemory_InstruSection = []
        listaAxu = []
        directionInstrucSec = 384
        threadId = 0
        for littleThreadItem in littlethreadList:
            archivo = open(littleThreadItem, "r")
            self.contextMat.setDirect_Id_Condition(directionInstrucSec, threadId, 'i')
            threadId = threadId + 1
            for line in archivo.readlines():
                listaAxu = list(map(int, line.split()))     #Pasa lista de isntruccion de string a int
                self.mainMemory.putInMainMemoryInstSec(listaAxu, directionInstrucSec)
                directionInstrucSec = directionInstrucSec + 4

        for reg in range(0, 32):
            self.registerVector_P1.append(0)
            self.registerVector_P2.append(0)


        archivo.close()
        self.mainMemory.showMainMemory()
        print(self.registerVector_P1[:])
        print(self.registerVector_P2[:])
        self.contextMat.showContextMatrix()

        self.contextMatrix_lock = threading.Lock()

    def processorBehaivor(self, threadId):
        data_Cache = dataCache()
        instr_Cache = instructionsCache()

        threadCondition = "working"

        self.contextMatrix_lock.acquire()
        print("Soy el hilo: " + str(threadId))
        print(self.contextMat.getNextThreadToExecute())
        self.contextMat.changeThreadToExecute()
        self.contextMatrix_lock.release()





def main():
    pru = processors()

    hilo1 = threading.Thread(target=pru.processorBehaivor(1), name=1)
    hilo2 = threading.Thread(target=pru.processorBehaivor(2), name=2)
    hilo1.start()
    hilo2.start()

if __name__ == "__main__":
    main()
