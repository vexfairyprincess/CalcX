# analisisNumerico.py

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                            QTextEdit, QDialog, QDialogButtonBox, QApplication, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from sympy import *
import re
import numpy as np

class VentanaMetodoBase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1400, 800)  # Ventana más alargada
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Layout para los controles (lado izquierdo)
        self.control_layout = QVBoxLayout()
        self.main_layout.addLayout(self.control_layout)

        # Área para la gráfica y la barra de herramientas (lado derecho)
        self.plot_layout = QVBoxLayout()
        self.main_layout.addLayout(self.plot_layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot_layout.addWidget(self.canvas)

        # Barra de herramientas para la gráfica
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plot_layout.addWidget(self.toolbar)

    def regresar_menu_analisis_numerico(self):
        from menu import MenuAnalisisNumerico
        self.menu_analisis_numerico = MenuAnalisisNumerico()
        self.menu_analisis_numerico.show()
        self.close()

    def create_math_keyboard(self):
        keyboard_layout = QVBoxLayout()

        # Primera fila de botones
        row1_layout = QHBoxLayout()
        row1_buttons = [
            ('+', '+'), ('-', '-'), ('x', '*'), ('÷', '/'),
            ('^', '**'), ('√', 'sqrt('), ('ln', 'ln(')
        ]
        for label, value in row1_buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda _, v=value, lbl=label: self.insert_text(v, lbl))
            row1_layout.addWidget(button)
        keyboard_layout.addLayout(row1_layout)

        # Segunda fila de botones
        row2_layout = QHBoxLayout()
        row2_buttons = [
            ('log₁₀', 'log(x, 10)'), ('logₐ', 'log(x, '),
            ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('),
            ('sinh', 'sinh('), ('cosh', 'cosh('), ('tanh', 'tanh(')
        ]
        for label, value in row2_buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda _, v=value, lbl=label: self.insert_text(v, lbl))
            row2_layout.addWidget(button)
        keyboard_layout.addLayout(row2_layout)

        # Tercera fila de botones
        row3_layout = QHBoxLayout()
        row3_buttons = [
            ('arcsin', 'arcsin('), ('arccos', 'arccos('), ('arctan', 'arctan('),
            ('cot', 'cot('), ('sec', 'sec('), ('csc', 'csc('),
            ('(', '('), (')', ')'), ('π', 'pi'), ('e', 'E')
        ]
        for label, value in row3_buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda _, v=value, lbl=label: self.insert_text(v, lbl))
            row3_layout.addWidget(button)
        keyboard_layout.addLayout(row3_layout)

        return keyboard_layout

    def insert_text(self, text, label):
        current_text = self.input_function.text()
        display_text = label if label not in ('+', '-', 'x', '÷', '^', '(', ')', 'π', 'e') else label

        if text == '**':
            display_text = "^"
            self.input_function.setText(current_text + '^')
        else:
            self.input_function.setText(current_text + text)

        self.input_function.setFocus()

    def load_mathjax(self):
        mathjax_html = r"""
        <html>
        <head>
            <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
            </script>
        </head>
        <body>
            <div id="math-output" style="font-size: 28px; color: black; padding: 20px;">
                \\( \    ext{Ingrese una función para ver la renderización} \\)
            </div>
        </body>
        </html>
        """
        self.rendered_view.setHtml(mathjax_html)

    def update_rendered_function(self):
        func_text = self.input_function.text()
        func_text = self.prepare_expression(func_text)

        try:
            expr = sympify(func_text)
            self.latex_expr = self.custom_latex_rendering(expr)
            html_content = f"""
            <html>
            <head>
                <script type="text/javascript" async
                    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
                </script>
            </head>
            <body>
                <div id="math-output" style="font-size: 28px; color: black; padding: 20px;">
                    \\( {self.latex_expr} \\)
                </div>
            </body>
            </html>
            """
            self.rendered_view.setHtml(html_content)
            self.update_plot()
        except:
            self.rendered_view.setHtml("<p style='color:red;'>Función no válida</p>")

    def prepare_expression(self, expr):
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        expr = expr.replace('^', '**')
        return expr

    def custom_latex_rendering(self, expr):
        expr_latex = latex(expr)
        expr_latex = expr_latex.replace(r'\log', r'\ln')
        expr_latex = re.sub(r'\\log_([a-zA-Z0-9]+)', r'\\log_{\1}', expr_latex)
        return expr_latex

    def update_plot(self):
        pass  # Este método será implementado en las clases derivadas

