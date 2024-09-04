import tkinter as tk
from matriz import Matriz 
from tkinter import messagebox

class MenuAplicacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú Principal")
        self.root.geometry("800x600")
        self.crear_menu()

    def crear_menu(self):
        # Etiqueta del menú
        etiqueta = tk.Label(self.root, text="Seleccione una opción:", font=("Arial", 14))
        etiqueta.pack(pady=20)

        boton_reduccion = tk.Button(self.root, text="Eliminación Gaussiana", font=("Arial", 12),
                                    command=self.abrir_interfaz_gauss)
        boton_reduccion.pack(pady=10)

        boton_salir = tk.Button(self.root, text="Salir", font=("Arial", 12), command=self.root.quit)
        boton_salir.pack(pady=10)

        self.root.mainloop()

    def abrir_interfaz_gauss(self):
        # Crear nueva ventana para Reducción Gaussiana
        self.ventana_gauss = tk.Toplevel(self.root)
        self.ventana_gauss.title("Eliminación Gaussiana")
        self.ventana_gauss.geometry("800x600")

        # Tamaño de la matriz
        frame_configuracion = tk.Frame(self.ventana_gauss)
        frame_configuracion.pack(pady=10)

        etiqueta_n = tk.Label(frame_configuracion, text="Número de ecuaciones:")
        etiqueta_n.pack(side=tk.LEFT)

        self.entrada_n = tk.Entry(frame_configuracion, width=5)
        self.entrada_n.pack(side=tk.LEFT)
        self.entrada_n.insert(0, "3")
        
        etiqueta_variables = tk.Label(frame_configuracion, text="Número de variables:")
        etiqueta_variables.pack(side=tk.LEFT)
        
        self.entrada_variables = tk.Entry(frame_configuracion, width=5)
        self.entrada_variables.pack(side=tk.LEFT)
        self.entrada_variables.insert(0, "3")

        boton_crear = tk.Button(frame_configuracion, text="Crear Matriz", command=self.crear_entradas_matriz)
        boton_crear.pack(side=tk.LEFT, padx=10)

        # Entradas para la matriz
        self.frame_matriz = tk.Frame(self.ventana_gauss)
        self.frame_matriz.pack(pady=10)

        self.etiqueta_titulo_matriz = tk.Label(self.ventana_gauss, text="Introduce los coeficientes de la matriz:")
        self.etiqueta_titulo_matriz.pack()

        # Área de texto para el resultado
        self.text_resultado = tk.Text(self.ventana_gauss, height=30, width=70)
        self.text_resultado.pack(pady=10)

        # Botón para calcular
        boton_calcular = tk.Button(self.ventana_gauss, text="Calcular", command=self.mostrar_resultado)
        boton_calcular.pack(pady=10)

    def crear_entradas_matriz(self):
        # Eliminar entradas anteriores si existen
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        try:
            n = int(self.entrada_n.get())
            variables = int(self.entrada_variables.get())
        
            if n<= 0 or variables <= 0:
                raise ValueError("El número de ecuaciones y variables debe ser mayor a 0.")
            
            self.entradas = [[tk.Entry(self.frame_matriz, width=10) for j in range(variables + 1)] for i in range(n)]

            for i in range(n):
                for j in range(variables + 1):
                    self.entradas[i][j].grid(row=i, column=j, padx=5, pady=5)

            self.etiqueta_titulo_matriz.config(text=f"Introduce los coeficientes de la matriz de {n}x{variables + 1}:")
            
        except ValueError as ve:
            messagebox.showerror("Error", f"Error en la entrada: {ve}")

    def mostrar_resultado(self):
        n = int(self.entrada_n.get())
        matriz = Matriz(n, self.entradas)  # Crear una instancia de la clase Matriz
        if matriz.matriz is not None:
            resultado = matriz.eliminacion_gaussiana()  # Llamar al método eliminacion_gaussiana
            self.text_resultado.delete("1.0", tk.END)
            self.text_resultado.insert(tk.END, resultado)

    def abrir_interfaz_ecuaciones(self):
        self.ventana_ecuaciones = tk.Toplevel(self.root)
        self.ventana_ecuaciones.title("Método de Eliminación para Ecuaciones 2x2")
        self.ventana_ecuaciones.geometry("500x200")

        # Marco para ingresar las ecuaciones de forma horizontal
        frame_ecuaciones = tk.Frame(self.ventana_ecuaciones)
        frame_ecuaciones.pack(pady=20, padx=20)

        labels = ["a1*x +", "b1*y =", "c1", "a2*x +", "b2*y =", "c2"]
        self.entries = {}
        row = 0
        col = 0
        for i, label in enumerate(labels):
            if i == 3:  # Nueva fila para la segunda ecuación
                row += 1
                col = 0
            entry = tk.Entry(frame_ecuaciones, width=5)
            entry.grid(row=row, column=col, padx=2)
            col += 1
            tk.Label(frame_ecuaciones, text=label).grid(row=row, column=col, padx=2)
            col += 1
            self.entries[label] = entry

        boton_calcular = tk.Button(self.ventana_ecuaciones, text="Calcular", command=self.calcular_solucion)
        boton_calcular.pack(pady=20)

        self.resultado_label = tk.Label(self.ventana_ecuaciones, text="")
        self.resultado_label.pack()

    def calcular_solucion(self):
        try:
            a1 = float(self.entries["a1*x +"].get())
            b1 = float(self.entries["b1*y ="].get())
            c1 = float(self.entries["c1"].get())
            a2 = float(self.entries["a2*x +"].get())
            b2 = float(self.entries["b2*y ="].get())
            c2 = float(self.entries["c2"].get())
            sistema = Ecuaciones_Lineales(a1, b1, c1, a2, b2, c2)
            x, y = sistema.resolver()
            self.resultado_label.config(text=f"La solución es x = {x}, y = {y}")
        except Exception as e:
            self.resultado_label.config(text=str(e))


def iniciar_menu():
    app = MenuAplicacion()
