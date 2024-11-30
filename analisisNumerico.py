# analisisNumerico.py

import sys
import os
import re
import numpy as np
from sympy import symbols, sympify, lambdify, latex, diff, S, solveset, Interval, Union, FiniteSet, EmptySet, oo
from sympy.calculus.util import continuous_domain
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                            QTextEdit, QDialog, QApplication, QMessageBox, QProgressDialog, QTableWidget, QTableWidgetItem)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QClipboard
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from manim import *
logger.setLevel("ERROR")  # Ocultar mensajes de registro de Manim

class AnimationThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, method, *args):
        super().__init__()
        self.method = method
        self.args = args

    def run(self):
        from manim import config

        # Directorio donde se guardará la animación
        output_dir = os.path.join(os.getcwd(), "videos")
        os.makedirs(output_dir, exist_ok=True)  # Crea el directorio si no existe

        # Ruta absoluta del archivo de salida
        output_file = os.path.join(output_dir, f"{self.method}_animation.mp4")

        # Configuración de Manim
        config.output_file = output_file
        config.format = "mp4"
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_rate = 30  # Opcional, para controlar los FPS
        config.media_dir = output_dir  # Opcionalmente, establecer media_dir al mismo directorio
        config.disable_caching = True
        config.progress_bar = 'none'

        # Crear la instancia de la escena correspondiente
        if self.method == 'bisection':
            scene = BisectionAnimation(*self.args)
        elif self.method == 'newton':
            scene = NewtonRaphsonAnimation(*self.args)
        elif self.method == 'false_position':
            scene = FalsePositionAnimation(*self.args)
        elif self.method == 'secant':
            scene = SecantMethodAnimation(*self.args)

        # Renderizar la escena
        try:
            scene.render()
            self.finished.emit(output_file)
        except Exception as e:
            self.finished.emit(f"Error: {e}")

