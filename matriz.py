import tkinter as tk
from tkinter import messagebox

# resolver error de impresion del paso a paso

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
        num_columnas = len(entradas[0])
        for i in range(self.n):  # Iterar sobre cada fila
            fila = []
            for j in range(num_columnas):  # Iterar sobre cada columna (incluida la columna de resultados)
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
           texto += "  ".join(f"{int(valor) if isinstance(valor, float) and valor.is_integer() else valor:.2f}" for valor in fila) + "\n"
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
        
        filas, columnas = len(self.matriz), len(self.matriz[0])
        fila_actual = 0

        for col in range(columnas - 1):
            if fila_actual >= filas:
                break

            # Encontrar el pivote no nulo más grande para reducir errores numéricos
            max_row = max(range(fila_actual, filas), key=lambda i: abs(self.matriz[i][col]))
            if abs(self.matriz[max_row][col]) < 1e-10:
                continue  # Saltar si el mejor pivote es cercano a cero

            # Intercambiar la fila actual con la fila del pivote máximo encontrado
            if fila_actual != max_row:
                self.matriz[fila_actual], self.matriz[max_row] = self.matriz[max_row], self.matriz[fila_actual]
                resultado += self.imprimir_matriz(paso, f"Intercambio f{fila_actual + 1} <-> f{max_row + 1}")
                paso += 1

            pivote = self.matriz[fila_actual][col]

            # Si el pivote sigue siendo cercano a cero, pasamos al siguiente paso
            if abs(pivote) < 1e-10:
                continue

            # Dividir toda la fila por el pivote para hacer que el pivote sea 1
            self.matriz[fila_actual] = [elemento / pivote for elemento in self.matriz[fila_actual]]
            resultado += self.imprimir_matriz(paso, f"f{fila_actual + 1} -> (1/{pivote:.2f}) * f{fila_actual + 1}")
            paso += 1

            # Hacer ceros en todas las demás filas en la columna del pivote
            for i in range(filas):
                if i != fila_actual:
                    factor = self.matriz[i][col]
                    if abs(factor) > 1e-10:  # Solo restar si el factor es significativo
                        self.matriz[i] = [self.matriz[i][k] - factor * self.matriz[fila_actual][k] for k in range(columnas)]
                        resultado += self.imprimir_matriz(paso, f"f{i + 1} -> f{i + 1} - ({factor:.2f}) * f{fila_actual + 1}")
                        paso += 1

            fila_actual += 1

        # Interpretar y presentar la solución
        resultado += self.interpretar_resultado()
        return resultado

    def interpretar_resultado(self):
        """
    Interpreta la matriz reducida para expresar las soluciones en términos de variables básicas y libres.

    Retorna:
    --------
    str
        Cadena de texto que representa la solución del sistema en términos de variables básicas y libres.
    """
        n, m = len(self.matriz), len(self.matriz[0]) - 1
        pivotes = [-1] * m  # Lista para almacenar las columnas de los pivotes
        resultado = "Solucion del sistema:\n"
        soluciones = {}

        for j in range(m):
            for i in range(n):
                if abs(self.matriz[i][j] - 1) < 1e-10 and all(abs(self.matriz[k][j]) < 1e-10 for k in range(n) if k != i):
                    pivotes[j] = i
                    break
                
        # Revisar si hay una fila inconsistente (0 = b, donde b != 0)
        fila_inconsistente = [i for i, fila in enumerate(self.matriz) if all(abs(val) < 1e-10 for val in fila[:-1]) and abs(fila[-1]) > 1e-10]
        inconsistente_var = set(f"x{i + 1}" for i in fila_inconsistente)


        # Generar expresiones para las variables y almacenar en el orden correcto
        for j in range(m):
            var_name = f"x{j + 1}"
            if var_name in inconsistente_var:
                soluciones[var_name] = f"{var_name} es inconsistente"
            elif pivotes[j] == -1:
                soluciones[var_name] = f"{var_name} es libre"
            else:
                fila = pivotes[j]
                constante = self.matriz[fila][-1]
                constante_str = f"{int(constante)}" if constante.is_integer() else f"{constante:.2f}" if abs(constante) > 1e-10 else ""

                terminos = []
                for k in range(m):
                    if k != j and abs(self.matriz[fila][k]) > 1e-10:
                        coef = -self.matriz[fila][k]
                        coef_str = "" if abs(coef - 1) < 1e-10 else f"{int(coef)}" if coef.is_integer() else f"{coef:.2f}"
                        terminos.append(f"{coef_str}x{k + 1}")

                ecuacion = constante_str
                for termino in terminos:
                    if ecuacion and not ecuacion.startswith("-") and constante_str:
                        ecuacion += " + " if not termino.startswith("-") else " "
                    ecuacion += termino

                ecuacion = ecuacion.strip()
                if ecuacion.startswith("0 "):
                    ecuacion = ecuacion[2:]
                soluciones[var_name] = f"{var_name} = {ecuacion}".strip()

        # Mostrar las soluciones en orden
        for i in range(m):
            var_name = f"x{i + 1}"
            if var_name in soluciones:
                resultado += f"{soluciones[var_name]}\n"

        # Determinación de tipo de solución
        if inconsistente_var:
            resultado += "El sistema es inconsistente y no tiene soluciones.\n"
        elif any(pivote == -1 for pivote in pivotes):
            resultado += "Hay infinitas soluciones debido a variables libres.\n"
        else:
            resultado += "La solución es única.\n"

        return resultado

    def calcular_result(self):
        self.eliminacion_gaussiana()
        return self.interpretar_resultado()
