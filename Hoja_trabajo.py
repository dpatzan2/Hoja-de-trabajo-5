import simpy
import random
import csv
import statistics
import matplotlib.pyplot as plt

class Programa:
    def __init__(self, env, ram, procesadores, tiempo_inicio, numero_proceso):
        self.memoria = 100
        self.num_instruc = 6  # Default number of instructions
        self.env = env
        self.ram = ram
        self.procesadores = procesadores if procesadores else 1  # Default to 1 processor
        self.tiempo_inicio = tiempo_inicio
        self.tiempo_ejecucion = 0
        self.numero_proceso = numero_proceso

    def pedir_memoria(self):
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Solicitando {self.memoria} de memoria RAM")
        yield self.ram.get(self.memoria)

    def usar_cpu(self):
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Usando CPU, Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.env.timeout(1 / self.procesadores)  # Adjusting for multiple processors
        self.tiempo_ejecucion += 1

    def pedir_io(self):
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Realizando operaciones de I/O, Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.env.timeout(1)
        self.tiempo_ejecucion += 1

    def run(self):
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Iniciando ejecución, Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        self.tiempo_inicio = self.env.now
        yield self.env.process(self.pedir_memoria())
        yield self.env.process(self.usar_cpu())
        self.num_instruc -= 3
        while self.num_instruc > 0:
            yield self.env.timeout(1 / self.procesadores)  # Adjusting for multiple processors
            self.num_instruc -= 3
            if random.randint(1, 21) == 1:
                yield self.env.process(self.pedir_io())
        print(f"Tiempo {self.env.now}: Proceso {self.numero_proceso} - Terminado, liberando memoria, Tiempo de ejecución del proceso: {self.env.now - self.tiempo_inicio}")
        yield self.ram.put(self.memoria)
        return self.tiempo_inicio, self.env.now

def simular(env, ram, num_procesos, intervalo, procesadores):
    tiempos_ejecucion = []
    print("Simulando....")
    for i in range(num_procesos):
        numero_proceso = i + 1
        programa = Programa(env, ram, procesadores, env.now, numero_proceso)
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
    nombre_archivo = f"{num_procesos}_procesos_{numero_random}_intervalo_{intervalo}_procesadores_{procesadores}.csv"
    
    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Numero_Proceso', 'Tiempo_Inicio', 'Tiempo_Final'])
        for i, (tiempo_inicio, tiempo_final) in enumerate(tiempos_ejecucion):
            writer.writerow([i + 1, tiempo_inicio, tiempo_final])

    print(f"Datos almacenados en el archivo: {nombre_archivo}")

    # Generar la gráfica
    plot_tiempo_vs_procesos(tiempos_ejecucion)

def plot_tiempo_vs_procesos(tiempos_ejecucion):
    num_procesos = range(1, len(tiempos_ejecucion) + 1)
    tiempo_total = [tiempo_final - tiempo_inicio for tiempo_inicio, tiempo_final in tiempos_ejecucion]
    tiempo_acumulado = [sum(tiempo_total[:i+1]) for i in range(len(tiempo_total))]

    plt.plot(num_procesos, tiempo_acumulado, marker='o')
    plt.title('Tiempo Total de Ejecución por Número de Procesos')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Tiempo Total de Ejecución')
    plt.grid(True)
    plt.show()

env = simpy.Environment()
ram_capacity = 200

num_procesos = int(input("Ingrese la cantidad de procesos a simular: "))
intervalo = int(input("Ingrese el intervalo entre procesos (en segundos): "))

# First simulation with increased memory
ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)
env.process(simular(env, ram, num_procesos, intervalo, 1))
env.run()

# Second simulation with faster processor
ram_capacity = 100
ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)
env.process(simular(env, ram, num_procesos, intervalo, 6))
env.run()

# Third simulation with multiple processors
ram_capacity = 100
ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)
env.process(simular(env, ram, num_procesos, intervalo, 2))
env.run()
