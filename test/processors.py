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
    processCounter_P1 = 0
    processCounter_P2 = 0
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
    #Definición de las caches de datos para cada procesador
    data_Cache_P1 = 0
    data_Cache_P2 = 0
    #Definición de las cachés de instrucciones para cada procesador
    instr_Cache_P1 = 0
    instr_Cache_P2 = 0

    def __init__(self):
        littlethreadList = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
        mainMemory_InstruSection = []
        listaAxu = []
        directionInstrucSec = 384
        threadId = 0
        self.data_Cache_P1 = dataCache()
        self.data_Cache_P2 = dataCache()
        self.instr_Cache_P1 = instructionsCache()
        self.instr_Cache_P2 = instructionsCache()
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
        if threadId == "1":
            self.threadCicleCounter_P1 = self.threadCicleCounter_P1 + 1
        else:
            self.threadCicleCounter_P2 = self.threadCicleCounter_P2 + 1

    def getThreadCondition(self, threadId):
        if threadId == "1":
            condition = self.threadCondition_P1
        else:
            condition = self.threadCondition_P2
        return condition

    #Sirve para los branch
    def changePCValue(self, threadId, newValue):
        if threadId == "1":
            self.processCounter_P1 = newValue
        else:
            self.processCounter_P2 = newValue

    def incrementPCValue(self, threadId):
        if threadId == "1":
            self.processCounter_P1 = self.processCounter_P1 + 4
        else:
            self.processCounter_P2 = self.processCounter_P2 + 4

    def resetRegisterVectorProcessor(self, threadId, vectorFormContextMatrix):
        if threadId == "1":
            self.registerVector_P1 = vectorFormContextMatrix
        else:
            self.registerVector_P2 = vectorFormContextMatrix

    def getBlockNumber(self, threadId):
        if threadId == "1":
            blockNum = int(self.processCounter_P1 / 16)
        else:
            blockNum = int(self.processCounter_P2 / 16)
        return blockNum

    def isInInstrucCache(self, threadId, blockNumber):
        isIn = False
        if threadId == "1":
            isIn = self.instr_Cache_P1.isInInstrucCache(blockNumber)
        else:
            isIn = self.instr_Cache_P2.isInInstrucCache(blockNumber)
        return isIn

    def getNumberOfWordInBlock(self, threadId, directionInMemory):
        wordNumber = 0
        if threadId == "1":
            wordNumber = self.instr_Cache_P1.getNumberOfWordInBlock(directionInMemory)
        else:
            wordNumber = self.instr_Cache_P2.getNumberOfWordInBlock(directionInMemory)
        return wordNumber

    def getPCValue(self, threadId):
        pc = 0
        if threadId == "1":
            pc = self.processCounter_P1
        else:
            pc = self.processCounter_P2
        return pc

    def getWordFromInstrCache(self, threadId, numberWordInBlock, numberOfBlock):
        if threadId == "1":
            word = self.instr_Cache_P1.getWordFromCache(numberWordInBlock, numberOfBlock)
        else:
            word = self.instr_Cache_P2.getWordFromCache(numberWordInBlock, numberOfBlock)
        return word

    # dr = destination register, r = register, i = inmediate
    def addi(self, dr, r, i, threadId):
        if threadId == "1":
            self.registerVector_P1[dr] = r+i
        else:
            self.registerVector_P2[dr] = r+i

    # dr = destination register, or1 = origin register 1, origen register 2
    def add(self, dr, or1, or2, threadId):
        if threadId == "1":
            self.registerVector_P1[dr] = or1+or2
        else:
            self.registerVector_P2[dr] = or1+or2

    # dr = destination register, or1 = origin register 1, origen register 2
    def sub(self, dr, or1, or2, threadId):
        if threadId == "1":
            self.registerVector_P1[dr] = or1-or2
        else:
            self.registerVector_P2[dr] = or1-or2

    # dr = destination register, or1 = origin register 1, origen register 2
    def mul(self, dr, or1, or2, threadId):
        if threadId == "1":
            self.registerVector_P1[dr] = or1 * or2
        else:
            self.registerVector_P2[dr] = or1 * or2

    # dr = destination register, or1 = origin register 1, origen register 2
    def div(self, dr, or1, or2, threadId):
        if threadId == "1":
            self.registerVector_P1[dr] = or1 // or2
        else:
            self.registerVector_P2[dr] = or1 // or2

    #dr = destination register, n = main memory position, r = register with offset
    def lw(self, dr, n, r, threadId):
        # hay que comprobar si el bloque está en caché

        # // significa división entera
        posInCache = n // 16
        posInCache = posInCache % 4  # 4 es la capacidad de bloques en caché
        print(posInCache)
        if threadId == "1":
            if n == self.data_Cache_P1.getBlockNumber(posInCache): #sí está en caché
                print(self.data_Cache_P1.getBlockNumber(posInCache))
            else:
                print("no está")
        else:
            if n == self.data_Cache_P1.getBlockNumber(posInCache):  # sí está en caché
                print(self.data_Cache_P1.getBlockNumber(posInCache))
            else:
                print("no está")


    def sw(self):
        pass

    def beq(self):
        pass

    def bne(self):
        pass

    def jal(self):
        pass

    def jalr(self):
        pass

    def fin(self):
        pass

    def selectInstructionType(self, operationCode):
        switcher = {
            19: self.addi(),
            71: self.add(),
            83: self.sub(),
            72: self.mul(),
            56: self.div(),
            5: self.lw(),
            37: self.sw(),
            99: self.beq(),
            100: self.bne(),
            111: self.jal(),
            103: self.jalr(),
            999: self.fin()
        }

    def processorBehaivor(self, threadId):
        with self.contextMatrix_lock:
            time.sleep(1)
            #Si aún quedan hilillos por ejecutar
            if 6 < self.contextMat.AmountOfLittleThreads:
                self.changePCValue(threadId, self.contextMat.getInstrDirectInMemory(self.contextMat.getNextThreadToExecute()))
                #Blanque el vector de registros del procesador cada vez que inicia una nueva instrucción
                self.resetRegisterVectorProcessor(threadId, self.contextMat.getRegisterVector(self.contextMat.getNextThreadToExecute()))
                self.contextMat.changeThreadToExecute()
            #Si ya no quedan hilillos por ejecutar
            else:
                #Si ya no encuentra más hilillos con qué trabajar, cambia el estado del hilo a terminado
                if threadId == "1":
                    self.threadCondition_P1 = False
                else:
                    self.threadCondition_P2 = False
            blockNumber = self.getBlockNumber(threadId)

            if self.isInInstrucCache(threadId, blockNumber):
                print("Hacer lógica de hit")
                wordNum = self.getNumberOfWordInBlock(threadId, self.getPCValue(threadId))
                word = self.getWordFromInstrCache(threadId, wordNum, blockNumber)

            else:
                print("Hacer lógica de fallo")










        #Esta condicional divide el programa en si el procesador continua o finaliza y espera a que finalize el otro hilo
        if self.getThreadCondition(threadId):
            print("Hago logic de verdad")
        else:
            print("Hago logica de falso. Soy el hilo: " + str(threadId))

            #Se implementa la lógica de un do-while para obligar a que los dos hilos se detengan
            while True:
                time.sleep(1)
                print(" BUCLE: " + str(threadId))

                self.threadBarrier.wait()

                self.incrementClockCicleCounter(threadId)

                if not self.threadCondition_P2 or not self.threadCondition_P1:
                    break


            with self.contextMatrix_lock:
                if threadId == "1":
                    self.data_Cache_P1.showDataSectionMatrix(threadId)
                else:
                    self.data_Cache_P2.showDataSectionMatrix(threadId)


    def threadInicializer(self):

        hilo1 = threading.Thread(target=self.processorBehaivor, args=("1"), name=1)
        hilo2 = threading.Thread(target=self.processorBehaivor, args=("2"), name=2)
        hilo2.start()
        hilo1.start()

        hilo1.join()
        hilo2.join()




def main():
    pru = processors()

    pru.threadInicializer()


    pru.lw(1, 4, 316, 0)

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