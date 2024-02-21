import matplotlib

matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Proceso:
    def __init__(self, nombre, num_rafagas, tiempo_rafaga, tiempo_espera):
        self.nombre = nombre
        self.estado = "Preparado"
        self.num_rafagas = num_rafagas
        self.tiempo_rafaga = tiempo_rafaga
        self.tiempo_espera = tiempo_espera
        self.num_rafagas_restantes = num_rafagas
        self.tiempo_rafaga_restante = tiempo_rafaga
        self.tiempo_espera_restante = tiempo_espera

    def preparado(self):
        return self.estado == "Preparado"

    def bloqueado(self):
        return self.estado == "Bloqueado"

    def espera_es(self):
        return self.estado == "Espera E/S"

    def ejecucion(self):
        return self.estado == "Ejecutando"

    def terminado(self):
        return self.estado == "Terminado"


class PoolProcesos:
    def __init__(self, procesos):
        self.procesos = procesos

    def hay_procesos_pendientes(self):
        return any(not proceso.terminado() for proceso in self.procesos)


class CPU:
    def __init__(self, num_cpu):
        self.num_cpu = num_cpu
        self.estado = "Libre"
        self.proceso_ejecutando = None

    def libre(self):
        return self.estado == "Libre"

    def ejecutar(self, proceso):
        self.estado = "Ocupado"
        self.proceso_ejecutando = proceso

    def liberar(self):
        self.estado = "Libre"
        self.proceso_ejecutando = None


class DispositivoES:
    def __init__(self, num_dispositivo):
        self.num_dispositivo = num_dispositivo
        self.estado = "Libre"
        self.proceso_espera = None

    def libre(self):
        return self.estado == "Libre"

    def asignar(self, proceso):
        self.estado = "Ocupado"
        self.proceso_espera = proceso

    def liberar(self):
        self.estado = "Libre"
        self.proceso_espera = None


class PoolCPUs:
    def __init__(self, cpus):
        self.cpus = cpus

    # Verifica si hay un CPU libre para asignar un proceso
    def hay_cpu_libre(self):
        return any(cpu.libre() for cpu in self.cpus)

    # Asigna un proceso a un CPU libre
    def asignar_cpu(self, proceso):
        for cpu in self.cpus:
            if cpu.libre():
                cpu.ejecutar(proceso)
                break

    # Libera un CPU que está ejecutando un proceso
    def liberar_cpu(self, proceso):
        for cpu in self.cpus:
            if cpu.proceso_ejecutando == proceso:
                cpu.liberar()
                break


class PoolDispositivosES:
    def __init__(self, dispositivos_es):
        self.dispositivos_es = dispositivos_es

    # Verifica si hay un dispositivo de E/S libre para asignar un proceso
    def hay_dispositivo_libre(self):
        return any(dispositivo.libre() for dispositivo in self.dispositivos_es)

    # Asigna un proceso a un dispositivo de E/S libre
    def asignar_dispositivo(self, proceso):
        for dispositivo in self.dispositivos_es:
            if dispositivo.libre():
                dispositivo.asignar(proceso)
                break

    # Libera un dispositivo de E/S que está esperando un proceso
    def liberar_dispositivo(self, proceso):
        for dispositivo in self.dispositivos_es:
            if dispositivo.proceso_espera == proceso:
                dispositivo.liberar()
                break


NUM_CPUS = 2
NUM_DISPOSITIVOS_ES = 1


def mensaje(msg):
    linea = "--" + " " + "-" * 54 + " " + "--"
    print(linea)
    print(f"-- -- {msg} {'-' * (50 - len(msg))} --")
    print(linea)


def dibujar_grafica_gantt(historial_estados):
    # ... Asumimos que la impresión del historial_estados es solo para depuración y no se muestra aquí ...

    fig, ax = plt.subplots(figsize=(10, len(historial_estados) / 2))  # Ajustar el tamaño de la figura
    yticks = []
    yticklabels = []
    estado_color = {
        "Ejecutando": "green",
        "Preparado": "yellow",
        "Bloqueado": "red",
        "Espera E/S": "brown"
    }

    for tiempo, estados in historial_estados.items():
        for estado in estados:
            nombre, estado_proceso = estado
            if nombre not in yticklabels:
                yticklabels.append(nombre)
                yticks.append(len(yticklabels) - 1)  # La posición en y se basa en el orden de aparición
            color = estado_color.get(estado_proceso, "white")  # Obtener el color del estado, blanco por defecto
            # Dibujar el rectángulo para el estado actual
            ax.broken_barh([(tiempo, 1)], (yticks[-1], 0.8),
                           facecolors=color)  # Ajustar la altura (0.8) según la necesidad

    ax.set_xticks(range(len(historial_estados)))  # Ajustar los ticks del eje x
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Proceso")
    ax.set_title("Planificación FCFS")
    plt.show()


