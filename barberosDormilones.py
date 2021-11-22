from threading import Thread, Event, Semaphore
import time, random

mutex = Semaphore(1)
clientesEsperando = []
asientos = 4
clientes = []

class Cliente: 
    def __init__(self,name):
        self.name = name

class Barbero:
    barberoTrabajando = Event() # Creamos un evento que se encargará de monitorear la actividad del barbero

    def durmiendo(self):
        self.barberoTrabajando.wait() # Se bloquea hasta que una bandera interna se active
    
    def despierto(self):
        self.barberoTrabajando.set() # Se activa la bandera interna y se inicia
    
    def cortandoCabello(self,cliente):
        self.barberoTrabajando.clear() # El barbero está ocupado

        print("Cortándole el cabello al cliente: {0}".format(cliente.name)) 
        tiempoDeCorte = random.randrange(5,15) # El tiempo puede variar entre 5 a 15 segundos por cada corte
        time.sleep(tiempoDeCorte)
        
        print(">>> {0} se terminó de cortar el cabello".format(cliente.name))

barbero = Barbero() # Creamos una instancia del barbero

def cortandoCabello():
    while True:
        mutex.acquire()

        if len(clientesEsperando) > 0:
            c = clientesEsperando[0]
            del clientesEsperando[0]

            mutex.release()
            barbero.cortandoCabello(c)
        else:
            mutex.release()
            print("El barbero está durmiendo.")

            barbero.durmiendo()
            print("Barbero se despertó.")

def clienteNuevo(cliente):
    mutex.acquire()
    print(">> El cliente: {0} llegó a la barbería".format(cliente.name))

    if len(clientesEsperando) == asientos:
        print('- El cuarto de espera ya está lleno, {0} se retira de la barbería'.format(cliente.name))
        mutex.release()
    else:
        print('>>> {0} se sentó en el cuarto de espera'.format(cliente.name))
        clientesEsperando.append(cliente)

        mutex.release()
        barbero.despierto()

def empiezaATtabajar():
    hilo = Thread(target = cortandoCabello)
    hilo.start()


def generaNombres():
    archivo = open("nombres.txt","r") # Modificar la dirección en caso de ser necesario
    nombres = archivo.readlines()    
    valores = random.randrange(30)

    for i in range(valores):
        nombre = nombres[random.randrange(900)]
        nombreLmp = nombre.replace("\n","")
        clientes.append(Cliente(nombreLmp))


if __name__ == '__main__':
    print("La barbería abrió")
    generaNombres()
    empiezaATtabajar()

    while len(clientes) > 0:
        c = clientes.pop()
        clienteNuevo(c) # Nuevo cliente entra a la barbería

        time.sleep(random.randrange(3,7))