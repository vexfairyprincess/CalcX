# menu.py

from utils import evaluar_expresion

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
import sys
from ventanasMenu import *
from analisisNumerico import *
from calculo import *

class MenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setStyleSheet("background-color: white;") 
        self.resize(800, 600)  # Resizable main window

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        self.main_layout = QVBoxLayout()

        # Image
        logo_layout = QHBoxLayout()
        self.imagen_svg = QSvgWidget("calcXlogo.svg")  # Update this path
        self.imagen_svg.setFixedSize(250,125)  # Increase the height for a larger logo
        logo_layout.addWidget(self.imagen_svg, alignment= Qt.AlignLeft | Qt.AlignTop)  # Center the logo in the grid
        
        self.main_layout.addLayout(logo_layout)
        
        self.cartas_layout = QGridLayout()
        self.cartas_layout.setSpacing(30)
        main_widget.setContentsMargins(20, 20, 20, 20)
        self.cartas_layout.setColumnStretch(0, 1)
        self.cartas_layout.setColumnStretch(1, 1)
        self.cartas_layout.setColumnStretch(2, 1)
        
        self.cartas_layout.setRowStretch(0, 1)
        self.cartas_layout.setRowStretch(1, 2)
        self.cartas_layout.setRowStretch(2, 3)
        
        self.main_layout.addLayout(self.cartas_layout)
        
        self.crear_carta("Álgebra Lineal", "1774128.png", self.abrir_menu_algebra_lineal, 0)
        self.crear_carta("Análisis Numérico", "43146.png", self.abrir_menu_analisis_numerico, 1)
        self.crear_carta("Cálculo", "5111141.png", self.abrir_menu_calculo, 2)
        
        main_widget.setLayout(self.main_layout)
        
        self.showMaximized()

        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setFont(QFont('Arial', 12))
        self.boton_salir.setFixedSize(150,30)
        self.boton_salir.clicked.connect(self.close)
        self.boton_salir.setStyleSheet("""QPushButton{
            background-color: #F0EBEB;
            border: 2px solid #80C8FF;
            border-radius: 10px;
            padding: 20px;
            font-size: 19px;
            font-weight: bold;
            color: black;
            text-align: center;
            padding-left: 25px;
        }
        QPushButton:hover{
            background-color: #ADD8E6;
            color: black;
        }
        
        QPushButton:pressed{
            background-color: #007F92;
        }
        """)	
        self.main_layout.addWidget(self.boton_salir, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.showMaximized()
        
        
    def crear_carta(self, text, icon, function, column):
        carta = QPushButton(text)
        icon_path = f"icons/{icon}"
        carta.setIcon(QIcon(icon_path))
        carta.setIconSize(QSize(50, 50))
        carta.setStyleSheet("""
        QPushButton{
            background-color: #F0EBEB;
            border: 4px solid #80C8FF;
            border-radius: 20px;
            padding: 30px;
            font-size: 18px;
            font-weight: bold;
            color: black;
            text-align: center;
            padding-left: 25px;
        }
        
        QPushButton:hover{
            background-color: #ADD8E6;
            color: black;
        }
        
        QPushButton:pressed{
            background-color: #007F92;
        }
    """)
        
        carta.setFixedSize(300, 300)
        carta.clicked.connect(function)
        
        self.cartas_layout.addWidget(carta, 1, column)
        
        
        

    def abrir_menu_algebra_lineal(self):
        # Abre el menú de Álgebra Lineal
        self.menu_algebra_lineal = MenuAlgebra()
        self.menu_algebra_lineal.show()
        self.close()

    def abrir_menu_analisis_numerico(self):
        self.menu_analisis_numerico = MenuAnalisisNumerico()
        self.menu_analisis_numerico.show()
        self.close()

    def abrir_menu_calculo(self):
        self.menu_calculo = MenuCalculo()
        self.menu_calculo.show()
        self.close()


class MenuAlgebra(QMainWindow):
    cambiar_fuente_signal = pyqtSignal(int)  # Señal para cambiar el tamaño de fuente global

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Álgebra")
        self.setGeometry(100, 100, 800, 600)

        # Fuente base
        self.tamano_fuente = 17  # Tamaño de fuente inicial

        # Widget principal
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout()
        self.main_widget.setLayout(self.layout)

        # Conectar la señal para cambiar fuente
        # Asegúrese de tener estas funciones definidas
        self.cambiar_fuente_signal.connect(self.actualizar_fuente_global)

        # Menú principal
        self.crear_menu_principal()
        self.showMaximized()

    def crear_menu_principal(self):
        # Limpiar el layout actual
        self.limpiar_layout(self.layout)

        # Establecer estilo
        self.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
            }
            QLabel {
                font-size: 18px;
            }
            QLineEdit, QTextEdit, QTableWidget {
                font-size: 16px;
            }
        """)

        # Configurar estiramientos de columnas para centrar elementos
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 1)

        # Título
        self.label_titulo = QLabel("Menú Álgebra Lineal", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(28)
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo, 0, 0, 1, 3)

        # Botón Matrices
        self.boton_matrices = QPushButton("Matrices", self)
        self.boton_matrices.setFixedSize(400, 50)
        self.boton_matrices.clicked.connect(self.abrir_menu_matrices)
        self.layout.addWidget(self.boton_matrices, 1, 1, alignment=Qt.AlignCenter)

        # Botón Vectores
        self.boton_vectores = QPushButton("Vectores", self)
        self.boton_vectores.setFixedSize(400, 50)
        self.boton_vectores.clicked.connect(self.abrir_menu_vectores)
        self.layout.addWidget(self.boton_vectores, 2, 1, alignment=Qt.AlignCenter)

        # Botones para ajustar el tamaño de fuente
        botones_fuente_layout = QHBoxLayout()
        self.layout.addLayout(botones_fuente_layout, 3, 1, alignment=Qt.AlignCenter)

        self.boton_aumentar_fuente = QPushButton("Aumentar tamaño de fuente", self)
        self.boton_aumentar_fuente.clicked.connect(self.aumentar_tamano_fuente)
        botones_fuente_layout.addWidget(self.boton_aumentar_fuente)

        self.boton_disminuir_fuente = QPushButton("Disminuir tamaño de fuente", self)
        self.boton_disminuir_fuente.clicked.connect(self.disminuir_tamano_fuente)
        botones_fuente_layout.addWidget(self.boton_disminuir_fuente)

        # Botón para regresar al menú principal
        self.boton_salir = QPushButton("Regresar al menú principal", self)
        self.boton_salir.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_salir, 4, 1, alignment=Qt.AlignCenter)

    def abrir_menu_matrices(self):
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()

    def abrir_menu_vectores(self):
        self.menu_vectores = MenuVectores(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_vectores.show()

    def aumentar_tamano_fuente(self):
        self.tamano_fuente += 2
        self.cambiar_fuente_signal.emit(self.tamano_fuente)

    def disminuir_tamano_fuente(self):
        if self.tamano_fuente > 8:
            self.tamano_fuente -= 2
            self.cambiar_fuente_signal.emit(self.tamano_fuente)

    def actualizar_fuente_global(self, tamano):
        fuente = QFont()
        fuente.setPointSize(tamano)
        app = QApplication.instance()
        app.setFont(fuente)

    def limpiar_layout(self, layout):
        """Elimina todos los widgets del layout dado."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def regresar_menu_principal(self):
        # Abre el menú principal inicial y cierra el actual
        self.menu_principal = MenuPrincipal()
        self.menu_principal.show()
        self.close()

    # menu matrices


