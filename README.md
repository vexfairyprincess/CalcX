# <img src="calcXlogo.svg" alt="Logo de Calculadora de Matrices" width="300">

## Descripción del Proyecto
Este proyecto es una calculadora de matrices y operaciones numéricas avanzadas diseñada para resolver problemas complejos de Álgebra Lineal y Análisis Numérico. Desarrollada para la clase de Álgebra Lineal impartida por el profesor Iván Argüello, esta herramienta ofrece una interfaz gráfica amigable y funcionalidades detalladas que permiten a los usuarios realizar una variedad de operaciones matemáticas de manera interactiva.

## Métodos Disponibles

### Álgebra Lineal
- **Multiplicación de Matrices**: Realiza la multiplicación de matrices de dimensiones compatibles.
- **Suma de Matrices**: Permite sumar matrices de las mismas dimensiones.
- **Determinante de Matrices**: Calcula el determinante de matrices cuadradas.
- **Inversa de Matrices**: Utiliza el método de eliminación Gauss-Jordan para encontrar la inversa de matrices cuadradas.
- **Transpuesta de Matriz**: Obtiene la transpuesta de cualquier matriz.
- **Producto Matriz por Vector**: Realiza el producto de una matriz por un vector.
- **Método de Cramer**: Resuelve sistemas de ecuaciones lineales utilizando la regla de Cramer.
- **Factorización LU**: Descompone matrices cuadradas en productos de matrices triangulares.
- **Reducción por el Método Escalonado**: Lleva una matriz a su forma escalonada.

### Análisis Numérico
- **Método de Bisección**:
  - **Descripción**: Busca una raíz de una función continua `f(x)` en un intervalo `[a, b]` donde `f(a)` y `f(b)` tienen signos opuestos. El intervalo se va dividiendo a la mitad sucesivamente hasta encontrar una aproximación de la raíz con la tolerancia deseada.
    - Permite la visualización de la función y la marcación de los puntos `a`, `b` y `c` en cada iteración.
    - Opción de mostrar los pasos iterativos en una tabla detallada.
    - Animación del proceso con ayuda de Manim, generando un video ilustrativo.

- **Método de Newton-Raphson**:
  - **Descripción**: Dado un valor inicial `x0`, utiliza la fórmula del método de Newton-Raphson para encontrar sucesivamente una mejor aproximación de la raíz. Este método requiere el cálculo de la derivada `f'(x)`.
  - **Características**:
    - Cálculo automático de la derivada de `f(x)` con Sympy.
    - Visualización de la función y de las tangentes en cada iteración.
    - Tabla con los pasos (valor actual, valor siguiente, error, etc.).
    - Animación del método para ilustrar el proceso iterativo mediante Manim.

- **Método de Falsa Posición**:
  - **Descripción**: Similar al método de bisección, pero en lugar de tomar el punto medio del intervalo, calcula una aproximación lineal entre `f(a)` y `f(b)` para encontrar un punto `xr` más cercano a la raíz.
  - **Características**:
    - Representación gráfica de las secantes utilizadas en cada iteración.
    - Tabla de resultados con error relativo y valores de `xl`, `xu`, `xr`.
    - Animación con Manim para visualizar el progreso del método a través de las iteraciones.

- **Método de la Secante**:
  - **Descripción**: No requiere el cálculo de la derivada. A partir de dos valores iniciales `x0` y `x1`, traza secantes sucesivas para aproximarse a la raíz.
  - **Características**:
    - Visualización de las secantes entre los puntos elegidos en cada iteración.
    - Tabla de resultados con el error relativo y valores iterativos.
    - Animación para mostrar el proceso de convergencia utilizando Manim.

### Cálculo
- **Cálculo de Derivadas**: Permite calcular la derivada de funciones con una o varias variables.  
  - Derivadas parciales: Posibilidad de elegir la variable respecto a la cual derivar.  
  - Visualización gráfica: Graficación de la función original y su derivada (hasta 3 variables) con el uso de isosuperficies en 3D.
- **Cálculo de Integrales**: Calcula integrales indefinidas y definidas.  
  - Integración de funciones con una, dos o tres variables.  
  - Visualización gráfica en 2D y 3D, con área bajo la curva en el caso de integrales definidas de una variable y superficies para integrales multivariadas.

## Instalación

Para usar la calculadora, sigue estos pasos:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/vexfairyprincess/matrix-calculator.git
   cd matrix-calculator
   ```

2. **Instala las dependencias** (si es necesario):
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta el programa**:
   ```bash
   python main.py
   ```

## Uso

1. Abre la aplicación y selecciona la operación que deseas realizar.
2. Ingresa las dimensiones y los valores de las matrices en las celdas correspondientes.
3. Haz clic en el botón de la operación para ejecutar el cálculo.
4. Usa la opción "Mostrar Solución Paso a Paso" para visualizar los detalles del proceso de cálculo.
5. Para el cálculo de derivadas, si no se especifica variable y hay múltiples variables, se tomará la primera encontrada.
6. Las funciones de integración y derivación incluyen opciones de graficación, siempre que la función sea adecuada (1 a 3 variables).

## Tecnologías Utilizadas

- **Python**: Lenguaje principal de programación.
- **PyQt**: Biblioteca para la construcción de la interfaz gráfica de usuario.
- **SymPy**: Utilizada para la manipulación simbólica y la evaluación de funciones matemáticas.
- **MathJax**: Integrada para la representación de fórmulas matemáticas en formato LaTeX.
- **Plotly**: Usada para la visualización interactiva de datos en 2D y 3D, incluyendo isosuperficies.

## Contribuciones

Si deseas contribuir al proyecto, sigue estos pasos:

1. Realiza un fork del repositorio.
2. Crea una rama nueva para tus cambios (`git checkout -b nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube tus cambios a tu repositorio (`git push origin nueva-funcionalidad`).
5. Abre un Pull Request para que se revisen tus cambios.

## Equipo de Desarrollo

Este proyecto fue desarrollado por:

- **Andrés Miguel Martínez Somarriba**
- **Halley Isela Castro Calero**
- **Samuel Benjamín Chavarria Baltodano**
- **Silvio Alejandro Mora Mendoza**

---

© 2024 CalcX. Todos los derechos reservados.