from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
import webbrowser
from sympy import *
import re

class VentanaMetodoBase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 700)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

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
        display_text = label if label not in ('+', '-', '×', '÷', '^', '(', ')', 'π', 'e') else label
        
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
                \\( \	ext{Ingrese una función para ver la renderización} \\)
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

            dialog.exec()
            webbrowser.open(f"https://www.desmos.com/calculator")
        else:
            QMessageBox.critical(self, "Error", "Primero ingrese una función válida para copiar su LaTeX.")
            
class VentanaMetodoBiseccion(VentanaMetodoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Bisección - Análisis Numérico")
        self.initUI()

    def initUI(self):
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función en términos de x (por ejemplo: x^2 - 4)")
        self.input_function.textChanged.connect(self.update_rendered_function)
        self.layout.addWidget(self.input_function)

        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(200)
        self.layout.addWidget(self.rendered_view)
        
        self.layout.addLayout(self.create_math_keyboard())
        
        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Ingrese el valor de a (inicio del intervalo)")
        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("Ingrese el valor de b (fin del intervalo)")
        self.input_tolerance = QLineEdit()
        self.input_tolerance.setPlaceholderText("Ingrese la tolerancia")

        self.layout.addWidget(self.input_a)
        self.layout.addWidget(self.input_b)
        self.layout.addWidget(self.input_tolerance)

        self.start_button = QPushButton("Calcular Raíz")
        self.start_button.clicked.connect(self.run_bisection)
        self.layout.addWidget(self.start_button)

        self.desmos_button = QPushButton("Copiar LaTeX y Abrir Desmos")
        self.desmos_button.clicked.connect(self.copy_latex_and_open_desmos)
        self.layout.addWidget(self.desmos_button)

        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.layout.addWidget(self.back_to_analysis_menu_button)

        self.result_area = QTextEdit
        
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

class VentanaMetodoNewtonRaphson(VentanaMetodoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Newton-Raphson - Análisis Numérico")
        self.initUI()

    def initUI(self):
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función en términos de x (por ejemplo: x^2 - 4)")
        self.input_function.textChanged.connect(self.update_rendered_function)
        self.layout.addWidget(QLabel("Función f(x):"))
        self.layout.addWidget(self.input_function)

        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(200)
        self.layout.addWidget(self.rendered_view)
        
        self.layout.addLayout(self.create_math_keyboard())

        self.input_initial_value = QLineEdit()
        self.input_initial_value.setPlaceholderText("Ingrese el valor inicial (x0)")
        self.layout.addWidget(QLabel("Valor inicial (x0):"))
        self.layout.addWidget(self.input_initial_value)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

        self.start_button = QPushButton("Calcular Raíz - Newton-Raphson")
        self.start_button.clicked.connect(self.run_newton_raphson)
        self.layout.addWidget(self.start_button)

        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.layout.addWidget(self.back_to_analysis_menu_button)

    def run_newton_raphson(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            func = sympify(func_text)
            derivative = func.diff(x)
            x0 = float(self.input_initial_value.text())
            
            tol = 1e-6
            max_iter = 100
            iter_count = 0
            error = float('inf')
            results = []

            while error > tol and iter_count < max_iter:
                f_x0 = func.evalf(subs={x: x0})
                f_prime_x0 = derivative.evalf(subs={x: x0})

                if f_prime_x0 == 0:
                    raise ZeroDivisionError("La derivada es cero. No se puede continuar con el método.")

                x1 = x0 - f_x0 / f_prime_x0
                error = abs(x1 - x0)
                results.append(f"Iteración {iter_count + 1}: x = {x1:.6f}, error = {error:.6e}")
                x0 = x1
                iter_count += 1

            if iter_count == max_iter:
                results.append("El método no convergió después del número máximo de iteraciones.")
            else:
                results.append(f"El método convergió en {iter_count} iteraciones. La raíz es aproximadamente x = {x1:.6f}")

            self.result_area.setText("\n".join(results))
        except ZeroDivisionError as e:
            self.result_area.setText(f"Error: {e}")
        except Exception as e:
            self.result_area.setText(f"Error en la entrada: {e}")