class VentanaMetodoBase(QMainWindow):
    def __init__(self, tamano_fuente):
        super().__init__()
        self.tamano_fuente = tamano_fuente
        self.setGeometry(100, 100, 1400, 800)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.actualizar_fuente_local(self.tamano_fuente)

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
        self.showMaximized()

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
            ('xˣ', '**'), ('√', 'sqrt('), ('ln', 'ln(')
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
        func_text_prepared = self.prepare_expression(func_text)

        def determinar_dominio(expr):
            x = symbols('x')
            try:
                func = sympify(expr)
                domain = continuous_domain(func, x, S.Reals)
                return domain
            except Exception:
                return None
            
        def dominio_a_latex(domain):
            if domain is None or domain == EmptySet:
                return "Dominio: ∅"
            else:
                return f"Dominio: {latex(domain)}"

        try:
            x = symbols('x')
            expr = sympify(func_text_prepared)

            # Determinar el dominio de la función
            domain = determinar_dominio(expr)
            domain_latex = dominio_a_latex(domain)

            # Renderizar la función y el dominio en LaTeX
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
                    <br>
                    \\( {domain_latex} \\)
                </div>
            </body>
            </html>
            """
            self.rendered_view.setHtml(html_content)
            self.update_plot()
        except Exception:
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

    def play_animation(self, video_path):
        # Crear una ventana para reproducir el video
        self.video_window = QMainWindow(self)
        self.video_window.setWindowTitle("Animación")
        self.video_window.resize(800, 600)

        # Configurar el reproductor de video
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_widget = QVideoWidget()
        self.video_window.setCentralWidget(video_widget)
        self.media_player.setVideoOutput(video_widget)

        # Cargar el video
        video_url = QUrl.fromLocalFile(os.path.abspath(video_path))
        self.media_player.setMedia(QMediaContent(video_url))

        # Reproducir el video
        self.media_player.play()
        self.video_window.show()

class VentanaMetodoBiseccion(VentanaMetodoBase):
    def __init__(self, tamano_fuente):
        super().__init__(tamano_fuente)
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

        self.show_steps_button = QPushButton("Mostrar pasos")
        self.show_steps_button.setEnabled(False)
        self.show_steps_button.clicked.connect(self.mostrar_pasos)
        self.control_layout.addWidget(self.show_steps_button)

        self.animation_button = QPushButton("Ver Animación")
        self.animation_button.setEnabled(False)
        self.animation_button.clicked.connect(self.generate_animation)
        self.control_layout.addWidget(self.animation_button)

        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.control_layout.addWidget(self.back_to_analysis_menu_button)

        self.result_area = QTextEdit()
        self.control_layout.addWidget(self.result_area)

    def run_bisection(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            self.func_sympy = sympify(func_text)
            func = lambdify(x, self.func_sympy, 'numpy')
            self.a = float(self.input_a.text())
            self.b = float(self.input_b.text())
            tol = float(self.input_tolerance.text())

            # Validación del intervalo
            if self.a > self.b:
                QMessageBox.critical(self, "Error", "El valor de 'a' debe ser menor que 'b'.")
                self.input_a.setFocus()
                return

            # Ejecutar el método de bisección
            self.result, self.steps_list = self.bisection(func, self.a, self.b, tol)

            # Mostrar solo la información resumida
            if self.steps_list:
                last_step = self.steps_list[-1]
                c = last_step[2]
                error_abs = abs(func(c))
                error_rel = abs((self.b - self.a) / c) * 100
                num_iter = len(self.steps_list)
                self.result_area.setText(f"Raíz aproximada: {c}\nError absoluto: {error_abs}\nError relativo: {error_rel}%\nNúmero de iteraciones: {num_iter}")
            else:
                self.result_area.setText(self.result)

            self.plot_function(self.func_sympy, self.a, self.b, self.steps_list)
            self.animation_button.setEnabled(True)
            self.show_steps_button.setEnabled(True)  # Habilitar el botón "Mostrar pasos"
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en la entrada: {e}")
            self.input_function.setFocus()

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
    
    def mostrar_pasos(self):
        # Crear la ventana de pasos
        self.steps_window = QDialog(self)
        self.steps_window.setWindowTitle("Pasos del Método de Bisección")
        layout = QVBoxLayout(self.steps_window)

        self.steps_window.resize(800, 600) 

        # Crear la tabla
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Iteración", "a", "b", "c", "f(c)"])
        table.setRowCount(len(self.steps_list))

        # Llenar la tabla con los datos
        for idx, (a_i, b_i, c_i) in enumerate(self.steps_list):
            table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
            table.setItem(idx, 1, QTableWidgetItem(str(a_i)))
            table.setItem(idx, 2, QTableWidgetItem(str(b_i)))
            table.setItem(idx, 3, QTableWidgetItem(str(c_i)))
            table.setItem(idx, 4, QTableWidgetItem(str(self.func_sympy.subs(symbols('x'), c_i))))

        # Ajustar el tamaño de las columnas
        table.resizeColumnsToContents()

        # Agregar la tabla al layout
        layout.addWidget(table)

        # Mostrar la ventana
        self.steps_window.exec_()

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

    def generate_animation(self):
        # Mostrar diálogo de progreso
        progress_dialog = QProgressDialog("Renderizando animación, por favor espere...", None, 0, 0, self)
        progress_dialog.setWindowTitle("Generando Animación")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        # Crear y ejecutar el hilo de animación
        self.animation_thread = AnimationThread('bisection', self.func_sympy, self.a, self.b, self.steps_list)
        self.animation_thread.finished.connect(lambda video_path: self.on_animation_finished(video_path, progress_dialog))
        self.animation_thread.start()

    def on_animation_finished(self, video_path, progress_dialog):
        progress_dialog.close()
        if "Error" in video_path:
            QMessageBox.critical(self, "Error", video_path)
        else:
            self.play_animation(video_path)

class BisectionAnimation(Scene):
    def __init__(self, func_sympy, a, b, steps_list, **kwargs):
        super().__init__(**kwargs)
        self.func_sympy = func_sympy
        self.a = a
        self.b = b
        self.steps_list = steps_list

    def construct(self):
        x = symbols('x')
        func = lambdify(x, self.func_sympy, 'numpy')

        def generar_segmentos_manual(x_min, x_max, num_puntos=500):
            """Divide el rango en pequeños segmentos y filtra discontinuidades."""
            x_vals = np.linspace(x_min, x_max, num_puntos)
            y_vals = func(x_vals)

            # Detectar discontinuidades por valores indefinidos o extremos
            valid_mask = np.isfinite(y_vals) & (np.abs(y_vals) < 1e6)
            segmentos = []
            current_segment = []

            for i, valid in enumerate(valid_mask):
                if valid:
                    current_segment.append((x_vals[i], y_vals[i]))
                else:
                    if current_segment:
                        # Agregar segmento válido
                        segmentos.append(current_segment)
                        current_segment = []
            if current_segment:
                # Agregar el último segmento válido
                segmentos.append(current_segment)

            return segmentos

        # Crear segmentos válidos para graficar
        segmentos_validos = generar_segmentos_manual(-10, 10, num_puntos=1000)

        if not segmentos_validos:
            text = Text("No se puede graficar en este dominio por discontinuidades.", font_size=24)
            self.add(text)
            self.wait(2)
            return

        # Crear ejes
        axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
            x_length=10,
            y_length=6,
            tips=False,
            x_axis_config={"include_ticks": True},
            y_axis_config={"include_ticks": True},
        ).add_coordinates()

        self.play(Create(axes))

        # Graficar cada segmento
        for segment in segmentos_validos:
            x_segment, y_segment = zip(*segment)
            graph = axes.plot_line_graph(
                x_values=x_segment,
                y_values=y_segment,
                add_vertex_dots=False,
                line_color=BLUE,
            )
            self.play(Create(graph))
            self.wait(0.5)

        # Animar el método de bisección
        for a_i, b_i, c_i in self.steps_list:
            try:
                dot_a = Dot(axes.coords_to_point(a_i, func(a_i)), color=RED)
                dot_b = Dot(axes.coords_to_point(b_i, func(b_i)), color=RED)
                dot_c = Dot(axes.coords_to_point(c_i, func(c_i)), color=GREEN)

                self.play(FadeIn(dot_a), FadeIn(dot_b), FadeIn(dot_c))
                self.wait(0.5)

                self.play(FadeOut(dot_a), FadeOut(dot_b), FadeOut(dot_c))
            except Exception as e:
                print(f"Error al renderizar punto: {e}")
                continue

class VentanaMetodoNewtonRaphson(VentanaMetodoBase):
    def __init__(self, tamano_fuente):
        super().__init__(tamano_fuente)
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

        self.start_button = QPushButton("Calcular Raíz")
        self.start_button.clicked.connect(self.run_newton_raphson)
        self.control_layout.addWidget(self.start_button)

        self.show_steps_button = QPushButton("Mostrar pasos")
        self.show_steps_button.setEnabled(False)
        self.show_steps_button.clicked.connect(self.mostrar_pasos)
        self.control_layout.addWidget(self.show_steps_button)

        self.animation_button = QPushButton("Ver Animación")
        self.animation_button.setEnabled(False)
        self.animation_button.clicked.connect(self.generate_animation)
        self.control_layout.addWidget(self.animation_button)

        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.control_layout.addWidget(self.back_to_analysis_menu_button)

    def update_rendered_function(self):
        func_text = self.input_function.text()
        func_text = self.prepare_expression(func_text)

        def determinar_dominio(expr):
            x = symbols('x')
            try:
                func = sympify(expr)
                domain = continuous_domain(func, x, S.Reals)
                return domain
            except Exception:
                return None

        def dominio_a_latex(domain):
            if domain is None or domain == EmptySet:
                return "Dominio: ∅"
            else:
                return f"Dominio: {latex(domain)}"

        try:
            x = symbols('x')
            expr = sympify(func_text)
            derivative = expr.diff(x)  # Calcula la derivada de la función

            # Determinar el dominio de la función
            domain = determinar_dominio(expr)
            domain_latex = dominio_a_latex(domain)

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
                    <p>\\( {domain_latex} \\)</p>
                </div>
            </body>
            </html>
            """
            self.rendered_view.setHtml(html_content)
            self.update_plot()
        except Exception:
            self.rendered_view.setHtml("<p style='color:red;'>Función no válida</p>")

    def run_newton_raphson(self):
        try:
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            self.func_expr = sympify(func_text)
            derivative_expr = self.func_expr.diff(x)
            func = lambdify(x, self.func_expr, 'numpy')
            derivative = lambdify(x, derivative_expr, 'numpy')
            x0 = float(self.input_initial_value.text())

            tol = 1e-6
            max_iter = 100
            iter_count = 0
            error = float('inf')
            self.steps_list = []

            while error > tol and iter_count < max_iter:
                f_x0 = func(x0)
                f_prime_x0 = derivative(x0)

                if f_prime_x0 == 0:
                    raise ZeroDivisionError("La derivada es cero. No se puede continuar con el método.")

                x1 = x0 - f_x0 / f_prime_x0
                error = abs(x1 - x0)
                error_relativo = abs(error / x1) * 100 if x1 != 0 else float('inf')
                self.steps_list.append((iter_count + 1, x0, f_x0, f_prime_x0, x1, error, error_relativo))

                x0 = x1
                iter_count += 1

            if iter_count == max_iter:
                self.result_area.setText("El método no convergió después del número máximo de iteraciones.")
            else:
                self.result_area.setText(f"Raíz aproximada: {x1}\nError absoluto: {error}\nError relativo: {error_relativo}%\nNúmero de iteraciones: {iter_count}")

            self.plot_function(self.func_expr, [step[1] for step in self.steps_list])
            self.animation_button.setEnabled(True)
            self.show_steps_button.setEnabled(True)
        except ZeroDivisionError as e:
            self.result_area.setText(f"Error: {e}")
        except Exception as e:
            self.result_area.setText(f"Error en la entrada: {e}")

    def mostrar_pasos(self):
        # Crear la ventana de pasos
        self.steps_window = QDialog(self)
        self.steps_window.setWindowTitle("Pasos del Método de Newton-Raphson")
        layout = QVBoxLayout(self.steps_window)

        self.steps_window.resize(900, 600)

        # Crear la tabla
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["Iteración", "x_i", "f(x_i)", "f'(x_i)", "x_{i+1}", "Error absoluto", "Error relativo (%)"])
        table.setRowCount(len(self.steps_list))

        # Llenar la tabla con los datos
        for idx, (iter_num, x_i, f_xi, f_prime_xi, x_next, error_abs, error_rel) in enumerate(self.steps_list):
            table.setItem(idx, 0, QTableWidgetItem(str(iter_num)))
            table.setItem(idx, 1, QTableWidgetItem(str(x_i)))
            table.setItem(idx, 2, QTableWidgetItem(str(f_xi)))
            table.setItem(idx, 3, QTableWidgetItem(str(f_prime_xi)))
            table.setItem(idx, 4, QTableWidgetItem(str(x_next)))
            table.setItem(idx, 5, QTableWidgetItem(str(error_abs)))
            table.setItem(idx, 6, QTableWidgetItem(str(error_rel)))

        # Ajustar el tamaño de las columnas
        table.resizeColumnsToContents()

        # Agregar la tabla al layout
        layout.addWidget(table)

        # Mostrar la ventana
        self.steps_window.exec_()

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

    def generate_animation(self):
        # Mostrar diálogo de progreso
        progress_dialog = QProgressDialog("Renderizando animación, por favor espere...", None, 0, 0, self)
        progress_dialog.setWindowTitle("Generando Animación")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        # Crear y ejecutar el hilo de animación
        self.animation_thread = AnimationThread('newton', self.func_expr, self.x_values)
        self.animation_thread.finished.connect(lambda video_path: self.on_animation_finished(video_path, progress_dialog))
        self.animation_thread.start()

    def on_animation_finished(self, video_path, progress_dialog):
        progress_dialog.close()
        if "Error" in video_path:
            QMessageBox.critical(self, "Error", video_path)
        else:
            self.play_animation(video_path)

