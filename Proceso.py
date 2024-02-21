import tkinter as tk
from tkinter import messagebox

class Proceso:
    def __init__(self, nombre, duracion_rafaga, tiempo_bloqueo):
        self.nombre = nombre
        self.estado = "Preparado"
        self.numRafagas = 0
        self.tiempoRafaga = duracion_rafaga
        self.tiempoEspera = tiempo_bloqueo
        self.numRafagasRestantes = 0
        self.tiempoRafagaRestante = duracion_rafaga
        self.tiempoEsperaRestante = tiempo_bloqueo

class PoolProcesos:
    def __init__(self, procesos):
        self.procesos = procesos

class CPU:
    def __init__(self, numCpu):
        self.numCpu = numCpu
        self.estado = "Libre"
        self.procesoEjecutando = None

class DispositivoES:
    def __init__(self, numDispositivo):
        self.numDispositivo = numDispositivo
        self.estado = "Libre"
        self.procesoEspera = None

class SimuladorPlanificacion:
    def __init__(self, root, tasks, num_rafagas):
        self.root = root
        self.root.title("Simulador de Planificación de Procesos")

        self.procesos = []
        self.pool = None
        self.cpus = []
        self.dispositivos_es = []

        self.num_rafagas = num_rafagas  # Número de ráfagas

        self.tiempo_label = tk.Label(root, text="Tiempo:")
        self.tiempo_label.pack()

        self.resultado_text = tk.Text(root, height=20, width=80)
        self.resultado_text.pack()

        for i, task in enumerate(tasks):
            nombre = list(task.keys())[0]
            duracion_rafaga = task[nombre]['duracion_rafaga']
            tiempo_bloqueo = task[nombre]['tiempo_bloqueado']

            proceso = Proceso(nombre, duracion_rafaga, tiempo_bloqueo)
            proceso.numRafagas = self.num_rafagas  # Asigna el número de ráfagas
            proceso.numRafagasRestantes = self.num_rafagas  # Inicializa el número de ráfagas restantes
            self.procesos.append(proceso)

        self.pool = PoolProcesos(self.procesos)

        self.cpus = [CPU(i) for i in range(2)]
        self.dispositivos_es = [DispositivoES(i) for i in range(1)]

        self.resultado_text.insert(tk.END, "Procesos ingresados\n")
        for proceso in self.procesos:
            self.resultado_text.insert(tk.END, f"Nombre: {proceso.nombre}\n")
            self.resultado_text.insert(tk.END, f"Estado: {proceso.estado}\n")
            self.resultado_text.insert(tk.END, f"Duracion de rafaga: {proceso.tiempoRafaga}\n")
            self.resultado_text.insert(tk.END, f"Tiempo de bloqueo: {proceso.tiempoEspera}\n")

    def mensaje(self, mensaje):
        return f"-- ------------------------------------------------------ --\n-- -- {mensaje} {'-' * (57 - len(mensaje))} --\n-- ------------------------------------------------------ --"

    def proceso_en_ejecucion(self, proceso):
        return proceso.estado == "Ejecutando"

    def proceso_preparado(self, proceso):
        return proceso.estado == "Preparado"

    def proceso_en_espera_es(self, proceso):
        return proceso.estado == "Espera E/S"

    def proceso_bloqueado(self, proceso):
        return proceso.estado == "Bloqueado"

    def proceso_terminado(self, proceso):
        return proceso.estado == "Terminado"

    def cpu_libre(self, cpu):
        return cpu.estado == "Libre"

    def dispositivo_es_libre(self, dispositivo):
        return dispositivo.estado == "Libre"

    def hay_procesos_pendientes(self):
        return any(not self.proceso_terminado(proceso) for proceso in self.pool.procesos)

    def hay_cpu_libre(self):
        return any(self.cpu_libre(cpu) for cpu in self.cpus)

    def hay_dispositivo_es_libre(self):
        return any(self.dispositivo_es_libre(dispositivo) for dispositivo in self.dispositivos_es)

    def cambia_estado(self, proceso, estado):
        proceso.estado = estado

    def asigna_cpu(self, proceso):
        for cpu in self.cpus:
            if self.cpu_libre(cpu):
                cpu.estado = "Ocupado"
                cpu.procesoEjecutando = proceso
                break

    def asigna_dispositivo_es(self, proceso):
        for dispositivo in self.dispositivos_es:
            if self.dispositivo_es_libre(dispositivo):
                dispositivo.estado = "Ocupado"
                dispositivo.procesoEspera = proceso
                break

    def libera_cpu(self, proceso):
        for cpu in self.cpus:
            if cpu.procesoEjecutando and cpu.procesoEjecutando.nombre == proceso.nombre:
                cpu.estado = "Libre"

    def libera_dispositivo_es(self, proceso):
        for dispositivo in self.dispositivos_es:
            if dispositivo.procesoEspera and dispositivo.procesoEspera.nombre == proceso.nombre:
                dispositivo.estado = "Libre"

    def iniciar_simulacion(self):
        self.resultado_text.delete(1.0, tk.END)

        self.resultado_text.insert(tk.END, self.mensaje("Planificacion de procesos") + "\n")
        self.resultado_text.insert(tk.END, f"Ingrese el numero de procesos a planificar: {len(self.procesos)}\n")
        self.resultado_text.insert(tk.END, self.mensaje("Planificacion de procesos") + "\n")

        tiempo = 0
        while self.hay_procesos_pendientes():
            self.resultado_text.insert(tk.END, f"Tiempo: {tiempo + 1}\n")

            for proceso in self.procesos:
                if self.proceso_preparado(proceso):
                    if self.hay_cpu_libre():
                        self.asigna_cpu(proceso)
                        self.cambia_estado(proceso, "Ejecutando")
                    else:
                        self.cambia_estado(proceso, "Preparado")

                if self.proceso_bloqueado(proceso):
                    if self.hay_dispositivo_es_libre():
                        self.asigna_dispositivo_es(proceso)
                        self.cambia_estado(proceso, "Espera E/S")
                    else:
                        self.cambia_estado(proceso, "Bloqueado")

                if self.proceso_en_espera_es(proceso):
                    proceso.tiempoEsperaRestante -= 1
                    if proceso.tiempoEsperaRestante > 0:
                        self.cambia_estado(proceso, "Espera E/S")
                    else:
                        self.libera_dispositivo_es(proceso)
                        proceso.tiempoEsperaRestante = proceso.tiempoEspera
                        if self.hay_cpu_libre():
                            self.asigna_cpu(proceso)
                            self.cambia_estado(proceso, "Ejecutando")
                        else:
                            self.cambia_estado(proceso, "Preparado")

                if self.proceso_en_ejecucion(proceso):
                    if proceso.tiempoRafagaRestante > 0:
                        proceso.tiempoRafagaRestante -= 1
                        self.cambia_estado(proceso, "Ejecutando")
                    else:
                        proceso.tiempoRafagaRestante = proceso.tiempoRafaga
                        self.libera_cpu(proceso)
                        if proceso.numRafagasRestantes > 0:
                            if self.hay_dispositivo_es_libre():
                                self.asigna_dispositivo_es(proceso)
                                self.cambia_estado(proceso, "Espera E/S")
                            else:
                                self.cambia_estado(proceso, "Bloqueado")
                        else:
                            self.cambia_estado(proceso, "Terminado")

            for proceso in self.procesos:
                self.resultado_text.insert(tk.END, f"Estado del proceso {proceso.nombre}: {proceso.estado}\n")

            tiempo += 1

        messagebox.showinfo("Simulación Finalizada", "La simulación ha finalizado.")
