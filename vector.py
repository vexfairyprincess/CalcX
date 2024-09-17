# vector.py

class Vector:
    """Clase para representar y operar con vectores."""
    
    def __init__(self, componentes):
        if not isinstance(componentes, list) or not all(isinstance(x, (int, float)) for x in componentes):
            raise ValueError("Las componentes deben ser una lista de números.")
        self.componentes = componentes

    def __str__(self):
        return f"Vector({self.componentes})"
    
    def suma(self, otro):
        """Suma de vectores."""
        if len(self.componentes) != len(otro.componentes):
            raise ValueError("Los vectores deben tener la misma longitud.")
        suma = [a + b for a, b in zip(self.componentes, otro.componentes)]
        return Vector(suma)
    
    def resta(self, otro):
        """Resta de vectores."""
        if len(self.componentes) != len(otro.componentes):
            raise ValueError("Los vectores deben tener la misma longitud.")
        resta = [a - b for a, b in zip(self.componentes, otro.componentes)]
        return Vector(resta)

    def multiplicacion(self, escalar):
        """Multiplicación por un escalar."""
        if not isinstance(escalar, (int, float)):
            raise ValueError("El escalar debe ser un número.")
        producto = [escalar * x for x in self.componentes]
        return Vector(producto)

    def producto_escalar(self, otro):
        """Producto escalar entre dos vectores."""
        if len(self.componentes) != len(otro.componentes):
            raise ValueError("Los vectores deben tener la misma longitud.")
        producto = sum(a * b for a, b in zip(self.componentes, otro.componentes))
        return producto

    def producto_cruz(self, otro):
        """Producto cruz entre dos vectores de 3 dimensiones."""
        if len(self.componentes) != 3 or len(otro.componentes) != 3:
            raise ValueError("Los vectores deben ser de longitud 3.")
        a, b, c = self.componentes
        d, e, f = otro.componentes
        cruz = [
            b * f - c * e,
            c * d - a * f,
            a * e - b * d
        ]
        return Vector(cruz)