class NewtonRaphsonAnimation(Scene):
    def __init__(self, func_expr, x_values, **kwargs):
        super().__init__(**kwargs)
        self.func_expr = func_expr
        self.x_values = x_values

    def construct(self):
        x = symbols('x')
        func = lambdify(x, self.func_expr, 'numpy')

        def generar_segmentos_manual(x_min, x_max, num_puntos=500):
            """Divide el rango en pequeños segmentos y filtra discontinuidades."""
            x_vals = np.linspace(x_min, x_max, num_puntos)
            y_vals = func(x_vals)

            # Detectar discontinuidades
            valid_mask = np.isfinite(y_vals) & (np.abs(y_vals) < 1e6)
            segmentos = []
            current_segment = []

            for i, valid in enumerate(valid_mask):
                if valid:
                    current_segment.append((x_vals[i], y_vals[i]))
                else:
                    if current_segment:
                        segmentos.append(current_segment)
                        current_segment = []
            if current_segment:
                segmentos.append(current_segment)

            return segmentos

        segmentos_validos = generar_segmentos_manual(-10, 10, num_puntos=1000)

        if not segmentos_validos:
            text = Text("No se puede graficar en este dominio por discontinuidades.", font_size=24)
            self.add(text)
            self.wait(2)
            return

        # Crear ejes
        axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
            x_length=10,
            y_length=6,
            tips=False,
            x_axis_config={"include_ticks": True},
            y_axis_config={"include_ticks": True},
        ).add_coordinates()

        self.play(Create(axes))

        # Graficar segmentos válidos
        for segment in segmentos_validos:
            x_segment, y_segment = zip(*segment)
            graph = axes.plot_line_graph(
                x_values=x_segment,
                y_values=y_segment,
                add_vertex_dots=False,
                line_color=BLUE,
            )
            self.play(Create(graph))
            self.wait(0.5)

        # Animar el método de Newton-Raphson
        for xi in self.x_values[:-1]:
            try:
                f_xi = func(xi)
                derivative = diff(self.func_expr, x).subs(x, xi)
                derivative_func = lambdify(x, derivative, 'numpy')

                tangent = lambda x_val: derivative_func(xi) * (x_val - xi) + f_xi
                tangent_graph = axes.plot(tangent, color=ORANGE)
                dot = Dot(axes.coords_to_point(xi, f_xi), color=RED)

                self.play(Create(tangent_graph), FadeIn(dot))
                self.wait(0.5)

                self.play(FadeOut(tangent_graph), FadeOut(dot))
            except Exception as e:
                print(f"Error al renderizar: {e}")

