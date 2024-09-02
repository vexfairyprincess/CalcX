class Ecuaciones_Lineales:
    def __init__(self, a1, b1, c1, a2, b2, c2):
        self.a1 = a1
        self.b1 = b1
        self.c1 = c1
        self.a2 = a2
        self.b2 = b2
        self.c2 = c2

    def calcular_mcd(self, a, b):
        #algoritmo de euclides para MCD
        while b != 0:
            a, b = b, a % b
        return a

    def simplificar_fraccion(self, numerador, denominador):
        #simplifica una fracción usando el MCD
        mcd = self.calcular_mcd(numerador, denominador)
        return numerador // mcd, denominador // mcd

    def resolver(self):
        # multiplicar las ecuaciones para igualar los coeficientes de una variable.
        factor1 = self.a2
        factor2 = self.a1

        a1_new = self.a1 * factor1
        b1_new = self.b1 * factor1
        c1_new = self.c1 * factor1

        a2_new = self.a2 * factor2
        b2_new = self.b2 * factor2
        c2_new = self.c2 * factor2

        # restar las dos ecuaciones para eliminar x.
        coef_y = b1_new - b2_new
        constante_y = c1_new - c2_new

        # resolver y
        if coef_y == 0:
            raise ValueError("El sistema no tiene solución única.")
        y_numerador, y_denominador = constante_y, coef_y
        y_numerador, y_denominador = self.simplificar_fraccion(y_numerador, y_denominador)
        y = y_numerador / y_denominador

        # sustituir y en una de las ecuaciones iniciales para encontrar x.
        x_numerador = self.c1 - self.b1 * y
        x_denominador = self.a1

        x_numerador, x_denominador = self.simplificar_fraccion(int(x_numerador), int(x_denominador))
        x = x_numerador / x_denominador

        return x, y