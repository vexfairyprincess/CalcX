# vector.py (actualizado)

class Vector:
    """Clase para representar y operar con vectores de tamaño variable."""

    def __init__(self, componentes):
        if not isinstance(componentes, list) or not all(isinstance(x, (int, float)) for x in componentes):
            raise ValueError("Las componentes deben ser una lista de números.")
        self.componentes = componentes

    def __str__(self):
        return f"Vector({self.componentes})"
    
    @staticmethod
    def suma_vectores(lista_vectores):
        """Suma todos los vectores en la lista."""
        if not lista_vectores:
            raise ValueError("La lista de vectores está vacía.")
        
        longitud = len(lista_vectores[0].componentes)
        for vector in lista_vectores:
            if len(vector.componentes) != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")

        suma = [0] * longitud
        for vector in lista_vectores:
            suma = [a + b for a, b in zip(suma, vector.componentes)]
        
        return Vector(suma)
    
    @staticmethod
    def resta_vectores(lista_vectores):
        """Resta todos los vectores en la lista, comenzando por el primero."""
        if not lista_vectores:
            raise ValueError("La lista de vectores está vacía.")
        
        longitud = len(lista_vectores[0].componentes)
        for vector in lista_vectores:
            if len(vector.componentes) != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")

        resta = lista_vectores[0].componentes.copy()
        for vector in lista_vectores[1:]:
            resta = [a - b for a, b in zip(resta, vector.componentes)]
        
        return Vector(resta)

    @staticmethod
    def multiplicacion_por_escalar(vector, escalar):
        """Multiplica un vector por un escalar dado."""
        if not isinstance(escalar, (int, float)):
            raise ValueError("El escalar debe ser un número.")
        producto = [escalar * x for x in vector.componentes]
        return Vector(producto)

    @staticmethod
    def suma_escalada(lista_vectores, lista_escalars):
        """Realiza la suma de los vectores, cada uno multiplicado por su escalar correspondiente."""
        if len(lista_vectores) != len(lista_escalars):
            raise ValueError("La cantidad de vectores debe coincidir con la cantidad de escalares.")
        
        longitud = len(lista_vectores[0].componentes)
        for vector in lista_vectores:
            if len(vector.componentes) != longitud:
                raise ValueError("Todos los vectores deben tener la misma longitud.")
        
        suma = [0] * longitud
        for vector, escalar in zip(lista_vectores, lista_escalars):
            suma = [s + (escalar * v) for s, v in zip(suma, vector.componentes)]
        
        return Vector(suma)

    @staticmethod
    def crear_vector_aleatorio(longitud):
        """Genera un vector aleatorio de la longitud especificada."""
        from random import randint
        return Vector([randint(-10, 10) for _ in range(longitud)])

# Ejemplo de uso:
# vectores = [Vector([1, 2, 3]), Vector([4, 5, 6]), Vector([7, 8, 9])]
# suma_resultado = Vector.suma_escalada(vectores, [1, 2, 3])
# print(suma_resultado)  # Output: Vector([30, 36, 42])