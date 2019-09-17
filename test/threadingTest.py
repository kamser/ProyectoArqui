import threading
import time

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

hilo1 = threading.Thread(target = contar, name = 1)
hilo2 = threading.Thread(target = contar, name = 2)
hilo1.start()
hilo2.start()

littlethreadList = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt"]
mainMemory_InstruSection = []
mainMemory_DataSection = []
matrixForEachInstruction = []
listaAxu = []

for littleThreadItem in littlethreadList:
    archivo = open(littleThreadItem, "r")
    for linea in archivo.readlines():
        listaAxu = linea.split()
        for item in listaAxu:
            mainMemory_InstruSection.append(item)

archivo.close()
print(mainMemory_InstruSection[:])


listaTest = [0, [1,2,3]]

print(listaTest[1][1])



