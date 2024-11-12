# utils.py

from sympy import sympify

def evaluar_expresion(expresion):
    """
    Evalúa una expresión matemática en formato de string.
    :param expresion: expresión en formato string.
    :return: valor evaluado de la expresión.
    """
    try:
        return float(sympify(expresion))  # Convierte la expresión a un número flotante
    except (TypeError, ValueError):
        raise ValueError(f"Expresión no válida: {expresion}")