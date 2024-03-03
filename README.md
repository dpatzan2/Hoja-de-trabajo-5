**README**

# Simulación de Procesos con SimPy

Esta aplicación simula el comportamiento de procesos en un entorno utilizando SimPy, una biblioteca de simulación en Python. Los procesos simulados solicitan memoria, utilizan la CPU y realizan operaciones de entrada/salida (I/O) de manera aleatoria.

## Especificaciones Técnicas

### Requerimientos del Sistema

- Python 3.11.2
- Bibliotecas: SimPy, matplotlib

### Funcionalidades

- **Simulación de Procesos:** La aplicación simula múltiples procesos que solicitan memoria, utilizan la CPU y realizan operaciones de entrada/salida (I/O).
- **Cálculo de Tiempo Promedio:** Calcula el tiempo promedio de ejecución de los procesos simulados.
- **Generación de Gráficos:** Muestra un gráfico que representa el tiempo promedio de ejecución en función del número de procesos simulados.
- **Almacenamiento de Datos:** Guarda los datos de ejecución de cada proceso en un archivo CSV para su posterior análisis.

### Estructura del Código

El código está organizado en las siguientes secciones:

1. **Clase Programa:** Representa un proceso en la simulación. Contiene métodos para solicitar memoria, utilizar CPU y realizar I/O.
2. **Función simular:** Realiza la simulación de múltiples procesos, calcula el tiempo promedio de ejecución y guarda los datos en un archivo CSV.
3. **Función plot_tiempo_vs_procesos:** Genera un gráfico que muestra el tiempo promedio de ejecución en función del número de procesos.
4. **Configuración de la Simulación:** Se solicita al usuario la cantidad de procesos a simular y el intervalo entre procesos.

### Ejecución del Código

1. Ejecute el archivo `simulacion_procesos.py`.
2. Ingrese la cantidad de procesos a simular y el intervalo entre procesos cuando se le solicite.
3. La simulación se ejecutará y mostrará el tiempo promedio de ejecución, la desviación estándar y el nombre del archivo donde se guardan los datos.
4. Se generará un gráfico mostrando la relación entre el número de procesos y el tiempo promedio de ejecución.

## Contribuyentes

- Diego Fernando Patzán Marroquín (23525)


