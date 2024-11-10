import sys
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, 
QHBoxLayout, QTextEdit, QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from sympy import symbols, sympify, latex, lambdify, log, sqrt, sin, cos, tan, sinh, cosh, tanh, pi, E
import re

class VentanaMetodoBiseccion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Bisección - Análisis Numérico")
        self.setGeometry(100, 100, 800, 700)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)
        
        # Campo de entrada para la función
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función en términos de x (por ejemplo: x^2 - 4x + cosh(x) -ln(x))")
        self.input_function.textChanged.connect(self.update_rendered_function)
        self.layout.addWidget(self.input_function)
        
        # Área para renderizar la función ingresada
        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(200)
        self.layout.addWidget(self.rendered_view)
        
        # Contenedor para el teclado matemático
        self.math_keyboard = self.create_math_keyboard()
        self.layout.addLayout(self.math_keyboard)
        
        # Entradas para los parámetros del método de bisección
        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Ingrese el valor de a (inicio del intervalo)")
        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("Ingrese el valor de b (fin del intervalo)")
        self.input_tolerance = QLineEdit()
        self.input_tolerance.setPlaceholderText("Ingrese la tolerancia")
        
        # Añadir las entradas al layout
        self.layout.addWidget(self.input_a)
        self.layout.addWidget(self.input_b)
        self.layout.addWidget(self.input_tolerance)
        
        # Botón para iniciar el cálculo de bisección
        self.start_button = QPushButton("Calcular Raíz")
        self.start_button.clicked.connect(self.run_bisection)
        self.layout.addWidget(self.start_button)
        
        # Botón para copiar LaTeX y abrir Desmos
        self.desmos_button = QPushButton("Copiar LaTeX y Abrir Desmos")
        self.desmos_button.clicked.connect(self.copy_latex_and_open_desmos)
        self.layout.addWidget(self.desmos_button)

        # Botón para regresar al menú de análisis numérico
        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.layout.addWidget(self.back_to_analysis_menu_button)

        #Area de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

    def regresar_menu_analisis_numerico(self):
        from menu import MenuAnalisisNumerico
        self.menu_analisis_numerico = MenuAnalisisNumerico()
        self.menu_analisis_numerico.show()
        self.close()
        
        # Área de resultados
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

        # Cargar MathJax en el QWebEngineView al inicio
        self.load_mathjax()

    def create_math_keyboard(self):
        # Layout principal para el teclado matemático
        keyboard_layout = QVBoxLayout()

        # Primera fila de botones
        row1_layout = QHBoxLayout()
        row1_buttons = [
            ('+', '+'), ('-', '-'), ('×', '*'), ('÷', '/'),
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
        
        if label in ('+', '-', '×', '÷', '^', '(', ')', 'π', 'e'):
            display_text = label
        elif label in ('ln', 'log₁₀', 'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', '√'):
            display_text = f"{label}("
            text += ''
        else:
            display_text = label
        
        if text == '**':
            display_text = "^"
            self.input_function.setText(current_text + '^')
        else:
            self.input_function.setText(current_text + text)
        
        self.input_function.setFocus()

    def load_mathjax(self):
        mathjax_html = """
        <html>
        <head>
            <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
            </script>
        </head>
        <body>
            <div id="math-output" style="font-size: 28px; color: black; padding: 20px;">
                \\( \\text{Ingrese una función para ver la renderización} \\)
            </div>
        </body>
        </html>
        """
        self.rendered_view.setHtml(mathjax_html)

    def update_rendered_function(self):
        func_text = self.input_function.text()
        
        # Reemplazar operadores de potencia y asegurar multiplicación implícita
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
        except:
            self.rendered_view.setHtml("<p style='color:red;'>Función no válida</p>")

    def prepare_expression(self, expr):
        # Insertar `*` automáticamente entre un número y una variable o paréntesis
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        # Reemplazar ^ con ** para poder usarlo en sympify
        expr = expr.replace('^', '**')
        return expr

    def custom_latex_rendering(self, expr):
        # Convertir la expresión a LaTeX
        expr_latex = latex(expr)
        
        # Reemplazar log por ln en LaTeX para mostrar logaritmo natural
        expr_latex = expr_latex.replace(r'\log', r'\ln')
        
        # Mostrar logaritmo en base específica como \log_{base}
        expr_latex = re.sub(r'\\log_([a-zA-Z0-9]+)', r'\\log_{\1}', expr_latex)
        
        return expr_latex

    def run_bisection(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func = lambdify(x, sympify(func_text), 'math')
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            tol = float(self.input_tolerance.text())
            
            result = self.bisection(func, a, b, tol)
            self.result_area.setText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la entrada: {e}")

    def bisection(self, func, a, b, tol):
        steps = ""
        if func(a) * func(b) >= 0:
            return "El intervalo no es válido para el método de bisección."
        
        iter_count = 0
        while (b - a) / 2.0 > tol:
            iter_count += 1
            c = (a + b) / 2.0
            steps += f"Iteración {iter_count}: a = {a}, b = {b}, c = {c}, f(c) = {func(c)}\n"
            
            if abs(func(c)) < tol:
                steps += f"Raíz aproximada encontrada en x = {c}\n"
                return steps
            
            if func(a) * func(c) < 0:
                b = c
            else:
                a = c

        steps += f"Raíz aproximada encontrada en x = {(a + b) / 2.0}\n"
        return steps

    def copy_latex_and_open_desmos(self):
        if hasattr(self, 'latex_expr'):
            dialog = QDialog(self)
            dialog.setWindowTitle("LaTeX de la función")
            dialog_layout = QVBoxLayout(dialog)
            
            latex_box = QTextEdit(self.latex_expr)
            latex_box.setReadOnly(True)
            dialog_layout.addWidget(latex_box)
            
            buttons = QDialogButtonBox(QDialogButtonBox.Ok)
            buttons.accepted.connect(dialog.accept)
            dialog_layout.addWidget(buttons)

            # Mostrar el diálogo y abrir Desmos con la función LaTeX en el portapapeles
            dialog.exec()
            webbrowser.open(f"https://www.desmos.com/calculator")
        else:
            QMessageBox.critical(self, "Error", "Primero ingrese una función válida para copiar su LaTeX.")
            
class VentanaMetodoNewtonRaphson(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Newton-Raphson - Análisis Numérico")
        self.setGeometry(100, 100, 800, 700)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)

        # Etiqueta de título
        self.label_titulo = QLabel("Método de Newton-Raphson", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_titulo)

        # Campo de entrada para la función
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función en términos de x (e.g., x**2 - 4)")
        self.layout.addWidget(QLabel("Función f(x):"))
        self.layout.addWidget(self.input_function)

        # Campo de entrada para el valor inicial x0
        self.input_initial_value = QLineEdit()
        self.input_initial_value.setPlaceholderText("Ingrese el valor inicial x0")
        self.layout.addWidget(QLabel("Valor inicial (x0):"))
        self.layout.addWidget(self.input_initial_value)

        # Área de texto para mostrar resultados
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

        # Botón de cálculo específico para Newton-Raphson
        self.calc_button_newton = QPushButton("Calcular Raíz - Newton-Raphson", self)
        self.layout.addWidget(self.calc_button_newton)

        # Conectar el botón de cálculo al método de Newton-Raphson
        self.calc_button_newton.clicked.connect(self.calcular_raiz_newton_raphson)

    def calcular_raiz_newton_raphson(self):
        try:
            # Obtener la función ingresada y reemplazar ^ por **
            if not self.input_function.text().strip():
                raise ValueError("Por favor, ingrese una función válida.")

            funcion_str = self.input_function.text().replace('^', '**')
            valor_inicial_str = self.input_initial_value.text()
            if not funcion_str or not valor_inicial_str.strip():
                raise ValueError("Por favor, ingrese tanto la función como el valor inicial.")

            # Parseo de la función y derivada
            x = symbols('x')
            try:
                funcion = sympify(funcion_str)
            except (ValueError, SyntaxError):
                raise ValueError("La función ingresada no es válida. Por favor, verifique la sintaxis.")
            derivada = funcion.diff(x)

            # Convertir el valor inicial a float
            x0 = float(valor_inicial_str)

            # Iteración para encontrar la raíz
            tol = 1e-6
            max_iter = 100
            iteracion = 0
            error = float('inf')
            resultado = []

            while error > tol and iteracion < max_iter:
                f_x0 = funcion.evalf(subs={x: x0})
                f_prime_x0 = derivada.evalf(subs={x: x0})

                if f_prime_x0 == 0:
                    raise ZeroDivisionError("La derivada se volvió cero. No se puede continuar.")

                x1 = x0 - float(f_x0) / float(f_prime_x0)
                error = abs(float(x1) - float(x0))
                resultado.append(f"Iteración {iteracion + 1}: x = {float(x1):.6f}, error = {error:.6e}")
                x0 = x1
                iteracion += 1

            if iteracion == max_iter:
                resultado.append("El método no convergió después del número máximo de iteraciones.")
            else:
                resultado.append(f"El método convergió en {iteracion} iteraciones. La raíz es aproximadamente x = {float(x1):.6f}")

            # Mostrar resultados
            self.result_text.setText("\n".join(resultado))

            # Mostrar la función y su derivada en formato LaTeX
            funcion_latex = latex(funcion)
            derivada_latex = latex(derivada)
            html_content = r"""
            <html>
            <head>
            <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
            </head>
            <body>
            <p>f(x): \({funcion_latex}\)</p>
            <p>f'(x): \({derivada_latex}\)</p>
            </body>
            </html>
            """
            self.update_rendered_function()
        
        except ZeroDivisionError as e:
            self.result_text.setText(str(e))
        except Exception as e:
            self.result_text.setText(f"Error: {str(e)}")
