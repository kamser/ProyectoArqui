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
    lock_MM_InstCache = 0
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
    # Candado de sicronización para la memoria princiapal o el bus de datos y de instrucciones
    mainMemory_lock = 0
    mainMemory_Lock_InstrBus = 0
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
        directionInstrucSec = 384
        threadId = 0
        self.lock = threading.Lock()
        self.lock_CD1 = threading.Lock()
        self.lock_CD2 = threading.Lock()
        self.lock_MC = threading.Lock()
        self.lock_MM = threading.Lock()                     #Candado para bus de datos
        self.lock_MM_InstCache = threading.Lock()           #Candado para bus de isntru
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
        self.mainMemory_Lock_InstrBus = threading.Condition(self.lock_MM_InstCache)
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

    # Sirve para los branch
    def changePCValue(self, newValue):
        myId = int(threading.current_thread().getName())
        self.generalProcessCounter[myId] = newValue

    def incrementPCValue(self):
        myId = int(threading.current_thread().getName())
        self.generalProcessCounter[myId] = self.generalProcessCounter[myId] + 4

    def resetRegisterVectorProcessor(self, vectorFormContextMatrix):
        myId = int(threading.current_thread().getName())
        self.generalResgisterVector[myId] = vectorFormContextMatrix

    def getBlockNumber(self, threadId):
        myId = int(threading.current_thread().getName())
        blockNum = int(self.generalProcessCounter[myId] / 16)
        return blockNum

    # dr = destination register, r = register, i = inmediate
    def addi(self, dr, r, i):
        print("*****************************************************************************************Se metio a addi" + ". Soy el hilo: " + threading.current_thread().getName())
        try:
            myId = int(threading.current_thread().getName())
            print("|||||||||||||||||||||||||||||El valor de registro antes: " + str(self.generalResgisterVector[myId][dr]) + ". Soy el hilo: " + threading.current_thread().getName())
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][r] + i
            print("|||||||||||||||||||||||||||||El valor de registro DESPUESss: " + str(self.generalResgisterVector[myId][dr]) + ". Soy el hilo: " + threading.current_thread().getName())

        except ValueError:
            print("hilo principal")

    # dr = destination register, or1 = origin register 1, origen register 2
    def add(self, dr, or1, or2):
        print("*****************************************************************************************Se metio a add" + ". Soy el hilo: " + threading.current_thread().getName())
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][or1] + \
                                                     self.generalResgisterVector[myId][or2]
        except ValueError:
            print("hilo principal")

    # dr = destination register, or1 = origin register 1, origen register 2
    def sub(self, dr, or1, or2):
        print("*****************************************************************************************Se metio a sub" + ". Soy el hilo: " + threading.current_thread().getName())
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][or1] - \
                                                     self.generalResgisterVector[myId][or2]
        except ValueError:
            print("hilo principal")

    # dr = destination register, or1 = origin register 1, origen register 2
    def mul(self, dr, or1, or2):
        print("*****************************************************************************************Se metio a mul" + ". Soy el hilo: " + threading.current_thread().getName())
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][or1] * \
                                                     self.generalResgisterVector[myId][or2]
        except ValueError:
            print("hilo principal")

    # dr = destination register, or1 = origin register 1, origen register 2
    def div(self, dr, or1, or2):
        print("*****************************************************************************************Se metio a div" + ". Soy el hilo: " + threading.current_thread().getName())
        myId = int(threading.current_thread().getName())
        if self.generalResgisterVector[myId][or2] != 0: #si el divisor es distinto a 0
            self.generalResgisterVector[myId][dr] = self.generalResgisterVector[myId][or1] // \
                                                self.generalResgisterVector[myId][or2]
        else:
            self.generalResgisterVector[myId][dr] = 0  # si el divisor es igual a 0, el resultado es 0 arbitrariamente

    # dr = destination register, n = main memory position, r = register with offset
    def lw(self, dr, n, r):
        print("*****************************************************************************************Se metio a lw" + ". Soy el hilo: " + threading.current_thread().getName())
        myId = int(threading.current_thread().getName())
        while True:
            # intenta bloquear caché propia
            if self.generalDataCache_lock[myId].acquire(False):
                # hay que comprobar si el bloque está en caché
                directionInMemory = n + r
                inCache = self.generalData_Cache[myId].isInDataCache(directionInMemory)
                if inCache is True:
                    word = self.generalData_Cache[myId].getNumberOfWordInBlock(directionInMemory)
                    self.generalResgisterVector[myId][dr] = self.generalData_Cache[myId].getWordFromCache(word, directionInMemory)
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

    def lw_InstrCach(self, blockToLoadNumber):
        print("*****************************************************************************************Se metio a lw_inst" + ". Soy el hilo: " + threading.current_thread().getName())
        myId = int(threading.current_thread().getName())           #Puede dar problemas el ponerlo ahí y que se sobrescriba
        while True:
            if self.mainMemory_Lock_InstrBus.acquire(False):
                print("lógica de obtenido el bus de instrucciones" + ". El bloque es: " + str(blockToLoadNumber) + ". Soy el hilo: " + threading.current_thread().getName())
                block = self.mainMemory.getInstructionBlock(blockToLoadNumber)
                self.generalInstr_Cache[myId].setBlock(blockToLoadNumber, block)
                self.mainMemory_Lock_InstrBus.release()
                break

            else:
                print("lógica de no obtenido el bus de isntrucciones" + ". El bloque es: " + str(blockToLoadNumber))
                self.threadBarrier.wait()
                self.generalThreadCicleCounter[myId] = self.generalThreadCicleCounter[myId] + 1

    def sw(self, valueToStore, displacement, registerValue):
        print("*****************************************************************************************Se metio a sw" + ". Soy el hilo: " + threading.current_thread().getName())
        directionToStore = displacement + registerValue
        blockConflict = int(directionToStore / 16)
        threadId = int(threading.current_thread().getName())
        otherThreadId = 0
        if threadId < 1:
            otherThreadId = 1

        while True:
            # intenta bloquear caché propia
            if self.generalDataCache_lock[threadId].acquire(False):
                # intenta bloquear caché del otro procesador
                if self.generalDataCache_lock[otherThreadId].acquire(False):
                    if self.generalData_Cache[otherThreadId].isInDataCache(blockConflict) and self.generalData_Cache[otherThreadId].isBlockInvalid(
                            blockConflict):
                        self.generalData_Cache[otherThreadId].invalidBlock(blockConflict)
                        self.threadBarrier.wait()
                        self.generalThreadCicleCounter[int(threadId)] = self.generalThreadCicleCounter[int(threadId)] + 1

                    #Libera la caché del otro procesador
                    self.generalDataCache_lock[otherThreadId].release()

                    # Intenta bloquear el bus de datos
                    if self.mainMemory_lock.acquire(False):
                        # Si el bloque está en la caché propia y no es invalido: ES HIT.
                        if self.generalData_Cache[threadId].isInDataCache(blockConflict) and not self.generalData_Cache[threadId].isBlockInvalid(
                                blockConflict):
                            print("lógica de hit" + ". Soy el hilo: " + threading.current_thread().getName())
                            #Se hace el cambio en memoria
                            self.mainMemory.putInMainMemoryDataSec(valueToStore, directionToStore)
                            #Se hace el cambio en la caché propia
                            self.generalData_Cache[threadId].putWordInDataCache(valueToStore, directionToStore)
                        else:
                            print("lógica de miss" + ". Soy el hilo: " + threading.current_thread().getName())
                            # Se hace el cambio en memoria
                            self.mainMemory.putInMainMemoryDataSec(valueToStore, directionToStore)

                        # Se pone a esperar al hilo los ciclos que le corresponden
                        for i in range(0, 5):
                            self.threadBarrier.wait()
                            self.generalThreadCicleCounter[int(threadId)] = self.generalThreadCicleCounter[
                                                                                int(threadId)] + 1
                        self.mainMemory_lock.release()
                        self.generalDataCache_lock[threadId].release()

                        # Se sale del while infinito
                        break
                    #Para el caso donde no logre obtener el bus de datos, se cree que no se va a poder dar nunca,
                    #ya que se requieren las dos caches para llegar a este punto, si sólo tiene la propia,
                    # núnca va a llegar hasta aquí.

                # Si se logra capturar la caché propia, pero no la del otro
                else:
                    print("lógica de no tomada la cache del otro. Soy el hilo " + str(threadId))
                    self.generalDataCache_lock[threadId].release()
                    self.threadBarrier.wait()
                    self.generalThreadCicleCounter[int(threadId)] = self.generalThreadCicleCounter[int(threadId)] + 1
            # Si no pudo tomar su propio candado
            else:
                print("lógica de no tomada la cache PROPIA. Soy el hilo " + str(threadId))
                self.threadBarrier.wait()
                self.generalThreadCicleCounter[int(threadId)] = self.generalThreadCicleCounter[int(threadId)] + 1

    def beq(self, x1, x2, inm):
        print("*****************************************************************************************Se metio a beq" + ". Soy el hilo: " + threading.current_thread().getName())
        myId = int(threading.current_thread().getName())
        print("_____________________________________________El valor del PC antes del BEQ: " + str(self.generalProcessCounter[myId]) + ". Soy el hilo: " + threading.current_thread().getName())
        print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||Valor X1: " + str(self.generalResgisterVector[myId][x1]) + ". Valor X2: " + str(self.generalResgisterVector[myId][x2]) + ". Soy el hilo: " + threading.current_thread().getName())

        if self.generalResgisterVector[myId][x1] == self.generalResgisterVector[myId][x2]:
            self.generalProcessCounter[myId] = self.generalProcessCounter[myId] + (inm * 4)

        print("_____________________________________________El valor del PC DESPUES del BEQ: " + str(
            self.generalProcessCounter[myId]) + ". Soy el hilo: " + threading.current_thread().getName())

    def bne(self, x1, x2, inm):
        print("*****************************************************************************************Se metio a bne" + ". Soy el hilo: " + threading.current_thread().getName())

        myId = int(threading.current_thread().getName())
        print("_____________________________________________El valor del PC antes del BEQ: " + str(
            self.generalProcessCounter[myId]) + ". Soy el hilo: " + threading.current_thread().getName())
        print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||Valor X1: " + str(self.generalResgisterVector[myId][x1]) + ". Valor X2: " + str(self.generalResgisterVector[myId][x2]) + ". Soy el hilo: " + threading.current_thread().getName())
        if self.generalResgisterVector[myId][x1] != self.generalResgisterVector[myId][x2]:
            self.generalProcessCounter[myId] = self.generalProcessCounter[myId] + (inm * 4)

        print("_____________________________________________El valor del PC DESPUES del BEQ: " + str(
            self.generalProcessCounter[myId]) + ". Soy el hilo: " + threading.current_thread().getName())

    def jal(self, x1, x2, inm):
        # x1<-PC, PC<-PC+n
        print("*****************************************************************************************Se metio a jal" + ". Soy el hilo: " + threading.current_thread().getName())
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][x1] = self.generalProcessCounter[myId]
            self.generalProcessCounter[myId] += self.generalProcessCounter[myId] + inm
        except ValueError:
            print("hilo principal")

    def jalr(self, x1, x2, inm):
        print("*****************************************************************************************Se metio a jalr" + ". Soy el hilo: " + threading.current_thread().getName())
        #x2= PC ; PC = x1+n
        try:
            myId = int(threading.current_thread().getName())
            self.generalResgisterVector[myId][x2] = self.generalProcessCounter[myId]
            self.generalProcessCounter[myId] = self.generalResgisterVector[myId][x1] + inm
        except ValueError:
            print("hilo principal")

    def fin(self):
        print("*****************************************************************************************Se metio a fin" + ". Soy el hilo: " + threading.current_thread().getName())
        myId = int(threading.current_thread().getName())
        littleThreadToUpdate = self.generalCurrentLittleThread[myId]
        self.threadBarrier.wait()
        self.generalThreadCicleCounter[myId] = self.generalThreadCicleCounter[myId] + 1
        self.contextMat.updateRegisterLittleThread(self.generalResgisterVector[myId], littleThreadToUpdate)
        self.contextMat.setConditionOfLittleThread(littleThreadToUpdate, "f")

    def selectInstructionType(self, operationCode, firstOperator, secondOperator, thrirdOperator):
        myId = int(threading.current_thread().getName())

        if operationCode == 19: #**
            self.addi(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 71:
            self.add(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 83:
            self.sub(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 72:
            self.mul(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 56:
            self.div(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 5: #**
            self.lw(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 37: #**
            self.sw(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 99:
            self.beq(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 100:
            self.bne(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 111:
            self.jal(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 103:
            self.jalr(firstOperator, secondOperator, thrirdOperator)
        elif operationCode == 999:
            self.fin()
        else:
            print("Codigo de operacion invalido")


    def processorBehaivor(self, threadId):
        # Hilo se mantiene procesando hasta que se terminen los hilillos///TENER CUIDADO CON LOS DO WHILE, POR LOS BREAKS
        while self.generalThreadCondition[0] or self.generalThreadCondition[1]:
            #Procesadores intentan bloquear matriz de contextos
            with self.contextMatrix_lock:
                self.generalCurrentLittleThread[
                    int(threading.current_thread().getName())] = self.contextMat.getNextThreadToExecute()
                print("El hilillo a ejecutar es: " + str(self.generalCurrentLittleThread[
                    int(threading.current_thread().getName())]) + ". Soy el hilo: " + threading.current_thread().getName())
                time.sleep(1)
                # Si aún quedan hilillos por ejecutar
                if self.contextMat.getNextThreadToExecute() < self.contextMat.AmountOfLittleThreads:
                    self.changePCValue(self.contextMat.getInstrDirectInMemory(self.contextMat.getNextThreadToExecute()))
                    print("LA direccion del bloque a ejecutar es: " + str(
                        self.generalProcessCounter[int(threadId)]) + ". Soy el hilo: " + threading.current_thread().getName())
                    # Blanque el vector de registros del procesador cada vez que inicia una nueva instrucción
                    self.resetRegisterVectorProcessor(self.contextMat.getRegisterVector(
                        self.generalCurrentLittleThread[int(threading.current_thread().getName())]))
                    self.contextMat.changeThreadToExecute()
                # Si ya no quedan hilillos por ejecutar
                else:
                    # Si ya no encuentra más hilillos con qué trabajar, cambia el estado del hilo a terminado
                    self.generalThreadCondition[int(threadId)] = False

            # Esta condicional divide el programa en si el procesador continua o finaliza y espera a que finalize el otro hilo
            if self.generalThreadCondition[int(threadId)]:
                print("Hago logic de continuar con siguiente hilillo" + ". Soy el hilo: " + str(threadId))
                while self.contextMat.getLittleThreadCondition(self.generalCurrentLittleThread[int(threadId)]) != "f":   #POSIBLE FALLO
                    blockNumber = int(self.generalProcessCounter[int(threadId)] / 16)
                    print("El bloque a ejecutar es: " + str(blockNumber) + ". Soy el hilo: " + threading.current_thread().getName())
                    self.incrementPCValue()

                    # Si no está la instrucción en la caché de isntrucciones
                    if not self.generalInstr_Cache[int(threadId)].isInInstrucCache(blockNumber):
                        self.lw_InstrCach(blockNumber)

                    # SIEMPRE se hace: Si está se sube y modifica los registros, si no, lo sube
                    # busca el bloque y hace lo mismo que si sí, por eso no se encapsula.
                    wordNum = self.generalInstr_Cache[int(threadId)].getNumberOfWordInBlock(
                        self.generalProcessCounter[int(threadId)])
                    word = self.generalInstr_Cache[int(threadId)].getWordFromCache(wordNum, blockNumber)

                    # Se selecciona la instrucción a ejecutar.
                    self.selectInstructionType(word[0], word[1], word[2], word[3])

                    # Cuando se termina una instrucción, se pone al procesador a esperar
                    self.threadBarrier.wait()
                    self.generalThreadCicleCounter[int(threadId)] = self.generalThreadCicleCounter[int(threadId)] + 1

                print("------------------------------------------------------------------------------------------------TERMINO CON EL HILILLO: " + str(self.generalCurrentLittleThread[int(threading.current_thread().getName())]))
                self.contextMat.showContextMatrix()
                self.mainMemory.showMainMemory()
                print("El PC es: " + str(self.generalProcessCounter[int(threadId)]) + ". Soy el hilo: " + str(threadId))
                time.sleep(1)
            else:
                print("Hago logica de Finalizar. Soy el hilo: " + str(threadId))

                # Se implementa la lógica de un do-while para obligar a que los dos hilos se detengan
                while True:
                    time.sleep(1)

                    self.threadBarrier.wait()

                    self.generalThreadCicleCounter[int(threadId)] = self.generalThreadCicleCounter[int(threadId)] + 1

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

    pru.threadInicializer()
    '''
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
    print(pru.generalResgisterVector[0][1])'''




if __name__ == "__main__":
    main()
