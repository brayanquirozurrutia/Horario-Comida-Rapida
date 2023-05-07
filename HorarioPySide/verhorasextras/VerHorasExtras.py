from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QMessageBox, QWidget, QLineEdit, QGridLayout, QDateEdit
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QIcon, QFont

from funciones.Funciones import ValidaRUT, empleado_registrado, ver_horas_extras


class VentanVerHorasExtras(QMainWindow):
    """Crea una ventana para poder ver las horas extras realizadas"""
    def __init__(self):
        super().__init__()
        # Asignamos título
        self.setWindowTitle('Visualización de Horas Extras')
        # Asignamos icono
        self.setIconSize(QSize(16, 16))
        self.setWindowIcon(QIcon("../Icono/iHorario.ico"))

        # Creamos un contenedor general para almacenar los layout
        self.contenedor_general = QWidget(self)
        # Publicamos el compoenente
        self.setCentralWidget(self.contenedor_general)

        # Creamos un layout vertical principal
        self.layout_principal = QVBoxLayout()
        # Lo publicamos
        self.contenedor_general.setLayout(self.layout_principal)
        # Creamos un título
        titulo = QLabel('Visualización de Horas Extras')
        # Posiciomos
        self.layout_principal.addWidget(titulo)
        # Centramos y agrandamos
        titulo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        titulo.setFont(QFont('Arial', 15))
        # Ponemos en negrita
        titulo.setStyleSheet("font-weight: bold")
        # Creamos un espacio intermedio entre el título y las entradas de datos
        label_intermedio = QLabel()
        # Lo posicionamos
        self.layout_principal.addWidget(label_intermedio)

        # Creamos un grid layout para los botones
        self.grid_layout = QGridLayout()
        # Publicamos el grid layout en el layout principal
        self.layout_principal.addLayout(self.grid_layout)

        # Creamos los componentes
        # Creamos el label
        label_rut = QLabel('RUT')
        label_fecha_inicial = QLabel('Fecha inicial')
        label_fecha_final = QLabel('Fecha final')
        # Posicionamos label
        self.grid_layout.addWidget(label_rut, 0, 0)
        self.grid_layout.addWidget(label_fecha_inicial, 1, 0)
        self.grid_layout.addWidget(label_fecha_final, 2, 0)
        # Creamos entradas de datos
        self.line_edit_rut = QLineEdit()
        self.edit_fecha_inicial = QDateEdit()
        self.edit_fecha_final = QDateEdit()
        # Asignamos placeholder al rut
        self.line_edit_rut.setPlaceholderText('12345678-5')
        # Asignamos como fecha máxima el día de hoy
        self.edit_fecha_inicial.setMaximumDate(QDate.currentDate())
        self.edit_fecha_final.setMaximumDate(QDate.currentDate())
        # Asignamos fecha de hoy a los edit
        self.edit_fecha_inicial.setDate(QDate.currentDate())
        self.edit_fecha_final.setDate(QDate.currentDate())
        # Posicionamos los Edit
        self.grid_layout.addWidget(self.line_edit_rut, 0, 1)
        self.grid_layout.addWidget(self.edit_fecha_inicial, 1, 1)
        self.grid_layout.addWidget(self.edit_fecha_final, 2, 1)
        # Creamos un label para hacer espacio
        label_intermedio_2 = QLabel()
        # Posicionamos
        self.grid_layout.addWidget(label_intermedio_2, 1, 0)

        # Creamos otro grid layout
        self.grid_layout_2 = QGridLayout()
        # Lo agregamos al layout principal
        self.layout_principal.addLayout(self.grid_layout_2)

        # Creamos botón Aceptar y cancelar
        self.boton_ver = QPushButton('Ver horas')
        self.boton_cancelar = QPushButton('Cancelar')
        # Los posicionamos
        self.grid_layout_2.addWidget(self.boton_ver, 0, 0)
        self.grid_layout_2.addWidget(self.boton_cancelar, 0, 1)

        # Nos conectamos a las señales de los botones crear y cancelar
        self.boton_ver.clicked.connect(self._aceptar)
        self.boton_cancelar.clicked.connect(self._cancelar)

    def _aceptar(self):
        """Evento al hacer click en el boton ver horas"""
        # Creamos un cantador auxiliar para validar las entradas de datos
        self.contador = 0

        # Recuperamos los valores
        rut = self.line_edit_rut.displayText()
        fecha_inicial = self.edit_fecha_inicial.date()
        fecha_final = self.edit_fecha_final.date()

        # Validamos un rut correcto
        rut_validado = ValidaRUT(rut)
        if(rut_validado == False):
            QMessageBox.warning(self, 'RUT ERROR', 'Debe ingresar un rut válido, sin puntos y con guion', buttons=QMessageBox.Ok)
        else:
            self.contador +=1
        
        # Validamos consistencia de fechas
        if(fecha_final >= fecha_inicial):
            self.contador += 1
        else:
             QMessageBox.warning(self, 'FECHA ERROR', 'La fecha final debe ser mayor o igual a la fecha inicial', buttons=QMessageBox.Ok)

        # Verificamos si se respetan las condiciones
        if(self.contador == 2):
            # Verificamos existencia del rut en el sistema
            gerencial_registrado = empleado_registrado(rut)

            if(gerencial_registrado is None):
                QMessageBox.warning(self, 'RUT ERROR', f'El rut {rut} no está registrado', buttons=QMessageBox.Ok)
            else:
                # Realizamos búsqueda
                horas_extras = ver_horas_extras(rut, fecha_inicial.toString('dd-MM-yyyy'), fecha_final.toString('dd-MM-yyyy'))

                # Mostramos resultado
                QMessageBox.information(self, 'Ver horas extras', f'RUT: {rut}\n\nUsted ha realizado {horas_extras} horas extras entre el {fecha_inicial.toString("dd-MM-yyyy")} y el {fecha_final.toString("dd-MM-yyyy")}',
                buttons=QMessageBox.Ok)
                    
    def _cancelar(self):
        """Evento al hacer click en el boton cancelar"""
        VentanVerHorasExtras.destroy(self)
        