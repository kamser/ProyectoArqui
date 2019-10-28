import threading
import time
from structureModules.contexMatrix import contexMatrix
from structureModules.MainMemory import MainMemory
from structureModules.dataCache import dataCache
from structureModules.instructionsCache import instructionsCache


class processors():
    lock_MC = 0
    lock_CD1 = 0
    lock_CD2 = 0
    lock_MM = 0
    contextMat = contexMatrix(7)
    mainMemory = MainMemory()
    # Vectores de registros de cada núcleo
    registerVector_P1 = [] * 32
    registerVector_P2 = [] * 32
    generalResgisterVector = []
    # mutex para sincronización en matriz de contexto.
    contextMatrix_lock = 0
    # Candado para sinconización de las caches de datos
    dataCache1_lock = 0
    dataCache2_lock = 0
    generalDataCache_lock = []
    # Candado de sicronización para la memoria princiapal o el bus de datos
    mainMemory_lock = 0
    # PC de cada procesador
    processCounter_P1 = 0
    processCounter_P2 = 0
    generalProcessCounter = []
    # Variables que registran los contadores de ciclos de reloj de los hilos
    threadCicleCounter_P1 = 0
    threadCicleCounter_P2 = 0
    generalThreadCicleCounter = []
    # Variables que representan si un hilo está activo o si ya terminó su trabajo.
    # false significa que se está ejecutando. True ya terminó la ejecución del hilillo.
    threadCondition_P1 = True
    threadCondition_P2 = True
    generalThreadCondition = []
    # barrera lógica para detener los hilos cierta cantidad de ciclos. El parámetro 2 es
    # que va a esperar hasta que 2 hilos se queden pegados
    threadBarrier = 0
    # Definición de las caches de datos para cada procesador
    data_Cache_P1 = 0
    data_Cache_P2 = 0
    generalData_Cache = []
    # Definición de las cachés de instrucciones para cada procesador
    instr_Cache_P1 = 0
    instr_Cache_P2 = 0
    generalInstr_Cache = []

    def __init__(self):
        littlethreadList = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
        mainMemory_InstruSection = []
        listaAxu = []
        directionInstrucSec = 384
        threadId = 0
        self.lock = threading.Lock()
        self.lock_CD1 = threading.Lock()
        self.lock_CD2 = threading.Lock()
        self.lock_MC = threading.Lock()
        self.lock_MM = threading.Lock()
        self.lock = threading.Lock()
        # Se crean las cachés y se ingresan en un vector de cachés de datos
        self.data_Cache_P1 = dataCache()
        self.data_Cache_P2 = dataCache()
        self.generalData_Cache.append(self.data_Cache_P1)
        self.generalData_Cache.append(self.data_Cache_P2)
        # Se crean las cachés y se ingresan en un vector de cachés de instrucciones
        self.instr_Cache_P1 = instructionsCache()
        self.instr_Cache_P2 = instructionsCache()
        self.generalInstr_Cache.append(self.instr_Cache_P1)
        self.generalInstr_Cache.append(self.instr_Cache_P2)
        # Se crean los candados y se ingresan en un vector de candados de cache de datos
        self.dataCache1_lock = threading.Condition(self.lock_CD1)
        self.dataCache2_lock = threading.Condition(self.lock_CD2)
        self.generalDataCache_lock.append(self.dataCache1_lock)
        self.generalDataCache_lock.append(self.dataCache2_lock)
        # Se crean los candados y se ingresan en un vector de candados de cache de instrucciones
        self.mainMemory_lock = threading.Condition(self.lock_MM)
        self.contextMatrix_lock = threading.Condition(self.lock_MC)
        self.threadBarrier = threading.Barrier(2)
        # Se crea un vector que contiene los PC de los dos núcleos
        self.generalProcessCounter.append(self.processCounter_P1)
        self.generalProcessCounter.append(self.processCounter_P2)
        # Se crea vector que contiene los contadores de ciclos de reloj de cada procesador
        self.generalThreadCicleCounter.append(self.threadCicleCounter_P1)
        self.generalThreadCicleCounter.append(self.threadCicleCounter_P2)
        # Se crea vector que contiene las condiciones de cada uno de los nucleos
        self.generalThreadCondition.append(self.threadCondition_P1)
        self.generalThreadCondition.append(self.threadCondition_P2)
        # Se extrae la información de los hilillos y se pasan a las memorias respectivas.
        for littleThreadItem in littlethreadList:
            archivo = open(littleThreadItem, "r")
            self.contextMat.setDirect_Id_Condition(directionInstrucSec, threadId, 'i')
            threadId = threadId + 1
            for line in archivo.readlines():
                listaAxu = list(map(int, line.split()))  # Pasa lista de isntruccion de string a int
                self.mainMemory.putInMainMemoryInstSec(listaAxu, directionInstrucSec)
                directionInstrucSec = directionInstrucSec + 4

        archivo.close()

        for reg in range(0, 32):
            self.registerVector_P1.append(0)
            self.registerVector_P2.append(0)

        self.generalResgisterVector.append(self.registerVector_P1)
        self.generalResgisterVector.append(self.registerVector_P2)

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

    # Sirve para los branch
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
        self.generalResgisterVector[threadId][dr] += self.generalResgisterVector[threadId][r]+i

    # dr = destination register, or1 = origin register 1, origen register 2
    def add(self, dr, or1, or2, threadId):
        self.generalResgisterVector[threadId][dr] += self.generalResgisterVector[threadId][or1] + self.generalResgisterVector[threadId][or2]

    # dr = destination register, or1 = origin register 1, origen register 2
    def sub(self, dr, or1, or2, threadId):
        self.generalResgisterVector[threadId][dr] += self.generalResgisterVector[threadId][or1] - self.generalResgisterVector[threadId][or2]

    # dr = destination register, or1 = origin register 1, origen register 2
    def mul(self, dr, or1, or2, threadId):
        self.generalResgisterVector[threadId][dr] += self.generalResgisterVector[threadId][or1] * self.generalResgisterVector[threadId][or2]

    # dr = destination register, or1 = origin register 1, origen register 2
    def div(self, dr, or1, or2, threadId):
        self.generalResgisterVector[threadId][dr] += self.generalResgisterVector[threadId][or1] // self.generalResgisterVector[threadId][or2]

    # dr = destination register, n = main memory position, r = register with offset
    def lw(self, dr, n, r, threadId):
        while True:
            # intenta bloquear caché propia
            if self.generalDataCache_lock[threadId].acquire(False):
                # hay que comprobar si el bloque está en caché
                inCache = self.generalData_Cache[threadId].isInDataCache(n)
                if inCache is True:
                    self.registerVector_P1[dr] = self.generalData_Cache[threadId].getWordFromCache(r, n)
                    #self.generalDataCache_lock[threadId].release()
                    break
                else:  # no está en caché
                    # Intenta bloquear el bus de datos
                    if self.mainMemory_lock.acquire(False):
                        block = self.mainMemory.getDataBlock(n)
                        # espera los ciclos correspondientes
                        for i in range(0, 20):
                            #self.threadBarrier.wait()
                            self.incrementClockCicleCounter(threadId)

                        self.generalData_Cache[threadId].setBlock(n, block)
                        self.registerVector_P1[dr] = self.generalData_Cache[threadId].getWordFromCache(r, n)
                #self.threadBarrier.wait()
                self.incrementClockCicleCounter(threadId)
                self.generalDataCache_lock[threadId].release()
                break

    def lockOwnDataCache(self, threadId):
        lockTaken = 0
        if threadId == "1":
            lockTaken = self.dataCache1_lock.acquire(
                False)  # Parametro sirve para que cuando un hilo intente tomarlo y no pueda, no se quede pegado esperando
        else:
            lockTaken = self.dataCache2_lock.acquire(False)
        return lockTaken

    def sw(self, valueToStore, displacement, registerValue, threadId):
        directionToStore = displacement + registerValue
        blockConflict = int(directionToStore / 16)
        while True:
            # intenta bloquear caché propia
            if self.dataCache1_lock.acquire(False):
                # intenta bloquear caché del otro procesador
                if self.dataCache2_lock.acquire(False):
                    if self.data_Cache_P2.isInDataCache(blockConflict) and self.data_Cache_P2.isBlockInvalid(
                            blockConflict):
                        self.data_Cache_P2.invalidBlock(blockConflict)
                        self.threadBarrier.wait()
                        self.incrementClockCicleCounter(threadId)
                    self.dataCache2_lock.release()
                    # Intenta bloquear el bus de datos
                    if self.mainMemory_lock.acquire(False):
                        # Si el bloque está en la caché propia y no es invalido: ES HIT.
                        if self.data_Cache_P1.isInDataCache(blockConflict) and not self.data_Cache_P1.isBlockInvalid(
                                blockConflict):
                            print("lógica de hit")
                            self.mainMemory.putInMainMemoryDataSec(valueToStore, directionToStore)
                            self.data_Cache_P1.putWordInDataCache(valueToStore, directionToStore)
                        else:
                            print("lógica de miss")
                            self.mainMemory.putInMainMemoryDataSec(valueToStore, directionToStore)

                        # Se pone a esperar al hilo los ciclos que le corresponden
                        for i in range(0, 5):
                            self.threadBarrier.wait()
                            self.incrementClockCicleCounter(threadId)
                        self.mainMemory_lock.release()
                        self.dataCache1_lock.release()

                        # Se sale del while infinito
                        break
                # Si se logra capturar la caché propia, pero no la del otro
                else:
                    print("lógica de no tomada la cache del otro")
                    self.dataCache1_lock.release()
                    self.threadBarrier.wait()
                    self.incrementClockCicleCounter(threadId)
            # Si no pudo tomar su propio candado
            else:
                self.threadBarrier.wait()
                self.incrementClockCicleCounter(threadId)

    def beq(self, x1, x2, inm, threadId):
        if x1 == x2:
            self.generalProcessCounter[threadId] = self.generalProcessCounter[threadId] + (inm * 4)

    def bne(self, x1, x2, inm, threadId):
        if x1 != x2:
            self.generalProcessCounter[threadId] = self.generalProcessCounter[threadId] + (inm * 4)

    def jal(self, x1, inm, threadId):
        #x1<-PC, PC<-PC+n
        self.generalResgisterVector[threadId][x1] = self.generalProcessCounter[threadId]
        self.generalProcessCounter[threadId] += self.generalProcessCounter[threadId] + inm

    def jalr(self, x1, x2, inm, threadId):
        #x2= PC ; PC = x1+n
        self.generalResgisterVector[x2] = self.generalProcessCounter[threadId]
        self.generalProcessCounter[threadId] = self.generalResgisterVector[x1] + inm

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
            # Si aún quedan hilillos por ejecutar
            if 7 < self.contextMat.AmountOfLittleThreads:
                self.changePCValue(threadId,
                                   self.contextMat.getInstrDirectInMemory(self.contextMat.getNextThreadToExecute()))
                # Blanque el vector de registros del procesador cada vez que inicia una nueva instrucción
                self.resetRegisterVectorProcessor(threadId, self.contextMat.getRegisterVector(
                    self.contextMat.getNextThreadToExecute()))
                self.contextMat.changeThreadToExecute()
            # Si ya no quedan hilillos por ejecutar
            else:
                # Si ya no encuentra más hilillos con qué trabajar, cambia el estado del hilo a terminado
                self.generalThreadCondition[int(threadId)] = False

            blockNumber = int(self.generalProcessCounter[int(threadId)] / 16)

            if self.generalInstr_Cache[int(threadId)].isInInstrucCache(blockNumber):
                print("Hacer lógica de hit")
                wordNum = self.getNumberOfWordInBlock(threadId, self.getPCValue(threadId))
                word = self.getWordFromInstrCache(threadId, wordNum, blockNumber)

            else:
                print("Hacer lógica de fallo: ")

        # Esta condicional divide el programa en si el procesador continua o finaliza y espera a que finalize el otro hilo
        if self.generalThreadCondition[int(threadId)]:
            # if self.getThreadCondition(threadId):
            print("Hago logic de verdad")
        else:
            print("Hago logica de falso. Soy el hilo: " + str(threadId))

            # Se implementa la lógica de un do-while para obligar a que los dos hilos se detengan
            while True:
                time.sleep(1)
                print(" BUCLE: " + str(threadId))

                self.threadBarrier.wait()

                self.incrementClockCicleCounter(threadId)

                print("condicion: " + str(self.generalThreadCondition[0]) + " condicion2: " + str(
                    self.generalThreadCondition[1]))

                # if not self.threadCondition_P2 or not self.threadCondition_P1:
                if not self.generalThreadCondition[0] or not self.generalThreadCondition[1]:
                    break

            with self.contextMatrix_lock:
                self.generalData_Cache[int(threadId)].showDataSectionMatrix(threadId)

    def threadInicializer(self):

        hilo1 = threading.Thread(target=self.processorBehaivor, args=("0"), name=0)
        hilo2 = threading.Thread(target=self.processorBehaivor, args=("1"), name=1)
        hilo2.start()
        hilo1.start()

        hilo1.join()
        hilo2.join()


def main():
    pru = processors()

    pru.threadInicializer()

    pru.generalData_Cache[0].setBlock(27, [2, 12, 13, 14])

    pru.lw(1, 21, 0, 0)
    pru.lw(30, 27, 0, 0)

    pru.generalData_Cache[0].showDataSectionMatrix("0")
    print(pru.registerVector_P1[1])
    print("Antes de la suma")
    print(pru.registerVector_P1[2])
    pru.div(2, 1, 30, 0)
    print("despues de la suma")
    print(pru.registerVector_P1[2])

    #pru.mainMemory.showMainMemory()

    #print(pru.registerVector_P1[1])
    #pru.data_Cache_P1.showDataSectionMatrix("1")



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
