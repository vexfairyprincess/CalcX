# menu.py

from utils import evaluar_expresion

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QMessageBox, QFrame, QScrollArea, QTableWidget, QHeaderView,
    QTableWidgetItem, QSpacerItem, QSizePolicy, QGridLayout, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QFont, QPixmap
import sys
from Ventanas_menu import *
from analisisNumerico import *

class MenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.resize(800, 600)  # Resizable main window

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout(self.main_widget)

        # Image
        self.imagen_svg = QSvgWidget("calcXlogo.svg")  # Update this path
        self.imagen_svg.setFixedSize(350,150)  # Increase the height for a larger logo
        self.layout.addWidget(self.imagen_svg, 0, 1, 1, 1, Qt.AlignCenter)  # Center the logo in the grid

        # Buttons for Algebra and Analysis
        self.boton_algebra_lineal = QPushButton("Álgebra Lineal")
        self.boton_algebra_lineal.setFont(QFont('Arial', 12))  # Set font size
        self.boton_algebra_lineal.setFixedSize(400,50)
        self.boton_algebra_lineal.clicked.connect(self.abrir_menu_algebra_lineal)
        self.layout.addWidget(self.boton_algebra_lineal, 1, 0, 1, 3, Qt.AlignCenter)  # Center button under the logo

        self.boton_analisis_numerico = QPushButton("Análisis Numérico")
        self.boton_analisis_numerico.setFont(QFont('Arial', 12))  # Set font size
        self.boton_analisis_numerico.setFixedSize(400,50)  # Medium-sized button
        self.boton_analisis_numerico.clicked.connect(self.abrir_menu_analisis_numerico)
        self.layout.addWidget(self.boton_analisis_numerico, 2, 0, 1, 3, Qt.AlignCenter)  # Center button under the logo

        # Button to exit application
        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setFont(QFont('Arial', 12))
        self.boton_salir.setFixedSize(150,30)
        self.boton_salir.clicked.connect(self.close)
        self.layout.addWidget(self.boton_salir, 3, 0, 1, 1, Qt.AlignBottom | Qt.AlignLeft)  # Bottom left


    def abrir_menu_algebra_lineal(self):
        # Abre el menú de Álgebra Lineal
        self.menu_algebra_lineal = MenuAlgebra()
        self.menu_algebra_lineal.show()
        self.close()

    def abrir_menu_analisis_numerico(self):
        self.menu_analisis_numerico = MenuAnalisisNumerico()
        self.menu_analisis_numerico.show()
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

    #menu matrices

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
        fuente_titulo.setPointSize(28)
        fuente_titulo.setBold(True)
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo, 0, 0, 1, 3)

        # Grupo Reducción de Matrices
        self.group_reduccion = QGroupBox("Reducción de Matrices")
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

        self.boton_producto_matriz = QPushButton("Producto Matriz por Vector", self)
        self.boton_producto_matriz.setFixedSize(400, 50)
        self.boton_producto_matriz.clicked.connect(self.abrir_producto_matriz_vector)
        self.layout.addWidget(self.boton_producto_matriz, 7, 1, alignment=Qt.AlignCenter)

        # Botón Regresar
        self.boton_regresar = QPushButton("Regresar", self)
        self.boton_regresar.setFixedSize(150, 40)
        self.boton_regresar.clicked.connect(self.close)
        # Agregar el botón al layout principal en la última fila, columna 0, alineado abajo a la izquierda
        self.layout.addWidget(self.boton_regresar, 8, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)


    def abrir_metodo_escalonado(self):
        self.ventana_escalonado = VentanaEscalonado(self.tamano_fuente)
        self.ventana_escalonado.show()
        self.cambiar_fuente_signal.connect(self.ventana_escalonado.actualizar_fuente_local)
        self.close()

    def abrir_producto_matriz_vector(self):
        self.ventana_producto_matriz_vector = VentanaProductoMatrizVector(self.tamano_fuente)
        self.ventana_producto_matriz_vector.show()
        self.cambiar_fuente_signal.connect(self.ventana_producto_matriz_vector.actualizar_fuente_local)
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

    #menu vectores
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

        # Buttons to adjust the font size (optional)
        botones_fuente_layout = QHBoxLayout()
        self.layout.addLayout(botones_fuente_layout, 2, 1, alignment=Qt.AlignCenter)

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
        self.layout.addWidget(self.boton_regresar, 3, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Update the style
        self.actualizar_fuente_local(self.tamano_fuente)

    def regresar_menu_principal(self):
        # Abre el menú principal inicial y cierra el actual
        self.menu_principal = MenuPrincipal()
        self.menu_principal.show()
        self.close()

    def abrir_metodo_biseccion(self):
        # Abre la ventana del método de bisección
        self.ventana_biseccion = VentanaMetodoBiseccion()
        self.ventana_biseccion.show()
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

def iniciar_menu():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  
    fuente_base = QFont()
    fuente_base.setPointSize(17)
    app.setFont(fuente_base)
    
    ventana = MenuPrincipal()
    ventana.show()
    sys.exit(app.exec())