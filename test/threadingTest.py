import threading
import time

from structureModules.contexMatrix import contexMatrix

testBarrier = threading.Barrier(2)


def contar():
    #Contar hasta cien
    contador = 0
    while contador < 20:
        contador += 1
        print("Hilo: " + threading.current_thread().getName()  + " Contador: " + str(contador))

        testBarrier.wait()
        if threading.current_thread().getName() == "1":
            print("Liberando hilos")
            time.sleep(1)



def main():
    '''pru = contexMatrix(7)
    pru.setDirect_Id_Condition(384, 0, "i")
    pru.setDirect_Id_Condition(384, 1, "i")
    pru.setDirect_Id_Condition(400, 2, "i")
    pru.setDirect_Id_Condition(500, 3, "i")
    pru.setDirect_Id_Condition(600, 4, "i")
    pru.setDirect_Id_Condition(700, 5, "i")
    pru.setDirect_Id_Condition(800, 6, "i")
    #pru.showContextMatrix()
    #print(str(pru.getInstrDirectInMemory(4)))

    hilo1 = threading.Thread(target=contar, name=1)
    hilo2 = threading.Thread(target=contar, name=2)
    hilo1.start()
    hilo2.start()'''

    littlethreadList = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
    mainMemory_InstruSection = []
    mainMemory_DataSection = []
    matrixForEachInstruction = []
    listaAxu = []

    for littleThreadItem in littlethreadList:
        archivo = open(littleThreadItem, "r")
        for linea in archivo.readlines():
            listaAxu = list(map(int, linea.split()))
            #listaAxu = list(map(int, listaAxu))
            print(listaAxu[:])
            for item in listaAxu:
                mainMemory_InstruSection.append(item)

    archivo.close()
    print(mainMemory_InstruSection[:])

    listaTest = [0, [1, 2, 3]]

    print(listaTest[1][1])


    l1 = [1, 2, 3, 4, 5]
    l2 = ['a', 'b', 'c', 'd']

    l2 = l1

    print(l2[:])

    print(str(416 / 16))

if __name__ == "__main__":
    main()





