#matriz.py

class Matriz:
    """Clase que representa una matriz y permite realizar eliminación Gaussiana."""

    def __init__(self, n, entradas=None):
        """Inicializa la matriz con el tamaño dado y las entradas del usuario."""
        self.n = n  # Número de ecuaciones
        self.matriz = self.obtener_matriz(entradas)  # Obtener la matriz desde las entradas

    def obtener_matriz(self, entradas):
        """Convierte las entradas (listas de listas de floats) en una matriz."""
        try:
            matriz = [[float(valor) for valor in fila] for fila in entradas]
        except ValueError:
            raise ValueError("Introduce un número válido en la matriz.")
        return matriz

    def imprimir_matriz(self, paso, operacion):
        """Genera un string que representa la matriz en un formato legible."""
        texto = f"Paso {paso} ({operacion}):\n"  # Encabezado con el paso y la operación
        for fila in self.matriz:
            texto += "  ".join(f"{valor:.2f}" for valor in fila) + "\n"  # Formato de cada fila
        texto += "\n"
        return texto

    def eliminacion_gaussiana(self):
        """Realiza la eliminación Gaussiana para resolver el sistema de ecuaciones."""
        if not self.matriz:
            return "Matriz no válida."

        paso = 1
        resultado = ""
        filas, columnas = len(self.matriz), len(self.matriz[0])  # Dimensiones de la matriz
        fila_actual = 0

        for col in range(columnas - 1):
            if fila_actual >= filas:
                break  # Si no hay más filas, detiene el proceso

            # Busca el pivote más grande en valor absoluto
            max_row = max(range(fila_actual, filas), key=lambda i: abs(self.matriz[i][col]))
            if abs(self.matriz[max_row][col]) < 1e-10:
                continue  # Salta si el pivote es muy pequeño (cercano a cero)

            # Intercambia la fila actual con la del pivote máximo
            if fila_actual != max_row:
                self.matriz[fila_actual], self.matriz[max_row] = self.matriz[max_row], self.matriz[fila_actual]
                resultado += self.imprimir_matriz(paso, f"Intercambio f{fila_actual + 1} <-> f{max_row + 1}")
                paso += 1

            pivote = self.matriz[fila_actual][col]  # Pivote de la fila actual

            # Normaliza la fila del pivote
            if abs(pivote) > 1e-10:
                self.matriz[fila_actual] = [elemento / pivote for elemento in self.matriz[fila_actual]]
                resultado += self.imprimir_matriz(paso, f"f{fila_actual + 1} -> (1/{pivote:.2f}) * f{fila_actual + 1}")
                paso += 1

            # Hace ceros en las demás filas de la columna actual
            for i in range(filas):
                if i != fila_actual:
                    factor = self.matriz[i][col]
                    if abs(factor) > 1e-10:
                        self.matriz[i] = [self.matriz[i][k] - factor * self.matriz[fila_actual][k] for k in range(columnas)]
                        resultado += self.imprimir_matriz(paso, f"f{i + 1} -> f{i + 1} - ({factor:.2f}) * f{fila_actual + 1}")
                        paso += 1

            fila_actual += 1  # Avanza a la siguiente fila

        resultado += self.interpretar_resultado()  # Interpreta el resultado final
        return resultado

    def interpretar_resultado(self):
        """Interpreta la matriz reducida para expresar las soluciones y muestra las columnas pivote."""
        n, m = len(self.matriz), len(self.matriz[0]) - 1  # Dimensiones sin la columna de resultados
        pivotes = [-1] * m  # Lista para almacenar las posiciones de los pivotes
        resultado = "Solución del sistema:\n"
        soluciones = {}
        columnas_pivote = []  # Lista para almacenar las columnas pivote

        # Identifica las columnas de los pivotes
        for j in range(m):
            for i in range(n):
                if abs(self.matriz[i][j] - 1) < 1e-10 and all(abs(self.matriz[k][j]) < 1e-10 for k in range(n) if k != i):
                    pivotes[j] = i
                    columnas_pivote.append(j + 1)  # Guarda la columna (indexada desde 1)
                    break

        # Detecta filas inconsistentes (0 = b, donde b != 0)
        fila_inconsistente = [
            i for i, fila in enumerate(self.matriz)
            if all(abs(val) < 1e-10 for val in fila[:-1]) and abs(fila[-1]) > 1e-10
        ]
        inconsistente_var = set(f"x{i + 1}" for i in fila_inconsistente)

        # Genera expresiones para las variables
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
                # Añade términos con variables libres
                for k in range(m):
                    if k != j and pivotes[k] == -1 and abs(self.matriz[fila][k]) > 1e-10:
                        coef = -self.matriz[fila][k]
                        coef_str = (
                            f"{int(coef)}" if coef.is_integer() else f"{coef:.2f}"
                        )
                        # Ajusta el formato para manejar el signo
                        if coef < 0:
                            terminos.append(f"{coef_str}x{k + 1}")
                        else:
                            terminos.append(f"+ {coef_str}x{k + 1}")

                # Construye la ecuación sin redundancias de signos
                ecuacion = ""
                if constante_str != "0":
                    ecuacion += constante_str

                # Junta los términos y ajusta el formato para evitar redundancias como "+ -"
                if terminos:
                    if ecuacion and ecuacion != "0":
                        ecuacion += " " + " ".join(terminos)
                    else:
                        ecuacion = " ".join(terminos).lstrip("+ ").strip()  # Quita el "+" inicial si es el primer término

                soluciones[var_name] = f"{var_name} = {ecuacion}".strip()

        # Imprime las soluciones en orden
        for i in range(m):
            var_name = f"x{i + 1}"
            if var_name in soluciones:
                resultado += f"{soluciones[var_name]}\n"

        # Determina el tipo de solución
        if inconsistente_var:
            resultado += "\nEl sistema es inconsistente y no tiene soluciones.\n"
        elif any(pivote == -1 for pivote in pivotes):
            resultado += "\nHay infinitas soluciones debido a variables libres.\n"
        else:
            resultado += "\nLa solución es única.\n"

        # Añade una línea indicando las columnas pivote
        resultado += f"\nLas columnas pivote son: {', '.join(map(str, columnas_pivote))}.\n"

        return resultado