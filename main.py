from tkinter import messagebox
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from Proceso import SimuladorPlanificacion
import tkinter as tk
class Task:
    # Método constructor
    def __init__(self):
        self.numero_rafagas = None
        self.opcion = 0
    def mostrar_ventana(self):
        # Cración de la ventana principal
        screen = tb.Window(themename="solar")
        screen.title('Planificadores')
        screen.geometry('900x550')
        screen.resizable(False, False)

        # Mensaje
        label_1 = tb.Label(text='Planificadores', font=('Helvetica', 16), bootstyle='default')
        label_1.pack(pady=25)

        # Extrae los valores de la lista Tasks_0 o Tasks_1
        Tasks_0_values = [list(task.values()) for task in Tasks_0]

        # Creación de tabla
        table = Tableview(
            master = screen,
            coldata = Task_coldata,
            rowdata = Tasks_0_values
        )
        table.pack(fill=BOTH)

        # Entrada para rafagas
        label_2 = tb.Label(screen, text='Ingrese el número de rafagas', font=('Helvetica', 10), bootstyle='default')
        label_2.pack(pady=35)

        rafagas = tb.Entry(screen)
        rafagas.pack(pady=10)

        # Función que valida la entrada del número de ráfagas
        def guardar_numero_rafagas():
            try:
                valor = int(rafagas.get())
                if valor <= 0:
                    messagebox.showinfo('Alerta', f'El número debe ser mayor a 0')
                    return
                else:
                    self.numero_rafagas = rafagas.get()
                    application = tk.Tk()
                    app = SimuladorPlanificacion(application, tasks=Tasks_0_Enviar, num_rafagas=self.numero_rafagas)
                    application.mainloop()
            except:
                messagebox.showinfo('Alerta', f'Valor no permitido')

        button_1 = tb.Button(screen, text='Ejecutar', bootstyle='success-outline', command=guardar_numero_rafagas)
        button_1.pack(pady=10)

        screen.mainloop()


Task_coldata = [
    {"text": "Tarea", "stretch": True},
    {"text": "Duración rafaga", "stretch": True},
    {"text": "Tiempo Bloqueado", "stretch": True},
]

Tasks_0 = [
    {'task_0': 'TO', 'duracion_rafaga': 5, 'tiempo_bloqueado': 4},
    {'task_1': 'T1', 'duracion_rafaga': 4, 'tiempo_bloqueado': 3},
    {'task_2': 'T2', 'duracion_rafaga': 3, 'tiempo_bloqueado': 2},
    {'task_3': 'T3', 'duracion_rafaga': 2, 'tiempo_bloqueado': 1},
    {'task_4': 'T4', 'duracion_rafaga': 2, 'tiempo_bloqueado': 2}
]

Tasks_0_Enviar = [
    {'task_0': {'duracion_rafaga': 5, 'tiempo_bloqueado': 4}},
    {'task_1': {'duracion_rafaga': 4, 'tiempo_bloqueado': 3}},
    {'task_2': {'duracion_rafaga': 3, 'tiempo_bloqueado': 2}},
    {'task_3': {'duracion_rafaga': 2, 'tiempo_bloqueado': 1}},
    {'task_4': {'duracion_rafaga': 2, 'tiempo_bloqueado': 2}}
]

Tasks_1 = [
    {'task_0': 'TO', 'duracion_rafaga': 7, 'tiempo_bloqueado': 4},
    {'task_1': 'T1', 'duracion_rafaga': 1, 'tiempo_bloqueado': 2},
    {'task_2': 'T2', 'duracion_rafaga': 1, 'tiempo_bloqueado': 2},
]

Tasks_1_Enviar = [
    {{'task_0': 'TO', 'duracion_rafaga': 7, 'tiempo_bloqueado': 4}},
    {{'task_1': 'T1', 'duracion_rafaga': 1, 'tiempo_bloqueado': 2}},
    {{'task_2': 'T2', 'duracion_rafaga': 1, 'tiempo_bloqueado': 2}}
]


if __name__ == '__main__':
    Proceso_1 = Task()
    Proceso_1.mostrar_ventana()