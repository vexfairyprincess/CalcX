# menu.py

from utils import evaluar_expresion
from menu import *

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QMessageBox, QFrame, QScrollArea, QTableWidget, QHeaderView,
    QTableWidgetItem, QSpacerItem, QSizePolicy, QGridLayout, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QFont, QPixmap
from matriz import Matriz
from vector import Vector
from matrizxvector import MxV
from analisisNumerico import VentanaMetodoBiseccion
import sys



class VentanaEscalonado(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Método Escalonado")
        self.setGeometry(50, 50, 1200, 800)
        self.tamano_fuente = tamano_fuente

        # Establecer estilo
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout Principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Título
        self.label_titulo = QLabel("Método Escalonado - Eliminación Gaussiana", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(self.tamano_fuente + 6)
        fuente_titulo.setBold(True)
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo)

        # Layout de Entrada de Datos
        self.layout_entrada = QHBoxLayout()
        self.layout.addLayout(self.layout_entrada)

        # Entrada para el número de ecuaciones
        self.label_ecuaciones = QLabel("Ecuaciones:", self)
        self.layout_entrada.addWidget(self.label_ecuaciones)
        self.input_ecuaciones = QLineEdit(self)
        self.input_ecuaciones.setFixedWidth(60)
        self.layout_entrada.addWidget(self.input_ecuaciones)

        # Entrada para el número de variables
        self.label_variables = QLabel("Variables:", self)
        self.layout_entrada.addWidget(self.label_variables)
        self.input_variables = QLineEdit(self)
        self.input_variables.setFixedWidth(60)
        self.layout_entrada.addWidget(self.input_variables)

        # Botón para crear la matriz
        self.boton_crear_matriz = QPushButton("Crear Matriz", self)
        self.boton_crear_matriz.setFixedWidth(150)
        self.boton_crear_matriz.clicked.connect(self.crear_matriz)
        self.layout_entrada.addWidget(self.boton_crear_matriz)

        # Espaciador
        self.layout_entrada.addStretch()

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(250)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout_entrada.addWidget(self.boton_regresar)

        # Layout para tabla y resultados
        self.layout_matriz_resultado = QHBoxLayout()
        self.layout.addLayout(self.layout_matriz_resultado)

        # Área de tabla para mostrar la matriz dentro de un QScrollArea
        self.scroll_area_tabla = QScrollArea(self)
        self.scroll_area_tabla.setWidgetResizable(True)
        self.tabla_matriz_widget = QWidget()
        self.tabla_matriz_layout = QVBoxLayout()
        self.tabla_matriz_widget.setLayout(self.tabla_matriz_layout)
        self.scroll_area_tabla.setWidget(self.tabla_matriz_widget)
        self.layout_matriz_resultado.addWidget(self.scroll_area_tabla)

        self.tabla_matriz = QTableWidget(self)
        self.tabla_matriz_layout.addWidget(self.tabla_matriz)

        # Ajustar la tabla
        self.tabla_matriz.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_matriz.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Espaciador
        self.layout_matriz_resultado.addStretch()

        # Área de resultados con estilo mejorado
        self.frame_resultado = QFrame(self)
        self.frame_resultado.setStyleSheet("""
            QFrame {
                border: 2px solid #B0BEC5;
                border-radius: 5px;
                background-color: #ECEFF1;
                padding: 10px;
                margin-top: 20px;
            }
        """)
        self.frame_resultado.setLayout(QVBoxLayout())
        self.texto_resultado = QTextEdit(self.frame_resultado)
        fuente_texto = QFont()
        fuente_texto.setPointSize(self.tamano_fuente)
        self.texto_resultado.setFont(fuente_texto)
        self.texto_resultado.setStyleSheet("background-color: #FAFAFA;")
        self.texto_resultado.setMinimumHeight(500)
        self.texto_resultado.setMinimumWidth(600)
        self.texto_resultado.setReadOnly(True)
        self.frame_resultado.layout().addWidget(self.texto_resultado)
        self.layout_matriz_resultado.addWidget(self.frame_resultado)

        # Botón para calcular
        self.boton_calcular = QPushButton("Calcular", self)
        self.boton_calcular.setFixedWidth(200)
        self.boton_calcular.clicked.connect(self.calcular_escalonado)
        self.layout.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Botón para mostrar paso a paso
        self.boton_paso_a_paso = QPushButton("Mostrar Solución Paso a Paso", self)
        self.boton_paso_a_paso.setFixedWidth(250)
        self.boton_paso_a_paso.clicked.connect(self.cambiar_modo)
        self.boton_paso_a_paso.hide()
        self.layout.addWidget(self.boton_paso_a_paso, alignment=Qt.AlignCenter)

        # Variable para almacenar los pasos
        self.resultado_pasos = ""
        self.resultado_final = ""
        self.modo_paso_a_paso = False
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
            QTableWidget QHeaderView::section {{
                background-color: #E0E0E0;
                padding: 4px;
                border: 1px solid #D0D0D0;
                font-size: {tamano}px;
            }}
            QTableWidget {{
                gridline-color: #D0D0D0;
            }}
        """)

    def crear_matriz(self):
        try:
            n = int(self.input_ecuaciones.text())
            m = int(self.input_variables.text())
            if n <= 0 or m <= 0:
                raise ValueError("El número de ecuaciones y variables debe ser positivo.")

            # Crear la tabla con n filas y m+1 columnas
            self.tabla_matriz.setRowCount(n)
            self.tabla_matriz.setColumnCount(m + 1)
            self.tabla_matriz.setHorizontalHeaderLabels([f"x{i + 1}" for i in range(m)] + ["Resultado"])

            # Ajustar el tamaño de las celdas
            self.tabla_matriz.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tabla_matriz.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def calcular_escalonado(self):
        try:
            n = self.tabla_matriz.rowCount()
            m = self.tabla_matriz.columnCount() - 1
            if n == 0 or m == 0:
                raise ValueError("Primero crea la matriz.")

            entradas = []
            for i in range(n):
                fila = []
                for j in range(m + 1):
                    item = self.tabla_matriz.item(i, j)
                    if item is None or not item.text():
                        raise ValueError(f"Introduce un valor válido en la posición ({i + 1}, {j + 1}).")
                    valor = evaluar_expresion(item.text())  # Evalúa la expresión
                    fila.append(valor)
                entradas.append(fila)

            matriz = Matriz(n, entradas)
            self.resultado_pasos = matriz.eliminacion_gaussiana()
            self.resultado_final = matriz.interpretar_resultado()
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
            self.boton_paso_a_paso.show()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def cambiar_modo(self):
        """Cambia entre mostrar solo el resultado o el paso a paso."""
        if self.modo_paso_a_paso:
            # Cambiar a mostrar solo el resultado
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
        else:
            # Cambiar a mostrar paso a paso
            self.texto_resultado.setText(self.resultado_pasos)
            self.boton_paso_a_paso.setText("Mostrar Solo Respuesta")
        # Alternar el modo
        self.modo_paso_a_paso = not self.modo_paso_a_paso

    def regresar_menu_principal(self):
        from menu import MenuMatrices
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()
        self.close()


class VentanaOperacionesCombinadas(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Operaciones Combinadas de Vectores")
        self.setGeometry(100, 100, 1200, 700)

        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Layout izquierdo para entrada de vectores y escalares
        self.layout_izquierdo = QVBoxLayout()
        self.layout.addLayout(self.layout_izquierdo)

        # Layout para Número de Vectores y Dimensión
        self.layout_entrada = QHBoxLayout()
        self.layout_izquierdo.addLayout(self.layout_entrada)

        # Número de Vectores
        self.label_vectores = QLabel("Número de Vectores:", self)
        self.layout_entrada.addWidget(self.label_vectores)
        self.input_vectores = QLineEdit(self)
        self.input_vectores.setFixedWidth(70)
        self.layout_entrada.addWidget(self.input_vectores)

        # Dimensión de los Vectores
        self.label_dimension = QLabel("Dimensión de los Vectores:", self)
        self.layout_entrada.addWidget(self.label_dimension)
        self.input_dimension = QLineEdit(self)
        self.input_dimension.setFixedWidth(70)
        self.layout_entrada.addWidget(self.input_dimension)

        # Botón Crear Entradas
        self.boton_crear_vectores = QPushButton("Crear Entradas", self)
        self.boton_crear_vectores.setFixedWidth(180)
        self.boton_crear_vectores.clicked.connect(self.crear_entradas_vectores)
        self.layout_entrada.addWidget(self.boton_crear_vectores)

        # Espaciador
        self.layout_entrada.addStretch()

        # Layout para Tablas de Vectores y Escalares
        self.layout_tablas = QVBoxLayout()
        self.layout_izquierdo.addLayout(self.layout_tablas)

        # Tabla para los vectores
        self.tabla_vectores = QTableWidget(self)
        self.tabla_vectores.setFixedWidth(400)
        self.tabla_vectores.setFixedHeight(250)
        self.layout_tablas.addWidget(self.tabla_vectores)

        # Tabla para los escalares
        self.tabla_escalars = QTableWidget(self)
        self.tabla_escalars.setFixedWidth(400)
        self.tabla_escalars.setFixedHeight(200)
        self.layout_tablas.addWidget(self.tabla_escalars)

        # Botón para calcular operación
        self.boton_calcular = QPushButton("Calcular Operación", self)
        self.boton_calcular.setFixedWidth(200)
        self.boton_calcular.clicked.connect(self.calcular_operacion)
        self.layout_tablas.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Área de resultados a la derecha con scroll y estilo mejorado
        self.layout_resultados = QVBoxLayout()
        self.layout.addLayout(self.layout_resultados)

        self.label_resultado = QLabel("Resultado de la Operación", self)
        self.label_resultado.setAlignment(Qt.AlignCenter)
        fuente_resultado = QFont()
        fuente_resultado.setPointSize(self.tamano_fuente + 2)
        self.label_resultado.setFont(fuente_resultado)
        self.layout_resultados.addWidget(self.label_resultado)

        # QScrollArea para contener el frame con los resultados
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout_resultados.addWidget(self.scroll_area)

        # Frame para contener el layout de resultado
        self.frame_resultado = QFrame(self)
        self.frame_resultado.setStyleSheet("""
            QFrame {
                border: 2px solid #B0BEC5;
                border-radius: 5px;
                background-color: #ECEFF1;
                padding: 10px;
                margin-top: 10px;
            }
        """)
        self.scroll_area.setWidget(self.frame_resultado)

        # Layout inicial para el frame de resultado
        self.frame_layout = QHBoxLayout()
        self.frame_resultado.setLayout(self.frame_layout)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(250)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout_resultados.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
            QTableWidget QHeaderView::section {{
                background-color: #E0E0E0;
                padding: 4px;
                border: 1px solid #D0D0D0;
                font-size: {tamano}px;
            }}
            QTableWidget {{
                gridline-color: #D0D0D0;
            }}
        """)

    def crear_entradas_vectores(self):
        try:
            numero_vectores = int(self.input_vectores.text())
            dimension = int(self.input_dimension.text())

            if numero_vectores <= 0 or dimension <= 0:
                raise ValueError("El número de vectores y la dimensión deben ser positivos.")

            # Configurar la tabla de vectores
            self.tabla_vectores.setRowCount(dimension)
            self.tabla_vectores.setColumnCount(numero_vectores)
            self.tabla_vectores.setHorizontalHeaderLabels([f"Vector {i + 1}" for i in range(numero_vectores)])
            self.tabla_vectores.setVerticalHeaderLabels([f"Componente {i + 1}" for i in range(dimension)])

            # Configurar la tabla de escalares
            self.tabla_escalars.setRowCount(numero_vectores)
            self.tabla_escalars.setColumnCount(1)
            self.tabla_escalars.setHorizontalHeaderLabels(["Escalar"])
            self.tabla_escalars.setVerticalHeaderLabels([f"Vector {i + 1}" for i in range(numero_vectores)])

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def calcular_operacion(self):
        try:
            numero_vectores = self.tabla_vectores.columnCount()
            dimension = self.tabla_vectores.rowCount()

            lista_vectores = []
            lista_escalars = []

            for i in range(numero_vectores):
                componentes = []
                for j in range(dimension):
                    item = self.tabla_vectores.item(j, i)
                    if item is None or not item.text():
                        raise ValueError(
                            f"Introduce un valor válido en la posición Vector {i + 1}, Componente {j + 1}.")
                    componentes.append(evaluar_expresion(item.text()))  # Evalúa la expresión
                vector = Vector.crear_vector_desde_entrada(componentes)
                lista_vectores.append(vector)

                # Obtener el escalar correspondiente
                item_escalar = self.tabla_escalars.item(i, 0)
                if item_escalar is None or not item_escalar.text():
                    raise ValueError(f"Introduce un escalar válido para el Vector {i + 1}.")
                escalar = evaluar_expresion(item_escalar.text())  # Evalúa la expresión
                lista_escalars.append(escalar)

            resultado = Vector.suma_escalada(lista_vectores, lista_escalars)

            # Limpiar el layout anterior de manera segura
            while self.frame_layout.count():
                child = self.frame_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Formatear la operación en un layout horizontal para mostrarla de izquierda a derecha
            for escalar, vector in zip(lista_escalars, lista_vectores):
                # Crear QLabel para el escalar
                label_escalar = QLabel(f"{escalar} *", self)
                label_escalar.setAlignment(Qt.AlignCenter)
                label_escalar.setStyleSheet("""
                    font-size: 18px;
                    background-color: #FFFFFF;
                    padding: 5px;
                    border-radius: 5px;
                """)
                self.frame_layout.addWidget(label_escalar)

                # Crear QLabel para el vector vertical
                vector_str = "\n".join([f"[{x}]" for x in vector.componentes])
                label_vector = QLabel(vector_str, self)
                label_vector.setAlignment(Qt.AlignCenter)
                label_vector.setStyleSheet("""
                    font-size: 18px;
                    border: 1px solid #B0BEC5;
                    background-color: #FFFFFF;
                    padding: 5px;
                    border-radius: 5px;
                """)
                self.frame_layout.addWidget(label_vector)

                # Agregar el símbolo de suma
                label_suma = QLabel(" + ", self)
                label_suma.setAlignment(Qt.AlignCenter)
                label_suma.setStyleSheet("""
                    font-size: 18px;
                    background-color: #FFFFFF;
                    padding: 5px;
                    border-radius: 5px;
                """)
                self.frame_layout.addWidget(label_suma)

            # Remover el último símbolo de suma
            if self.frame_layout.count() > 0:
                item = self.frame_layout.takeAt(self.frame_layout.count() - 1)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # Agregar el símbolo de igual y el resultado
            label_igual = QLabel(" = ", self)
            label_igual.setAlignment(Qt.AlignCenter)
            label_igual.setStyleSheet("""
                font-size: 18px;
                background-color: #FFFFFF;
                padding: 5px;
                border-radius: 5px;
            """)
            self.frame_layout.addWidget(label_igual)

            # Crear QLabel para el resultado
            resultado_str = "\n".join([f"[{x:.2f}]" for x in resultado.componentes])
            label_resultado = QLabel(resultado_str, self)
            label_resultado.setAlignment(Qt.AlignCenter)
            label_resultado.setStyleSheet("""
                font-size: 18px;
                border: 1px solid #B0BEC5;
                background-color: #FFFFFF;
                padding: 5px;
                border-radius: 5px;
            """)
            self.frame_layout.addWidget(label_resultado)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def regresar_menu_principal(self):
        from menu import MenuVectores
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_vectores = MenuVectores(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_vectores.show()
        self.close()


class VentanaProductoVectorial(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Multiplicación de Vector Fila por Vector Columna")
        self.setGeometry(100, 100, 1200, 700)  # Tamaño de la ventana principal
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Layout superior para entrada de dimensión y creación de vectores
        self.layout_superior = QHBoxLayout()
        self.layout.addLayout(self.layout_superior)

        self.label_dimension = QLabel("Dimensión del Vector:", self)
        self.layout_superior.addWidget(self.label_dimension)
        self.input_dimension = QLineEdit(self)
        self.input_dimension.setPlaceholderText("Ejemplo: 3")
        self.input_dimension.setFixedWidth(200)
        self.layout_superior.addWidget(self.input_dimension)

        self.boton_crear_vectores = QPushButton("Crear Vectores", self)
        self.boton_crear_vectores.setFixedWidth(150)
        self.boton_crear_vectores.clicked.connect(self.crear_vectores)
        self.layout_superior.addWidget(self.boton_crear_vectores)

        # Layout para las tablas de vectores fila y columna
        self.layout_vectores = QVBoxLayout()  # Cambiado a QVBoxLayout para apilarlos verticalmente
        self.layout.addLayout(self.layout_vectores)

        # Tabla para el vector fila
        self.tabla_vector_fila = QTableWidget(self)
        self.tabla_vector_fila.setFixedWidth(500)  # Ajuste del tamaño
        self.tabla_vector_fila.setFixedHeight(70)  # Ajuste del tamaño
        self.tabla_vector_fila.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_vectores.addWidget(self.tabla_vector_fila)

        # Tabla para el vector columna
        self.tabla_vector_columna = QTableWidget(self)
        self.tabla_vector_columna.setFixedWidth(200)  # Ajuste del tamaño
        self.tabla_vector_columna.setFixedHeight(250)  # Ajuste del tamaño
        self.tabla_vector_columna.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_vectores.addWidget(self.tabla_vector_columna)

        # Layout para los botones
        self.layout_botones = QHBoxLayout()
        self.layout.addLayout(self.layout_botones)

        # Botón para calcular el producto escalar
        self.boton_calcular = QPushButton("Calcular Producto", self)
        self.boton_calcular.setFixedWidth(200)
        self.boton_calcular.clicked.connect(self.calcular_producto)
        self.layout_botones.addWidget(self.boton_calcular, alignment=Qt.AlignLeft)  # Mantiene su posición en X

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(250)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout_botones.addWidget(self.boton_regresar, alignment=Qt.AlignRight)  # Mantiene su posición en X

        # Layout derecho para resultados
        self.layout_resultados = QVBoxLayout()
        self.layout.addLayout(self.layout_resultados)

        self.label_resultado = QLabel("Resultado del Producto Escalar", self)
        self.label_resultado.setAlignment(Qt.AlignCenter)
        fuente_resultado = QFont()
        fuente_resultado.setPointSize(self.tamano_fuente + 2)
        self.label_resultado.setFont(fuente_resultado)
        self.layout_resultados.addWidget(self.label_resultado)

        # Área de resultados
        self.area_resultados = QTextEdit(self)
        self.area_resultados.setFixedHeight(250)
        self.area_resultados.setReadOnly(True)
        self.layout_resultados.addWidget(self.area_resultados)
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
            QTableWidget QHeaderView::section {{
                background-color: #E0E0E0;
                padding: 4px;
                border: 1px solid #D0D0D0;
                font-size: {tamano}px;
            }}
            QTableWidget {{
                gridline-color: #D0D0D0;
            }}
        """)

    def crear_vectores(self):
        try:
            dimension = int(self.input_dimension.text())
            if dimension <= 0:
                raise ValueError("La dimensión debe ser un número positivo.")

            # Configurar tabla para el vector fila
            self.tabla_vector_fila.setRowCount(1)
            self.tabla_vector_fila.setColumnCount(dimension)
            self.tabla_vector_fila.setHorizontalHeaderLabels([f"Componente {i + 1}" for i in range(dimension)])
            self.tabla_vector_fila.setVerticalHeaderLabels(["Vector Fila"])

            # Ajustar tamaño de la tabla de vector fila
            self.tabla_vector_fila.setFixedWidth(600)  # Aumentar el ancho para mostrar componentes completos
            self.tabla_vector_fila.setFixedHeight(80)  # Ajustar la altura para que se vea bien

            # Configurar tabla para el vector columna
            self.tabla_vector_columna.setRowCount(dimension)
            self.tabla_vector_columna.setColumnCount(1)
            self.tabla_vector_columna.setHorizontalHeaderLabels(["Vector Columna"])
            self.tabla_vector_columna.setVerticalHeaderLabels([f"Componente {i + 1}" for i in range(dimension)])

            # Ajustar tamaño de la tabla de vector columna
            self.tabla_vector_columna.setFixedWidth(300)  # Ajuste de ancho
            self.tabla_vector_columna.setFixedHeight(
                100 + (dimension * 30))  # Ajuste de altura dinámica según dimensión

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def calcular_producto(self):
        try:
            dimension = self.tabla_vector_fila.columnCount()
            vector_fila = []
            vector_columna = []

            for i in range(dimension):
                item = self.tabla_vector_fila.item(0, i)
                if item is None or not item.text():
                    raise ValueError(f"Introduce un valor válido en la posición Vector Fila, Componente {i + 1}.")
                vector_fila.append(evaluar_expresion(item.text()))  # Evalúa la expresión

            for i in range(dimension):
                item = self.tabla_vector_columna.item(i, 0)
                if item is None or not item.text():
                    raise ValueError(f"Introduce un valor válido en la posición Vector Columna, Componente {i + 1}.")
                vector_columna.append(evaluar_expresion(item.text()))  # Evalúa la expresión

            vector_obj_fila = Vector(vector_fila)
            vector_obj_columna = Vector(vector_columna)
            producto = vector_obj_fila.producto_punto(vector_obj_columna)

            # Mostrar el resultado en el área de resultados
            self.area_resultados.clear()
            resultado_texto = "Producto Escalar:\n\n" + \
                              "Vector Fila: " + str(vector_fila) + "\n\n" + \
                              "Vector Columna:\n" + "\n".join([f"[{x}]" for x in vector_columna]) + "\n\n" + \
                              f"Resultado: {producto:.2f}"
            self.area_resultados.setText(resultado_texto)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def regresar_menu_principal(self):
        from menu import MenuVectores
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_vectores = MenuVectores(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_vectores.show()
        self.close()


class VentanaProductoMatrizVector(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Producto Matriz por Vector (Propiedad A(u + v))")
        self.setGeometry(100, 100, 1000, 700)
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Título
        self.label_titulo = QLabel("Producto Matriz por Vector y Propiedad A(u + v)", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(self.tamano_fuente + 4)
        fuente_titulo.setBold(True)
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo)

        # Layout de entrada de datos
        self.layout_entrada = QVBoxLayout()
        self.layout.addLayout(self.layout_entrada)

        # Configurar tabla para la matriz
        self.tabla_matriz = QTableWidget(self)
        self.layout_entrada.addWidget(self.tabla_matriz)

        # Configurar tablas para los vectores
        self.layout_vectores = QHBoxLayout()
        self.tabla_vector_u = QTableWidget(self)
        self.tabla_vector_u.setFixedWidth(300)
        self.tabla_vector_u.setFixedHeight(250)
        self.tabla_vector_u.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_vectores.addWidget(self.tabla_vector_u)

        self.tabla_vector_v = QTableWidget(self)
        self.tabla_vector_v.setFixedWidth(300)
        self.tabla_vector_v.setFixedHeight(250)
        self.tabla_vector_v.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_vectores.addWidget(self.tabla_vector_v)

        self.layout_entrada.addLayout(self.layout_vectores)

        # Layout para el botón de creación de matriz y vectores
        self.layout_botones = QHBoxLayout()
        self.layout.addLayout(self.layout_botones)

        # Entrada para tamaño de matriz
        self.input_filas = QLineEdit(self)
        self.input_filas.setPlaceholderText("Filas de la Matriz")
        self.input_filas.setFixedWidth(150)
        self.layout_botones.addWidget(self.input_filas)

        self.input_columnas = QLineEdit(self)
        self.input_columnas.setPlaceholderText("Columnas de la Matriz")
        self.input_columnas.setFixedWidth(150)
        self.layout_botones.addWidget(self.input_columnas)

        # Botón para crear la matriz y vectores
        self.boton_crear = QPushButton("Crear Matriz y Vectores", self)
        self.boton_crear.clicked.connect(self.crear_matriz_vectores)
        self.layout_botones.addWidget(self.boton_crear)

        # Botón para calcular
        self.boton_calcular = QPushButton("Aplicar Propiedad A(u + v)", self)
        self.boton_calcular.clicked.connect(self.aplicar_propiedad)
        self.layout.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Área de resultados
        self.area_resultados = QTextEdit(self)
        self.area_resultados.setReadOnly(True)
        self.layout.addWidget(self.area_resultados)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
            QTableWidget QHeaderView::section {{
                background-color: #E0E0E0;
                padding: 4px;
                border: 1px solid #D0D0D0;
                font-size: {tamano}px;
            }}
            QTableWidget {{
                gridline-color: #D0D0D0;
            }}
        """)

    def crear_matriz_vectores(self):
        try:
            filas = int(self.input_filas.text())
            columnas = int(self.input_columnas.text())

            if filas <= 0 or columnas <= 0:
                raise ValueError("El número de filas y columnas debe ser positivo.")

            # Crear tabla de matriz
            self.tabla_matriz.setRowCount(filas)
            self.tabla_matriz.setColumnCount(columnas)
            self.tabla_matriz.setHorizontalHeaderLabels([f"Columna {i + 1}" for i in range(columnas)])
            self.tabla_matriz.setVerticalHeaderLabels([f"Fila {i + 1}" for i in range(filas)])

            # Crear tabla para los vectores u y v
            self.tabla_vector_u.setRowCount(columnas)
            self.tabla_vector_u.setColumnCount(1)
            self.tabla_vector_u.setHorizontalHeaderLabels(["Vector u"])
            self.tabla_vector_u.setVerticalHeaderLabels([f"Componente {i + 1}" for i in range(columnas)])

            self.tabla_vector_v.setRowCount(columnas)
            self.tabla_vector_v.setColumnCount(1)
            self.tabla_vector_v.setHorizontalHeaderLabels(["Vector v"])
            self.tabla_vector_v.setVerticalHeaderLabels([f"Componente {i + 1}" for i in range(columnas)])

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def aplicar_propiedad(self):
        try:
            filas = self.tabla_matriz.rowCount()
            columnas = self.tabla_matriz.columnCount()

            matriz = []
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    item = self.tabla_matriz.item(i, j)
                    if item is None or not item.text():
                        raise ValueError(f"Introduce un valor válido en la posición ({i + 1}, {j + 1}) de la matriz.")
                    fila.append(evaluar_expresion(item.text()))  # Evalúa la expresión
                matriz.append(fila)

            vector_u = []
            for i in range(columnas):
                item = self.tabla_vector_u.item(i, 0)
                if item is None or not item.text():
                    raise ValueError(f"Introduce un valor válido en la posición ({i + 1}) del vector u.")
                vector_u.append(evaluar_expresion(item.text()))  # Evalúa la expresión

            vector_v = []
            for i in range(columnas):
                item = self.tabla_vector_v.item(i, 0)
                if item is None or not item.text():
                    raise ValueError(f"Introduce un valor válido en la posición ({i + 1}) del vector v.")
                vector_v.append(evaluar_expresion(item.text()))  # Evalúa la expresión

            mxv = MxV(matriz=matriz, vectores=[vector_u, vector_v])
            Au, Av, A_u_plus_v = mxv.aplicar_propiedad()

            # Calcular suma u + v
            u_plus_v = [vector_u[i] + vector_v[i] for i in range(len(vector_u))]

            # Calcular Au + Av
            Au_plus_Av = [Au[i] + Av[i] for i in range(len(Au))]

            # Determinar si la propiedad se cumple
            conclusion = ""
            if Au_plus_Av == A_u_plus_v:
                conclusion = "La propiedad A(u + v) = Au + Av se cumple."
            else:
                conclusion = "La propiedad A(u + v) = Au + Av no se cumple."

            # Mostrar resultados
            resultado_texto = f"Matriz A:\n{self.formatear_matriz(matriz)}\n\n"
            resultado_texto += f"Vector u:\n{self.formatear_vector(vector_u)}\n\n"
            resultado_texto += f"Vector v:\n{self.formatear_vector(vector_v)}\n\n"
            resultado_texto += f"u + v:\n{self.formatear_vector(u_plus_v)}\n\n"

            resultado_texto += "Pasos para calcular Au:\n"
            for i in range(len(Au)):
                pasos_Au = " + ".join([f"{matriz[i][j]}*{vector_u[j]}" for j in range(len(vector_u))])
                resultado_texto += f"A[{i + 1}]u = {pasos_Au} = {Au[i]:.2f}\n"

            resultado_texto += "\nPasos para calcular Av:\n"
            for i in range(len(Av)):
                pasos_Av = " + ".join([f"{matriz[i][j]}*{vector_v[j]}" for j in range(len(vector_v))])
                resultado_texto += f"A[{i + 1}]v = {pasos_Av} = {Av[i]:.2f}\n"

            resultado_texto += "\nPasos para calcular A(u + v):\n"
            for i in range(len(A_u_plus_v)):
                pasos_A_u_v = " + ".join([f"{matriz[i][j]}*{u_plus_v[j]}" for j in range(len(u_plus_v))])
                resultado_texto += f"A[{i + 1}](u + v) = {pasos_A_u_v} = {A_u_plus_v[i]:.2f}\n"

            resultado_texto += f"\nAu:\n{self.formatear_vector(Au)}\n"
            resultado_texto += f"Av:\n{self.formatear_vector(Av)}\n"
            resultado_texto += f"Au + Av:\n{self.formatear_vector(Au_plus_Av)}\n"
            resultado_texto += f"A(u + v):\n{self.formatear_vector(A_u_plus_v)}\n"

            # Mostrar la conclusión final
            resultado_texto += f"\nConclusión:\n{conclusion}"

            self.area_resultados.setText(resultado_texto)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def formatear_vector(self, vector):
        """Convierte un vector (lista) en una representación vertical."""
        return "\n".join([f"[{val:.2f}]" for val in vector])

    def formatear_matriz(self, matriz):
        """Convierte una lista de listas en una representación de cadena para la matriz."""
        return "\n".join(["\t".join([f"{val:.2f}" for val in fila]) for fila in matriz])

    def regresar_menu_principal(self):
        from menu import MenuVectores
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_vectores = MenuVectores(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_vectores.show()
        self.close()


class VentanaSumaMatrices(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Suma de Matrices")
        self.setGeometry(100, 100, 800, 600)
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Layout para entrada de número de matrices, filas y columnas
        self.layout_entrada = QHBoxLayout()
        self.layout.addLayout(self.layout_entrada)

        # Número de matrices
        self.label_matrices = QLabel("Número de Matrices:", self)
        self.layout_entrada.addWidget(self.label_matrices)
        self.input_matrices = QLineEdit(self)
        self.input_matrices.setFixedWidth(70)
        self.layout_entrada.addWidget(self.input_matrices)

        # Número de filas
        self.label_filas = QLabel("Número de Filas:", self)
        self.layout_entrada.addWidget(self.label_filas)
        self.input_filas = QLineEdit(self)
        self.input_filas.setFixedWidth(70)
        self.layout_entrada.addWidget(self.input_filas)

        # Número de columnas
        self.label_columnas = QLabel("Número de Columnas:", self)
        self.layout_entrada.addWidget(self.label_columnas)
        self.input_columnas = QLineEdit(self)
        self.input_columnas.setFixedWidth(70)
        self.layout_entrada.addWidget(self.input_columnas)

        # Botón Crear Matrices
        self.boton_crear_matrices = QPushButton("Crear Entradas", self)
        self.boton_crear_matrices.setFixedWidth(180)
        self.boton_crear_matrices.clicked.connect(self.crear_entradas_matrices)
        self.layout_entrada.addWidget(self.boton_crear_matrices)

        # Espaciador
        self.layout_entrada.addStretch()

        # Layout para las tablas de matrices y escalares
        self.layout_tablas = QVBoxLayout()
        self.layout.addLayout(self.layout_tablas)

        # Tabla para las matrices
        self.tabla_matrices = QTableWidget(self)
        self.tabla_matrices.setFixedWidth(600)
        self.tabla_matrices.setFixedHeight(300)
        self.layout_tablas.addWidget(self.tabla_matrices)

        # Tabla para los escalares
        self.tabla_escalares = QTableWidget(self)
        self.tabla_escalares.setFixedWidth(200)
        self.tabla_escalares.setFixedHeight(200)
        self.layout_tablas.addWidget(self.tabla_escalares)

        # Layout para los botones de cálculo y paso a paso
        self.layout_botones = QHBoxLayout()
        self.layout.addLayout(self.layout_botones)

        # Botón para calcular la suma
        self.boton_calcular = QPushButton("Calcular Suma", self)
        self.boton_calcular.setFixedWidth(200)
        self.boton_calcular.clicked.connect(self.calcular_suma)
        self.layout_botones.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Botón para alternar vista de paso a paso y solo resultado
        self.boton_paso_a_paso = QPushButton("Mostrar Solución Paso a Paso", self)
        self.boton_paso_a_paso.setFixedWidth(250)
        self.boton_paso_a_paso.clicked.connect(self.cambiar_modo)
        self.boton_paso_a_paso.hide()
        self.layout_botones.addWidget(self.boton_paso_a_paso, alignment=Qt.AlignCenter)

        # Área de resultados de estilo horizontal
        self.texto_resultado = QTextEdit(self)
        self.texto_resultado.setReadOnly(True)
        self.texto_resultado.setStyleSheet("background-color: #FAFAFA; padding: 10px;")
        self.texto_resultado.setMinimumHeight(250)
        self.layout.addWidget(self.texto_resultado)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(250)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

        # Variables para almacenar los pasos
        self.resultado_pasos = ""
        self.resultado_final = ""
        self.modo_paso_a_paso = False
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
            QTableWidget QHeaderView::section {{
                background-color: #E0E0E0;
                padding: 4px;
                border: 1px solid #D0D0D0;
                font-size: {tamano}px;
            }}
            QTableWidget {{
                gridline-color: #D0D0D0;
            }}
        """)

    def cambiar_modo(self):
        """Cambia entre mostrar solo el resultado o el paso a paso."""
        if self.modo_paso_a_paso:
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
        else:
            self.texto_resultado.setText(self.resultado_pasos)
            self.boton_paso_a_paso.setText("Mostrar Solo Respuesta")
        self.modo_paso_a_paso = not self.modo_paso_a_paso

    def crear_entradas_matrices(self):
        try:
            numero_matrices = int(self.input_matrices.text())
            filas = int(self.input_filas.text())
            columnas = int(self.input_columnas.text())

            if numero_matrices <= 0 or filas <= 0 or columnas <= 0:
                raise ValueError("El número de matrices, filas y columnas deben ser positivos.")

            # Configurar la tabla de matrices
            self.tabla_matrices.setRowCount(filas * numero_matrices)
            self.tabla_matrices.setColumnCount(columnas)
            self.tabla_matrices.setHorizontalHeaderLabels([f"Columna {i + 1}" for i in range(columnas)])
            self.tabla_matrices.setVerticalHeaderLabels(
                [f"Matriz {i // filas + 1}, Fila {i % filas + 1}" for i in range(filas * numero_matrices)])

            # Configurar la tabla de escalares
            self.tabla_escalares.setRowCount(numero_matrices)
            self.tabla_escalares.setColumnCount(1)
            self.tabla_escalares.setHorizontalHeaderLabels(["Escalar"])
            self.tabla_escalares.setVerticalHeaderLabels([f"Matriz {i + 1}" for i in range(numero_matrices)])

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def calcular_suma(self):
        try:
            numero_matrices = int(self.input_matrices.text())
            filas = int(self.input_filas.text())
            columnas = int(self.input_columnas.text())
            lista_matrices = []
            lista_escalares = []

            # Captura las matrices y escalares de la interfaz
            for m in range(numero_matrices):
                matriz = []
                for i in range(filas):
                    fila = []
                    for j in range(columnas):
                        item = self.tabla_matrices.item(m * filas + i, j)
                        if item is None or not item.text():
                            raise ValueError(
                                f"Introduce un valor válido en la posición Matriz {m + 1}, Fila {i + 1}, Columna {j + 1}.")
                        fila.append(evaluar_expresion(item.text()))  # Evalúa la expresión
                    matriz.append(fila)
                lista_matrices.append(Matriz(filas, matriz))
                item_escalar = self.tabla_escalares.item(m, 0)
                if item_escalar is None or not item_escalar.text():
                    raise ValueError(f"Introduce un escalar válido para la Matriz {m + 1}.")
                lista_escalares.append(evaluar_expresion(item_escalar.text()))  # Evalúa el escalar

            # Procesar la suma de matrices
            resultado = Matriz(filas, [[0] * columnas for _ in range(filas)])
            pasos = "Proceso de Suma de Matrices:\n\n"
            for index, (matriz, escalar) in enumerate(zip(lista_matrices, lista_escalares), 1):
                matriz_escalada = matriz.escalar_por_matriz(escalar)
                resultado = resultado.suma(matriz_escalada)
                pasos += f"Paso {index}: {escalar} * Matriz {index}\n"
                pasos += self.formatear_matriz(matriz_escalada.matriz) + "\n\n"
                pasos += f"Resultado parcial:\n{self.formatear_matriz(resultado.matriz)}\n\n"

            # Almacenar resultado final y mostrarlo
            self.resultado_final = f"Resultado final:\n{self.formatear_matriz(resultado.matriz)}"
            self.resultado_pasos = pasos + "\n" + self.resultado_final
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.show()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def formatear_matriz(self, matriz):
        """Convierte la matriz en un formato de texto tabular legible"""
        texto_matriz = ""
        for fila in matriz:
            texto_matriz += "  ".join(f"{val:.2f}" for val in fila) + "\n"
        return texto_matriz

    def regresar_menu_principal(self):
        from menu import MenuMatrices
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()
        self.close()


class VentanaTranspuesta(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Transpuesta de la Matriz")

        # Ajustar el tamaño de la ventana
        self.setGeometry(100, 100, 1200, 700)

        # Fuente
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Layout para entrada de filas y columnas
        self.layout_entrada = QHBoxLayout()
        self.layout.addLayout(self.layout_entrada)

        # Número de filas
        self.label_filas = QLabel("Número de Filas:", self)
        self.layout_entrada.addWidget(self.label_filas)
        self.input_filas = QLineEdit(self)
        self.input_filas.setFixedWidth(70)
        self.layout_entrada.addWidget(self.input_filas)

        # Número de columnas
        self.label_columnas = QLabel("Número de Columnas:", self)
        self.layout_entrada.addWidget(self.label_columnas)
        self.input_columnas = QLineEdit(self)
        self.input_columnas.setFixedWidth(70)
        self.layout_entrada.addWidget(self.input_columnas)

        # Botón Crear Matriz
        self.boton_crear_matriz = QPushButton("Crear Matriz", self)
        self.boton_crear_matriz.setFixedWidth(180)
        self.boton_crear_matriz.clicked.connect(self.crear_matriz)
        self.layout_entrada.addWidget(self.boton_crear_matriz)

        # Espaciador
        self.layout_entrada.addStretch()

        # Área para tabla de la matriz
        self.tabla_matriz = QTableWidget(self)
        self.tabla_matriz.setFixedWidth(600)
        self.tabla_matriz.setFixedHeight(300)
        self.layout.addWidget(self.tabla_matriz)

        # Botón para calcular la transpuesta
        self.boton_calcular_transpuesta = QPushButton("Calcular Transpuesta")
        self.boton_calcular_transpuesta.clicked.connect(self.calcular_transpuesta)
        self.layout.addWidget(self.boton_calcular_transpuesta, alignment=Qt.AlignCenter)

        # Área de resultados
        self.texto_resultado = QTextEdit(self)
        self.texto_resultado.setReadOnly(True)
        self.texto_resultado.setStyleSheet("background-color: #FAFAFA; padding: 10px;")
        self.texto_resultado.setMinimumHeight(250)
        self.layout.addWidget(self.texto_resultado)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(250)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
        """)

    def crear_matriz(self):
        try:
            filas = int(self.input_filas.text())
            columnas = int(self.input_columnas.text())

            # Configuración de la tabla de matriz
            self.tabla_matriz.setRowCount(filas)
            self.tabla_matriz.setColumnCount(columnas)
            self.tabla_matriz.setHorizontalHeaderLabels([f"Columna {i + 1}" for i in range(columnas)])
            self.tabla_matriz.setVerticalHeaderLabels([f"Fila {i + 1}" for i in range(filas)])

        except ValueError:
            QMessageBox.critical(self, "Error", "Introduce valores válidos para filas y columnas.")

    def calcular_transpuesta(self):
        try:
            filas = self.tabla_matriz.rowCount()
            columnas = self.tabla_matriz.columnCount()

            matriz = []
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    item = self.tabla_matriz.item(i, j)
                    if item is None or not item.text():
                        raise ValueError(f"Introduce un valor válido en la posición ({i + 1}, {j + 1}).")
                    fila.append(evaluar_expresion(item.text()))  # Evalúa la expresión
                matriz.append(fila)

            matriz_obj = Matriz(filas, matriz)
            matriz_transpuesta = matriz_obj.calcular_transpuesta()
            self.texto_resultado.setText("Matriz Transpuesta:\n" + matriz_transpuesta.formatear_matriz())

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def regresar_menu_principal(self):
        from menu import MenuMatrices
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()
        self.close()


class VentanaMultiplicacionMatrices(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Multiplicación de Matrices")

        # Tamaño inicial redimensionable
        self.resize(800, 600)

        # Fuente
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Layout para entrada de número de matrices
        self.layout_entrada = QHBoxLayout()
        self.layout.addLayout(self.layout_entrada)

        # Número de matrices
        self.label_matrices = QLabel("Número de Matrices:", self)
        self.layout_entrada.addWidget(self.label_matrices)
        self.input_matrices = QLineEdit(self)
        self.input_matrices.setFixedWidth(70)
        self.layout_entrada.addWidget(self.input_matrices)

        # Botón Crear Entradas
        self.boton_crear_matrices = QPushButton("Crear Entradas", self)
        self.boton_crear_matrices.setFixedWidth(180)
        self.boton_crear_matrices.clicked.connect(self.crear_entradas_matrices)
        self.layout_entrada.addWidget(self.boton_crear_matrices)

        # Espaciador
        self.layout_entrada.addStretch()

        # Área de matrices
        self.scroll_area_matrices = QScrollArea(self)
        self.scroll_area_matrices.setWidgetResizable(True)
        self.widget_matrices = QWidget()
        self.layout_matrices = QVBoxLayout()
        self.widget_matrices.setLayout(self.layout_matrices)
        self.scroll_area_matrices.setWidget(self.widget_matrices)
        self.layout.addWidget(self.scroll_area_matrices)

        # Botones de validación y cálculo
        self.layout_botones = QHBoxLayout()
        self.layout.addLayout(self.layout_botones)

        # Botón para confirmar validez
        self.boton_confirmar_validez = QPushButton("Confirmar Validez")
        self.boton_confirmar_validez.clicked.connect(self.verificar_dimensiones)
        self.layout_botones.addWidget(self.boton_confirmar_validez, alignment=Qt.AlignCenter)

        # Botón para calcular el producto
        self.boton_calcular_producto = QPushButton("Calcular Producto")
        self.boton_calcular_producto.clicked.connect(self.calcular_producto)
        self.boton_calcular_producto.setEnabled(False)  # Deshabilitado hasta que se confirme la validez
        self.layout_botones.addWidget(self.boton_calcular_producto, alignment=Qt.AlignCenter)

        # Botón para alternar vista de paso a paso y solo resultado
        self.boton_paso_a_paso = QPushButton("Mostrar Solución Paso a Paso")
        self.boton_paso_a_paso.clicked.connect(self.cambiar_modo)
        self.boton_paso_a_paso.hide()
        self.layout_botones.addWidget(self.boton_paso_a_paso, alignment=Qt.AlignCenter)

        # Área de resultados
        self.texto_resultado = QTextEdit(self)
        self.texto_resultado.setReadOnly(True)
        self.texto_resultado.setStyleSheet("background-color: #FAFAFA; padding: 10px;")
        self.texto_resultado.setMinimumHeight(250)
        self.layout.addWidget(self.texto_resultado)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(250)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

        # Variables para almacenar los pasos y el resultado
        self.resultado_pasos = ""
        self.resultado_final = ""
        self.modo_paso_a_paso = False
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        """Actualiza el estilo y tamaño de fuente localmente."""
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
        """)

    def crear_entradas_matrices(self):
        try:
            numero_matrices = int(self.input_matrices.text())
            if numero_matrices < 2:
                raise ValueError("Se necesitan al menos dos matrices para la multiplicación.")

            # Limpiar layout de matrices
            for i in reversed(range(self.layout_matrices.count())):
                widget = self.layout_matrices.takeAt(i).widget()
                if widget:
                    widget.deleteLater()

            self.matrices_widgets = []
            self.matrices_dimensiones = []

            for i in range(numero_matrices):
                layout = QVBoxLayout()
                label_matriz = QLabel(f"Matriz {i + 1}")
                layout.addWidget(label_matriz)

                # Entradas para dimensiones de la matriz
                layout_dimensiones = QHBoxLayout()
                input_filas = QLineEdit()
                input_filas.setPlaceholderText("Filas")
                input_filas.setFixedWidth(70)
                layout_dimensiones.addWidget(input_filas)

                input_columnas = QLineEdit()
                input_columnas.setPlaceholderText("Columnas")
                input_columnas.setFixedWidth(70)
                layout_dimensiones.addWidget(input_columnas)

                layout.addLayout(layout_dimensiones)
                self.matrices_dimensiones.append((input_filas, input_columnas))

                # Tabla de matriz
                tabla_matriz = QTableWidget()
                tabla_matriz.setFixedWidth(600)
                tabla_matriz.setFixedHeight(150)
                layout.addWidget(tabla_matriz)
                self.matrices_widgets.append(tabla_matriz)

                self.layout_matrices.addLayout(layout)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def verificar_dimensiones(self):
        try:
            matrices = []
            for filas_input, columnas_input in self.matrices_dimensiones:
                filas = int(filas_input.text())
                columnas = int(columnas_input.text())
                matrices.append((filas, columnas))

            # Verificar compatibilidad para multiplicación secuencial
            for i in range(len(matrices) - 1):
                if matrices[i][1] != matrices[i + 1][0]:
                    self.boton_calcular_producto.setEnabled(False)
                    raise ValueError("Las dimensiones de las matrices no permiten multiplicación en serie. "
                                     f"La Matriz {i + 1} tiene {matrices[i][1]} columnas y "
                                     f"la Matriz {i + 2} tiene {matrices[i + 1][0]} filas.")

            # Si son compatibles, configurar las tablas para recibir entradas
            for tabla, (filas_input, columnas_input) in zip(self.matrices_widgets, self.matrices_dimensiones):
                filas = int(filas_input.text())
                columnas = int(columnas_input.text())
                tabla.setRowCount(filas)
                tabla.setColumnCount(columnas)

                # Habilitar edición en las celdas de la tabla
                for i in range(filas):
                    for j in range(columnas):
                        tabla.setItem(i, j, QTableWidgetItem())
                        tabla.item(i, j).setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)

            # Habilitar el botón para calcular el producto si las dimensiones son correctas
            self.boton_calcular_producto.setEnabled(True)
            QMessageBox.information(self, "Dimensiones Válidas",
                                    "Las dimensiones de las matrices son compatibles para multiplicación.")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.boton_calcular_producto.setEnabled(False)

    def calcular_producto(self):
        try:
            matrices = []
            for tabla, (filas_input, columnas_input) in zip(self.matrices_widgets, self.matrices_dimensiones):
                filas = int(filas_input.text())
                columnas = int(columnas_input.text())

                matriz = []
                for i in range(filas):
                    fila = []
                    for j in range(columnas):
                        item = tabla.item(i, j)
                        if item is None or not item.text():
                            raise ValueError(f"Introduce un valor válido en la posición ({i + 1}, {j + 1}).")
                        fila.append(evaluar_expresion(item.text()))  # Evalúa la expresión
                    matriz.append(fila)

                matrices.append(Matriz(filas, matriz))

            resultado = matrices[0]
            pasos = "Proceso de Multiplicación de Matrices:\n\n"

            for i in range(1, len(matrices)):
                matriz_b = matrices[i]
                resultado_nuevo = []

                for r in range(len(resultado.matriz)):
                    nueva_fila = []
                    for c in range(len(matriz_b.matriz[0])):
                        suma = sum(resultado.matriz[r][k] * matriz_b.matriz[k][c] for k in range(len(matriz_b.matriz)))
                        detalle_operacion = " + ".join(
                            [f"{resultado.matriz[r][k]}*{matriz_b.matriz[k][c]}" for k in range(len(matriz_b.matriz))])
                        pasos += f"Elemento ({r + 1}, {c + 1}): {detalle_operacion} = {suma:.2f}\n"
                        nueva_fila.append(suma)
                    resultado_nuevo.append(nueva_fila)

                resultado = Matriz(len(resultado_nuevo), resultado_nuevo)
                pasos += "\nPaso {}: Resultado parcial después de multiplicar con Matriz {}\n".format(i, i + 1)
                pasos += resultado.formatear_matriz() + "\n\n"

            self.resultado_final = f"Resultado final:\n{resultado.formatear_matriz()}"
            self.resultado_pasos = pasos + "\n" + self.resultado_final
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.show()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def cambiar_modo(self):
        if self.modo_paso_a_paso:
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
        else:
            self.texto_resultado.setText(self.resultado_pasos)
            self.boton_paso_a_paso.setText("Mostrar Solo Respuesta")
        self.modo_paso_a_paso = not self.modo_paso_a_paso

    def regresar_menu_principal(self):
        from menu import MenuMatrices
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()
        self.close()


class VentanaDeterminante(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Cálculo del Determinante de la Matriz")
        self.setGeometry(100, 100, 800, 600)
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Título
        self.label_titulo = QLabel("Cálculo del Determinante", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(self.tamano_fuente + 6)
        fuente_titulo.setBold(True)
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo)

        # Entrada de tamaño de la matriz
        self.layout_entrada = QHBoxLayout()
        self.label_dimension = QLabel("Tamaño de la Matriz (n x n):", self)
        self.input_dimension = QLineEdit(self)
        self.input_dimension.setFixedWidth(60)
        self.boton_crear_matriz = QPushButton("Crear Matriz", self)
        self.boton_crear_matriz.setFixedWidth(150)
        self.boton_crear_matriz.clicked.connect(self.crear_matriz)

        self.layout_entrada.addWidget(self.label_dimension)
        self.layout_entrada.addWidget(self.input_dimension)
        self.layout_entrada.addWidget(self.boton_crear_matriz)
        self.layout.addLayout(self.layout_entrada)

        # Tabla para introducir la matriz
        self.tabla_matriz = QTableWidget(self)
        self.layout.addWidget(self.tabla_matriz)

        # Botón para calcular el determinante
        self.boton_calcular = QPushButton("Calcular Determinante", self)
        self.boton_calcular.clicked.connect(self.calcular_determinante)
        self.layout.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Botón para alternar entre modo paso a paso y solo respuesta
        self.boton_paso_a_paso = QPushButton("Mostrar Solución Paso a Paso", self)
        self.boton_paso_a_paso.clicked.connect(self.cambiar_modo)
        self.boton_paso_a_paso.hide()
        self.layout.addWidget(self.boton_paso_a_paso, alignment=Qt.AlignCenter)

        # Área de resultados
        self.texto_resultado = QTextEdit(self)
        self.texto_resultado.setReadOnly(True)
        self.layout.addWidget(self.texto_resultado)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

        # Variables para almacenar el resultado y los pasos
        self.resultado_final = ""
        self.resultado_pasos = ""
        self.modo_paso_a_paso = False
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
        """)

    def crear_matriz(self):
        try:
            n = int(self.input_dimension.text())
            if n <= 0:
                raise ValueError("El tamaño de la matriz debe ser un número positivo.")

            # Crear la tabla de la matriz nxn
            self.tabla_matriz.setRowCount(n)
            self.tabla_matriz.setColumnCount(n)
            self.tabla_matriz.setHorizontalHeaderLabels([f"Columna {i + 1}" for i in range(n)])
            self.tabla_matriz.setVerticalHeaderLabels([f"Fila {i + 1}" for i in range(n)])

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def calcular_determinante(self):
        try:
            n = self.tabla_matriz.rowCount()
            matriz = []
            for i in range(n):
                fila = []
                for j in range(n):
                    item = self.tabla_matriz.item(i, j)
                    if item is None or not item.text():
                        raise ValueError(f"Introduce un valor válido en la posición ({i + 1}, {j + 1}).")
                    fila.append(evaluar_expresion(item.text()))  # Evalúa la expresión
                matriz.append(fila)

            matriz_obj = Matriz(n, matriz)
            determinante, pasos = matriz_obj.calcular_determinante(paso_a_paso=True)
            self.resultado_final = f"El determinante de la matriz es: {determinante:.2f}"
            self.resultado_pasos = f"Pasos de cálculo:\n\n{pasos}\n\n{self.resultado_final}"
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.show()
            self.modo_paso_a_paso = False

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def cambiar_modo(self):
        # Alternar entre los modos y actualizar el texto mostrado
        if self.modo_paso_a_paso:
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
        else:
            self.texto_resultado.setText(self.resultado_pasos)
            self.boton_paso_a_paso.setText("Mostrar Solo Respuesta")
        self.modo_paso_a_paso = not self.modo_paso_a_paso

    def regresar_menu_principal(self):
        from menu import MenuMatrices
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()
        self.close()


class VentanaInversa(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Cálculo de la Inversa de una Matriz")
        self.setGeometry(100, 100, 800, 600)
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Título
        self.label_titulo = QLabel("Cálculo de la Inversa", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(self.tamano_fuente + 6)
        fuente_titulo.setBold(True)
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo)

        # Entrada de tamaño de la matriz
        self.layout_entrada = QHBoxLayout()
        self.label_dimension = QLabel("Tamaño de la Matriz (n x n):", self)
        self.input_dimension = QLineEdit(self)
        self.input_dimension.setFixedWidth(60)
        self.boton_crear_matriz = QPushButton("Crear Matriz", self)
        self.boton_crear_matriz.setFixedWidth(150)
        self.boton_crear_matriz.clicked.connect(self.crear_matriz)

        self.layout_entrada.addWidget(self.label_dimension)
        self.layout_entrada.addWidget(self.input_dimension)
        self.layout_entrada.addWidget(self.boton_crear_matriz)
        self.layout.addLayout(self.layout_entrada)

        # Tabla para introducir la matriz
        self.tabla_matriz = QTableWidget(self)
        self.layout.addWidget(self.tabla_matriz)

        # Botón para calcular la inversa
        self.boton_calcular = QPushButton("Calcular Inversa", self)
        self.boton_calcular.clicked.connect(self.calcular_inversa)
        self.layout.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Botón para alternar entre modo paso a paso y solo respuesta
        self.boton_paso_a_paso = QPushButton("Mostrar Solución Paso a Paso", self)
        self.boton_paso_a_paso.clicked.connect(self.cambiar_modo)
        self.boton_paso_a_paso.hide()
        self.layout.addWidget(self.boton_paso_a_paso, alignment=Qt.AlignCenter)

        # Área de resultados
        self.texto_resultado = QTextEdit(self)
        self.texto_resultado.setReadOnly(True)
        self.layout.addWidget(self.texto_resultado)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

        # Variables para almacenar el resultado y los pasos
        self.resultado_final = ""
        self.resultado_pasos = ""
        self.modo_paso_a_paso = False
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
        """)

    def crear_matriz(self):
        try:
            n = int(self.input_dimension.text())
            if n <= 0:
                raise ValueError("El tamaño de la matriz debe ser un número positivo.")

            # Crear la tabla de la matriz nxn
            self.tabla_matriz.setRowCount(n)
            self.tabla_matriz.setColumnCount(n)
            self.tabla_matriz.setHorizontalHeaderLabels([f"Columna {i + 1}" for i in range(n)])
            self.tabla_matriz.setVerticalHeaderLabels([f"Fila {i + 1}" for i in range(n)])

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def calcular_inversa(self):
        try:
            n = self.tabla_matriz.rowCount()
            matriz = []
            for i in range(n):
                fila = []
                for j in range(n):
                    item = self.tabla_matriz.item(i, j)
                    if item is None or not item.text():
                        raise ValueError(f"Introduce un valor válido en la posición ({i + 1}, {j + 1}).")
                    fila.append(evaluar_expresion(item.text()))  # Evalúa la expresión
                matriz.append(fila)

            matriz_obj = Matriz(n, matriz)
            inversa, pasos = matriz_obj.calcular_inversa(paso_a_paso=True)
            self.resultado_final = "La inversa de la matriz es:\n" + inversa.formatear_matriz()
            self.resultado_pasos = f"Pasos de cálculo:\n\n{pasos}\n\n{self.resultado_final}"
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.show()
            self.modo_paso_a_paso = False

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def cambiar_modo(self):
        if self.modo_paso_a_paso:
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
        else:
            self.texto_resultado.setText(self.resultado_pasos)
            self.boton_paso_a_paso.setText("Mostrar Solo Respuesta")
        self.modo_paso_a_paso = not self.modo_paso_a_paso

    def regresar_menu_principal(self):
        from menu import MenuMatrices
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()
        self.close()


class VentanaCramer(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Resolver Sistema con Regla de Cramer")
        self.setGeometry(100, 100, 1000, 600)
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Entrada para el tamaño de la matriz
        self.layout_entrada = QHBoxLayout()
        self.label_dimension = QLabel("Tamaño de la Matriz (n x n):")
        self.input_dimension = QLineEdit()
        self.boton_crear_matriz = QPushButton("Crear Matriz")
        self.boton_crear_matriz.clicked.connect(self.crear_matriz)

        self.layout_entrada.addWidget(self.label_dimension)
        self.layout_entrada.addWidget(self.input_dimension)
        self.layout_entrada.addWidget(self.boton_crear_matriz)
        self.layout.addLayout(self.layout_entrada)

        # Matriz de coeficientes
        self.tabla_matriz = QTableWidget()
        self.layout.addWidget(self.tabla_matriz)

        # Vector de resultados (tabla de una sola columna)
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(1)
        self.tabla_resultados.setHorizontalHeaderLabels(["Terminos"])
        self.layout.addWidget(self.tabla_resultados)

        # Botón para calcular la regla de Cramer
        self.boton_calcular = QPushButton("Calcular")
        self.boton_calcular.clicked.connect(self.aplicar_cramer)
        self.layout.addWidget(self.boton_calcular)

        # Área para mostrar los resultados
        self.texto_resultado = QTextEdit()
        self.texto_resultado.setReadOnly(True)
        self.layout.addWidget(self.texto_resultado)

        # Botón para alternar entre paso a paso y solo resultado
        self.boton_paso_a_paso = QPushButton("Mostrar Solución Paso a Paso")
        self.boton_paso_a_paso.clicked.connect(self.cambiar_modo)
        self.boton_paso_a_paso.hide()
        self.layout.addWidget(self.boton_paso_a_paso)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(250)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

        # Variables para almacenar los pasos
        self.resultado_pasos = ""
        self.resultado_final = ""
        self.modo_paso_a_paso = False
        self.showMaximized()

    def actualizar_fuente_local(self, tamano):
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
        """)

    def crear_matriz(self):
        try:
            n = int(self.input_dimension.text())
            if n <= 0:
                raise ValueError("El tamaño de la matriz debe ser positivo.")

            # Configuración de tabla de coeficientes
            self.tabla_matriz.setRowCount(n)
            self.tabla_matriz.setColumnCount(n)
            self.tabla_matriz.setHorizontalHeaderLabels([f"Columna {i + 1}" for i in range(n)])
            self.tabla_matriz.setVerticalHeaderLabels([f"Fila {i + 1}" for i in range(n)])

            # Configuración de tabla de resultados
            self.tabla_resultados.setRowCount(n)
            self.tabla_resultados.setVerticalHeaderLabels([f"Término independiente {i + 1}" for i in range(n)])

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def aplicar_cramer(self):
        try:
            n = self.tabla_matriz.rowCount()
            entradas = []
            for i in range(n):
                fila = []
                for j in range(n):
                    item = self.tabla_matriz.item(i, j)
                    if item is None or not item.text():
                        raise ValueError(f"Introduce un valor válido en la posición ({i + 1}, {j + 1}).")
                    fila.append(evaluar_expresion(item.text()))  # Evalúa la expresión
                entradas.append(fila)

            resultados = []
            for i in range(n):
                item = self.tabla_resultados.item(i, 0)
                if item is None or not item.text():
                    raise ValueError(f"Introduce un valor válido en el resultado de la fila {i + 1}.")
                resultados.append(evaluar_expresion(item.text()))  # Evalúa la expresión

            matriz_obj = Matriz(n, entradas)
            soluciones, pasos = matriz_obj.cramer(resultados, paso_a_paso=True)
            resultado_texto = "Soluciones del sistema:\n"
            for i, solucion in enumerate(soluciones, 1):
                resultado_texto += f"x{i} = {solucion:.2f}\n"

            self.resultado_final = resultado_texto
            self.resultado_pasos = f"Pasos de cálculo:\n\n{pasos}\n\n{self.resultado_final}"
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.show()
            self.modo_paso_a_paso = False

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def cambiar_modo(self):
        if self.modo_paso_a_paso:
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
        else:
            self.texto_resultado.setText(self.resultado_pasos)
            self.boton_paso_a_paso.setText("Mostrar Solo Respuesta")
        self.modo_paso_a_paso = not self.modo_paso_a_paso

    def regresar_menu_principal(self):
        from menu import MenuMatrices
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()
        self.close()


class VentanaLU(QWidget):
    cambiar_fuente_signal = pyqtSignal(int)
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Factorización LU")
        self.setGeometry(100, 100, 1000, 800)
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Entrada para el tamaño de la matriz
        self.layout_entrada = QHBoxLayout()
        self.label_dimension = QLabel("Tamaño de la Matriz (n x n):")
        self.input_dimension = QLineEdit()
        self.input_dimension.setFixedWidth(60)
        self.boton_crear_matriz = QPushButton("Crear Matriz y Vector")
        self.boton_crear_matriz.clicked.connect(self.crear_matriz_vector)

        self.layout_entrada.addWidget(self.label_dimension)
        self.layout_entrada.addWidget(self.input_dimension)
        self.layout_entrada.addWidget(self.boton_crear_matriz)
        self.layout.addLayout(self.layout_entrada)

        # Tabla para la matriz A (creada dinámicamente)
        self.label_matriz = QLabel("Matriz A:")
        self.layout.addWidget(self.label_matriz)
        self.tabla_matriz = QTableWidget(self)
        self.layout.addWidget(self.tabla_matriz)

        # Tabla para el vector b (creada dinámicamente)
        self.label_vector_b = QLabel("Vector b:")
        self.layout.addWidget(self.label_vector_b)
        self.tabla_vector_b = QTableWidget(self)
        self.layout.addWidget(self.tabla_vector_b)

        # Botón para calcular la factorización LU y resolver Ax = b
        self.boton_calcular = QPushButton("Calcular LU y Resolver Ax = b", self)
        self.boton_calcular.setFixedWidth(250)
        self.boton_calcular.clicked.connect(self.calcular_lu)
        self.layout.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Botón para mostrar paso a paso
        self.boton_paso_a_paso = QPushButton("Mostrar Solución Paso a Paso", self)
        self.boton_paso_a_paso.setFixedWidth(250)
        self.boton_paso_a_paso.clicked.connect(self.cambiar_modo)
        self.boton_paso_a_paso.hide()  # Se oculta inicialmente hasta que se realice el cálculo
        self.layout.addWidget(self.boton_paso_a_paso, alignment=Qt.AlignCenter)

        # Área de resultados
        self.resultado = QTextEdit(self)
        self.resultado.setReadOnly(True)
        self.layout.addWidget(self.resultado)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

        # Variables para almacenar los resultados y los pasos
        self.resultado_final = ""
        self.resultado_pasos = ""
        self.modo_paso_a_paso = False
        self.showMaximized()

    def crear_matriz_vector(self):
        try:
            n = int(self.input_dimension.text())
            if n <= 0:
                raise ValueError("El tamaño de la matriz debe ser un número positivo.")

            # Crear tabla para la matriz A
            self.tabla_matriz.setRowCount(n)
            self.tabla_matriz.setColumnCount(n)
            self.tabla_matriz.setHorizontalHeaderLabels([f"Columna {i + 1}" for i in range(n)])
            self.tabla_matriz.setVerticalHeaderLabels([f"Fila {i + 1}" for i in range(n)])

            # Crear tabla para el vector b
            self.tabla_vector_b.setRowCount(n)
            self.tabla_vector_b.setColumnCount(1)
            self.tabla_vector_b.setHorizontalHeaderLabels(["b"])
            self.tabla_vector_b.setVerticalHeaderLabels([f"Componente {i + 1}" for i in range(n)])

        except ValueError:
            QMessageBox.critical(self, "Error", "Introduce un tamaño válido para la matriz.")

    def calcular_lu(self):
        try:
            # Leer la matriz A y el vector b desde las tablas
            n = self.tabla_matriz.rowCount()
            A = []
            for i in range(n):
                fila = []
                for j in range(n):
                    item = self.tabla_matriz.item(i, j)
                    if item is None or not item.text():
                        raise ValueError(f"Introduce un valor en la posición ({i + 1}, {j + 1}) de la matriz.")
                    fila.append(evaluar_expresion(item.text()))
                A.append(fila)

            b = []
            for i in range(n):
                item = self.tabla_vector_b.item(i, 0)
                if item is None or not item.text():
                    raise ValueError(f"Introduce un valor en la posición {i + 1} del vector b.")
                b.append(evaluar_expresion(item.text()))

            # Crear la matriz A y resolver usando LU
            matriz_a = Matriz(n, A)
            x, pasos = matriz_a.resolver_lu(b, paso_a_paso=True)

            # Mostrar los pasos y la solución
            self.resultado_pasos = pasos
            self.resultado_final = "\nSolución del sistema (x):\n" + "\n".join(
                f"x[{i + 1}] = {val:.2f}" for i, val in enumerate(x))
            self.resultado.setText(self.resultado_final)

            # Mostrar el botón para ver el paso a paso
            self.boton_paso_a_paso.show()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def cambiar_modo(self):
        """Cambia entre mostrar solo el resultado final o los pasos completos."""
        if self.modo_paso_a_paso:
            self.resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
        else:
            self.resultado.setText(self.resultado_pasos)
            self.boton_paso_a_paso.setText("Mostrar Solo Respuesta")
        self.modo_paso_a_paso = not self.modo_paso_a_paso

    def regresar_menu_principal(self):
        from menu import MenuMatrices
        # Pasamos tamano_fuente y cambiar_fuente_signal
        self.menu_matrices = MenuMatrices(self.tamano_fuente, self.cambiar_fuente_signal)
        self.menu_matrices.show()
        self.close()

    def actualizar_fuente_local(self, tamano):
        """Actualizar estilo y fuente en toda la ventana"""
        self.setStyleSheet(f"""
            QLabel {{
                font-size: {tamano + 2}px;
            }}
            QPushButton {{
                font-size: {tamano}px;
                padding: 8px;
            }}
            QLineEdit, QTextEdit, QTableWidget {{
                font-size: {tamano}px;
            }}
        """)