class VentanaMetodoFalsaPosicion(VentanaMetodoBase):
    def __init__(self, tamano_fuente):
        super().__init__(tamano_fuente)
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

        self.show_steps_button = QPushButton("Mostrar pasos")
        self.show_steps_button.setEnabled(False)
        self.show_steps_button.clicked.connect(self.mostrar_pasos)
        self.control_layout.addWidget(self.show_steps_button)

        self.animation_button = QPushButton("Ver Animación")
        self.animation_button.setEnabled(False)
        self.animation_button.clicked.connect(self.generate_animation)
        self.control_layout.addWidget(self.animation_button)

        # Botón para regresar al menú de análisis numérico
        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.control_layout.addWidget(self.back_to_analysis_menu_button)

        # Área de texto para mostrar resultados
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.control_layout.addWidget(self.result_display)

    def ejecutar_falsa_posicion(self):
        try:
            # Obtiene los valores de entrada de la interfaz
            func_text = self.prepare_expression(self.input_function.text())
            x = symbols('x')
            self.func_expr = sympify(func_text)
            funcion = lambdify(x, self.func_expr, 'numpy')
            xl = float(self.xl_input.text())
            xu = float(self.xu_input.text())
            tolerancia = float(self.tol_input.text())
            iter_max = int(self.iter_input.text())

            # Validación del intervalo
            if xl > xu:
                QMessageBox.critical(self, "Error", "El valor de 'xl' debe ser menor que 'xu'.")
                self.xl_input.setFocus()
                return

            # Valida que xl y xu encierren una raíz
            if funcion(xl) * funcion(xu) >= 0:
                QMessageBox.critical(self, "Error", "El intervalo [xl, xu] no encierra una raíz.")
                self.xl_input.setFocus()
                return

            # Ejecuta el cálculo del método de Falsa Posición
            self.resultado, self.error, self.iteraciones, self.steps_list = self.calcular_raiz(funcion, xl, xu, tolerancia, iter_max)
            self.mostrar_resultados()
            self.plot_function(self.func_expr, xl, xu, self.steps_list)
            self.animation_button.setEnabled(True)
            self.show_steps_button.setEnabled(True)
        except Exception as e:
            self.result_display.setText(f"Error: {str(e)}")
            self.input_function.setFocus()

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

            # Cálculo del error relativo
            if xr != 0:
                error_aprox = abs((xr - xr_prev) / xr) * 100
            else:
                error_aprox = float('inf')  # Evitar división por cero

            # Guardar los valores para graficar y para los pasos
            steps_list.append((xl, xu, xr, error_aprox))

            # Actualización del intervalo
            if funcion(xl) * funcion(xr) < 0:
                xu = xr
            elif funcion(xu) * funcion(xr) < 0:
                xl = xr
            else:
                break  # Si f(xr) es aproximadamente cero, encontramos la raíz

            iteraciones += 1

        return xr, error_aprox, iteraciones, steps_list

    def mostrar_resultados(self):
        if self.steps_list:
            last_step = self.steps_list[-1]
            xr = last_step[2]
            error_abs = abs(self.func_expr.subs(symbols('x'), xr))
            error_rel = last_step[3]  # Error relativo de la última iteración
            num_iter = len(self.steps_list)
            self.result_display.setText(f"Raíz aproximada: {xr}\nError absoluto: {error_abs}\nError relativo: {error_rel}%\nNúmero de iteraciones: {num_iter}")
        else:
            self.result_display.setText("No se encontró raíz.")

    def mostrar_pasos(self):
        # Crear la ventana de pasos
        self.steps_window = QDialog(self)
        self.steps_window.setWindowTitle("Pasos del Método de Falsa Posición")
        layout = QVBoxLayout(self.steps_window)

        self.steps_window.resize(1000, 600)

        # Crear la tabla
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["Iteración", "xl", "xu", "xr", "f(xl)", "f(xu)", "f(xr)", "Error relativo (%)"])
        table.setRowCount(len(self.steps_list))

        funcion = lambdify(symbols('x'), self.func_expr, 'numpy')

        # Llenar la tabla con los datos
        for idx, (xl_i, xu_i, xr_i, error_relativo) in enumerate(self.steps_list):
            f_xl = funcion(xl_i)
            f_xu = funcion(xu_i)
            f_xr = funcion(xr_i)
            table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
            table.setItem(idx, 1, QTableWidgetItem(f"{xl_i:.6f}"))
            table.setItem(idx, 2, QTableWidgetItem(f"{xu_i:.6f}"))
            table.setItem(idx, 3, QTableWidgetItem(f"{xr_i:.6f}"))
            table.setItem(idx, 4, QTableWidgetItem(f"{f_xl:.6f}"))
            table.setItem(idx, 5, QTableWidgetItem(f"{f_xu:.6f}"))
            table.setItem(idx, 6, QTableWidgetItem(f"{f_xr:.6f}"))
            table.setItem(idx, 7, QTableWidgetItem(f"{error_relativo:.6f}"))

        # Ajustar el tamaño de las columnas
        table.resizeColumnsToContents()

        # Agregar la tabla al layout
        layout.addWidget(table)

        # Mostrar la ventana
        self.steps_window.exec_()

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
        for idx, (xl_i, xu_i, xr_i, error_relativo) in enumerate(steps_list):
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

    def generate_animation(self):
        # Mostrar diálogo de progreso
        progress_dialog = QProgressDialog("Renderizando animación, por favor espere...", None, 0, 0, self)
        progress_dialog.setWindowTitle("Generando Animación")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        # Crear y ejecutar el hilo de animación
        self.animation_thread = AnimationThread('false_position', self.func_expr, self.steps_list)
        self.animation_thread.finished.connect(lambda video_path: self.on_animation_finished(video_path, progress_dialog))
        self.animation_thread.start()

    def on_animation_finished(self, video_path, progress_dialog):
        progress_dialog.close()
        if "Error" in video_path:
            QMessageBox.critical(self, "Error", video_path)
        else:
            self.play_animation(video_path)

