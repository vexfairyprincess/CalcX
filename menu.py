import tkinter as tk
from matriz import Matriz
from vector import Vector
from tkinter import messagebox

class MenuAplicacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú Principal")
        self.root.geometry("800x600")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.crear_menu()

    def crear_logo(self):
        frame_logo = tk.Frame(self.root)
        frame_logo.grid(row=0, column=0, columnspan=3, pady=20)

        self.logo_path = "calculadora_finalfinalGIF.gif"
        self.logo = tk.PhotoImage(file=self.logo_path)

        label_logo = tk.Label(frame_logo, image=self.logo)
        label_logo.image = self.logo
        label_logo.grid(row=0, column=0, padx=20)

        label_nombre = tk.Label(frame_logo, text="CalcX", font=("Helvetica", 36, "bold"))
        label_nombre.grid(row=0, column=1, padx=10)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def crear_menu(self):
        self.crear_logo()
        etiqueta = tk.Label(self.root, text="Seleccione una opción:", font=("Arial", 14))
        etiqueta.grid(row=2, column=1, pady=20, sticky="ew")

        boton_reduccion = tk.Button(self.root, text="Método escalonado", font=("Arial", 12),
                                    command=self.abrir_interfaz_gauss)
        boton_reduccion.grid(row=4, column=1, pady=10, sticky="ew")

        boton_vectores = tk.Button(self.root, text="Operaciones Vectoriales", font=("Arial", 12),
                                   command=self.abrir_operaciones_vectoriales)
        boton_vectores.grid(row=5, column=1, pady=10, sticky="ew")

        boton_salir = tk.Button(self.root, text="Salir", font=("Arial", 12), command=self.root.quit)
        boton_salir.grid(row=6, column=1, pady=10, sticky="ew")

        self.root.mainloop()

    def abrir_interfaz_gauss(self):
        self.root.withdraw()
        # Crear nueva ventana para Reducción Gaussiana
        self.ventana_gauss = tk.Toplevel(self.root)
        self.ventana_gauss.title("Metodo Escalonado")
        self.ventana_gauss.geometry("800x600")
        screen_width = self.ventana_gauss.winfo_screenwidth()
        screen_height = self.ventana_gauss.winfo_screenheight()
        self.ventana_gauss.geometry(f"{screen_width}x{screen_height}")

        # Añadir barra de menú
        menubar = tk.Menu(self.ventana_gauss)
        self.ventana_gauss.config(menu=menubar)

        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="| | |", menu=archivo_menu)
        archivo_menu.add_command(label="Regresar al menú", command=self.root.deiconify)
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

    def regresar_menu_principal(self):
        """Método para regresar al menú principal."""
        self.ventana_vectores.destroy()
        self.root.deiconify()

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
            
            self.boton_paso_a_paso = tk.Button(self.ventana_gauss, text="Paso a Paso", bg="light yellow",
                                               command=lambda: self.mostrar_paso_a_paso(resultado_pasos))
            self.boton_paso_a_paso.grid(row=3, column=3, padx=10, pady=10)

    def mostrar_paso_a_paso(self, resultado_pasos):
        self.text_resultado.delete("1.0", tk.END)
        self.text_resultado.insert(tk.END, resultado_pasos)

        # Regresar a resultado final, único propósito: estética
        self.boton_regresar = tk.Button(self.ventana_gauss, text="←", font=("Helvetica", 15), bg="light yellow",
                                        command=self.mostrar_resultado)
        self.boton_regresar.grid(row=3, column=1, padx=0, pady=0)

    def abrir_operaciones_vectoriales(self):
        self.root.withdraw()
        self.ventana_vectores = tk.Toplevel(self.root)
        self.ventana_vectores.title("Operaciones Vectoriales")
        self.ventana_vectores.geometry("800x600")
        screen_width = self.ventana_vectores.winfo_screenwidth()
        screen_height = self.ventana_vectores.winfo_screenheight()
        self.ventana_vectores.geometry(f"{screen_width}x{screen_height}")

        menubar = tk.Menu(self.ventana_vectores)
        self.ventana_vectores.config(menu=menubar)

        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="| | |", menu=archivo_menu)
        archivo_menu.add_command(label="Regresar al menú", command=self.regresar_menu_principal)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        # Configurar columnas y filas para que se expandan
        for i in range(4):
            self.ventana_vectores.grid_columnconfigure(i, weight=1)

        # Etiqueta y entrada para la dimensión del vector
        etiqueta_instrucciones = tk.Label(self.ventana_vectores, text="Ingrese la dimensión del vector:", font=("Arial", 14))
        etiqueta_instrucciones.grid(row=0, column=0, columnspan=2, pady=10, sticky="e")

        self.entrada_dimension = tk.Entry(self.ventana_vectores, width=5)
        self.entrada_dimension.grid(row=0, column=2, padx=5, sticky="w")

        boton_generar = tk.Button(self.ventana_vectores, text="Generar Entradas", command=self.generar_entradas_vectores)
        boton_generar.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Frame para entradas de vectores y escalares
        self.frame_entradas = tk.Frame(self.ventana_vectores)
        self.frame_entradas.grid(row=1, column=0, columnspan=4, pady=20)

        # Configuración de las opciones de operación
        self.operacion_var = tk.StringVar(value="suma")
        opciones = [("Suma de vectores", "suma"),
                    ("Resta de vectores", "resta"),
                    ("Multiplicación por escalar", "escalar"),
                    ("Producto escalar", "producto_escalar"),
                    ("Producto cruz", "producto_cruz")]

        fila_actual = 2
        for texto, valor in opciones:
            tk.Radiobutton(self.ventana_vectores, text=texto, variable=self.operacion_var, value=valor).grid(
                row=fila_actual, column=0, columnspan=2, padx=20, sticky="w")
            fila_actual += 1

        # Botón para calcular
        boton_calcular = tk.Button(self.ventana_vectores, text="Calcular", command=self.realizar_operacion)
        boton_calcular.grid(row=fila_actual, column=1, pady=10, sticky="ew")

        # Área de texto para mostrar el resultado
        self.text_resultado_vectorial = tk.Text(self.ventana_vectores, height=10, width=70)
        self.text_resultado_vectorial.grid(row=fila_actual + 1, column=0, columnspan=4, padx=10, pady=10)

    def generar_entradas_vectores(self):
        try:
            dimension = int(self.entrada_dimension.get())
            if dimension <= 0:
                raise ValueError("La dimensión debe ser un número positivo.")
            
            # Limpiar entradas previas si existen
            for widget in self.frame_entradas.winfo_children():
                widget.destroy()

            # Entradas para los componentes del vector u
            tk.Label(self.frame_entradas, text="Componentes de Vector u:", font=("Arial", 12)).grid(row=0, column=0, columnspan=dimension, pady=5)
            self.entradas_u = [tk.Entry(self.frame_entradas, width=5) for _ in range(dimension)]
            for i, entrada in enumerate(self.entradas_u):
                entrada.grid(row=1, column=i, padx=5, pady=5)

            # Entradas para los componentes del vector v
            tk.Label(self.frame_entradas, text="Componentes de Vector v:", font=("Arial", 12)).grid(row=2, column=0, columnspan=dimension, pady=5)
            self.entradas_v = [tk.Entry(self.frame_entradas, width=5) for _ in range(dimension)]
            for i, entrada in enumerate(self.entradas_v):
                entrada.grid(row=3, column=i, padx=5, pady=5)

            # Entradas para los escalares
            tk.Label(self.frame_entradas, text="Escalar a:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", pady=5)
            self.entrada_escalar_a = tk.Entry(self.frame_entradas, width=5)
            self.entrada_escalar_a.grid(row=4, column=1, padx=5, pady=5, sticky="w")

            tk.Label(self.frame_entradas, text="Escalar b:", font=("Arial", 12)).grid(row=4, column=2, sticky="e", pady=5)
            self.entrada_escalar_b = tk.Entry(self.frame_entradas, width=5)
            self.entrada_escalar_b.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        except ValueError as ve:
            messagebox.showerror("Error", f"Entrada no válida: {ve}")

    def realizar_operacion(self):
        try:
            componentes_u = [float(entry.get()) for entry in self.entradas_u]
            componentes_v = [float(entry.get()) for entry in self.entradas_v]
            escalar_a = float(self.entrada_escalar_a.get()) if self.entrada_escalar_a.get() else None
            escalar_b = float(self.entrada_escalar_b.get()) if self.entrada_escalar_b.get() else None

            u = Vector(componentes_u)
            v = Vector(componentes_v)
            operacion = self.operacion_var.get()

            resultado = ""

            if operacion == "suma":
                resultado_vector = u.suma(v)
                resultado = f"u + v = {resultado_vector}"
            elif operacion == "resta":
                resultado_vector = u.resta(v)
                resultado = f"u - v = {resultado_vector}"
            elif operacion == "escalar":
                if escalar_a is not None and escalar_b is not None:
                    resultado_u = u.multiplicacion(escalar_a)
                    resultado_v = v.multiplicacion(escalar_b)
                    resultado = f"{escalar_a} * u = {resultado_u}\n{escalar_b} * v = {resultado_v}"
                else:
                    raise ValueError("Debe ingresar ambos escalares a y b.")
            elif operacion == "producto_escalar":
                resultado_escalar = u.producto_escalar(v)
                resultado = f"u · v = {resultado_escalar}"
            elif operacion == "producto_cruz":
                resultado_vector = u.producto_cruz(v)
                resultado = f"u × v = {resultado_vector}"
            else:
                resultado = "Operación no reconocida."

            self.text_resultado_vectorial.delete("1.0", tk.END)
            self.text_resultado_vectorial.insert(tk.END, resultado)

        except ValueError as ve:
            messagebox.showerror("Error", f"Error en la entrada: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

def iniciar_menu():
    app = MenuAplicacion()
