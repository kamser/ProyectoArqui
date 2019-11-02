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
    # variable que contiene hilillo actual con el que se está trbajando
    currentLittleThread_P1 = 0
    currentLittleThread_P2 = 0
    generalCurrentLittleThread = []

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
        # Se llena el vector que contiene el hilo actual en ejecución de cada proccesador
        self.generalCurrentLittleThread.append(self.currentLittleThread_P1)
        self.generalCurrentLittleThread.append(self.currentLittleThread_P2)
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
    def addi(self, dr, r, i):
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][r] + i
        except ValueError:
            print("hilo principal")

    # dr = destination register, or1 = origin register 1, origen register 2
    def add(self, dr, or1, or2):
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][or1] + \
                                                     self.generalResgisterVector[myId][or2]
        except ValueError:
            print("hilo principal")

    # dr = destination register, or1 = origin register 1, origen register 2
    def sub(self, dr, or1, or2):
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][or1] - \
                                                     self.generalResgisterVector[myId][or2]
        except ValueError:
            print("hilo principal")

    # dr = destination register, or1 = origin register 1, origen register 2
    def mul(self, dr, or1, or2):
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][or1] * \
                                                     self.generalResgisterVector[myId][or2]
        except ValueError:
            print("hilo principal")

    # dr = destination register, or1 = origin register 1, origen register 2
    def div(self, dr, or1, or2):
        myId = int(threading.current_thread().getName())
        if self.generalResgisterVector[myId][or2] != 0: #si el divisor es distinto a 0
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][or1] // \
                                                self.generalResgisterVector[myId][or2]
        else:
            self.generalResgisterVector[myId][dr] = 0  # si el divisor es igual a 0, el resultado es 0 arbitrariamente

    # dr = destination register, n = main memory position, r = register with offset
    def lw(self, dr, n, r):
        myId = int(threading.current_thread().getName())
        while True:
            # intenta bloquear caché propia
            if self.generalDataCache_lock[myId].acquire(False):
                # hay que comprobar si el bloque está en caché
                inCache = self.generalData_Cache[myId].isInDataCache(n)
                if inCache is True:
                    self.generalResgisterVector[myId][dr] = self.generalData_Cache[myId].getWordFromCache(r, n)
                    #self.generalDataCache_lock[threadId].release()
                    break
                else:  # no está en caché
                    # Intenta bloquear el bus de datos
                    if self.mainMemory_lock.acquire(False):
                        block = self.mainMemory.getDataBlock(n)
                        # espera los ciclos correspondientes
                        for i in range(0, 20):
                            #self.threadBarrier.wait()
                            #self.incrementClockCicleCounter(threadId)
                            self.generalThreadCicleCounter[int(myId)] = self.generalThreadCicleCounter[int(myId)] + 1

                        self.generalData_Cache[myId].setBlock(n, block)
                        self.generalResgisterVector[myId][dr] = self.generalData_Cache[myId].getWordFromCache(r, n)
                #self.threadBarrier.wait()
                #self.incrementClockCicleCounter(threadId)
                self.generalThreadCicleCounter[int(myId)] = self.generalThreadCicleCounter[int(myId)] + 1
                self.generalDataCache_lock[myId].release()
                break


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
                        # self.incrementClockCicleCounter(threadId)
                        self.generalThreadCicleCounter[int(threadId)] = self.generalThreadCicleCounter[
                                                                            int(threadId)] + 1
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
        try:
            myId = int(threading.current_thread().getName())
            if x1 == x2:
                self.generalProcessCounter[myId] = self.generalProcessCounter[myId] + (inm * 4)
        except ValueError:
            print("hilo principal")

    def bne(self, x1, x2, inm, threadId):
        try:
            myId = int(threading.current_thread().getName())
            if x1 != x2:
                self.generalProcessCounter[myId] = self.generalProcessCounter[myId] + (inm * 4)
        except ValueError:
            print("hilo principal")

    def jal(self, x1, x2, inm):
        # x1<-PC, PC<-PC+n
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][x1] = self.generalProcessCounter[myId]
            self.generalProcessCounter[myId] += self.generalProcessCounter[myId] + inm
        except ValueError:
            print("hilo principal")

    def jalr(self, x1, x2, inm):
        #x2= PC ; PC = x1+n
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][x2] = self.generalProcessCounter[myId]
            self.generalProcessCounter[myId] = self.generalResgisterVector[myId][x1] + inm
        except ValueError:
            print("hilo principal")

    def fin(self):
        print("Se metio a fin")
        myId = int(threading.current_thread().getName())
        littleThreadToUpdate = self.generalCurrentLittleThread[myId]
        self.threadBarrier.wait()
        print("My id: " + str(myId))
        self.generalThreadCicleCounter[myId] = self.generalThreadCicleCounter[myId] + 1
        self.contextMat.updateRegisterLittleThread(self.generalResgisterVector[myId], littleThreadToUpdate)

    def selectInstructionType(self, operationCode, firstOperator, secondOperator, thrirdOperator, threadId):
        if operationCode == 19:
            self.addi(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 71:
            self.add(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 83:
            self.sub(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 72:
            self.mul(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 56:
            self.div(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 5:
            self.lw(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 37:
            self.sw(firstOperator, secondOperator, thrirdOperator, threadId)
        elif operationCode == 99:
            self.beq(firstOperator, secondOperator, thrirdOperator, threadId)
        elif operationCode == 100:
            self.bne(firstOperator, secondOperator, thrirdOperator, threadId)
        elif operationCode == 111:
            self.jal(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 103:
            self.jalr(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 999:
            self.fin()
        else:
            print("Codigo de operacion invalido")
        '''switcher = {
            19: self.addi(firstOperator, secondOperator, thrirdOperator),
            71: self.add(firstOperator, secondOperator, thrirdOperator),
            83: self.sub(firstOperator, secondOperator, thrirdOperator),
            72: self.mul(firstOperator, secondOperator, thrirdOperator),
            #56: self.div(firstOperator, secondOperator, thrirdOperator),
            #5: self.lw(firstOperator, secondOperator, thrirdOperator, threadId),
            37: self.sw(firstOperator, secondOperator, thrirdOperator, threadId),
            99: self.beq(firstOperator, secondOperator, thrirdOperator, threadId),
            100: self.bne(firstOperator, secondOperator, thrirdOperator, threadId),
            111: self.jal(firstOperator, secondOperator, thrirdOperator),
            #103: self.jalr(firstOperator, secondOperator, thrirdOperator),
            999: self.fin()
        }
        return switcher.get(operationCode, "Invalido")'''

        # switcher.get(operationCode, "parameter value out of range")

        #if operationCode == 999:
         #   self.fin()

    def processorBehaivor(self, threadId):
        # Hilo se mantiene procesando hasta que se terminen los hilillos///TENER CUIDADO CON LOS DO WHILE, POR LOS BREAKS
        while self.contextMat.getNextThreadToExecute() < self.contextMat.AmountOfLittleThreads:
            with self.contextMatrix_lock:
                self.generalCurrentLittleThread[
                    int(threading.current_thread().getName())] = self.contextMat.getNextThreadToExecute()
                time.sleep(1)
                # Si aún quedan hilillos por ejecutar
                if 7 < self.contextMat.AmountOfLittleThreads:
                    self.changePCValue(threadId,
                                       self.contextMat.getInstrDirectInMemory(self.contextMat.getNextThreadToExecute()))
                    # Blanque el vector de registros del procesador cada vez que inicia una nueva instrucción
                    self.resetRegisterVectorProcessor(threadId, self.contextMat.getRegisterVector(
                        self.generalCurrentLittleThread[int(threading.current_thread().getName())]))
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

        hilo1 = threading.Thread(target=self.processorBehaivor, args=("0"), name="0")
        hilo2 = threading.Thread(target=self.processorBehaivor, args=("1"), name="1")
        hilo2.start()
        hilo1.start()

        hilo1.join()
        hilo2.join()


def main():
    pru = processors()

    # pru.threadInicializer()

    pru.generalData_Cache[0].setBlock(27, [2, 12, 13, 14])
    pru.generalData_Cache[1].setBlock(12, [20, 21, 22, 23])

    # pru.lw(1, 21, 0, 0)
    # pru.lw(30, 27, 0, 0)
    pru.registerVector_P1[1] = 30
    pru.registerVector_P1[5] = 5
    # RESULADO 30/5 = 6

    pru.registerVector_P2[1] = 25
    pru.registerVector_P2[5] = 5
    # RESULADO 25/5 = 5
    print("----------------------------")
    hilo1 = threading.Thread(target=pru.div, args=(2, 1, 5), name="0")
    hilo2 = threading.Thread(target=pru.div, args=(3, 1, 5), name="1")
    hilo2.start()
    hilo1.start()

    print(pru.registerVector_P1[2])
    print(pru.registerVector_P2[3])

    hilo1 = threading.Thread(target=pru.lw, args=(3, 27, 0), name="0") # debe cargar un 2 en la pos 3
    hilo2 = threading.Thread(target=pru.lw, args=(4, 12, 2), name="1") # debe cargar un 22 en la pos 4
    hilo2.start()
    hilo1.start()
    print("----------------------------")
    print(pru.registerVector_P1[3])
    print(pru.registerVector_P2[4])

    print("----------------------------")
    print("PC ANTES DE JALR:")
    print(pru.generalProcessCounter[0])
    print(pru.generalProcessCounter[1])

    pru.generalProcessCounter[0] = 39
    pru.generalProcessCounter[1] = 45

    hilo1 = threading.Thread(target=pru.jalr, args=(3, 9, 90), name="0")  # X2 = PC = 39, new PC = 2 + 90
    hilo2 = threading.Thread(target=pru.jalr, args=(4, 8, 67), name="1")  # X2 = PC = 45, new PC = 22 + 67
    hilo2.start()
    hilo1.start()

    print("X2 Y PC DESP DE JALR:")
    print(pru.generalResgisterVector[0][9], "---", pru.generalProcessCounter[0])
    print(pru.generalResgisterVector[1][8], "---", pru.generalProcessCounter[1])
    print("----------------------------")

    hilo1 = threading.Thread(target=pru.selectInstructionType, args=(19, 1, 9, 1, 0), name="0")
    hilo1.start()
    print(pru.generalResgisterVector[0][1])




if __name__ == "__main__":
    main()
