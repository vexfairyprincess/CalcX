class MxV:
    def __init__(self, matriz=None, vectores=None):
        """Recibe una matriz y una lista de vectores."""
        self.matriz = self.obtener_matriz(matriz)
        self.vectores = [self.obtener_vector(vector) for vector in vectores]

    def obtener_matriz(self, entradas):
        """Convierte las entradas (listas de listas de floats) en una matriz."""
        try:
            matriz = [[float(n) for n in fila] for fila in entradas]
        except ValueError:
            raise ValueError("Introduce un número válido en la matriz.")
        return matriz

    def obtener_vector(self, entradas):
        """Convierte las entradas (lista de floats) en un vector."""
        try:
            vector = [float(n) for n in entradas]
        except ValueError:
            raise ValueError("Introduce un número válido en el vector.")
        return vector

    def sumar_vectores(self):
        """Suma todos los vectores en la lista de vectores."""
        if not self.vectores:
            raise ValueError("No se proporcionaron vectores para sumar.")

        # Suponiendo que todos los vectores tienen la misma longitud
        n = len(self.vectores[0])
        vector_suma = [0] * n

        for vector in self.vectores:
            for i in range(n):
                vector_suma[i] += vector[i]

        return vector_suma

    def multiplicar_matriz_por_vector(self, vector):
        """Multiplica una matriz por un vector."""
        filas = len(self.matriz)
        columnas = len(self.matriz[0])

        if columnas != len(vector):
            raise ValueError("El número de columnas de la matriz debe coincidir con el tamaño del vector")

        # Inicializar el vector resultado
        resultado = [0] * filas

        for i in range(filas):
            suma = 0
            for j in range(columnas):
                suma += self.matriz[i][j] * vector[j]
            resultado[i] = suma

        return resultado

    def aplicar_propiedad(self):
        """Aplica la propiedad A(u + v) = Au + Av."""
        if len(self.vectores) != 2:
            raise ValueError("Se requieren exactamente 2 vectores para aplicar la propiedad.")

        # Extraer los vectores u y v
        u = self.vectores[0]
        v = self.vectores[1]

        # Multiplicar A por u
        Au = self.multiplicar_matriz_por_vector(u)

        # Multiplicar A por v
        Av = self.multiplicar_matriz_por_vector(v)

        # Sumar los vectores u y v
        u_plus_v = self.sumar_vectores()

        # Multiplicar A por (u + v)
        A_u_plus_v = self.multiplicar_matriz_por_vector(u_plus_v)

        return Au, Av, A_u_plus_v

"""
 Ejemplo de uso

# Definir una matriz
matriz = [
    [1, 2, 3, 4],
    [4, 5, 6, 4],
    [7, 8, 9, 4],
    [7, 9, 8, 2]
]

# Definir vectores
vector_u = [1, 0, 1, 4]
vector_v = [1, 1, 3, 4]

mxv_instance = MxV(matriz=matriz, vectores=[vector_u, vector_v])

Au, Av, A_u_plus_v = mxv_instance.aplicar_propiedad()

# Mostrar los resultados
print(f"Au: {Au}")
print(f"Av: {Av}")
print(f"A(u + v): {A_u_plus_v}")

# Verificar si Au + Av es igual a A(u + v)
Au_plus_Av = [Au[i] + Av[i] for i in range(len(Au))]
print(f"Au + Av: {Au_plus_Av}")

if Au_plus_Av == A_u_plus_v:
    print("La propiedad A(u + v) = Au + Av se cumple.")
else:
    print("La propiedad no se cumple.")
"""