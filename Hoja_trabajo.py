import simpy
import random
import csv
import statistics

class Programa:
    def __init__(self, env, ram, procesador, tiempo_inicio, numero_proceso):
        self.memoria = random.randint(1, 10)
        self.num_instruc = random.randint(1, 10)
        self.env = env
        self.ram = ram
        self.procesador = procesador
        self.tiempo_inicio = tiempo_inicio
        self.tiempo_ejecucion = 0
        self.numero_proceso = numero_proceso

    def pedir_memoria(self):
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Solicitando {self.memoria} de memoria RAM")
        yield self.ram.get(self.memoria)

    def usar_cpu(self):
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Usando CPU , Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.env.timeout(1)
        self.tiempo_ejecucion += 1

    def pedir_io(self):
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Realizando operaciones de I/O , Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.env.timeout(1)
        self.tiempo_ejecucion += 1

    def run(self):
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Iniciando ejecución , Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        self.tiempo_inicio = self.env.now
        yield self.env.process(self.pedir_memoria())
        yield self.env.process(self.usar_cpu())
        self.num_instruc -= 3
        while self.num_instruc > 0:
            yield self.env.timeout(1)
            self.num_instruc -= 3
            if random.randint(1, 21) == 1:
                yield self.env.process(self.pedir_io())
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Terminado, liberando memoria, Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.ram.put(self.memoria)
        return self.tiempo_inicio, self.env.now

def simular(env, ram, num_procesos, intervalo):
    tiempos_ejecucion = []
    print("Simulando....")
    for i in range(num_procesos):
        numero_proceso = i + 1
        programa = Programa(env, ram, None, env.now, numero_proceso)
        tiempo_inicio, tiempo_final = yield env.process(programa.run())
        tiempos_ejecucion.append((tiempo_inicio, tiempo_final))
        yield env.timeout(intervalo)
    
    tiempo_promedio = statistics.mean(tiempo_final - tiempo_inicio for tiempo_inicio, tiempo_final in tiempos_ejecucion)
    desviacion_estandar = statistics.stdev(tiempo_final - tiempo_inicio for tiempo_inicio, tiempo_final in tiempos_ejecucion)
    print(f"-------------------------------------------------") 
    print(f"Tiempo promedio de ejecución: {tiempo_promedio}")
    print(f"Desviación estándar: {desviacion_estandar}")
    print(f"-------------------------------------------------")

    numero_random = random.randint(1, 1000)
    nombre_archivo = f"{num_procesos}_procesos_{numero_random}.csv"
    
    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Numero_Proceso', 'Tiempo_Inicio', 'Tiempo_Final'])
        for i, (tiempo_inicio, tiempo_final) in enumerate(tiempos_ejecucion):
            writer.writerow([i + 1, tiempo_inicio, tiempo_final])

    print(f"Datos almacenados en el archivo: {nombre_archivo}")

env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)

num_procesos = int(input("Ingrese la cantidad de procesos a simular: "))
intervalo = int(input("Ingrese el intervalo entre procesos (en segundos): "))

env.process(simular(env, ram, num_procesos, intervalo))

env.run()