class FalsePositionAnimation(Scene):
    def __init__(self, func_expr, steps_list, **kwargs):
        super().__init__(**kwargs)
        self.func_expr = func_expr
        self.steps_list = steps_list

    def construct(self):
        x = symbols('x')
        func = lambdify(x, self.func_expr, 'numpy')

        def generar_segmentos_manual(x_min, x_max, num_puntos=500):
            """Divide el rango en pequeños segmentos y filtra discontinuidades."""
            x_vals = np.linspace(x_min, x_max, num_puntos)
            y_vals = func(x_vals)

            # Detectar discontinuidades
            valid_mask = np.isfinite(y_vals) & (np.abs(y_vals) < 1e6)
            segmentos = []
            current_segment = []

            for i, valid in enumerate(valid_mask):
                if valid:
                    current_segment.append((x_vals[i], y_vals[i]))
                else:
                    if current_segment:
                        segmentos.append(current_segment)
                        current_segment = []
            if current_segment:
                segmentos.append(current_segment)

            return segmentos

        segmentos_validos = generar_segmentos_manual(-10, 10, num_puntos=1000)

        if not segmentos_validos:
            text = Text("No se puede graficar en este dominio por discontinuidades.", font_size=24)
            self.add(text)
            self.wait(2)
            return

        # Crear ejes
        axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
            x_length=10,
            y_length=6,
            tips=False,
            x_axis_config={"include_ticks": True},
            y_axis_config={"include_ticks": True},
        ).add_coordinates()

        self.play(Create(axes))

        # Graficar segmentos válidos
        for segment in segmentos_validos:
            x_segment, y_segment = zip(*segment)
            graph = axes.plot_line_graph(
                x_values=x_segment,
                y_values=y_segment,
                add_vertex_dots=False,
                line_color=BLUE,
            )
            self.play(Create(graph))
            self.wait(0.5)

        # Animar el método de Falsa Posición
        for xl_i, xu_i, xr_i in self.steps_list:
            try:
                f_xl = func(xl_i)
                f_xu = func(xu_i)

                secant_line = axes.plot_line_graph(
                    x_values=[xl_i, xu_i],
                    y_values=[f_xl, f_xu],
                    add_vertex_dots=False,
                    line_color=ORANGE,
                )
                dot_xr = Dot(axes.coords_to_point(xr_i, func(xr_i)), color=GREEN)

                self.play(Create(secant_line), FadeIn(dot_xr))
                self.wait(0.5)

                self.play(FadeOut(secant_line), FadeOut(dot_xr))
            except Exception as e:
                print(f"Error al renderizar: {e}")

