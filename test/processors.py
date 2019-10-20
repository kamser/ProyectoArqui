import sys
import threading
import time
from structureModules.contexMatrix import contexMatrix
from structureModules.MainMemory import MainMemory
from structureModules.dataCache import dataCache
from structureModules.instructionsCache import instructionsCache

#sys.setswitchinterval(0.1)

class processors():
    lock = 0
    contextMat = contexMatrix(7)
    mainMemory = MainMemory()
    #Vectores de registros de cada núcleo
    registerVector_P1 = []*32
    registerVector_P2 = []*32
    # mutex para sincronización en matriz de contexto.
    contextMatrix_lock = 0
    # PC de cada procesador
    ProcessCounter_P1 = 0
    ProcessCounter_P2 = 0
    # Variables que registran los contadores de ciclos de reloj de los hilos
    threadCicleCounter_P1 = 0
    threadCicleCounter_P2 = 0
    # Variables que representan si un hilo está activo o si ya terminó su trabajo.
    #false significa que se está ejecutando. True ya terminó la ejecución del hilillo.
    threadCondition_P1 = True
    threadCondition_P2 = True
    #barrera lógica para detener los hilos cierta cantidad de ciclos. El parámetro 2 es
    #que va a esperar hasta que 2 hilos se queden pegados
    threadBarrier = 0


    def __init__(self):
        littlethreadList = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
        mainMemory_InstruSection = []
        listaAxu = []
        directionInstrucSec = 384
        threadId = 0
        self.lock = threading.Lock()
        self.contextMatrix_lock = threading.Condition(self.lock)
        self.threadBarrier = threading.Barrier(2)
        for littleThreadItem in littlethreadList:
            archivo = open(littleThreadItem, "r")
            self.contextMat.setDirect_Id_Condition(directionInstrucSec, threadId, 'i')
            threadId = threadId + 1
            for line in archivo.readlines():
                listaAxu = list(map(int, line.split()))     #Pasa lista de isntruccion de string a int
                self.mainMemory.putInMainMemoryInstSec(listaAxu, directionInstrucSec)
                directionInstrucSec = directionInstrucSec + 4

        archivo.close()

        for reg in range(0, 32):
            self.registerVector_P1.append(0)
            self.registerVector_P2.append(0)


    def incrementClockCicleCounter(self, threadId):
        if threadId == 1:
            self.threadCicleCounter_P1 = self.threadCicleCounter_P1 + 1
        else:
            self.threadCicleCounter_P2 = self.threadCicleCounter_P2 + 1

    def getThreadCondition(self, threadId):
        condition = True
        if threadId == 1:
            condition = self.threadCondition_P1
        else:
            condition = self.threadCondition_P2
        return condition

    def processorBehaivor(self, threadId):

        data_Cache = dataCache()
        instr_Cache = instructionsCache()
        print("Soy el hilo: " + str(threadId))
        #self.threadBarrier.wait()
        with self.contextMatrix_lock:
            time.sleep(1)
            if 7 < self.contextMat.AmountOfLittleThreads:
                print("Soy el hilo: " + str(threadId))
                print(self.contextMat.getNextThreadToExecute())
                self.contextMat.changeThreadToExecute()

            else:
                #Si ya no encuentra más hilillos con qué trabajar, cambia el estado del hilo a terminado
                if threadId == 1:
                    print("Soy el hilo: " + str(threadId))
                    self.threadCondition_P1 = False
                else:
                    print("Soy el hilo: " + str(threadId))
                    self.threadCondition_P2 = False

        #Esta condicional divide el programa en si el procesador continua o finaliza y espera a que finalize el otro hilo
        if self.getThreadCondition(threadId):
            print("Hago logic de verdad")
        else:
            print("Hago logica de falso. Soy el hilo: " + str(threadId))
            while self.threadCondition_P2 or self.threadCondition_P1:
                time.sleep(1)
                print(" BUCLE: " + str(threadId))

                #self.threadBarrier.wait()

                self.incrementClockCicleCounter(threadId)

                #self.threadCondition_P2 = False

            print("Se elimina el hilo")
            data_Cache.showDataSectionMatrix()

        data_Cache.showDataSectionMatrix()

    def threadInicializer(self):

        hilo1 = threading.Thread(target=self.processorBehaivor(1), name=1)
        hilo2 = threading.Thread(target=self.processorBehaivor(2), name=2)
        hilo2.start()
        hilo1.start()

        hilo1.join()
        hilo2.join()




def main():
    pru = processors()

    pru.threadInicializer()

    '''hilo1 = threading.Thread(target=pru.processorBehaivor(1), name=1)
    hilo2 = threading.Thread(target=pru.processorBehaivor(2), name=2)
    hilo2.start()
    hilo1.start()'''


if __name__ == "__main__":
    main()

'''
https://www.genbeta.com/desarrollo/multiprocesamiento-en-python-esquivando-el-gil
https://emptysqua.re/blog/grok-the-gil-fast-thread-safe-python/
https://hackernoon.com/synchronization-primitives-in-python-564f89fee732
https://aaronlelevier.github.io/multithreading-in-python/


'''