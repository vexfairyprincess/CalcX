#matriz.py

class Matriz:
    """
    Clase que representa una matriz y permite realizar eliminación Gaussiana.
    """

    def __init__(self, n, entradas=None):
        """
        Inicializa la matriz con el tamaño dado y las entradas del usuario.
        :param n: número de ecuaciones (filas) y de incógnitas (columnas)
        :param entradas: lista de listas con los coeficientes de las ecuaciones
        """
        self.n = n  # Almacena el número de ecuaciones
        self.matriz = self.obtener_matriz(entradas)  # Construye la matriz a partir de las entradas

    def obtener_matriz(self, entradas):
        """
        Convierte las entradas en formato de lista de listas a una matriz de números flotantes.
        :param entradas: lista de listas con los coeficientes de las ecuaciones
        :return: matriz convertida a tipo flotante
        :raises ValueError: Si alguna entrada no puede ser convertida a float
        """
        try:
            matriz = [[float(valor) for valor in fila] for fila in entradas]  # Convierte cada entrada a float
        except ValueError:
            raise ValueError("Introduce un número válido en la matriz.")
        return matriz

    def imprimir_matriz(self, paso, operacion):
        """
        Crea una representación string de la matriz en un formato legible.
        :param paso: número del paso actual en el proceso de eliminación
        :param operacion: descripción de la operación realizada
        :return: string que representa el estado actual de la matriz
        """
        texto = f"Paso {paso} ({operacion}):\n"  # Encabezado del paso
        for fila in self.matriz:
            texto += "  ".join(f"{valor:.2f}" for valor in fila) + "\n"  # Formato de cada fila con dos decimales
        texto += "\n"
        return texto

    def eliminacion_gaussiana(self):
        """
        Aplica el método de eliminación Gaussiana para transformar la matriz a su forma escalonada.
        :return: string con todos los pasos de la eliminación y la solución interpretada
        """
        if not self.matriz:
            return "Matriz no válida."

        paso = 1
        resultado = ""
        filas, columnas = len(self.matriz), len(self.matriz[0])  # Determina las dimensiones de la matriz
        fila_actual = 0

        for col in range(columnas - 1):
            if fila_actual >= filas:
                break  # Si se alcanza el número de filas, termina el proceso

            # Encuentra el pivote más grande en la columna actual
            max_row = max(range(fila_actual, filas), key=lambda i: abs(self.matriz[i][col]))
            if abs(self.matriz[max_row][col]) < 1e-10:
                continue  # Omite la columna si el pivote es cercano a cero

            # Intercambia filas si es necesario
            if fila_actual != max_row:
                self.matriz[fila_actual], self.matriz[max_row] = self.matriz[max_row], self.matriz[fila_actual]
                resultado += self.imprimir_matriz(paso, f"Intercambio f{fila_actual + 1} <-> f{max_row + 1}")
                paso += 1

            pivote = self.matriz[fila_actual][col]  # Establece el pivote actual

            # Normaliza la fila del pivote
            if abs(pivote) > 1e-10:
                self.matriz[fila_actual] = [elemento / pivote for elemento in self.matriz[fila_actual]]
                resultado += self.imprimir_matriz(paso, f"f{fila_actual + 1} -> (1/{pivote:.2f}) * f{fila_actual + 1}")
                paso += 1

            # Elimina los elementos debajo del pivote
            for i in range(filas):
                if i != fila_actual:
                    factor = self.matriz[i][col]
                    if abs(factor) > 1e-10:
                        self.matriz[i] = [self.matriz[i][k] - factor * self.matriz[fila_actual][k] for k in range(columnas)]
                        resultado += self.imprimir_matriz(paso, f"f{i + 1} -> f{i + 1} - ({factor:.2f}) * f{fila_actual + 1}")
                        paso += 1

            fila_actual += 1  # Avanza a la siguiente fila a considerar

        resultado += self.interpretar_resultado()  # Interpreta y añade el resultado final
        return resultado

    def interpretar_resultado(self):
        """
        Interpreta la matriz escalonada reducida, indicando si el sistema es consistente, y hallando las soluciones.
        :return: string que describe la solución del sistema y las columnas pivote
        """
        n, m = len(self.matriz), len(self.matriz[0]) - 1  # Dimensiones excluyendo la columna de resultados
        pivotes = [-1] * m  # Inicializa los índices de las columnas pivote
        resultado = "Solución del sistema:\n"
        soluciones = {}
        columnas_pivote = []  # Lista para registrar las columnas pivote

        # Identifica las columnas pivote
        for j in range(m):
            for i in range(n):
                if abs(self.matriz[i][j] - 1) < 1e-10 and all(abs(self.matriz[k][j]) < 1e-10 for k in range(n) if k != i):
                    pivotes[j] = i
                    columnas_pivote.append(j + 1)  # Almacena la columna con índice 1-based
                    break

        # Detecta filas inconsistentes (cero igual a un número no cero)
        fila_inconsistente = [
            i for i, fila in enumerate(self.matriz)
            if all(abs(val) < 1e-10 for val in fila[:-1]) and abs(fila[-1]) > 1e-10
        ]
        inconsistente_var = set(f"x{i + 1}" for i in fila_inconsistente)

        # Genera las soluciones o identifica variables libres/inconsistentes
        for j in range(m):
            var_name = f"x{j + 1}"
            if var_name in inconsistente_var:
                soluciones[var_name] = f"{var_name} es inconsistente"
            elif pivotes[j] == -1:
                soluciones[var_name] = f"{var_name} es libre"
            else:
                fila = pivotes[j]
                constante = self.matriz[fila][-1]
                constante_str = (
                    f"{int(constante)}" if constante.is_integer() else f"{constante:.2f}"
                )
                terminos = []
                # Agrega términos de variables libres con coeficientes
                for k in range(m):
                    if k != j and pivotes[k] == -1 and abs(self.matriz[fila][k]) > 1e-10:
                        coef = -self.matriz[fila][k]
                        coef_str = (
                            f"{int(coef)}" if coef.is_integer() else f"{coef:.2f}"
                        )
                        if coef < 0:
                            terminos.append(f"{coef_str}x{k + 1}")
                        else:
                            terminos.append(f"+ {coef_str}x{k + 1}")
                ecuacion = ""
                if constante_str != "0":
                    ecuacion += constante_str
                if terminos:
                    if ecuacion and ecuacion != "0":
                        ecuacion += " " + " ".join(terminos)
                    else:
                        ecuacion = " ".join(terminos).lstrip("+ ").strip()

                soluciones[var_name] = f"{var_name} = {ecuacion}".strip()

        # Compila y muestra las soluciones ordenadas
        for i in range(m):
            var_name = f"x{i + 1}"
            if var_name in soluciones:
                resultado += f"{soluciones[var_name]}\n"

        # Determina si el sistema tiene solución única, infinitas soluciones o es inconsistente
        if inconsistente_var:
            resultado += "\nEl sistema es inconsistente y no tiene soluciones.\n"
        elif any(pivote == -1 for pivote in pivotes):
            resultado += "\nHay infinitas soluciones debido a variables libres.\n"
        else:
            resultado += "\nLa solución es única.\n"

        # Muestra las columnas pivote
        resultado += f"\nLas columnas pivote son: {', '.join(map(str, columnas_pivote))}.\n"

        return resultado
    
    def escalar_por_matriz(self, escalar):
        """Multiplica la matriz actual por un escalar."""
        resultado = []
        for fila in self.matriz:
            fila_resultado = [escalar * valor for valor in fila]
            resultado.append(fila_resultado)
        return Matriz(len(self.matriz), resultado)
    
    def suma(self, otra_matriz):
        """Suma la matriz actual con otra matriz del mismo tamaño."""
        if len(self.matriz) != len(otra_matriz.matriz) or len(self.matriz[0]) != len(otra_matriz.matriz[0]):
            raise ValueError("Las matrices deben tener el mismo tamaño para sumarse.")
        
        resultado = []
        for i in range(len(self.matriz)):
            fila_resultado = []
            for j in range(len(self.matriz[0])):
                suma = self.matriz[i][j] + otra_matriz.matriz[i][j]
                fila_resultado.append(suma)
            resultado.append(fila_resultado)
        
        return Matriz(len(self.matriz), resultado)
    
    def calcular_transpuesta(self):
        """
        Calcula la transpuesta de la matriz.
        :return: nueva instancia de Matriz que representa la matriz transpuesta
        """
        if not self.matriz or not self.matriz[0]:
            raise ValueError("La matriz no puede estar vacía.")
        
        transpuesta = [[self.matriz[j][i] for j in range(self.n)] for i in range(len(self.matriz[0]))]
        return Matriz(len(transpuesta), transpuesta)

    def formatear_matriz(self):
        """
        Formatea la matriz para visualización en un string legible.
        :return: string que muestra la matriz
        """
        texto_matriz = ""
        for fila in self.matriz:
            texto_matriz += "  ".join(f"{val:.2f}" for val in fila) + "\n"
        return texto_matriz
    
    def multiplicar_por(self, otra_matriz):
        """
        Multiplica la matriz actual por otra matriz si las dimensiones son compatibles.
        :param otra_matriz: instancia de Matriz que será multiplicada con la matriz actual
        :return: nueva instancia de Matriz que representa el producto de las dos matrices
        """
        if len(self.matriz[0]) != len(otra_matriz.matriz):
            raise ValueError("El número de columnas de la primera matriz debe coincidir con el número de filas de la segunda matriz.")
        
        # Inicializar la matriz resultado con ceros
        resultado = [[0] * len(otra_matriz.matriz[0]) for _ in range(len(self.matriz))]
        
        # Multiplicar matrices
        for i in range(len(self.matriz)):
            for j in range(len(otra_matriz.matriz[0])):
                for k in range(len(otra_matriz.matriz)):
                    resultado[i][j] += self.matriz[i][k] * otra_matriz.matriz[k][j]
        
        return Matriz(len(resultado), resultado)
    
    def calcular_determinante(self, paso_a_paso=False):
        """
        Calcula el determinante de la matriz utilizando el método de eliminación Gaussiana.
        :param paso_a_paso: si es True, guarda cada paso de la eliminación
        :return: tupla con el determinante y los pasos como un string
        :raises ValueError: si la matriz no es cuadrada
        """
        if len(self.matriz) != len(self.matriz[0]):
            raise ValueError("El determinante solo se puede calcular para matrices cuadradas.")

        n = len(self.matriz)
        # Copia la matriz para no modificar la original
        matriz_temp = [fila[:] for fila in self.matriz]
        determinante = 1
        pasos = "" if paso_a_paso else None

        for i in range(n):
            # Encontrar el pivote más grande en la columna actual
            max_row = max(range(i, n), key=lambda x: abs(matriz_temp[x][i]))
            if abs(matriz_temp[max_row][i]) < 1e-10:
                return 0, pasos if paso_a_paso else 0  # Si el pivote es 0, el determinante es 0

            # Intercambiar filas si el pivote no está en la fila actual
            if i != max_row:
                matriz_temp[i], matriz_temp[max_row] = matriz_temp[max_row], matriz_temp[i]
                determinante *= -1  # Cambia de signo el determinante por el intercambio
                if paso_a_paso:
                    pasos += f"Intercambio de filas {i + 1} y {max_row + 1} cambia el signo del determinante.\n"
                    pasos += self.formatear_matriz(matriz_temp) + "\n"

            # Multiplicar el elemento diagonal al determinante
            pivote = matriz_temp[i][i]
            determinante *= pivote
            if paso_a_paso:
                pasos += f"Multiplicando por el pivote {pivote:.2f} en la posición ({i + 1}, {i + 1}) acumula el determinante: {determinante:.2f}\n"
                pasos += self.formatear_matriz(matriz_temp) + "\n"

            # Hacer el pivote igual a 1 y reducir las filas debajo de la fila actual
            for j in range(i + 1, n):
                factor = matriz_temp[j][i] / pivote
                for k in range(i, n):
                    matriz_temp[j][k] -= factor * matriz_temp[i][k]

                if paso_a_paso:
                    pasos += f"Reduciendo Fila {j + 1}: F{j + 1} -> F{j + 1} - ({factor:.2f}) * F{i + 1}\n"
                    pasos += self.formatear_matriz(matriz_temp) + "\n"

        # Después de reducir la matriz, el determinante final es el producto de los elementos de la diagonal.
        if paso_a_paso:
            pasos += f"\nDeterminante final (producto de los elementos de la diagonal): {determinante:.2f}\n"

        return determinante, pasos if paso_a_paso else determinante

    def formatear_matriz(self, matriz):
        """Convierte una matriz en una representación string para mostrar los pasos"""
        texto_matriz = ""
        for fila in matriz:
            texto_matriz += "  ".join(f"{val:.2f}" for val in fila) + "\n"
        return texto_matriz