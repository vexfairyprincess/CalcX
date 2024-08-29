import tkinter as tk
from tkinter import messagebox

class Matriz:
    """
    Clase que representa una matriz y permite realizar operaciones como la eliminación Gaussiana.

    Atributos:
    -----------
    n : int
        Número de ecuaciones (tamaño de la matriz).
    matriz : list
        Lista que contiene la matriz extendida (incluyendo la columna de resultados).

    Métodos:
    --------
    __init__(self, n, entradas=None):
        Constructor que inicializa la matriz y obtiene sus valores a partir de las entradas proporcionadas.
    
    obtener_matriz(self, entradas):
        Método que convierte las entradas de la interfaz gráfica en una lista de listas (matriz).

    imprimir_matriz(self, paso, operacion):
        Método que genera un string que representa la matriz en un formato legible.

    eliminacion_gaussiana(self):
        Método que realiza la eliminación Gaussiana para resolver sistemas de ecuaciones lineales.
    """

    def __init__(self, n, entradas=None):
        """
        Inicializa una instancia de la clase Matriz.

        Parámetros:
        -----------
        n : int
            Número de ecuaciones (tamaño de la matriz).
        entradas : list, opcional
            Lista de widgets Entry de Tkinter que contienen los valores de la matriz ingresados por el usuario.
        """
        self.n = n  # Número de ecuaciones
        self.matriz = []  # Inicialización de la matriz como una lista vacía
        if entradas:
            # Si se proporcionan entradas, obtener los valores de la matriz de ellas
            self.matriz = self.obtener_matriz(entradas)

    def obtener_matriz(self, entradas):
        """
        Convierte las entradas de la interfaz gráfica en una matriz (lista de listas).

        Parámetros:
        -----------
        entradas : list
            Lista de widgets Entry de Tkinter que contienen los valores de la matriz ingresados por el usuario.

        Retorna:
        --------
        list or None
            Una lista de listas que representa la matriz si todas las entradas son válidas.
            Retorna None y muestra un mensaje de error si alguna entrada no es un número válido.
        """
        matriz = []
        for i in range(self.n):  # Iterar sobre cada fila
            fila = []
            for j in range(self.n + 1):  # Iterar sobre cada columna (incluida la columna de resultados)
                try:
                    # Intentar convertir el valor de entrada a float
                    valor = float(entradas[i][j].get())
                except ValueError:
                    # Mostrar un mensaje de error si la entrada no es válida
                    messagebox.showerror("Error", f"Introduce un número válido en la posición [{i + 1}, {j + 1}].")
                    return None
                fila.append(valor)  # Agregar el valor a la fila actual
            matriz.append(fila)  # Agregar la fila completa a la matriz
        return matriz

    def imprimir_matriz(self, paso, operacion):
        """
        Genera un string que representa la matriz en un formato legible.

        Parámetros:
        -----------
        paso : int
            Número de paso del algoritmo para mostrar en la salida.
        operacion : str
            Descripción de la operación realizada.

        Retorna:
        --------
        str
            Cadena de texto que representa la matriz formateada con los valores actuales.
        """
        texto = f"Paso {paso} ({operacion}):\n"  # Encabezado con el número del paso y la operación realizada
        for fila in self.matriz:
            # Formatear cada valor de la fila a 8 caracteres de ancho y 4 decimales de precisión
            texto += "  ".join(f"{valor:.2f}" if valor != 0 else "0.00" for valor in fila) + "\n"
        texto += "\n"
        return texto

    def eliminacion_gaussiana(self):
        """
        Realiza la eliminación Gaussiana para resolver un sistema de ecuaciones lineales.

        Retorna:
        --------
        str
            Cadena de texto que muestra el paso a paso de la eliminación Gaussiana.
        """
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
                        resultado += self.imprimir_matriz(paso, f"Intercambiar fila {i + 1} con fila {j + 1}")
                        paso += 1
                        break
                pivote = self.matriz[i][i]

            # Dividir toda la fila por el pivote para hacer que el pivote sea 1
            self.matriz[i] = [elemento / pivote for elemento in self.matriz[i]]
            resultado += self.imprimir_matriz(paso, f"Dividir fila {i + 1} entre {pivote:.2f}")
            paso += 1

            # Hacer ceros en todas las demás posiciones de la columna del pivote
            for j in range(self.n):
                if i != j:
                    factor = self.matriz[j][i]
                    self.matriz[j] = [self.matriz[j][k] - factor * self.matriz[i][k] for k in range(self.n + 1)]
                    resultado += self.imprimir_matriz(paso, f"Restar {factor:.2f} veces la fila {i + 1} de la fila {j + 1}")
                    paso += 1

        return resultado