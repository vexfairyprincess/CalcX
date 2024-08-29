import tkinter as tk
from matriz import Matriz  # Importa la clase Matriz desde matriz.py

class MenuAplicacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú Principal")
        self.root.geometry("300x200")
        self.crear_menu()

    def crear_menu(self):
        # Etiqueta del menú
        etiqueta = tk.Label(self.root, text="Seleccione una opción:", font=("Arial", 14))
        etiqueta.pack(pady=20)

        # Botón para Reducción Gaussiana
        boton_reduccion = tk.Button(self.root, text="Reducción Gaussiana", font=("Arial", 12), command=self.abrir_interfaz_gauss)
        boton_reduccion.pack(pady=10)

        # Botón para salir
        boton_salir = tk.Button(self.root, text="Salir", font=("Arial", 12), command=self.root.quit)
        boton_salir.pack(pady=10)

        self.root.mainloop()

    def abrir_interfaz_gauss(self):
        # Crear nueva ventana para Reducción Gaussiana
        self.ventana_gauss = tk.Toplevel(self.root)
        self.ventana_gauss.title("Método de Gauss-Jordan")
        self.ventana_gauss.geometry("600x400")

        # Tamaño de la matriz
        frame_tamano = tk.Frame(self.ventana_gauss)
        frame_tamano.pack(pady=10)

        etiqueta_n = tk.Label(frame_tamano, text="Número de ecuaciones:")
        etiqueta_n.pack(side=tk.LEFT)

        self.entrada_n = tk.Entry(frame_tamano, width=5)
        self.entrada_n.pack(side=tk.LEFT)
        self.entrada_n.insert(0, "3")

        boton_crear = tk.Button(frame_tamano, text="Crear Matriz", command=self.crear_entradas_matriz)
        boton_crear.pack(side=tk.LEFT, padx=10)

        # Entradas para la matriz
        self.frame_matriz = tk.Frame(self.ventana_gauss)
        self.frame_matriz.pack(pady=10)

        self.etiqueta_titulo_matriz = tk.Label(self.ventana_gauss, text="Introduce los coeficientes de la matriz:")
        self.etiqueta_titulo_matriz.pack()

        # Área de texto para el resultado
        self.text_resultado = tk.Text(self.ventana_gauss, height=10, width=50)
        self.text_resultado.pack(pady=10)

        # Botón para calcular
        boton_calcular = tk.Button(self.ventana_gauss, text="Calcular", command=self.mostrar_resultado)
        boton_calcular.pack(pady=10)

    def crear_entradas_matriz(self):
        # Eliminar entradas anteriores si existen
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        n = int(self.entrada_n.get())
        self.entradas = [[tk.Entry(self.frame_matriz, width=10) for j in range(n + 1)] for i in range(n)]

        for i in range(n):
            for j in range(n + 1):
                self.entradas[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.etiqueta_titulo_matriz.config(text=f"Introduce los coeficientes de la matriz de {n}x{n+1}:")

    def mostrar_resultado(self):
        n = int(self.entrada_n.get())
        matriz = Matriz(n, self.entradas)  # Crear una instancia de la clase Matriz
        if matriz.matriz is not None:
            resultado = matriz.gauss_jordan()  # Llamar al método gauss_jordan
            self.text_resultado.delete("1.0", tk.END)
            self.text_resultado.insert(tk.END, resultado)

def iniciar_menu():
    app = MenuAplicacion()

