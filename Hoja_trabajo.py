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
        print(f"Tiempo {self.env.now}: Iniciando ejecución")
        yield self.env.process(self.pedir_memoria())
        yield self.env.process(self.usar_cpu())
        self.num_instruc -= 3  # Se ejecutan 3 instrucciones en cada ciclo
        while self.num_instruc > 0:
            yield self.env.timeout(1)  # Simular el tiempo de ejecución de instrucciones
            self.num_instruc -= 3  # Se ejecutan 3 instrucciones en cada ciclo
            if random.randint(1, 21) == 1:
                yield self.env.process(self.pedir_io())
        print(f"Tiempo {self.env.now}: Proceso terminado, liberando memoria")
        yield self.ram.put(self.memoria)

def simular(env, ram, num_procesos):
    print("Simulando....")
    for i in range(num_procesos):  # Simular la cantidad de programas especificada por el usuario
        programa = Programa(env, ram, None, env.now)  # El procesador no se usa en esta versión
        env.process(programa.run())
        yield env.timeout(1)  # Simular intervalos de llegada de programas

env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)  # Inicializar la memoria RAM con capacidad 100

num_procesos = int(input("Ingrese la cantidad de procesos a simular: "))
env.process(simular(env, ram, num_procesos))

env.run()