class VentanaMetodoBiseccion(VentanaMetodoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Bisección - Análisis Numérico")
        self.initUI()

    def initUI(self):
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función en términos de x (por ejemplo: x^2 - 4)")
        self.input_function.textChanged.connect(self.update_rendered_function)
        self.control_layout.addWidget(self.input_function)

        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(150)
        self.control_layout.addWidget(self.rendered_view)

        self.control_layout.addLayout(self.create_math_keyboard())

        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Ingrese el valor de a (inicio del intervalo)")
        self.input_a.textChanged.connect(self.update_plot)
        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("Ingrese el valor de b (fin del intervalo)")
        self.input_b.textChanged.connect(self.update_plot)
        self.input_tolerance = QLineEdit()
        self.input_tolerance.setPlaceholderText("Ingrese la tolerancia")

        self.control_layout.addWidget(self.input_a)
        self.control_layout.addWidget(self.input_b)
        self.control_layout.addWidget(self.input_tolerance)

        self.start_button = QPushButton("Calcular Raíz")
        self.start_button.clicked.connect(self.run_bisection)
        self.control_layout.addWidget(self.start_button)

        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.control_layout.addWidget(self.back_to_analysis_menu_button)

        self.result_area = QTextEdit()
        self.control_layout.addWidget(self.result_area)

    def run_bisection(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func_sympy = sympify(func_text)
            func = lambdify(x, func_sympy, 'numpy')
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            tol = float(self.input_tolerance.text())

            result, steps_list = self.bisection(func, a, b, tol)
            self.result_area.setText(result)
            self.plot_function(func_sympy, a, b, steps_list)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la entrada: {e}")

    def bisection(self, func, a, b, tol):
        steps = ""
        steps_list = []
        if func(a) * func(b) >= 0:
            return "El intervalo no es válido para el método de bisección.", steps_list

        iter_count = 0
        while (b - a) / 2.0 > tol:
            iter_count += 1
            c = (a + b) / 2.0
            steps += f"Iteración {iter_count}: a = {a}, b = {b}, c = {c}, f(c) = {func(c)}\n"
            steps_list.append((a, b, c))

            if abs(func(c)) < tol:
                steps += f"Raíz aproximada encontrada en x = {c}\n"
                return steps, steps_list

            if func(a) * func(c) < 0:
                b = c
            else:
                a = c

        c = (a + b) / 2.0
        steps_list.append((a, b, c))
        steps += f"Raíz aproximada encontrada en x = {c}\n"
        return steps, steps_list

    def plot_function(self, func_sympy, a, b, steps_list):
        x = symbols('x')
        func = lambdify(x, func_sympy, 'numpy')
        x_vals = np.linspace(-10, 10, 800)  # Mostrar todos los cuadrantes
        y_vals = func(x_vals)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_vals, y_vals, label='f(x)')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        # Marcar los puntos a, b y c
        for idx, (a_i, b_i, c_i) in enumerate(steps_list):
            ax.plot(a_i, func(a_i), 'ro')
            ax.plot(b_i, func(b_i), 'ro')
            ax.plot(c_i, func(c_i), 'go')
            ax.vlines(c_i, ymin=0, ymax=func(c_i), linestyles='dashed', colors='green')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        self.canvas.draw()

    def update_plot(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func_sympy = sympify(func_text)
            func = lambdify(x, func_sympy, 'numpy')

            x_vals = np.linspace(-10, 10, 800)  # Mostrar todos los cuadrantes
            y_vals = func(x_vals)

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_vals, y_vals, label='f(x)')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)

            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.legend()
            self.canvas.draw()
        except Exception:
            pass