class VentanaMetodoSecante(VentanaMetodoBase):
    def __init__(self, tamano_fuente):
        super().__init__(tamano_fuente)
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

        self.start_button = QPushButton("Calcular Raíz")
        self.start_button.clicked.connect(self.run_secant)
        self.control_layout.addWidget(self.start_button)

        self.show_steps_button = QPushButton("Mostrar pasos")
        self.show_steps_button.setEnabled(False)
        self.show_steps_button.clicked.connect(self.mostrar_pasos)
        self.control_layout.addWidget(self.show_steps_button)

        self.animation_button = QPushButton("Ver Animación")
        self.animation_button.setEnabled(False)
        self.animation_button.clicked.connect(self.generate_animation)
        self.control_layout.addWidget(self.animation_button)

        self.back_to_analysis_menu_button = QPushButton("Regresar al Menú de Análisis Numérico")
        self.back_to_analysis_menu_button.clicked.connect(self.regresar_menu_analisis_numerico)
        self.control_layout.addWidget(self.back_to_analysis_menu_button)

    def run_secant(self):
        try:
            x = symbols('x')
            func_text = self.prepare_expression(self.input_function.text())
            self.func_expr = sympify(func_text)
            funcion = lambdify(x, self.func_expr, 'numpy')
            x0 = float(self.input_x0.text())
            x1 = float(self.input_x1.text())

            tol = 1e-5
            max_iter = 100
            self.x_values = [x0, x1]
            self.steps_list = []
            results = []
            for i in range(max_iter):
                fx0 = funcion(x0)
                fx1 = funcion(x1)

                if fx1 - fx0 == 0:
                    raise ZeroDivisionError("División por cero en la fórmula de la secante.")

                # Fórmula de la secante
                x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
                error_abs = abs(x2 - x1)
                error_rel = abs(error_abs / x2) * 100 if x2 != 0 else float('inf')
                self.steps_list.append((i + 1, x0, x1, x2, fx0, fx1, error_abs, error_rel))

                # Verificar convergencia
                if error_abs < tol:
                    self.result_area.setText(f"Raíz aproximada: {x2}\nError absoluto: {error_abs}\nError relativo: {error_rel}%\nNúmero de iteraciones: {i + 1}")
                    self.x_values.append(x2)
                    self.plot_function(self.func_expr, self.x_values)
                    self.animation_button.setEnabled(True)
                    self.show_steps_button.setEnabled(True)
                    return

                x0, x1 = x1, x2
                self.x_values.append(x1)

            self.result_area.setText("No converge en el número máximo de iteraciones")
            self.plot_function(self.func_expr, self.x_values)
            self.animation_button.setEnabled(True)
            self.show_steps_button.setEnabled(True)
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

    def mostrar_pasos(self):
        # Crear la ventana de pasos
        self.steps_window = QDialog(self)
        self.steps_window.setWindowTitle("Pasos del Método de la Secante")
        layout = QVBoxLayout(self.steps_window)

        self.steps_window.resize(900, 600)

        # Crear la tabla
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["Iteración", "x_i-1", "x_i", "x_i+1", "f(x_i-1)", "f(x_i)", "Error absoluto", "Error relativo (%)"])
        table.setRowCount(len(self.steps_list))

        # Llenar la tabla con los datos
        for idx, (iter_num, x_prev, x_curr, x_next, f_x_prev, f_x_curr, error_abs, error_rel) in enumerate(self.steps_list):
            table.setItem(idx, 0, QTableWidgetItem(str(iter_num)))
            table.setItem(idx, 1, QTableWidgetItem(str(x_prev)))
            table.setItem(idx, 2, QTableWidgetItem(str(x_curr)))
            table.setItem(idx, 3, QTableWidgetItem(str(x_next)))
            table.setItem(idx, 4, QTableWidgetItem(str(f_x_prev)))
            table.setItem(idx, 5, QTableWidgetItem(str(f_x_curr)))
            table.setItem(idx, 6, QTableWidgetItem(str(error_abs)))
            table.setItem(idx, 7, QTableWidgetItem(str(error_rel)))

        # Ajustar el tamaño de las columnas
        table.resizeColumnsToContents()

        # Agregar la tabla al layout
        layout.addWidget(table)

        # Mostrar la ventana
        self.steps_window.exec_()

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

    def generate_animation(self):
        # Mostrar diálogo de progreso
        progress_dialog = QProgressDialog("Renderizando animación, por favor espere...", None, 0, 0, self)
        progress_dialog.setWindowTitle("Generando Animación")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        # Crear y ejecutar el hilo de animación
        self.animation_thread = AnimationThread('secant', self.func_expr, self.x_values)
        self.animation_thread.finished.connect(lambda video_path: self.on_animation_finished(video_path, progress_dialog))
        self.animation_thread.start()

    def on_animation_finished(self, video_path, progress_dialog):
        progress_dialog.close()
        if "Error" in video_path:
            QMessageBox.critical(self, "Error", video_path)
        else:
            self.play_animation(video_path)

