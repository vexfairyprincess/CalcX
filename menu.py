import tkinter as tk
from matriz import Matriz
from tkinter import messagebox

class MenuAplicacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú Principal")
        self.root.geometry("800x600")

        # Hacer que las columnas se expandan para centrar el contenido
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.crear_menu()

    def crear_menu(self):
        # Etiqueta del menú
        etiqueta = tk.Label(self.root, text="Seleccione una opción:", font=("Arial", 14))
        etiqueta.grid(row=0, column=1, pady=20, sticky="ew")  # Centrar en la columna 1

        boton_reduccion = tk.Button(self.root, text="Metodo escalonado", font=("Arial", 12),
                                    command=self.abrir_interfaz_gauss)
        boton_reduccion.grid(row=1, column=1, pady=10, sticky="ew")

        boton_salir = tk.Button(self.root, text="Salir", font=("Arial", 12), command=self.root.quit)
        boton_salir.grid(row=2, column=1, pady=10, sticky="ew")

        self.root.mainloop()

    def abrir_interfaz_gauss(self):
        # Crear nueva ventana para Reducción Gaussiana
        self.ventana_gauss = tk.Toplevel(self.root)
        self.ventana_gauss.title("Metodo Escalonado")
        self.ventana_gauss.geometry("800x600")

        # Añadir barra de menú
        menubar = tk.Menu(self.ventana_gauss)
        self.ventana_gauss.config(menu=menubar)

        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="| | |", menu=archivo_menu)
        archivo_menu.add_command(label="Regresar al menú", command=self.ventana_gauss.destroy)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        # Configurar las columnas para que se expandan
        for i in range(5):
            self.ventana_gauss.grid_columnconfigure(i, weight=1)

        frame_configuracion = tk.Frame(self.ventana_gauss)
        frame_configuracion.grid(row=0, column=0, columnspan=5, pady=10, sticky="ew")

        etiqueta_n = tk.Label(frame_configuracion, text="Número de ecuaciones:")
        etiqueta_n.grid(row=0, column=0, sticky="e")

        self.entrada_n = tk.Entry(frame_configuracion, width=5)
        self.entrada_n.grid(row=0, column=1, sticky="w")
        self.entrada_n.insert(0, "3")

        etiqueta_variables = tk.Label(frame_configuracion, text="Número de variables:")
        etiqueta_variables.grid(row=0, column=2, sticky="e")

        self.entrada_variables = tk.Entry(frame_configuracion, width=5)
        self.entrada_variables.grid(row=0, column=3, sticky="w")
        self.entrada_variables.insert(0, "3")

        boton_crear = tk.Button(frame_configuracion, text="Crear Matriz", command=self.crear_entradas_matriz)
        boton_crear.grid(row=0, column=4, padx=10, sticky="w")

        # Asegurarse de que el frame esté centrado dentro de la ventana
        frame_configuracion.grid_columnconfigure(0, weight=1)
        frame_configuracion.grid_columnconfigure(1, weight=1)
        frame_configuracion.grid_columnconfigure(2, weight=1)
        frame_configuracion.grid_columnconfigure(3, weight=1)
        frame_configuracion.grid_columnconfigure(4, weight=1)

        # Entradas para la matriz
        self.frame_matriz = tk.Frame(self.ventana_gauss)
        self.frame_matriz.grid(row=1, column=1, columnspan=3, pady=10)  # Centramos las entradas en las columnas 1 a 3

        self.etiqueta_titulo_matriz = tk.Label(self.ventana_gauss, text="Introduce los coeficientes de la matriz:")
        self.etiqueta_titulo_matriz.grid(row=2, column=0, columnspan=5, sticky="ew")

        # Botón para calcular
        self.boton_calcular = None

        # Área de texto para el resultado
        self.text_resultado = tk.Text(self.ventana_gauss, height=10, width=50)
        self.text_resultado.grid(row=4, column=1, columnspan=3, pady=5, sticky="nsew")

        # Permitir que la columna 4 se expanda para centrar el texto
        self.ventana_gauss.grid_rowconfigure(4, weight=1)

    def crear_entradas_matriz(self):
        # Eliminar entradas anteriores si existen
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        try:
            n = int(self.entrada_n.get())
            variables = int(self.entrada_variables.get())

            if n <= 0 or variables <= 0:
                raise ValueError("El número de ecuaciones y variables debe ser mayor a 0.")

            # Crear entradas centradas en la matriz
            self.entradas = [[tk.Entry(self.frame_matriz, width=10) for j in range(variables + 1)] for i in range(n)]

            for i in range(n):
                for j in range(variables + 1):
                    self.entradas[i][j].grid(row=i, column=j, padx=10, pady=10, sticky="ns")

            self.etiqueta_titulo_matriz.config(text=f"Introduce los coeficientes de la matriz de {n}x{variables + 1}:")

            # Crear el botón "Calcular" solo después de crear la matriz
            self.boton_calcular = tk.Button(self.ventana_gauss, text="Calcular", command=self.mostrar_resultado)
            self.boton_calcular.grid(row=3, column=2, pady=10, sticky="ew")

        except ValueError as ve:
            messagebox.showerror("Error", f"Error en la entrada: {ve}")

    def mostrar_resultado(self):
        n = int(self.entrada_n.get())
        matriz = Matriz(n, self.entradas)  # Crear una instancia de la clase Matriz
        
        if matriz.matriz is not None:
            resultado_pasos = matriz.eliminacion_gaussiana()  # Calcular el paso a paso
            resultado_final = matriz.interpretar_resultado()
            
            self.text_resultado.delete("1.0", tk.END)
            self.text_resultado.insert(tk.END, resultado_final)
            
            self.boton_paso_a_paso = tk.Button(self.ventana_gauss, text = "Paso a Paso", bg="light yellow",
                                            command=lambda: self.mostrar_paso_a_paso(resultado_pasos))
            self.boton_paso_a_paso.grid(row=3, column=3, padx=10, pady=10)
            
    def mostrar_paso_a_paso(self, resultado_pasos):
        self.text_resultado.delete("1.0", tk.END)
        self.text_resultado.insert(tk.END, resultado_pasos)


def iniciar_menu():
    app = MenuAplicacion()