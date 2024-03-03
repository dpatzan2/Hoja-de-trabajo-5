import simpy
import random

class Programa:

    def __init__(self, env, ram, procesador, tiempo_inicio):
        self.memoria = random.randint(1, 10)  # Cambiar
        self.num_instruc = random.randint(1, 10)  # Cambiar
        self.env = env
        self.ram = ram
        self.procesador = procesador
        self.tiempo_inicio = tiempo_inicio
        self.tiempo_ejecucion = 0  # Variable para almacenar el tiempo de ejecución

    def pedir_memoria(self):
        print(f"Tiempo {self.env.now}: Solicitando {self.memoria} de memoria RAM")
        yield self.ram.get(self.memoria)

    def usar_cpu(self):
        print(f"Tiempo {self.env.now}: Usando CPU , Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.env.timeout(1)  # Simular el tiempo de ejecución de instrucciones
        self.tiempo_ejecucion += 1

    def pedir_io(self):
        print(f"Tiempo {self.env.now}: Realizando operaciones de I/O , Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.env.timeout(1)  # Simular el tiempo de operaciones de I/O
        self.tiempo_ejecucion += 1

    def run(self):
        print(f"Tiempo {self.env.now}: Iniciando ejecución , Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        self.tiempo_inicio = self.env.now
        yield self.env.process(self.pedir_memoria())
        yield self.env.process(self.usar_cpu())
        self.num_instruc -= 3  # Se ejecutan 3 instrucciones en cada ciclo
        while self.num_instruc > 0:
            yield self.env.timeout(1)  # Simular el tiempo de ejecución de instrucciones
            self.num_instruc -= 3  # Se ejecutan 3 instrucciones en cada ciclo
            if random.randint(1, 21) == 1:
                yield self.env.process(self.pedir_io())
        print(f"Tiempo {self.env.now}: Proceso terminado, liberando memoria, Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.ram.put(self.memoria)
        return self.tiempo_ejecucion

def simular(env, ram, num_procesos):
    tiempos_ejecucion = []
    print("Simulando....")
    for i in range(num_procesos):  # Simular la cantidad de programas especificada por el usuario
        programa = Programa(env, ram, None, env.now)  # El procesador no se usa en esta versión
        tiempo_ejecucion = yield env.process(programa.run())
        tiempos_ejecucion.append(tiempo_ejecucion)
        yield env.timeout(1)  # Simular intervalos de llegada de programas
    tiempo_promedio = sum(tiempos_ejecucion) / len(tiempos_ejecucion)
    print(f"-------------------------------------------------")
    print(f"Tiempo promedio de ejecución: {tiempo_promedio}")
    print(f"-------------------------------------------------")

env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)  # Inicializar la memoria RAM con capacidad 100

num_procesos = int(input("Ingrese la cantidad de procesos a simular: "))
env.process(simular(env, ram, num_procesos))

env.run()
