import tkinter as tk
from tkinter import messagebox

class Matriz:
    def __init__(self, n, entradas=None):
        self.n = n
        self.matriz = []
        if entradas:
            self.matriz = self.obtener_matriz(entradas)

    def obtener_matriz(self, entradas):
        # Obtiene los valores de las entradas y los convierte en una matriz utilizando listas anidadas
        matriz = []
        for i in range(self.n):
            fila = []
            for j in range(self.n + 1):
                try:
                    valor = float(entradas[i][j].get())
                    #Convierte el valor a float
                except ValueError:
                    messagebox.showerror("Error", f"Introduce un número válido en la posición [{i + 1}, {j + 1}].")
                    return None
                fila.append(valor)
            matriz.append(fila)
        return matriz

    def imprimir_matriz(self, paso):
        # Genera un string que representa la matriz de manera legible
        texto = f"Paso {paso}:\n"
        for fila in self.matriz:
            texto += "  ".join(f"{valor:8.4f}" for valor in fila) + "\n"
        texto += "\n"
        return texto

    def gauss_jordan(self):
        if not self.matriz:
            return "Matriz no válida."

        paso = 1
        resultado = ""

        # Operación de Gauss-Jordan
        for i in range(self.n):
            # Hacer que el pivote sea 1 dividiendo la fila por el pivote
            pivote = self.matriz[i][i]
            if pivote == 0:
                # Verificar si hay un 0 en el pivote y cambiar filas si es necesario
                for j in range(i + 1, self.n):
                    if self.matriz[j][i] != 0:
                        # Intercambiar filas
                        self.matriz[i], self.matriz[j] = self.matriz[j], self.matriz[i]
                        break
                pivote = self.matriz[i][i]

            # Dividir toda la fila por el pivote para hacer que el pivote sea 1
            self.matriz[i] = [elemento / pivote for elemento in self.matriz[i]]
            resultado += self.imprimir_matriz(paso)
            paso += 1

            # Hacer ceros en todas las demás posiciones de la columna del pivote
            for j in range(self.n):
                if i != j:
                    factor = self.matriz[j][i]
                    self.matriz[j] = [self.matriz[j][k] - factor * self.matriz[i][k] for k in range(self.n + 1)]
                    resultado += self.imprimir_matriz(paso)
                    paso += 1

        return resultado