def main():
    mensaje("Planificación de procesos")
    num_procesos = int(input("Ingrese el número de procesos a planificar: "))

    mensaje("Ingreso de datos de procesos")
    procesos = []
    for i in range(num_procesos):
        nombre = f"T{i}"
        num_rafagas = int(input(f"Ingrese el número de ráfagas del proceso {nombre}: "))
        tiempo_rafaga = int(input(f"Ingrese el tiempo de ráfaga del proceso {nombre}: "))
        tiempo_espera = int(input(f"Ingrese el tiempo de espera de E/S del proceso {nombre}: "))
        procesos.append(Proceso(nombre, num_rafagas, tiempo_rafaga, tiempo_espera))

    pool = PoolProcesos(procesos)

    pool_cpus = PoolCPUs([CPU(i) for i in range(NUM_CPUS)])
    pool_disp = PoolDispositivosES([DispositivoES(i) for i in range(NUM_DISPOSITIVOS_ES)])

    mensaje("Procesos ingresados")
    for proceso in procesos:
        print(f"Nombre: {proceso.nombre}")
        print(f"Estado: {proceso.estado}")
        print(f"Número de ráfagas: {proceso.num_rafagas}")
        print(f"Tiempo de ráfaga: {proceso.tiempo_rafaga}")
        print(f"Tiempo de espera de E/S: {proceso.tiempo_espera}")

    mensaje("Planificación de procesos")
    historial_estados = {}
    tiempo = 0

    print(f"Tiempo: {tiempo}")
    for proceso in procesos:
        print(f"Estado del proceso {proceso.nombre}: Ejecutando")

    while pool.hay_procesos_pendientes():
        print(f"Tiempo: {tiempo + 1}")

        # Primero, procesa todos los estados y acciones de los procesos
        for proceso in procesos:
            if proceso.preparado() and pool_cpus.hay_cpu_libre():
                pool_cpus.asignar_cpu(proceso)
                proceso.estado = "Ejecutando"

            if proceso.bloqueado() and pool_disp.hay_dispositivo_libre():
                pool_disp.asignar_dispositivo(proceso)
                proceso.estado = "Espera E/S"

            if proceso.espera_es():
                proceso.tiempo_espera_restante -= 1
                if proceso.tiempo_espera_restante <= 0:
                    pool_disp.liberar_dispositivo(proceso)
                    proceso.tiempo_espera_restante = proceso.tiempo_espera
                    proceso.estado = "Preparado"  # Cambia a preparado y espera asignación de CPU en la revisión intermedia

            if proceso.ejecucion():
                proceso.tiempo_rafaga_restante -= 1
                if proceso.tiempo_rafaga_restante <= 0:
                    proceso.num_rafagas_restantes -= 1
                    proceso.tiempo_rafaga_restante = proceso.tiempo_rafaga
                    pool_cpus.liberar_cpu(proceso)
                    if proceso.num_rafagas_restantes > 0:
                        proceso.estado = "Bloqueado"  # Espera asignación de dispositivo E/S en la revisión intermedia
                    else:
                        proceso.estado = "Terminado"

        # Revisión intermedia: asignar recursos liberados antes de incrementar el tiempo
        for proceso in procesos:
            if proceso.preparado() and pool_cpus.hay_cpu_libre():
                pool_cpus.asignar_cpu(proceso)
                proceso.estado = "Ejecutando"
            elif proceso.bloqueado() and pool_disp.hay_dispositivo_libre():
                pool_disp.asignar_dispositivo(proceso)
                proceso.estado = "Espera E/S"

        historial_estados[tiempo] = []
        # Actualizar historial de estados después de todas las asignaciones
        for proceso in procesos:
            historial_estados[tiempo].append((proceso.nombre, proceso.estado))
            print(f"Estado del proceso {proceso.nombre}: {proceso.estado}")

        tiempo += 1

    print(historial_estados)
    dibujar_grafica_gantt(historial_estados)


if __name__ == "__main__":
    main()