class SecantMethodAnimation(Scene):
    def __init__(self, func_expr, x_values, **kwargs):
        super().__init__(**kwargs)
        self.func_expr = func_expr
        self.x_values = x_values

    def construct(self):
        x = symbols('x')
        func = lambdify(x, self.func_expr, 'numpy')

        def generar_segmentos_manual(x_min, x_max, num_puntos=500):
            """Divide el rango en pequeños segmentos y filtra discontinuidades."""
            x_vals = np.linspace(x_min, x_max, num_puntos)
            y_vals = func(x_vals)

            # Detectar discontinuidades
            valid_mask = np.isfinite(y_vals) & (np.abs(y_vals) < 1e6)
            segmentos = []
            current_segment = []

            for i, valid in enumerate(valid_mask):
                if valid:
                    current_segment.append((x_vals[i], y_vals[i]))
                else:
                    if current_segment:
                        segmentos.append(current_segment)
                        current_segment = []
            if current_segment:
                segmentos.append(current_segment)

            return segmentos

        segmentos_validos = generar_segmentos_manual(-10, 10, num_puntos=1000)

        if not segmentos_validos:
            text = Text("No se puede graficar en este dominio por discontinuidades.", font_size=24)
            self.add(text)
            self.wait(2)
            return

        # Crear ejes
        axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
            x_length=10,
            y_length=6,
            tips=False,
            x_axis_config={"include_ticks": True},
            y_axis_config={"include_ticks": True},
        ).add_coordinates()

        self.play(Create(axes))

        # Graficar segmentos válidos
        for segment in segmentos_validos:
            x_segment, y_segment = zip(*segment)
            graph = axes.plot_line_graph(
                x_values=x_segment,
                y_values=y_segment,
                add_vertex_dots=False,
                line_color=BLUE,
            )
            self.play(Create(graph))
            self.wait(0.5)

        # Animar el método de la Secante
        for i in range(len(self.x_values) - 2):
            try:
                x0, x1 = self.x_values[i], self.x_values[i + 1]
                fx0, fx1 = func(x0), func(x1)

                secant_line = axes.plot_line_graph(
                    x_values=[x0, x1],
                    y_values=[fx0, fx1],
                    add_vertex_dots=False,
                    line_color=ORANGE,
                )
                dot_x1 = Dot(axes.coords_to_point(x1, fx1), color=RED)

                self.play(Create(secant_line), FadeIn(dot_x1))
                self.wait(0.5)

                self.play(FadeOut(secant_line), FadeOut(dot_x1))
            except Exception as e:
                print(f"Error al renderizar: {e}")