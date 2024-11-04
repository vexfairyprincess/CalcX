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

        # Primer fila de botones
        row1_layout = QHBoxLayout()
        row1_buttons = [
            ('+', '+'), ('-', '-'), ('×', '*'), ('÷', '/'),
            ('^', '**'), ('√', 'sqrt('), ('ln', 'ln('), ('log₁₀', 'log(x, 10)'),
            ('logₐ', 'log(x, '), ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan(')
        ]
        for label, value in row1_buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda _, v=value, lbl=label: self.insert_text(v, lbl))
            row1_layout.addWidget(button)
        keyboard_layout.addLayout(row1_layout)

        # Segunda fila de botones
        row2_layout = QHBoxLayout()
        row2_buttons = [
            ('sinh', 'sinh('), ('cosh', 'cosh('), ('tanh', 'tanh('),
            ('(', '('), (')', ')'), ('π', 'pi'), ('e', 'E')
        ]
        for label, value in row2_buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda _, v=value, lbl=label: self.insert_text(v, lbl))
            row2_layout.addWidget(button)
        keyboard_layout.addLayout(row2_layout)

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