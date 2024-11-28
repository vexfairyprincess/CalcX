import sys
import os
import re
import numpy as np
from sympy import symbols, sympify, lambdify, latex, integrate
from sympy.core.sympify import SympifyError
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTextEdit, QDialog, QApplication, QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QClipboard
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class VentanaCalculoBase(QMainWindow):
    def __init__(self, tamano_fuente):
        super().__init__()
        self.tamano_fuente = tamano_fuente
        self.setGeometry(100, 100, 1400, 800)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.actualizar_fuente_local(self.tamano_fuente)

        self.control_layout = QVBoxLayout()
        self.main_layout.addLayout(self.control_layout)

        self.plot_layout = QVBoxLayout()
        self.main_layout.addLayout(self.plot_layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot_layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plot_layout.addWidget(self.toolbar)
        self.showMaximized()

    def create_math_keyboard(self):
        keyboard_layout = QVBoxLayout()
        button_layouts = [QHBoxLayout() for _ in range(3)]
        button_configs = [
            [('+', '+'), ('-', '-'), ('x', '*'), ('÷', '/'), ('xˣ', '**'), ('√', 'sqrt('), ('ln', 'ln(')],
            [('log₁₀', 'log(10, x)'), ('logₐ', 'log('), ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('), ('sinh', 'sinh('), ('cosh', 'cosh('), ('tanh', 'tanh(')],
            [('arcsin', 'asin('), ('arccos', 'acos('), ('arctan', 'atan('), ('cot', 'cot('), ('sec', 'sec('), ('csc', 'csc('), ('(', '('), (')', ')'), ('π', 'pi'), ('e', 'E')]
        ]
        for layout, buttons in zip(button_layouts, button_configs):
            for label, value in buttons:
                button = QPushButton(label)
                button.clicked.connect(lambda _, v=value, lbl=label: self.insert_text(v, lbl))
                layout.addWidget(button)
            keyboard_layout.addLayout(layout)
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

    def actualizar_fuente_local(self, tamano):
        self.setStyleSheet(f"""
            QPushButton {{
                font-size: {tamano}px;
                padding: 10px;
            }}
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
        """)

    def prepare_expression(self, expr):
        expr = expr.replace('^', '**').replace('√', 'sqrt').replace('π', 'pi').replace('÷', '/')
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        return expr

    def custom_latex_rendering(self, expr):
        expr_latex = latex(expr)
        expr_latex = expr_latex.replace(r'\log', r'\ln').replace(r'\\log_([a-zA-Z0-9]+)', r'\\log_{\1}')
        return expr_latex

class VentanaCalculadoraIntegrales(VentanaCalculoBase):
    def __init__(self, tamano_fuente):
        super().__init__(tamano_fuente)
        self.setWindowTitle("Calculadora de Integrales")
        self.initUI()

    def initUI(self):
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función a integrar en términos de x")
        self.control_layout.addWidget(self.input_function)

        self.input_function.textChanged.connect(self.update_rendered_function)
        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(150)
        self.control_layout.addWidget(self.rendered_view)

        self.control_layout.addLayout(self.create_math_keyboard())

        self.lower_limit_input = QLineEdit()
        self.lower_limit_input.setPlaceholderText("Límite inferior (opcional)")
        self.control_layout.addWidget(self.lower_limit_input)

        self.upper_limit_input = QLineEdit()
        self.upper_limit_input.setPlaceholderText("Límite superior (opcional)")
        self.control_layout.addWidget(self.upper_limit_input)

        self.calculate_button = QPushButton("Calcular Integral")
        self.calculate_button.clicked.connect(self.calculate_integral)
        self.control_layout.addWidget(self.calculate_button)

        # Reemplazar QTextEdit por QWebEngineView para renderizar resultados con MathJax
        self.result_view = QWebEngineView(self)
        self.result_view.setFixedHeight(200)
        self.control_layout.addWidget(self.result_view)

    def update_rendered_function(self):
        func_text = self.input_function.text()
        func_text_prepared = self.prepare_expression(func_text)

        try:
            x = symbols('x')
            expr = sympify(func_text_prepared)
            self.func_expr = expr

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
                    \\( f(x) = {self.latex_expr} \\)
                </div>
            </body>
            </html>
            """
            self.rendered_view.setHtml(html_content)
        except Exception as e:
            self.rendered_view.setHtml("<p style='color:red;'>Función no válida</p>")

    def calculate_integral(self):
        func_text = self.input_function.text()
        func_text_prepared = self.prepare_expression(func_text)

        lower_limit_text = self.lower_limit_input.text()
        upper_limit_text = self.upper_limit_input.text()

        try:
            x = symbols('x')
            expr = sympify(func_text_prepared)
            self.func_expr = expr

            # Si se especificaron límites, calcular la integral definida
            if lower_limit_text and upper_limit_text:
                lower_limit = sympify(lower_limit_text)
                upper_limit = sympify(upper_limit_text)
                result = integrate(expr, (x, lower_limit, upper_limit))  # integral definida
                result_numeric = result.evalf()  # Valor numérico de la integral

                latex_result = self.custom_latex_rendering(result)  # Renderizado en LaTeX

                # Renderizar la integral y el valor numérico
                html_content = f"""
                <html>
                <head>
                    <script type="text/javascript" async
                        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
                    </script>
                </head>
                <body>
                    <div style="font-size: 24px; color: black; padding: 20px;">
                        \\( \\int_{{{latex(lower_limit)}}}^{{{latex(upper_limit)}}} {self.latex_expr} \\, dx = {latex_result} \\)
                    </div>
                    <div style="font-size: 20px; color: grey; margin-top: 10px;">
                        \\( \\text{{Valor aproximado: }} {result_numeric} \\)
                    </div>
                </body>
                </html>
                """
            else:
                # Si no se especificaron límites, calcular la integral indefinida
                result = integrate(expr, x)  # integral indefinida
                latex_result = self.custom_latex_rendering(result)  # Renderizado en LaTeX

                # Renderizar la integral y añadir la constante de integración (C)
                html_content = f"""
                <html>
                <head>
                    <script type="text/javascript" async
                        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
                    </script>
                </head>
                <body>
                    <div style="font-size: 24px; color: black; padding: 20px;">
                        \\( \\int {self.latex_expr} \\, dx = {latex_result} + C \\)
                    </div>
                </body>
                </html>
                """
            # Mostrar el resultado de la integral en el QWebEngineView
            self.result_view.setHtml(html_content)

            self.plot_integral(expr)

        except SympifyError as e:
            error_html = f"<p style='color:red;'>Error al interpretar la función: {e}</p>"
            self.result_view.setHtml(error_html)
        except Exception as e:
            error_html = f"<p style='color:red;'>Error al calcular la integral: {e}</p>"
            self.result_view.setHtml(error_html)

    def plot_integral(self, expr):
         self.figure.clear()
         ax = self.figure.add_subplot(111)
         x_vals = np.linspace(-10, 10, 400)
         f = lambdify(symbols('x'), expr, modules=['numpy'])
         try:
             y_vals = f(x_vals)
             ax.plot(x_vals, y_vals, label='f(x)')
             ax.legend()
             self.canvas.draw()
         except Exception as e:
             QMessageBox.warning(self, "Error de Graficación", f"No se pudo graficar la función: {e}")