class VentanaMetodoNewtonRaphson(VentanaMetodoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Newton-Raphson - Análisis Numérico")
        self.initUI()

    def initUI(self):
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función en términos de x (por ejemplo: x^2 - 4)")
        self.input_function.textChanged.connect(self.update_rendered_function)
        self.control_layout.addWidget(self.input_function)

        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(150)
        self.control_layout.addWidget(self.rendered_view)

        self.control_layout.addLayout(self.create_math_keyboard())

        self.input_initial_value = QLineEdit()
        self.input_initial_value.setPlaceholderText("Ingrese el valor inicial (x0)")
        self.input_initial_value.textChanged.connect(self.update_plot)
        self.control_layout.addWidget(QLabel("Valor inicial (x0):"))
        self.control_layout.addWidget(self.input_initial_value)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.control_layout.addWidget(self.result_area)

        self.start_button = QPushButton("Calcular Raíz - Newton-Raphson")
        self.start_button.clicked.connect(self.run_newton_raphson)
        self.control_layout.addWidget(self.start_button)

        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.control_layout.addWidget(self.back_to_analysis_menu_button)

    def update_rendered_function(self):
        func_text = self.input_function.text()
        func_text = self.prepare_expression(func_text)

        try:
            x = symbols('x')
            expr = sympify(func_text)
            derivative = expr.diff(x)  # Calcula la derivada de la función

            # Renderizar en LaTeX
            self.latex_expr = self.custom_latex_rendering(expr)
            self.latex_derivative = self.custom_latex_rendering(derivative)

            html_content = f"""
            <html>
            <head>
                <script type="text/javascript" async
                    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
                </script>
            </head>
            <body>
                <div id="math-output" style="font-size: 28px; color: black; padding: 20px;">
                    <p>\\( f(x) = {self.latex_expr} \\)</p>
                    <p>\\( f'(x) = {self.latex_derivative} \\)</p>
                </div>
            </body>
            </html>
            """
            self.rendered_view.setHtml(html_content)
            self.update_plot()
        except:
            self.rendered_view.setHtml("<p style='color:red;'>Función no válida</p>")

    def run_newton_raphson(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func_expr = sympify(func_text)
            derivative_expr = func_expr.diff(x)
            func = lambdify(x, func_expr, 'numpy')
            derivative = lambdify(x, derivative_expr, 'numpy')
            x0 = float(self.input_initial_value.text())

            tol = 1e-6
            max_iter = 100
            iter_count = 0
            error = float('inf')
            results = []
            x_values = [x0]

            while error > tol and iter_count < max_iter:
                f_x0 = func(x0)
                f_prime_x0 = derivative(x0)

                if f_prime_x0 == 0:
                    raise ZeroDivisionError("La derivada es cero. No se puede continuar con el método.")

                x1 = x0 - f_x0 / f_prime_x0
                error = abs(x1 - x0)
                results.append(f"Iteración {iter_count + 1}: x = {x1}, error = {error}")
                x0 = x1
                x_values.append(x0)
                iter_count += 1

            if iter_count == max_iter:
                results.append("El método no convergió después del número máximo de iteraciones.")
            else:
                results.append(f"El método convergió en {iter_count} iteraciones. La raíz es aproximadamente x = {x1:.6f}")

            self.result_area.setText("\n".join(results))
            self.plot_function(func_expr, x_values)
        except ZeroDivisionError as e:
            self.result_area.setText(f"Error: {e}")
        except Exception as e:
            self.result_area.setText(f"Error en la entrada: {e}")

    def plot_function(self, func_expr, x_values):
        x = symbols('x')
        func = lambdify(x, func_expr, 'numpy')

        x_vals = np.linspace(-10, 10, 800)  # Mostrar todos los cuadrantes
        y_vals = func(x_vals)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_vals, y_vals, label='f(x)')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        # Dibujar las tangentes en cada iteración
        for xi in x_values[:-1]:
            f_xi = func(xi)
            derivative = diff(func_expr, x).subs(x, xi)
            tangent_line = derivative * (x_vals - xi) + f_xi
            ax.plot(x_vals, tangent_line, '--', label=f'Tangente en x={xi:.2f}')

        # Marcar los puntos x_i
        for xi in x_values:
            ax.plot(xi, func(xi), 'ro')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        self.canvas.draw()

    def update_plot(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func_expr = sympify(func_text)
            func = lambdify(x, func_expr, 'numpy')

            x_vals = np.linspace(-10, 10, 800)  # Mostrar todos los cuadrantes
            y_vals = func(x_vals)

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_vals, y_vals, label='f(x)')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)

            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.legend()
            self.canvas.draw()
        except Exception:
            pass

