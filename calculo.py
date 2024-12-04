# calculo.py

import sys
import os
import re
import numpy as np
from sympy import symbols, sympify, lambdify, latex, integrate, diff
from sympy.core.sympify import SympifyError
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTextEdit, QDialog, QApplication, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QClipboard

from custom_modules import custom_math

# Importar Plotly
import plotly.graph_objects as go
from plotly.offline import plot


class PlotlyViewer(QWebEngineView):
    def __init__(self, figure, parent=None):
        super(PlotlyViewer, self).__init__(parent)
        self.figure = figure
        self.init_ui()

    def init_ui(self):
        html = plot(self.figure, output_type='div', include_plotlyjs='cdn', auto_open=False)
        self.setHtml(html)
        self.show()


class VentanaCalculoBase(QMainWindow):
    def __init__(self, tamano_fuente):
        super().__init__()
        self.tamano_fuente = tamano_fuente
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.actualizar_fuente_local(self.tamano_fuente)

        self.control_layout = QVBoxLayout()
        self.main_layout.addLayout(self.control_layout)

        self.show()

    def create_math_keyboard(self):
        keyboard_layout = QVBoxLayout()

        # Primera fila de botones
        row1_layout = QHBoxLayout()
        row1_buttons = [
            ('+', '+'), ('-', '-'), ('x', '*'), ('÷', '/'),
            ('xˣ', '**'), ('√', 'sqrt('), ('ln', 'log(')
        ]
        for label, value in row1_buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda _, v=value: self.insert_text(v))
            row1_layout.addWidget(button)
        keyboard_layout.addLayout(row1_layout)

        # Segunda fila de botones
        row2_layout = QHBoxLayout()
        row2_buttons = [
            ('log₁₀', 'log10('), ('logₐ', 'log('),
            ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('),
            ('sinh', 'sinh('), ('cosh', 'cosh('), ('tanh', 'tanh(')
        ]
        for label, value in row2_buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda _, v=value: self.insert_text(v))
            row2_layout.addWidget(button)
        keyboard_layout.addLayout(row2_layout)

        # Tercera fila de botones
        row3_layout = QHBoxLayout()
        row3_buttons = [
            ('arcsin', 'asin('), ('arccos', 'acos('), ('arctan', 'atan('),
            ('cot', 'cot('), ('sec', 'sec('), ('csc', 'csc('),
            ('(', '('), (')', ')'), ('π', 'pi'), ('e', 'E')
        ]
        for label, value in row3_buttons:
            button = QPushButton(label)
            button.clicked.connect(lambda _, v=value: self.insert_text(v))
            row3_layout.addWidget(button)
        keyboard_layout.addLayout(row3_layout)

        return keyboard_layout

    def insert_text(self, text):
        current_text = self.input_function.text()
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
        expr = expr.replace('ln(', 'log(')
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        return expr

    def custom_latex_rendering(self, expr):
        expr_latex = latex(expr)
        expr_latex = expr_latex.replace(r'\log', r'\ln')
        return expr_latex

    def regresar_menu_calculo(self):
        from menu import MenuCalculo
        self.menu_calculo = MenuCalculo()
        self.menu_calculo.show()
        self.close()


