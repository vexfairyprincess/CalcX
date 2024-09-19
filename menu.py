# Código Principal (menu.py combinado con interfaz para operaciones vectoriales y método escalonado)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QMessageBox, QGridLayout, QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QFrame, QComboBox,
    QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matriz import Matriz
from vector import Vector
import sys

class MenuAplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget principal
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Menú principal
        self.crear_menu_principal()

    def crear_menu_principal(self):
        # Limpiar el layout actual
        self.limpiar_layout(self.layout)

        # Título
        self.label_titulo = QLabel("Menú Principal", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(self.label_titulo)

        # Botón para el método escalonado
        self.boton_escalonado = QPushButton("Método Escalonado", self)
        self.boton_escalonado.clicked.connect(self.abrir_metodo_escalonado)
        self.layout.addWidget(self.boton_escalonado)

        # Botón para operaciones combinadas de vectores
        self.boton_vectorial = QPushButton("Operaciones Combinadas de Vectores", self)
        self.boton_vectorial.clicked.connect(self.abrir_operaciones_vectoriales_combinadas)
        self.layout.addWidget(self.boton_vectorial)

        # Botón para multiplicación de vector fila por vector columna
        self.boton_producto_vectorial = QPushButton("Multiplicación Vector Fila x Columna", self)
        self.boton_producto_vectorial.clicked.connect(self.abrir_producto_vectorial)
        self.layout.addWidget(self.boton_producto_vectorial)

        # Espaciador
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón para salir
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(self.close)
        self.layout.addWidget(self.boton_salir)

    def abrir_metodo_escalonado(self):
        self.ventana_escalonado = VentanaEscalonado()
        self.ventana_escalonado.show()
        self.close()

    def abrir_operaciones_vectoriales_combinadas(self):
        self.ventana_operaciones_combinadas = VentanaOperacionesCombinadas()
        self.ventana_operaciones_combinadas.show()
        self.close()

    def abrir_producto_vectorial(self):
        self.ventana_producto_vectorial = VentanaProductoVectorial()
        self.ventana_producto_vectorial.show()
        self.close()

    def limpiar_layout(self, layout):
        """Elimina todos los widgets del layout dado."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class VentanaEscalonado(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método Escalonado")
        self.setGeometry(100, 100, 1200, 700)  # Ajustar tamaño de ventana para más espacio
        
        # Layout Principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Título
        self.label_titulo = QLabel("Método Escalonado - Eliminación Gaussiana", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(self.label_titulo)

        # Layout de Entrada de Datos
        self.layout_entrada = QHBoxLayout()
        self.layout.addLayout(self.layout_entrada)

        # Entrada para el número de ecuaciones
        self.label_ecuaciones = QLabel("Ecuaciones:", self)
        self.layout_entrada.addWidget(self.label_ecuaciones)
        self.input_ecuaciones = QLineEdit(self)
        self.input_ecuaciones.setFixedWidth(50)  # Reducir ancho
        self.layout_entrada.addWidget(self.input_ecuaciones)

        # Entrada para el número de variables
        self.label_variables = QLabel("Variables:", self)
        self.layout_entrada.addWidget(self.label_variables)
        self.input_variables = QLineEdit(self)
        self.input_variables.setFixedWidth(50)  # Reducir ancho
        self.layout_entrada.addWidget(self.input_variables)

        # Botón para crear la matriz
        self.boton_crear_matriz = QPushButton("Crear Matriz", self)
        self.boton_crear_matriz.setFixedWidth(120)  # Reducir ancho del botón
        self.boton_crear_matriz.clicked.connect(self.crear_matriz)
        self.layout_entrada.addWidget(self.boton_crear_matriz)

        # Espaciador
        self.layout_entrada.addStretch()

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(200)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout_entrada.addWidget(self.boton_regresar)

        # Layout para tabla y resultados
        self.layout_matriz_resultado = QHBoxLayout()
        self.layout.addLayout(self.layout_matriz_resultado)

        # Área de tabla para mostrar la matriz
        self.tabla_matriz = QTableWidget(self)
        self.tabla_matriz.setFixedWidth(400)  # Establecer ancho fijo para la tabla
        self.layout_matriz_resultado.addWidget(self.tabla_matriz)

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
        self.texto_resultado.setFont(QFont("Arial", 12))
        self.texto_resultado.setStyleSheet("background-color: #FAFAFA;")
        self.texto_resultado.setFixedHeight(450)  # Aumentar la altura del área de texto
        self.texto_resultado.setFixedWidth(600)  # Aumentar el ancho del área de texto
        self.frame_resultado.layout().addWidget(self.texto_resultado)
        self.layout_matriz_resultado.addWidget(self.frame_resultado)

        # Botón para calcular
        self.boton_calcular = QPushButton("Calcular", self)
        self.boton_calcular.setFixedWidth(150)  # Reducir ancho del botón
        self.boton_calcular.clicked.connect(self.calcular_escalonado)
        self.layout.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Botón para mostrar paso a paso
        self.boton_paso_a_paso = QPushButton("Mostrar Solución Paso a Paso", self)
        self.boton_paso_a_paso.setFixedWidth(200)  # Aumentar ancho del botón
        self.boton_paso_a_paso.clicked.connect(self.cambiar_modo)
        self.boton_paso_a_paso.hide()  # Ocultar inicialmente
        self.layout.addWidget(self.boton_paso_a_paso, alignment=Qt.AlignCenter)

        # Variable para almacenar los pasos
        self.resultado_pasos = ""
        self.resultado_final = ""
        self.modo_paso_a_paso = False  # Variable para controlar el modo

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
            matriz = Matriz(n, entradas)  # Modificar para aceptar entradas directas
            self.resultado_pasos = matriz.eliminacion_gaussiana()  # Guardar pasos para mostrar luego
            self.resultado_final = matriz.interpretar_resultado()  # Guardar resultado final
            
            # Mostrar resultado simplificado
            self.texto_resultado.setText(self.resultado_final)
            self.boton_paso_a_paso.setText("Mostrar Solución Paso a Paso")
            self.boton_paso_a_paso.show()  # Mostrar el botón para ver los pasos

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
        self.main_window.show()
        self.close()

# menu.py (con corrección del layout y estilo de fondo)

class VentanaOperacionesCombinadas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones Combinadas de Vectores")
        self.setGeometry(100, 100, 1200, 700)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Layout Izquierdo para entrada de vectores y escalares
        self.layout_izquierdo = QVBoxLayout()
        self.layout.addLayout(self.layout_izquierdo)

        # Layout para Número de Vectores y Dimensión
        self.layout_entrada = QHBoxLayout()
        self.layout_izquierdo.addLayout(self.layout_entrada)

        # Número de Vectores
        self.label_vectores = QLabel("Número de Vectores:", self)
        self.layout_entrada.addWidget(self.label_vectores)
        self.input_vectores = QLineEdit(self)
        self.input_vectores.setFixedWidth(50)
        self.layout_entrada.addWidget(self.input_vectores)

        # Dimensión de los Vectores
        self.label_dimension = QLabel("Dimensión de los Vectores:", self)
        self.layout_entrada.addWidget(self.label_dimension)
        self.input_dimension = QLineEdit(self)
        self.input_dimension.setFixedWidth(50)
        self.layout_entrada.addWidget(self.input_dimension)

        # Botón Crear Entradas
        self.boton_crear_vectores = QPushButton("Crear Entradas", self)
        self.boton_crear_vectores.setFixedWidth(150)
        self.boton_crear_vectores.clicked.connect(self.crear_entradas_vectores)
        self.layout_entrada.addWidget(self.boton_crear_vectores)

        # Espaciador
        self.layout_entrada.addStretch()

        # Layout para Tablas de Vectores y Escalares
        self.layout_tablas = QVBoxLayout()
        self.layout_izquierdo.addLayout(self.layout_tablas)

        # Tabla para los vectores (más larga y ancha)
        self.tabla_vectores = QTableWidget(self)
        self.tabla_vectores.setFixedWidth(350)  # Aumento del ancho para la tabla de vectores
        self.tabla_vectores.setFixedHeight(250)  # Mantener la altura
        self.layout_tablas.addWidget(self.tabla_vectores)

        # Tabla para los escalares (más larga y ancha)
        self.tabla_escalars = QTableWidget(self)
        self.tabla_escalars.setFixedWidth(350)  # Aumento del ancho para la tabla de escalares
        self.tabla_escalars.setFixedHeight(200)  # Mantener la altura
        self.layout_tablas.addWidget(self.tabla_escalars)

        # Botón para calcular operación (más cerca de las tablas)
        self.boton_calcular = QPushButton("Calcular Operación", self)
        self.boton_calcular.setFixedWidth(200)
        self.boton_calcular.clicked.connect(self.calcular_operacion)
        self.layout_tablas.addWidget(self.boton_calcular, alignment=Qt.AlignCenter)

        # Área de resultados a la derecha con scroll y estilo mejorado
        self.layout_resultados = QVBoxLayout()
        self.layout.addLayout(self.layout_resultados)

        self.label_resultado = QLabel("Resultado de la Operación", self)
        self.label_resultado.setAlignment(Qt.AlignCenter)
        self.label_resultado.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.layout_resultados.addWidget(self.label_resultado)

        # QScrollArea para contener el frame con los resultados
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout_resultados.addWidget(self.scroll_area)

        # Frame para contener el layout de resultado en formato horizontal
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
        self.scroll_area.setWidget(self.frame_resultado)  # Agregar el frame al scroll area

        # Layout inicial para el frame de resultado
        self.frame_layout = QHBoxLayout()
        self.frame_resultado.setLayout(self.frame_layout)

        # Botón para regresar al menú principal, ubicado más abajo y centrado
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(200)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout_resultados.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

    def crear_entradas_vectores(self):
        try:
            numero_vectores = int(self.input_vectores.text())
            dimension = int(self.input_dimension.text())

            if numero_vectores <= 0 or dimension <= 0:
                raise ValueError("El número de vectores y la dimensión deben ser positivos.")
            
            # Configurar la tabla de vectores (más grande)
            self.tabla_vectores.setRowCount(dimension)
            self.tabla_vectores.setColumnCount(numero_vectores)
            self.tabla_vectores.setHorizontalHeaderLabels([f"Vector {i+1}" for i in range(numero_vectores)])
            self.tabla_vectores.setVerticalHeaderLabels([f"Componente {i+1}" for i in range(dimension)])

            # Configurar la tabla de escalares (más grande)
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
                    componentes.append(float(item.text()))
                lista_vectores.append(Vector(componentes))

                # Obtener el escalar correspondiente
                item_escalar = self.tabla_escalars.item(i, 0)
                if item_escalar is None or not item_escalar.text():
                    raise ValueError(f"Introduce un escalar válido para el Vector {i + 1}.")
                escalar = float(item_escalar.text())
                lista_escalars.append(escalar)

            # Calcular la suma escalada de los vectores
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
                label_escalar.setAlignment(Qt.AlignCenter)  # Centrar el escalar
                label_escalar.setStyleSheet("""
                    font-size: 18px;
                    background-color: #FFFFFF;  # Fondo blanco para mejor visibilidad
                    padding: 5px;
                    border-radius: 5px;
                """)
                self.frame_layout.addWidget(label_escalar)

                # Crear QLabel para el vector vertical
                vector_str = "\n".join([f"[{x}]" for x in vector.componentes])
                label_vector = QLabel(vector_str, self)
                label_vector.setAlignment(Qt.AlignCenter)  # Centrar el vector
                label_vector.setStyleSheet("""
                    font-size: 18px;
                    border: 1px solid #B0BEC5;
                    background-color: #FFFFFF;  # Fondo blanco para mejor visibilidad
                    padding: 5px;
                    border-radius: 5px;
                """)
                self.frame_layout.addWidget(label_vector)

                # Agregar el símbolo de suma
                label_suma = QLabel(" + ", self)
                label_suma.setAlignment(Qt.AlignCenter)  # Centrar el símbolo de suma
                label_suma.setStyleSheet("""
                    font-size: 18px;
                    background-color: #FFFFFF;  # Fondo blanco para mejor visibilidad
                    padding: 5px;
                    border-radius: 5px;
                """)
                self.frame_layout.addWidget(label_suma)

            # Remover el último símbolo de suma
            self.frame_layout.takeAt(self.frame_layout.count() - 1)

            # Agregar el símbolo de igual y el resultado
            label_igual = QLabel(" = ", self)
            label_igual.setAlignment(Qt.AlignCenter)  # Centrar el símbolo de igual
            label_igual.setStyleSheet("""
                font-size: 18px;
                background-color: #FFFFFF;  # Fondo blanco para mejor visibilidad
                padding: 5px;
                border-radius: 5px;
            """)
            self.frame_layout.addWidget(label_igual)

            # Crear QLabel para el resultado
            resultado_str = "\n".join([f"[{x:.2f}]" for x in resultado.componentes])
            label_resultado = QLabel(resultado_str, self)
            label_resultado.setAlignment(Qt.AlignCenter)  # Centrar el resultado
            label_resultado.setStyleSheet("""
                font-size: 18px;
                border: 1px solid #B0BEC5;
                background-color: #FFFFFF;  # Fondo blanco para mejor visibilidad
                padding: 5px;
                border-radius: 5px;
            """)
            self.frame_layout.addWidget(label_resultado)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def regresar_menu_principal(self):
        self.main_window = MenuAplicacion()
        self.main_window.show()
        self.close()

class VentanaProductoVectorial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiplicación de Vector Fila x Vector Columna")
        self.setGeometry(100, 100, 1200, 700)
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

        # Tabla para el vector fila (más ancha horizontalmente)
        self.tabla_vector_fila = QTableWidget(self)
        self.tabla_vector_fila.setFixedWidth(350)  # Ajuste del ancho horizontal
        self.tabla_vector_fila.setFixedHeight(70)
        self.tabla_vector_fila.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_vectores.addWidget(self.tabla_vector_fila)

        # Tabla para el vector columna (más ancha horizontalmente)
        self.tabla_vector_columna = QTableWidget(self)
        self.tabla_vector_columna.setFixedWidth(190)  # Ajuste del ancho horizontal
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
        self.label_resultado.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.layout_resultados.addWidget(self.label_resultado)

        # Área de resultados
        self.area_resultados = QTextEdit(self)
        self.area_resultados.setFixedHeight(250)
        self.area_resultados.setReadOnly(True)
        self.layout_resultados.addWidget(self.area_resultados)

        # Botón para regresar al menú principal
        self.boton_regresar = QPushButton("Regresar al Menú Principal", self)
        self.boton_regresar.setFixedWidth(200)
        self.boton_regresar.clicked.connect(self.regresar_menu_principal)
        self.layout_resultados.addWidget(self.boton_regresar, alignment=Qt.AlignCenter)

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
            producto = sum(f * c for f, c in zip(vector_fila, vector_columna))

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
        self.main_window.show()
        self.close()

def iniciar_menu():
    app = QApplication(sys.argv)
    ventana = MenuAplicacion()
    ventana.show()
    sys.exit(app.exec_())