class VentanaMetodoFalsaPosicion(VentanaMetodoBase):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle("Método de Falsa Posición")

        # Configurar el campo de entrada de la función
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función en términos de x (por ejemplo: x^2 - 4)")
        self.input_function.textChanged.connect(self.update_rendered_function)
        self.control_layout.addWidget(self.input_function)

        # Configurar el visor de la función renderizada
        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(150)
        self.control_layout.addWidget(self.rendered_view)

        # Agregar el teclado matemático
        self.control_layout.addLayout(self.create_math_keyboard())

        # Crear campos para el intervalo, tolerancia y número máximo de iteraciones
        self.xl_input = QLineEdit()
        self.xl_input.setPlaceholderText("Ingrese el valor de xl (intervalo inferior)")
        self.xl_input.textChanged.connect(self.update_plot)
        self.control_layout.addWidget(self.xl_input)

        self.xu_input = QLineEdit()
        self.xu_input.setPlaceholderText("Ingrese el valor de xu (intervalo superior)")
        self.xu_input.textChanged.connect(self.update_plot)
        self.control_layout.addWidget(self.xu_input)

        self.tol_input = QLineEdit()
        self.tol_input.setPlaceholderText("Ingrese la tolerancia")
        self.control_layout.addWidget(self.tol_input)

        self.iter_input = QLineEdit()
        self.iter_input.setPlaceholderText("Ingrese el número máximo de iteraciones")
        self.control_layout.addWidget(self.iter_input)

        # Botón para ejecutar el cálculo
        self.calc_button = QPushButton("Calcular Raíz")
        self.calc_button.clicked.connect(self.ejecutar_falsa_posicion)
        self.control_layout.addWidget(self.calc_button)

        # Botón para regresar al menú de análisis numérico
        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.control_layout.addWidget(self.back_to_analysis_menu_button)

        # Área de texto para mostrar resultados
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.control_layout.addWidget(self.result_display)

        # Ajusta el tamaño de la ventana
        self.resize(400, 500)

    def ejecutar_falsa_posicion(self):
        try:
            # Obtiene los valores de entrada de la interfaz
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func_expr = sympify(func_text)
            funcion = lambdify(x, func_expr, 'numpy')
            xl = float(self.xl_input.text())
            xu = float(self.xu_input.text())
            tolerancia = float(self.tol_input.text())
            iter_max = int(self.iter_input.text())

            # Valida que xl y xu encierren una raíz
            if funcion(xl) * funcion(xu) >= 0:
                raise ValueError("El intervalo [xl, xu] no encierra una raíz.")

            # Ejecuta el cálculo del método de Falsa Posición
            self.resultado, self.error, self.iteraciones, self.steps_list = self.calcular_raiz(funcion, xl, xu, tolerancia, iter_max)
            self.mostrar_resultados()
            self.plot_function(func_expr, xl, xu, self.steps_list)
        except Exception as e:
            self.result_display.setText(f"Error: {str(e)}")

    def calcular_raiz(self, funcion, xl, xu, tolerancia, iter_max):
        iteraciones = 0
        xr = xl  # Valor inicial de xr
        error_aprox = float('inf')  # Error inicial alto
        steps_list = []

        # Iteración del método de Falsa Posición
        while error_aprox > tolerancia and iteraciones < iter_max:
            xr_prev = xr
            # Cálculo de xr usando la fórmula de Falsa Posición
            xr = xu - (funcion(xu) * (xl - xu)) / (funcion(xl) - funcion(xu))

            # Guardar los valores para graficar
            steps_list.append((xl, xu, xr))

            # Actualización del intervalo
            if funcion(xl) * funcion(xr) < 0:
                xu = xr
            elif funcion(xu) * funcion(xr) < 0:
                xl = xr
            else:
                break  # Si f(xr) es aproximadamente cero, encontramos la raíz

            # Cálculo del error relativo
            if xr != 0:
                error_aprox = abs((xr - xr_prev) / xr) * 100
            iteraciones += 1

        return xr, error_aprox, iteraciones, steps_list

    def mostrar_resultados(self):
        # Muestra los resultados en el área de resultados de la UI
        self.result_display.setText(f"Raíz aproximada: {self.resultado}\n"
                                    f"Error aproximado: {self.error}%\n"
                                    f"Iteraciones: {self.iteraciones}")

    def plot_function(self, func_expr, xl, xu, steps_list):
        x = symbols('x')
        funcion = lambdify(x, func_expr, 'numpy')
        x_vals = np.linspace(-10, 10, 800)  # Mostrar todos los cuadrantes
        y_vals = funcion(x_vals)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_vals, y_vals, label='f(x)')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        # Dibujar líneas de falsa posición
        for idx, (xl_i, xu_i, xr_i) in enumerate(steps_list):
            f_xl = funcion(xl_i)
            f_xu = funcion(xu_i)
            ax.plot([xl_i, xu_i], [f_xl, f_xu], 'r--')
            ax.plot(xr_i, funcion(xr_i), 'go')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        self.canvas.draw()

    def update_plot(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func_expr = sympify(func_text)
            funcion = lambdify(x, func_expr, 'numpy')

            x_vals = np.linspace(-10, 10, 800)  # Mostrar todos los cuadrantes
            y_vals = funcion(x_vals)

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_vals, y_vals, label='f(x)')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)

            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.legend()
            self.canvas.draw()
        except Exception:
            pass

