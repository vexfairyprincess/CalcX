#matrizxvector.py

class MxV:
    def __init__(self, matriz=None, vectores=None):
        """
        Inicializa la clase MxV con una matriz y una lista de vectores.
        :param matriz: lista de listas de floats que representa la matriz
        :param vectores: lista de listas de floats que representan vectores
        """
        self.matriz = self.obtener_matriz(matriz)  # Procesa y almacena la matriz
        self.vectores = [self.obtener_vector(vector) for vector in vectores]  # Procesa y almacena los vectores

    def obtener_matriz(self, entradas):
        """
        Convierte una lista de listas de cadenas o números en una matriz de floats.
        :param entradas: lista de listas que representan la matriz
        :return: matriz de floats
        :raises ValueError: Si algún elemento no puede convertirse a float
        """
        try:
            matriz = [[float(n) for n in fila] for fila in entradas]
        except ValueError:
            raise ValueError("Introduce un número válido en la matriz.")
        return matriz

    def obtener_vector(self, entradas):
        """
        Convierte una lista de cadenas o números en un vector de floats.
        :param entradas: lista que representa el vector
        :return: vector de floats
        :raises ValueError: Si algún elemento no puede convertirse a float
        """
        try:
            vector = [float(n) for n in entradas]
        except ValueError:
            raise ValueError("Introduce un número válido en el vector.")
        return vector

    def sumar_vectores(self):
        """
        Suma todos los vectores proporcionados en la lista de vectores.
        :return: vector resultante de la suma
        :raises ValueError: Si no hay vectores proporcionados
        """
        if not self.vectores:
            raise ValueError("No se proporcionaron vectores para sumar.")

        n = len(self.vectores[0])  # Longitud de los vectores
        vector_suma = [0] * n  # Vector inicializado a cero

        for vector in self.vectores:
            for i in range(n):
                vector_suma[i] += vector[i]  # Suma cada componente del vector

        return vector_suma

    def multiplicar_matriz_por_vector(self, vector):
        """
        Multiplica la matriz almacenada por un vector dado.
        :param vector: vector por el cual multiplicar la matriz
        :return: vector resultante de la multiplicación
        :raises ValueError: Si las dimensiones de la matriz y el vector no coinciden
        """
        filas = len(self.matriz)
        columnas = len(self.matriz[0])

        if columnas != len(vector):
            raise ValueError("El número de columnas de la matriz debe coincidir con el tamaño del vector")

        resultado = [0] * filas  # Vector resultado inicializado a cero

        for i in range(filas):
            suma = 0
            for j in range(columnas):
                suma += self.matriz[i][j] * vector[j]  # Multiplica y suma la fila por el vector
            resultado[i] = suma

        return resultado

    def aplicar_propiedad(self):
        """
        Aplica la propiedad lineal A(u + v) = Au + Av para dos vectores u y v.
        :return: tupla con los resultados Au, Av y A(u + v)
        :raises ValueError: Si no hay exactamente dos vectores para aplicar la propiedad
        """
        if len(self.vectores) != 2:
            raise ValueError("Se requieren exactamente 2 vectores para aplicar la propiedad.")

        u = self.vectores[0]  # Vector u
        v = self.vectores[1]  # Vector v

        Au = self.multiplicar_matriz_por_vector(u)  # Multiplica la matriz por u
        Av = self.multiplicar_matriz_por_vector(v)  # Multiplica la matriz por v

        u_plus_v = self.sumar_vectores()  # Suma los vectores u y v
        A_u_plus_v = self.multiplicar_matriz_por_vector(u_plus_v)  # Multiplica la matriz por u+v

        return Au, Av, A_u_plus_v  # Retorna los tres resultados