import tkinter as tk
from tkinter import messagebox

def imprimir_matriz(matriz, paso):
    texto = f"Paso {paso}:\n"
    for fila in matriz:
        texto += "  ".join(f"{valor:8.4f}" for valor in fila) + "\n"
    texto += "\n"
    return texto

def gauss_jordan(matriz):
    n = len(matriz)
    paso = 1
    resultado = ""
    
    # Operación de Gauss-Jordan
    for i in range(n):
        # Hacer que el pivote sea 1 dividiendo la fila por el pivote
        pivote = matriz[i][i]
        if pivote == 0:
            # Verificar si hay un 0 en el pivote y cambiar filas si es necesario
            for j in range(i + 1, n):
                if matriz[j][i] != 0:
                    # Intercambiar filas
                    matriz[i], matriz[j] = matriz[j], matriz[i]
                    break
            pivote = matriz[i][i]
        
        # Dividir toda la fila por el pivote para hacer que el pivote sea 1
        matriz[i] = [elemento / pivote for elemento in matriz[i]]
        resultado += imprimir_matriz(matriz, paso)
        paso += 1
        
        # Hacer ceros en todas las demás posiciones de la columna del pivote
        for j in range(n):
            if i != j:
                factor = matriz[j][i]
                matriz[j] = [matriz[j][k] - factor * matriz[i][k] for k in range(n + 1)]
                resultado += imprimir_matriz(matriz, paso)
                paso += 1

    return resultado

def obtener_matriz(n, entradas):
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n + 1):
            try:
                valor = float(entradas[i][j].get())
            except ValueError:
                messagebox.showerror("Error", f"Introduce un número válido en la posición [{i+1}, {j+1}].")
                return None
            fila.append(valor)
        matriz.append(fila)
    return matriz

def mostrar_resultado():
    n = int(entrada_n.get())
    matriz = obtener_matriz(n, entradas)
    if matriz is not None:
        resultado = gauss_jordan(matriz)
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, resultado)

def crear_entradas_matriz():
    for widget in frame_matriz.winfo_children():
        widget.destroy()
    
    n = int(entrada_n.get())
    global entradas
    entradas = [[tk.Entry(frame_matriz, width=10) for j in range(n + 1)] for i in range(n)]

    for i in range(n):
        for j in range(n + 1):
            entradas[i][j].grid(row=i, column=j, padx=5, pady=5)
    
    etiqueta_titulo_matriz.config(text=f"Introduce los coeficientes de la matriz de {n}x{n+1}:")

# Interfaz gráfica usando tkinter
root = tk.Tk()
root.title("Método de Gauss-Jordan")

# Tamaño de la matriz
frame_tamano = tk.Frame(root)
frame_tamano.pack(pady=10)

etiqueta_n = tk.Label(frame_tamano, text="Número de ecuaciones:")
etiqueta_n.pack(side=tk.LEFT)

entrada_n = tk.Entry(frame_tamano, width=5)
entrada_n.pack(side=tk.LEFT)
entrada_n.insert(0, "3")

boton_crear = tk.Button(frame_tamano, text="Crear Matriz", command=crear_entradas_matriz)
boton_crear.pack(side=tk.LEFT, padx=10)

# Entradas para la matriz
frame_matriz = tk.Frame(root)
frame_matriz.pack(pady=10)

etiqueta_titulo_matriz = tk.Label(root, text="Introduce los coeficientes de la matriz:")
etiqueta_titulo_matriz.pack()

# Área de texto para el resultado
text_resultado = tk.Text(root, height=20, width=70)
text_resultado.pack(pady=10)

# Botón para calcular
boton_calcular = tk.Button(root, text="Calcular", command=mostrar_resultado)
boton_calcular.pack(pady=10)

root.mainloop()