class VentanaCalculadoraIntegrales(VentanaCalculoBase):
    def __init__(self, tamano_fuente):
        super().__init__(tamano_fuente)
        self.setWindowTitle("Calculadora de Integrales")
        self.initUI()

    def initUI(self):
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese la función a integrar")
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

        self.plot_button = QPushButton("Graficar Función")
        self.plot_button.clicked.connect(self.plot_function)
        self.plot_button.setEnabled(False)
        self.control_layout.addWidget(self.plot_button)

        self.result_view = QWebEngineView(self)
        self.result_view.setFixedHeight(200)
        self.control_layout.addWidget(self.result_view)

        self.back_to_calculo_menu_button = QPushButton("Regresar al Menú de Cálculo")
        self.back_to_calculo_menu_button.clicked.connect(self.regresar_menu_calculo)
        self.control_layout.addWidget(self.back_to_calculo_menu_button)

    def update_rendered_function(self):
        func_text = self.input_function.text()
        func_text_prepared = self.prepare_expression(func_text)

        try:
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
                    \\( f = {self.latex_expr} \\)
                </div>
            </body>
            </html>
            """
            self.rendered_view.setHtml(html_content)

            # Verificar si el número de variables es adecuado para graficar
            variables = expr.free_symbols
            num_vars = len(variables)
            if num_vars in [1, 2, 3]:
                self.plot_button.setEnabled(True)
            else:
                self.plot_button.setEnabled(False)

        except Exception as e:
            self.rendered_view.setHtml("<p style='color:red;'>Función no válida</p>")
            self.plot_button.setEnabled(False)

    def calculate_integral(self):
        func_text = self.input_function.text()
        func_text_prepared = self.prepare_expression(func_text)

        lower_limit_text = self.lower_limit_input.text()
        upper_limit_text = self.upper_limit_input.text()

        try:
            expr = sympify(func_text_prepared)
            self.func_expr = expr
            variables = expr.free_symbols

            if not variables:
                QMessageBox.warning(self, "Variables no encontradas", "No se encontraron variables en la función.")
                self.plot_button.setEnabled(False)
                return

            if len(variables) >= 1:
                var = sorted(variables, key=lambda x: str(x))[0]
                QMessageBox.information(self, "Variable seleccionada", f"Se utilizará la variable '{var}' para integrar.")

            if lower_limit_text and upper_limit_text:
                lower_limit = sympify(lower_limit_text)
                upper_limit = sympify(upper_limit_text)
                result = integrate(expr, (var, lower_limit, upper_limit))
                result_numeric = result.evalf()

                latex_result = self.custom_latex_rendering(result)

                html_content = f"""
                <html>
                <head>
                    <script type="text/javascript" async
                        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
                    </script>
                </head>
                <body>
                    <div style="font-size: 24px; color: black; padding: 20px;">
                        \\( \\int_{{{latex(lower_limit)}}}^{{{latex(upper_limit)}}} {self.latex_expr} \\, d{var} = {latex_result} \\)
                    </div>
                    <div style="font-size: 20px; color: grey; margin-top: 10px;">
                        \\( \\text{{Valor aproximado: }} {result_numeric} \\)
                    </div>
                </body>
                </html>
                """
            else:
                result = integrate(expr, var)
                latex_result = self.custom_latex_rendering(result)

                html_content = f"""
                <html>
                <head>
                    <script type="text/javascript" async
                        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
                    </script>
                </head>
                <body>
                    <div style="font-size: 24px; color: black; padding: 20px;">
                        \\( \\int {self.latex_expr} \\, d{var} = {latex_result} + C \\)
                    </div>
                </body>
                </html>
                """
            self.result_view.setHtml(html_content)

        except SympifyError as e:
            error_html = f"<p style='color:red;'>Error al interpretar la función: {e}</p>"
            self.result_view.setHtml(error_html)
            self.plot_button.setEnabled(False)
        except Exception as e:
            error_html = f"<p style='color:red;'>Error al calcular la integral: {e}</p>"
            self.result_view.setHtml(error_html)
            self.plot_button.setEnabled(False)

    def plot_function(self):
        func_text = self.input_function.text()
        func_text_prepared = self.prepare_expression(func_text)
        try:
            expr = sympify(func_text_prepared)
            variables = expr.free_symbols
            num_vars = len(variables)
            vars_sorted = sorted(variables, key=lambda x: str(x))

            if num_vars == 1:
                # Gráfica 2D
                var = vars_sorted[0]
                f = lambdify(var, expr, modules=['numpy', custom_math])

                x_vals = np.linspace(-10, 10, 400)
                y_vals = f(x_vals)

                fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='lines', name='f(x)'))
                fig.update_layout(title='Gráfica de f(x)', xaxis_title=str(var), yaxis_title='f({})'.format(var))

            elif num_vars == 2:
                # Gráfica 3D de superficie
                var_x = vars_sorted[0]
                var_y = vars_sorted[1]
                f = lambdify((var_x, var_y), expr, modules=['numpy', custom_math])

                x_vals = np.linspace(-5, 5, 50)
                y_vals = np.linspace(-5, 5, 50)
                X, Y = np.meshgrid(x_vals, y_vals)
                Z = f(X, Y)

                # Manejar valores NaN o infinitos
                Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)

                fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
                fig.update_layout(title='Gráfica 3D de la función', autosize=True,
                                  scene=dict(
                                      xaxis_title=str(var_x),
                                      yaxis_title=str(var_y),
                                      zaxis_title='f({},{})'.format(var_x, var_y),
                                  ))

            elif num_vars == 3:
                # Gráfica 3D de isosuperficie
                var_x = vars_sorted[0]
                var_y = vars_sorted[1]
                var_z = vars_sorted[2]
                f = lambdify((var_x, var_y, var_z), expr, modules=['numpy', custom_math])

                x_vals = np.linspace(-5, 5, 20)
                y_vals = np.linspace(-5, 5, 20)
                z_vals = np.linspace(-5, 5, 20)
                X, Y, Z = np.meshgrid(x_vals, y_vals, z_vals)
                F = f(X, Y, Z)

                # Manejar valores NaN o infinitos
                F = np.nan_to_num(F, nan=np.nan, posinf=np.nan, neginf=np.nan)

                fig = go.Figure(data=go.Isosurface(
                    x=X.flatten(),
                    y=Y.flatten(),
                    z=Z.flatten(),
                    value=F.flatten(),
                    isomin=np.nanmin(F),
                    isomax=np.nanmax(F),
                    surface_count=3,
                    colorscale='Plasma',  # Asignar escala de colores
                    caps=dict(x_show=False, y_show=False, z_show=False),
                ))

                fig.update_layout(title='Gráfica 3D de la función', autosize=True,
                                  scene=dict(
                                      xaxis_title=str(var_x),
                                      yaxis_title=str(var_y),
                                      zaxis_title=str(var_z),
                                  ))

            else:
                QMessageBox.warning(self, "Variables incorrectas",
                                    "La función debe tener exactamente 1, 2 o 3 variables para graficar.")
                return

            # Mostrar la gráfica en el QWebEngineView
            viewer = PlotlyViewer(fig)
            self.plot_window = QDialog(self)
            self.plot_window.setWindowTitle("Gráfica de la Función")
            layout = QVBoxLayout()
            self.plot_window.setLayout(layout)
            layout.addWidget(viewer)
            self.plot_window.resize(800, 600)
            self.plot_window.exec_()

        except Exception as e:
            QMessageBox.warning(self, "Error al graficar", f"No se pudo graficar la función: {e}")


class VentanaCalculadoraDerivadas(VentanaCalculoBase):
    def __init__(self, tamano_fuente):
        super().__init__(tamano_fuente)
        self.setWindowTitle("Calculadora de Derivadas")
        self.initUI()

    def initUI(self):
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Ingrese una función en términos de una sola variable (por ejemplo, x)")
        self.control_layout.addWidget(self.input_function)

        self.input_function.textChanged.connect(self.update_rendered_function)
        self.rendered_view = QWebEngineView(self)
        self.rendered_view.setFixedHeight(150)
        self.control_layout.addWidget(self.rendered_view)

        self.control_layout.addLayout(self.create_math_keyboard())

        self.calculateDerivada_button = QPushButton("Calcular Derivada")
        self.calculateDerivada_button.clicked.connect(self.calculate_derivada)
        self.control_layout.addWidget(self.calculateDerivada_button)

        self.plot_button = QPushButton("Graficar Derivada")
        self.plot_button.clicked.connect(self.plot_function)
        self.plot_button.setEnabled(False)  # Deshabilitar inicialmente
        self.control_layout.addWidget(self.plot_button)

        self.result_view = QWebEngineView(self)
        self.result_view.setFixedHeight(200)
        self.control_layout.addWidget(self.result_view)

        self.back_to_calculo_menu_button = QPushButton("Regresar al Menú de Cálculo")
        self.back_to_calculo_menu_button.clicked.connect(self.regresar_menu_calculo)
        self.control_layout.addWidget(self.back_to_calculo_menu_button)

    def update_rendered_function(self):
        func_text = self.input_function.text()
        func_text_prepared = self.prepare_expression(func_text)

        try:
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
                    \\( f = {self.latex_expr} \\)
                </div>
            </body>
            </html>
            """
            self.rendered_view.setHtml(html_content)

            # Deshabilitar el botón de graficar hasta que se calcule la derivada
            self.plot_button.setEnabled(False)

        except Exception as e:
            self.rendered_view.setHtml("<p style='color:red;'>Función no válida</p>")
            self.plot_button.setEnabled(False)

    def calculate_derivada(self):
        func_text = self.input_function.text()
        func_text_prepared = self.prepare_expression(func_text)

        try:
            expr = sympify(func_text_prepared)
            self.func_expr = expr
            variables = expr.free_symbols

            if not variables:
                QMessageBox.warning(self, "Variables no encontradas", "No se encontraron variables en la función.")
                self.plot_button.setEnabled(False)
                return

            if len(variables) == 1:
                var = variables.pop()
                QMessageBox.information(self, "Variable seleccionada", f"Se utilizará la variable '{var}' para derivar.")
            else:
                QMessageBox.warning(self, "Demasiadas variables", "Por favor, ingrese una función con una sola variable.")
                self.plot_button.setEnabled(False)
                return

            result = diff(expr, var)
            self.derivative_expr = result  # Guardar para graficar
            self.derivative_var = var      # Guardar la variable de derivación
            latex_result = self.custom_latex_rendering(result)

            html_content = f"""
            <html>
            <head>
                <script type="text/javascript" async
                    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js">
                </script>
            </head>
            <body>
                <div style="font-size: 24px; color: black; padding: 20px;">
                    \\( \\frac{{d}}{{d{var}}} {self.latex_expr} = {latex_result} \\)
                </div>
            </body>
            </html>
            """
            self.result_view.setHtml(html_content)

            # Habilitar el botón de graficar ya que la derivada es de una variable
            self.plot_button.setEnabled(True)

        except SympifyError as e:
            error_html = f"<p style='color:red;'>Error al interpretar la función: {e}</p>"
            self.result_view.setHtml(error_html)
            self.plot_button.setEnabled(False)
        except Exception as e:
            error_html = f"<p style='color:red;'>Error al calcular la derivada: {e}</p>"
            self.result_view.setHtml(error_html)
            self.plot_button.setEnabled(False)

    def plot_function(self):
        try:
            # Verificar si derivative_expr está definido
            if not hasattr(self, 'derivative_expr'):
                QMessageBox.warning(self, "Derivada no calculada", "Primero debe calcular la derivada antes de graficar.")
                return

            expr = self.derivative_expr
            var = self.derivative_var  # Usar la variable de derivación

            # Convertir la expresión a una función numérica
            f = lambdify(var, expr, modules=['numpy', custom_math])

            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)

            # Manejar valores NaN o infinitos
            y_vals = np.nan_to_num(y_vals, nan=np.nan, posinf=np.nan, neginf=np.nan)

            fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"f'({var})"))
            fig.update_layout(title=f"Gráfica de la derivada f'({var})", xaxis_title=str(var), yaxis_title=f"f'({var})")

            # Mostrar la gráfica en el QWebEngineView
            viewer = PlotlyViewer(fig)
            self.plot_window = QDialog(self)
            self.plot_window.setWindowTitle("Gráfica de la Derivada")
            layout = QVBoxLayout()
            self.plot_window.setLayout(layout)
            layout.addWidget(viewer)
            self.plot_window.resize(800, 600)
            self.plot_window.exec_()

        except Exception as e:
            QMessageBox.warning(self, "Error al graficar", f"No se pudo graficar la derivada: {e}")