class VentanaMetodoSecante(VentanaMetodoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de la Secante - Análisis Numérico")
        self.initUI()

    def initUI(self):
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función en términos de x (por ejemplo: x^2 - 4)")
        self.input_function.textChanged.connect(self.update_rendered_function)
        self.control_layout.addWidget(self.input_function)

        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(150)
        self.control_layout.addWidget(self.rendered_view)

        self.control_layout.addLayout(self.create_math_keyboard())

        self.input_x0 = QLineEdit()
        self.input_x0.setPlaceholderText("Ingrese el valor inicial x0:")
        self.input_x0.textChanged.connect(self.update_plot)
        self.control_layout.addWidget(QLabel("Valor inicial (x0):"))
        self.control_layout.addWidget(self.input_x0)

        self.input_x1 = QLineEdit()
        self.input_x1.setPlaceholderText("Ingrese el valor inicial x1:")
        self.input_x1.textChanged.connect(self.update_plot)
        self.control_layout.addWidget(QLabel("Valor inicial (x1):"))
        self.control_layout.addWidget(self.input_x1)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.control_layout.addWidget(self.result_area)

        self.start_button = QPushButton("Calcular Raíz - Secante")
        self.start_button.clicked.connect(self.run_secant)
        self.control_layout.addWidget(self.start_button)

        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.control_layout.addWidget(self.back_to_analysis_menu_button)

    def run_secant(self):
        try:
            x = symbols('x')
            func_text = self.prepare_expression(self.input_function.text())
            func_expr = sympify(func_text)
            funcion = lambdify(x, func_expr, 'numpy')
            x0 = float(self.input_x0.text())
            x1 = float(self.input_x1.text())

            tol = 1e-5
            max_iter = 100
            x_values = [x0, x1]
            results = []
            for i in range(max_iter):
                fx0 = funcion(x0)
                fx1 = funcion(x1)

                if fx1 - fx0 == 0:
                    raise ZeroDivisionError("División por cero en la fórmula de la secante.")

                # Fórmula de la secante
                x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

                # Verificar convergencia
                if abs(x2 - x1) < tol:
                    results.append(f"Raíz aproximada: {x2:.5f}")
                    self.result_area.setText("\n".join(results))
                    x_values.append(x2)
                    self.plot_function(func_expr, x_values)
                    return

                x0, x1 = x1, x2
                x_values.append(x1)
                results.append(f"Iteración {i + 1}: x = {x1}, f(x) = {funcion(x1)}")

            results.append("No converge en el número máximo de iteraciones")
            self.result_area.setText("\n".join(results))
            self.plot_function(func_expr, x_values)
        except Exception as e:
            self.result_area.setText(f"Error: {e}")

    def plot_function(self, func_expr, x_values):
        x = symbols('x')
        funcion = lambdify(x, func_expr, 'numpy')
        x_vals = np.linspace(-10, 10, 800)  # Mostrar todos los cuadrantes
        y_vals = funcion(x_vals)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_vals, y_vals, label='f(x)')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        # Dibujar líneas secantes
        for i in range(len(x_values) - 2):
            x0, x1 = x_values[i], x_values[i + 1]
            fx0, fx1 = funcion(x0), funcion(x1)
            ax.plot([x0, x1], [fx0, fx1], 'r--', label=f'Secante {i + 1}' if i == 0 else "")

        # Marcar los puntos x_i
        for xi in x_values:
            ax.plot(xi, funcion(xi), 'ro')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        self.canvas.draw()

    def update_plot(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func_expr = sympify(func_text)
            funcion = lambdify(x, func_expr, 'numpy')

            x_vals = np.linspace(-10, 10, 800)  # Mostrar todos los cuadrantes
            y_vals = funcion(x_vals)

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_vals, y_vals, label='f(x)')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)

            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.legend()
            self.canvas.draw()
        except Exception:
            pass