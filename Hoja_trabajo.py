import simpy
import random

class Programa:

    def __init__(self, env, ram, procesador, tiempo_inicio):
        self.memoria = random.randint(1, 10) # Cambiar
        self.num_instruc = random.randint(1, 10) # Cambiar
        self.env = env
        self.ram = ram
        self.procesador = procesador
        self.tiempo_inicio = tiempo_inicio

    def pedir_memoria(self):
        print(f"Tiempo {self.env.now}: Solicitando {self.memoria} de memoria RAM")
        yield self.ram.get(self.memoria)

    def usar_cpu(self):
        print(f"Tiempo {self.env.now}: Usando CPU")
        yield self.env.timeout(1)  # Simular el tiempo de ejecución de instrucciones

    def pedir_io(self):
        print(f"Tiempo {self.env.now}: Realizando operaciones de I/O")
        yield self.env.timeout(1)  # Simular el tiempo de operaciones de I/O

    def run(self):
        # logica de como cambiar de estados
        # Pedir memoria
        # with request etc
            # pedir cpu
        yield self.env.timeout(10)
               # ejecutar 3 instrucciones
               # ponga un timeout
            # pedir io/o no
               # esperar
            # fin
            
def simular(env, param):
    #cambiar
    print("Simulando....")
        
# Cambiar a procesos
        

env = simpy.Environment()
track = simpy.Resource(env, capacity=1)  # Define the race track as a shared resource
print("Llamada a simular")
env.process(simular(env, track))

env.run()

# TODO
# - construir cpu
# - construir ram
# - crear programas/procesos
# - solicitar memoria