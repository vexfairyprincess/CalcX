def print_matrix(matrix):
    for row in matrix:
        print(' '.join(f"{x:8.4f}" for x in row))
    print()

def make_identity(matrix):
    n = len(matrix)

    for i in range(n):
        # Hacer que el elemento diagonal sea 1
        diag = matrix[i][i]
        if diag != 1:
            print(f"Dividiendo la fila {i+1} por {diag:.4f}")
            for j in range(n):
                matrix[i][j] /= diag
            print_matrix(matrix)

        # Hacer ceros en la columna de la diagonal
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                if factor != 0:
                    print(f"Restando {factor:.4f} veces la fila {i+1} de la fila {k+1}")
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
                    print_matrix(matrix)

    return matrix

def main():
    # Solicitar el tamaño de la matriz
    n = int(input("Introduce el tamaño de la matriz cuadrada: "))

    # Crear la matriz
    matrix = []
    print("Introduce los elementos de la matriz fila por fila:")
    for i in range(n):
        row = list(map(float, input(f"Fila {i+1}: ").split()))
        matrix.append(row)

    # Mostrar la matriz inicial
    print("\nMatriz inicial:")
    print_matrix(matrix)

    # Convertir la matriz en la identidad
    identity_matrix = make_identity(matrix)

    # Mostrar la matriz identidad resultante
    print("Matriz identidad resultante:")
    print_matrix(identity_matrix)

if __name__ == "__main__":
    main()