class MenuMatrices(QMainWindow):
    def __init__(self, tamano_fuente, cambiar_fuente_signal):
        super().__init__()
        self.setWindowTitle("Menú Matrices")
        self.setGeometry(150, 150, 800, 600)

        # Widget principal
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout()  # Cambiamos a QGridLayout para posicionar los botones
        self.main_widget.setLayout(self.layout)

        self.tamano_fuente = tamano_fuente
        self.cambiar_fuente_signal = cambiar_fuente_signal

        # Conectar la señal para cambiar la fuente
        self.cambiar_fuente_signal.connect(self.actualizar_fuente_local)

        # Establecer estilo
        self.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
            }
            QLabel {
                font-size: 18px;
            }
            QLineEdit, QTextEdit, QTableWidget {
                font-size: 16px;
            }
        """)

        # Configurar estiramientos de columnas para centrar elementos
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 1)

        # Título
        self.label_titulo = QLabel("Operaciones con Matrices", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(30)
        fuente_titulo.setBold(True)
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo, 0, 0, 1, 3)

        # Grupo Reducción de Matrices
        self.group_reduccion = QGroupBox("Reducción de Matrices")
        self.group_reduccion.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.group_reduccion, 1, 0, 1, 3)
        reduccion_layout = QGridLayout()  # Usamos QGridLayout dentro del grupo
        self.group_reduccion.setLayout(reduccion_layout)

        # Configurar estiramientos de columnas en el layout interno
        reduccion_layout.setColumnStretch(0, 1)
        reduccion_layout.setColumnStretch(1, 2)
        reduccion_layout.setColumnStretch(2, 1)

        # Botón Método Escalonado
        self.boton_escalonado = QPushButton("Método Escalonado", self)
        self.boton_escalonado.setFixedSize(400, 50)
        self.boton_escalonado.clicked.connect(self.abrir_metodo_escalonado)
        reduccion_layout.addWidget(self.boton_escalonado, 0, 1, alignment=Qt.AlignCenter)

        # Botón Regla de Cramer
        self.boton_cramer = QPushButton("Regla de Cramer", self)
        self.boton_cramer.setFixedSize(400, 50)
        self.boton_cramer.clicked.connect(self.abrir_cramer)
        reduccion_layout.addWidget(self.boton_cramer, 1, 1, alignment=Qt.AlignCenter)

        # Botón Factorización LU
        self.boton_lu = QPushButton("Factorización LU", self)
        self.boton_lu.setFixedSize(400, 50)
        self.boton_lu.clicked.connect(self.abrir_lu)
        reduccion_layout.addWidget(self.boton_lu, 2, 1, alignment=Qt.AlignCenter)

        # Otros botones de matrices
        self.boton_suma_matrices = QPushButton("Suma de Matrices", self)
        self.boton_suma_matrices.setFixedSize(400, 50)
        self.boton_suma_matrices.clicked.connect(self.abrir_suma_matrices)
        self.layout.addWidget(self.boton_suma_matrices, 2, 1, alignment=Qt.AlignCenter)

        self.boton_multiplicacion_matrices = QPushButton("Multiplicación de Matrices", self)
        self.boton_multiplicacion_matrices.setFixedSize(400, 50)
        self.boton_multiplicacion_matrices.clicked.connect(self.abrir_multiplicacion_matrices)
        self.layout.addWidget(self.boton_multiplicacion_matrices, 3, 1, alignment=Qt.AlignCenter)

        self.boton_transpuesta = QPushButton("Transpuesta de Matriz", self)
        self.boton_transpuesta.setFixedSize(400, 50)
        self.boton_transpuesta.clicked.connect(self.abrir_transpuesta_matriz)
        self.layout.addWidget(self.boton_transpuesta, 4, 1, alignment=Qt.AlignCenter)

        self.boton_determinante = QPushButton("Calcular Determinante", self)
        self.boton_determinante.setFixedSize(400, 50)
        self.boton_determinante.clicked.connect(self.abrir_determinante)
        self.layout.addWidget(self.boton_determinante, 5, 1, alignment=Qt.AlignCenter)

        self.boton_inversa = QPushButton("Inversa de Matriz", self)
        self.boton_inversa.setFixedSize(400, 50)
        self.boton_inversa.clicked.connect(self.abrir_inversa_matriz)
        self.layout.addWidget(self.boton_inversa, 6, 1, alignment=Qt.AlignCenter)

        # Botón Regresar
        self.boton_regresar = QPushButton("Regresar", self)
        self.boton_regresar.setFixedSize(150, 40)
        self.boton_regresar.clicked.connect(self.close)
        # Agregar el botón al layout principal en la última fila, columna 0, alineado abajo a la izquierda
        self.layout.addWidget(self.boton_regresar, 8, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.showMaximized()

    def abrir_metodo_escalonado(self):
        self.ventana_escalonado = VentanaEscalonado(self.tamano_fuente)
        self.ventana_escalonado.show()
        self.cambiar_fuente_signal.connect(self.ventana_escalonado.actualizar_fuente_local)
        self.close()

    def abrir_suma_matrices(self):
        self.ventana_suma_matrices = VentanaSumaMatrices(self.tamano_fuente)
        self.ventana_suma_matrices.show()
        self.cambiar_fuente_signal.connect(self.ventana_suma_matrices.actualizar_fuente_local)
        self.close()

    def abrir_transpuesta_matriz(self):
        self.ventana_transpuesta = VentanaTranspuesta(self.tamano_fuente)
        self.ventana_transpuesta.show()
        self.cambiar_fuente_signal.connect(self.ventana_transpuesta.actualizar_fuente_local)
        self.close()

    def abrir_multiplicacion_matrices(self):
        self.ventana_multiplicacion = VentanaMultiplicacionMatrices(self.tamano_fuente)
        self.ventana_multiplicacion.show()
        self.cambiar_fuente_signal.connect(self.ventana_multiplicacion.actualizar_fuente_local)
        self.close()

    def abrir_determinante(self):
        self.ventana_determinante = VentanaDeterminante(self.tamano_fuente)
        self.ventana_determinante.show()
        self.cambiar_fuente_signal.connect(self.ventana_determinante.actualizar_fuente_local)
        self.close()

    def abrir_inversa_matriz(self):
        self.ventana_inversa = VentanaInversa(self.tamano_fuente)
        self.ventana_inversa.show()
        self.cambiar_fuente_signal.connect(self.ventana_inversa.actualizar_fuente_local)
        self.close()

    def abrir_cramer(self):
        self.ventana_cramer = VentanaCramer(self.tamano_fuente)
        self.ventana_cramer.show()
        self.cambiar_fuente_signal.connect(self.ventana_cramer.actualizar_fuente_local)
        self.close()

    def abrir_lu(self):
        self.ventana_lu = VentanaLU(self.tamano_fuente)
        self.ventana_lu.show()
        self.cambiar_fuente_signal.connect(self.ventana_lu.actualizar_fuente_local)
        self.close()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
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

    # menu vectores


class MenuVectores(QMainWindow):
    def __init__(self, tamano_fuente, cambiar_fuente_signal):
        super().__init__()
        self.setWindowTitle("Menú Vectores")
        self.setGeometry(150, 150, 600, 400)

        self.tamano_fuente = tamano_fuente
        self.cambiar_fuente_signal = cambiar_fuente_signal

        # Conectar la señal para cambiar la fuente
        self.cambiar_fuente_signal.connect(self.actualizar_fuente_local)

        # Widget principal
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout()
        self.main_widget.setLayout(self.layout)

        # Configurar estiramientos de columnas para centrar elementos
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 1)

        # Título
        self.label_titulo = QLabel("Operaciones con Vectores", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(24)
        fuente_titulo.setBold(True)  # El título principal en negrita
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo, 0, 0, 1, 3)

        # Botones de vectores
        self.boton_operaciones_vectores = QPushButton("Operaciones Combinadas de Vectores", self)
        self.boton_operaciones_vectores.setFixedSize(500, 50)
        self.boton_operaciones_vectores.clicked.connect(self.abrir_operaciones_vectoriales_combinadas)
        self.layout.addWidget(self.boton_operaciones_vectores, 1, 1, alignment=Qt.AlignCenter)

        self.boton_multiplicacion_vectores = QPushButton("Multiplicación Vector Fila por Vector Columna", self)
        self.boton_multiplicacion_vectores.setFixedSize(500, 50)
        self.boton_multiplicacion_vectores.clicked.connect(self.abrir_producto_vectorial)
        self.layout.addWidget(self.boton_multiplicacion_vectores, 2, 1, alignment=Qt.AlignCenter)

        self.boton_producto_matriz_vector = QPushButton("Producto Matriz por Vector", self)
        self.boton_producto_matriz_vector.setFixedSize(500, 50)
        self.boton_producto_matriz_vector.clicked.connect(self.abrir_producto_matriz_vector)
        self.layout.addWidget(self.boton_producto_matriz_vector, 3, 1, alignment=Qt.AlignCenter)

        # Botón Regresar
        self.boton_regresar = QPushButton("Regresar", self)
        self.boton_regresar.setFixedSize(150, 40)
        self.boton_regresar.clicked.connect(self.close)
        self.layout.addWidget(self.boton_regresar, 4, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Actualizar el estilo inicialmente
        self.actualizar_fuente_local(self.tamano_fuente)
        self.showMaximized()

    def abrir_producto_matriz_vector(self):
        self.ventana_producto_matriz_vector = VentanaProductoMatrizVector(self.tamano_fuente)
        self.ventana_producto_matriz_vector.show()
        self.cambiar_fuente_signal.connect(self.ventana_producto_matriz_vector.actualizar_fuente_local)
        self.close()

    def abrir_operaciones_vectoriales_combinadas(self):
        self.ventana_operaciones_combinadas = VentanaOperacionesCombinadas(self.tamano_fuente)
        self.ventana_operaciones_combinadas.show()
        self.cambiar_fuente_signal.connect(self.ventana_operaciones_combinadas.actualizar_fuente_local)
        self.close()

    def abrir_producto_vectorial(self):
        self.ventana_producto_vectorial = VentanaProductoVectorial(self.tamano_fuente)
        self.ventana_producto_vectorial.show()
        self.cambiar_fuente_signal.connect(self.ventana_producto_vectorial.actualizar_fuente_local)
        self.close()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
        self.setStyleSheet(f"""
            QPushButton {{
                font-size: {tamano}px;
                font-weight: normal;
                padding: 10px;
            }}
            QLabel {{
                font-size: {tamano + 2}px;
                font-weight: normal;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
                font-weight: normal;
            }}
        """)


class MenuAnalisisNumerico(QMainWindow):
    cambiar_fuente_signal = pyqtSignal(int)  # Signal to change the global font size

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú de Análisis Numérico")
        self.setGeometry(100, 100, 800, 600)

        self.tamano_fuente = 17  # Initial font size

        # Connect the signal to change the font
        self.cambiar_fuente_signal.connect(self.actualizar_fuente_local)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout()
        self.main_widget.setLayout(self.layout)

        # Configure column stretches to center elements
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 1)

        # Title
        self.label_titulo = QLabel("Análisis Numérico", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(28)
        fuente_titulo.setBold(True)  # Only the main title is bold
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo, 0, 0, 1, 3)

        # Bisection Method Button
        self.boton_biseccion = QPushButton("Método de Bisección", self)
        self.boton_biseccion.setFixedSize(400, 50)
        self.boton_biseccion.clicked.connect(self.abrir_metodo_biseccion)
        self.layout.addWidget(self.boton_biseccion, 1, 1, alignment=Qt.AlignCenter)

        # Newton-Raphson Method Button
        self.boton_newton_raphson = QPushButton("Método de Newton-Raphson", self)
        self.boton_newton_raphson.setFixedSize(400, 50)
        self.boton_newton_raphson.clicked.connect(self.abrir_metodo_newton_raphson)
        self.layout.addWidget(self.boton_newton_raphson, 2, 1, alignment=Qt.AlignCenter)

        # False Position Method Button
        self.boton_falsa_posicion = QPushButton("Método de Falsa Posición", self)
        self.boton_falsa_posicion.setFixedSize(400, 50)
        self.boton_falsa_posicion.clicked.connect(self.abrir_metodo_falsa_posicion)
        self.layout.addWidget(self.boton_falsa_posicion, 3, 1, alignment=Qt.AlignCenter)
        
        # Boton de metodo secante
        self.boton_secante = QPushButton("Método de la Secante", self)
        self.boton_secante.setFixedSize(400, 50)
        self.boton_secante.clicked.connect(self.abrir_metodo_secante)
        self.layout.addWidget(self.boton_secante, 4, 1, alignment=Qt.AlignCenter)
        
        botones_fuente_layout = QHBoxLayout()
        self.layout.addLayout(botones_fuente_layout, 6, 1, alignment=Qt.AlignCenter)

        self.boton_aumentar_fuente = QPushButton("Aumentar tamaño de fuente", self)
        self.boton_aumentar_fuente.clicked.connect(self.aumentar_tamano_fuente)
        botones_fuente_layout.addWidget(self.boton_aumentar_fuente)

        self.boton_disminuir_fuente = QPushButton("Disminuir tamaño de fuente", self)
        self.boton_disminuir_fuente.clicked.connect(self.disminuir_tamano_fuente)
        botones_fuente_layout.addWidget(self.boton_disminuir_fuente)

        # Back Button
        self.boton_regresar = QPushButton("Regresar", self)
        self.boton_regresar.setFixedSize(150, 40)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, 6, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Update the style
        self.actualizar_fuente_local(self.tamano_fuente)
        self.showMaximized()

    def regresar_menu_principal(self):
        # Abre el menú principal inicial y cierra el actual
        self.menu_principal = MenuPrincipal()
        self.menu_principal.show()
        self.close()

    def abrir_metodo_biseccion(self):
        # Abre la ventana del método de bisección
        self.ventana_biseccion = VentanaMetodoBiseccion(self.tamano_fuente)
        self.ventana_biseccion.show()
        self.close()

    def abrir_metodo_newton_raphson(self):
        # Abre la ventana del método de Newton-Raphson
        self.ventana_newton_raphson = VentanaMetodoNewtonRaphson(self.tamano_fuente)
        self.ventana_newton_raphson.show()
        self.close()
    
    def abrir_metodo_falsa_posicion(self):
        # Abre la ventana del método de falsa posición
        self.ventana_falsa_posicion = VentanaMetodoFalsaPosicion(self.tamano_fuente)
        self.ventana_falsa_posicion.show()
        self.close()
        
    def abrir_metodo_secante(self):
        # Abre la ventana del método de la secante
        self.ventana_secante = VentanaMetodoSecante(self.tamano_fuente)
        self.ventana_secante.show()
        self.close()

    def aumentar_tamano_fuente(self):
        self.tamano_fuente += 2
        self.cambiar_fuente_signal.emit(self.tamano_fuente)

    def disminuir_tamano_fuente(self):
        if self.tamano_fuente > 8:
            self.tamano_fuente -= 2
            self.cambiar_fuente_signal.emit(self.tamano_fuente)

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

class MenuCalculo(QMainWindow):
    cambiar_fuente_signal = pyqtSignal(int)  # Signal to change the global font size

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Cálculo")
        self.setGeometry(100, 100, 800, 600)

        self.tamano_fuente = 17  # Initial font size

        # Connect the signal to change the font
        self.cambiar_fuente_signal.connect(self.actualizar_fuente_local)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout()
        self.main_widget.setLayout(self.layout)

        # Configure column stretches to center elements
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 1)

        # Title
        self.label_titulo = QLabel("Cálculo", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(28)
        fuente_titulo.setBold(True)  # Only the main title is bold
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo, 0, 0, 1, 3)

        self.boton_integrales = QPushButton("Integrales", self)
        self.boton_integrales.setFixedSize(400, 50)
        self.boton_integrales.clicked.connect(self.abrir_integrales)
        self.layout.addWidget(self.boton_integrales, 1, 1, alignment=Qt.AlignCenter)

        self.boton_derivadas = QPushButton("Derivadas", self)
        self.boton_derivadas.setFixedSize(400, 50)
        self.boton_derivadas.clicked.connect(self.abrir_derivadas)
        self.layout.addWidget(self.boton_derivadas, 2, 1, alignment=Qt.AlignCenter)

        botones_fuente_layout = QHBoxLayout()
        self.layout.addLayout(botones_fuente_layout, 6, 1, alignment=Qt.AlignCenter)

        self.boton_aumentar_fuente = QPushButton("Aumentar tamaño de fuente", self)
        self.boton_aumentar_fuente.clicked.connect(self.aumentar_tamano_fuente)
        botones_fuente_layout.addWidget(self.boton_aumentar_fuente)

        self.boton_disminuir_fuente = QPushButton("Disminuir tamaño de fuente", self)
        self.boton_disminuir_fuente.clicked.connect(self.disminuir_tamano_fuente)
        botones_fuente_layout.addWidget(self.boton_disminuir_fuente)

        # Back Button
        self.boton_regresar = QPushButton("Regresar", self)
        self.boton_regresar.setFixedSize(150, 40)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, 6, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Update the style
        self.actualizar_fuente_local(self.tamano_fuente)
        self.showMaximized()

    def regresar_menu_principal(self):
        # Abre el menú principal inicial y cierra el actual
        self.menu_principal = MenuPrincipal()
        self.menu_principal.show()
        self.close()

    def abrir_integrales(self):
        self.ventana_integrales = VentanaCalculadoraIntegrales(self.tamano_fuente)
        self.ventana_integrales.show()
        self.close()

    def abrir_derivadas(self):
        self.ventana_derivadas = VentanaCalculadoraDerivadas(self.tamano_fuente)
        self.ventana_derivadas.show()
        self.close()


    def aumentar_tamano_fuente(self):
        self.tamano_fuente += 2
        self.cambiar_fuente_signal.emit(self.tamano_fuente)

    def disminuir_tamano_fuente(self):
        if self.tamano_fuente > 8:
            self.tamano_fuente -= 2
            self.cambiar_fuente_signal.emit(self.tamano_fuente)

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

def apply_stylesheet(app, style_path):
    with open(style_path, "r") as file:
        qss = file.read()
    app.setStyleSheet(qss)

def iniciar_menu():
    app = QApplication(sys.argv)
    apply_stylesheet(app, "themes.qss")
    fuente_base = QFont()
    fuente_base.setPointSize(17)
    app.setFont(fuente_base)
    
    ventana = MenuPrincipal()
    ventana.show()
    sys.exit(app.exec())