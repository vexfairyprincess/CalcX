# menu.py

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QMessageBox, QSpacerItem, QSizePolicy, QFrame, QScrollArea, QTableWidget, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from matriz import Matriz
from vector import Vector
import sys

class MenuAplicacion(QMainWindow):
    cambiar_fuente_signal = pyqtSignal(int)  # Señal para cambiar el tamaño de fuente global

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 800, 600)
        
        # Fuente base
        self.tamano_fuente = 14  # Tamaño de fuente inicial
        
        # Widget principal
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Conectar la señal para cambiar fuente
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

        # Título
        self.label_titulo = QLabel("Menú Principal", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        fuente_titulo = QFont()
        fuente_titulo.setPointSize(28)
        fuente_titulo.setBold(True)
        self.label_titulo.setFont(fuente_titulo)
        self.layout.addWidget(self.label_titulo)

        # Botones de opciones
        self.boton_escalonado = QPushButton("Método Escalonado", self)
        self.boton_escalonado.clicked.connect(self.abrir_metodo_escalonado)
        self.layout.addWidget(self.boton_escalonado)

        self.boton_vectorial = QPushButton("Operaciones Combinadas de Vectores", self)
        self.boton_vectorial.clicked.connect(self.abrir_operaciones_vectoriales_combinadas)
        self.layout.addWidget(self.boton_vectorial)

        self.boton_producto_vectorial = QPushButton("Multiplicación Vector Fila x Columna", self)
        self.boton_producto_vectorial.clicked.connect(self.abrir_producto_vectorial)
        self.layout.addWidget(self.boton_producto_vectorial)
        
        # Espaciador
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Botones para ajustar el tamaño de fuente
        botones_fuente_layout = QHBoxLayout()
        self.layout.addLayout(botones_fuente_layout)

        self.boton_aumentar_fuente = QPushButton("Aumentar Tamaño de Fuente", self)
        self.boton_aumentar_fuente.clicked.connect(self.aumentar_tamano_fuente)
        botones_fuente_layout.addWidget(self.boton_aumentar_fuente)

        self.boton_disminuir_fuente = QPushButton("Disminuir Tamaño de Fuente", self)
        self.boton_disminuir_fuente.clicked.connect(self.disminuir_tamano_fuente)
        botones_fuente_layout.addWidget(self.boton_disminuir_fuente)
        
        # Botón para salir
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(self.close)
        self.layout.addWidget(self.boton_salir)
        
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
        
    def abrir_metodo_escalonado(self):
        self.ventana_escalonado = VentanaEscalonado(self.tamano_fuente)
        self.ventana_escalonado.show()
        self.cambiar_fuente_signal.connect(self.ventana_escalonado.actualizar_fuente_local)
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

    def limpiar_layout(self, layout):
        """Elimina todos los widgets del layout dado."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class VentanaEscalonado(QWidget):
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
            self.tabla_matriz.setHorizontalHeaderLabels([f"x{i+1}" for i in range(m)] + ["Resultado"])
            
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
                    valor = float(item.text())
                    fila.append(valor)
                entradas.append(fila)

            # Calcular el método escalonado
            matriz = Matriz(n, entradas)
            self.resultado_pasos = matriz.eliminacion_gaussiana()
            self.resultado_final = matriz.interpretar_resultado()
            
            # Mostrar resultado simplificado
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
        self.main_window = MenuAplicacion()
        self.main_window.tamano_fuente = self.tamano_fuente
        self.main_window.cambiar_fuente_signal.emit(self.tamano_fuente)
        self.main_window.show()
        self.close()

# Implementación de las clases VentanaOperacionesCombinadas y VentanaProductoVectorial con ajustes similares...

class VentanaOperacionesCombinadas(QWidget):
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
            self.tabla_vectores.setHorizontalHeaderLabels([f"Vector {i+1}" for i in range(numero_vectores)])
            self.tabla_vectores.setVerticalHeaderLabels([f"Componente {i+1}" for i in range(dimension)])

            # Configurar la tabla de escalares
            self.tabla_escalars.setRowCount(numero_vectores)
            self.tabla_escalars.setColumnCount(1)
            self.tabla_escalars.setHorizontalHeaderLabels(["Escalar"])
            self.tabla_escalars.setVerticalHeaderLabels([f"Vector {i+1}" for i in range(numero_vectores)])
        
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
                        raise ValueError(f"Introduce un valor válido en la posición Vector {i + 1}, Componente {j + 1}.")
                    componentes.append(item.text())
                vector = Vector.crear_vector_desde_entrada(componentes)
                lista_vectores.append(vector)

                # Obtener el escalar correspondiente
                item_escalar = self.tabla_escalars.item(i, 0)
                if item_escalar is None or not item_escalar.text():
                    raise ValueError(f"Introduce un escalar válido para el Vector {i + 1}.")
                escalar = float(item_escalar.text())
                lista_escalars.append(escalar)

            # Calcular la suma escalada de los vectores utilizando vector.py
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
        self.main_window = MenuAplicacion()
        self.main_window.tamano_fuente = self.tamano_fuente
        self.main_window.cambiar_fuente_signal.emit(self.tamano_fuente)
        self.main_window.show()
        self.close()


class VentanaProductoVectorial(QWidget):
    def __init__(self, tamano_fuente):
        super().__init__()
        self.setWindowTitle("Multiplicación de Vector Fila x Vector Columna")
        self.setGeometry(100, 100, 1200, 700)
        self.tamano_fuente = tamano_fuente
        self.actualizar_fuente_local(self.tamano_fuente)

        # Layout principal
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Layout izquierdo para entrada de dimensión y vectores
        self.layout_izquierdo = QVBoxLayout()
        self.layout.addLayout(self.layout_izquierdo)

        # Entrada para la dimensión de los vectores
        self.layout_dimension = QHBoxLayout()
        self.layout_izquierdo.addLayout(self.layout_dimension)

        self.label_dimension = QLabel("Dimensión del Vector:", self)
        self.layout_dimension.addWidget(self.label_dimension)
        self.input_dimension = QLineEdit(self)
        self.input_dimension.setPlaceholderText("Ejemplo: 3")
        self.input_dimension.setFixedWidth(200)
        self.layout_dimension.addWidget(self.input_dimension)

        self.boton_crear_vectores = QPushButton("Crear Vectores", self)
        self.boton_crear_vectores.setFixedWidth(150)
        self.boton_crear_vectores.clicked.connect(self.crear_vectores)
        self.layout_dimension.addWidget(self.boton_crear_vectores)

        # Área para la tabla de vectores fila y columna
        self.layout_vectores = QHBoxLayout()
        self.layout_izquierdo.addLayout(self.layout_vectores)

        # Tabla para el vector fila
        self.tabla_vector_fila = QTableWidget(self)
        self.tabla_vector_fila.setFixedWidth(350)
        self.tabla_vector_fila.setFixedHeight(70)
        self.tabla_vector_fila.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_vectores.addWidget(self.tabla_vector_fila)

        # Tabla para el vector columna
        self.tabla_vector_columna = QTableWidget(self)
        self.tabla_vector_columna.setFixedWidth(190)
        self.tabla_vector_columna.setFixedHeight(250)
        self.tabla_vector_columna.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_vectores.addWidget(self.tabla_vector_columna)

        # Botón para calcular el producto escalar
        self.boton_calcular = QPushButton("Calcular Producto", self)
        self.boton_calcular.setFixedWidth(200)
        self.boton_calcular.clicked.connect(self.calcular_producto)
        self.layout_izquierdo.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

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

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(250)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout_resultados.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

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

            # Configurar tabla para el vector columna
            self.tabla_vector_columna.setRowCount(dimension)
            self.tabla_vector_columna.setColumnCount(1)
            self.tabla_vector_columna.setHorizontalHeaderLabels(["Vector Columna"])
            self.tabla_vector_columna.setVerticalHeaderLabels([f"Componente {i + 1}" for i in range(dimension)])

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def calcular_producto(self):
        try:
            dimension = self.tabla_vector_fila.columnCount()
            vector_fila = []
            vector_columna = []

            # Leer componentes del vector fila
            for i in range(dimension):
                item = self.tabla_vector_fila.item(0, i)
                if item is None or not item.text():
                    raise ValueError(f"Introduce un valor válido en la posición Vector Fila, Componente {i + 1}.")
                vector_fila.append(float(item.text()))

            # Leer componentes del vector columna
            for i in range(dimension):
                item = self.tabla_vector_columna.item(i, 0)
                if item is None or not item.text():
                    raise ValueError(f"Introduce un valor válido en la posición Vector Columna, Componente {i + 1}.")
                vector_columna.append(float(item.text()))

            # Realizar el cálculo del producto escalar
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
        self.main_window = MenuAplicacion()
        self.main_window.tamano_fuente = self.tamano_fuente
        self.main_window.cambiar_fuente_signal.emit(self.tamano_fuente)
        self.main_window.show()
        self.close()


def iniciar_menu():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    fuente_base = QFont()
    fuente_base.setPointSize(14)  # Tamaño de fuente inicial
    app.setFont(fuente_base)
    
    ventana = MenuAplicacion()
    ventana.show()
    sys.exit(app.exec())