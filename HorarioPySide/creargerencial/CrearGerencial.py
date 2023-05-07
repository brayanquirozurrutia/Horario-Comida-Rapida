import sys
import os

from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QMessageBox, QWidget, QLineEdit, QGridLayout, QComboBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

from funciones.Funciones import ValidaRUT, crear_trabajador, empleado_registrado, jefe


class VentanaCrearGerencial(QMainWindow):
    """Crea una ventana para poder ingresar un nuevo gerencial"""
    def __init__(self):
        super().__init__()
        # Asignamos título
        self.setWindowTitle('Ingreso de Gerencial')
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
        titulo = QLabel('Ingreso de Gerencial')
        # Posicionamos
        self.layout_principal.addWidget(titulo)
        # Centramos y agrandamos
        titulo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        titulo.setFont(QFont('Arial', 15))
        # Creamos un espacio intermedio entre el título y las entradas de datos
        label_intermedio = QLabel()
        # Lo posicionamos
        self.layout_principal.addWidget(label_intermedio)

        # Creamos un grid layout para los botones
        self.grid_layout = QGridLayout()

        # Publicamos el grid layout en el layou principal
        self.layout_principal.addLayout(self.grid_layout)

        # Creamos los componentes
        # Creamos los label
        label_rut = QLabel('RUT')
        label_nombre = QLabel('Nombre')
        label_apellido = QLabel('Apellido')
        label_horas_contrato= QLabel('Horas')
        label_id_cargo = QLabel('ID cargo')
        # Posicionamos label
        self.grid_layout.addWidget(label_rut, 0, 0)
        self.grid_layout.addWidget(label_nombre, 1, 0)
        self.grid_layout.addWidget(label_apellido, 2, 0)
        self.grid_layout.addWidget(label_horas_contrato, 3, 0)
        self.grid_layout.addWidget(label_id_cargo, 4, 0)
        # Creamos entradas de datos
        self.line_edit_rut = QLineEdit()
        self.line_edit_nombre = QLineEdit()
        self.line_edit_apellido = QLineEdit()
        # Asignamos placeholder al rut
        self.line_edit_rut.setPlaceholderText('12345678-5')
        # Posicionamos los Line Edit
        self.grid_layout.addWidget(self.line_edit_rut, 0, 1)
        self.grid_layout.addWidget(self.line_edit_nombre, 1, 1)
        self.grid_layout.addWidget(self.line_edit_apellido, 2, 1)
        # Creamos combobox
        self.combobox_horas = QComboBox()
        self.combobox_cargo = QComboBox()
        # Asignamos valores
        self.combobox_horas.addItems(['45', '30', '20'])
        self.combobox_cargo.addItems(['1: Gerente', '2: Sub Gerente 1', '3: Sub Gerente 2'])
        # Lo posicionamos
        self.grid_layout.addWidget(self.combobox_horas, 3, 1)
        self.grid_layout.addWidget(self.combobox_cargo, 4, 1)
        # Creamos un label para hacer espacio
        label_intermedio_2 = QLabel()
        # Posicionamos
        self.grid_layout.addWidget(label_intermedio_2, 5, 0)

        # Creamos otro grid layout
        self.grid_layout_2 = QGridLayout()
        # Loa gregamos al layout principal
        self.layout_principal.addLayout(self.grid_layout_2)

        # Creamos botón Aceptar y cancelar
        self.boton_crear = QPushButton('Crear')
        self.boton_cancelar = QPushButton('Cancelar')
        # Los posicionamos
        self.grid_layout_2.addWidget(self.boton_crear, 0, 0)
        self.grid_layout_2.addWidget(self.boton_cancelar, 0, 1)

        # Nos conectamos a las señales de los botones crear y cancelar
        self.boton_crear.clicked.connect(self._aceptar)
        self.boton_cancelar.clicked.connect(self._cancelar)

    def _aceptar(self):
        """Evento al hacer click en el boton crear"""
        # Creamos un cantador auxiliar para validar las entradas de datos
        self.contador = 0

        # Recuperamos los valores
        rut = self.line_edit_rut.displayText()
        nombre = self.line_edit_nombre.displayText().capitalize().strip()
        apellido = self.line_edit_apellido.displayText().capitalize().strip()
        horas = int(self.combobox_horas.currentText())
        cargo = self.combobox_cargo.currentIndex()

        # Validamos los campos
        if(len(rut) == 0):
            QMessageBox.warning(self, 'ERROR', 'Debe ingresar un RUT, vuelva a intentarlo', buttons=QMessageBox.Ok)
        elif(len(nombre) == 0):
            QMessageBox.warning(self, 'ERROR', 'Debe ingresar un nombre, vuelva a intentarlo', buttons=QMessageBox.Ok)
        elif(len(apellido) == 0):
            QMessageBox.warning(self, 'ERROR', 'Debe ingresar un apellido, vuelva a intentarlo', buttons=QMessageBox.Ok)
        else:
            # Aumentamos contador
            self.contador +=1

        # Validamos un rut correcto
        rut_validado = ValidaRUT(rut)
        if(rut_validado == False):
            QMessageBox.warning(self, 'RUT ERROR', 'Debe ingresar un rut válido, sin puntos y con guion', buttons=QMessageBox.Ok)
        else:
            self.contador +=1

        # Verificamos si se respetan las condiciones
        if(self.contador == 2):
            # Verificamos existencia del rut en el sistema
            gerencial_registrado = empleado_registrado(rut)

            if(gerencial_registrado != None):
                QMessageBox.warning(self, 'RUT ERROR', f'El rut {rut} ya está registrado', buttons=QMessageBox.Ok)
            else:
                # Corroboramos puesto: Si es gerente, es el jefe
                if(cargo == 0):
                    rut_jefe = rut
                else:
                    rut_jefe = jefe()
                # Corroboramos el ingreso y preguntamos si se desea ingresar
                self.pregunta = QMessageBox.question(self, 'Crear Gerencial', f'RUT: {rut}\nNombre: {nombre}\nApellido: {apellido}\nHoras: {horas}\nCargo: {self.combobox_cargo.currentText()}\n\n¿Confirma creación de gerencial?',
                buttons=QMessageBox.Yes | QMessageBox.No)
                
                # Verificamos respuesta
                if(self.pregunta == QMessageBox.Yes):
                    crear_trabajador(rut, nombre, apellido, horas, (cargo + 1), rut_jefe)
                    QMessageBox.information(self, 'Crear Gerencial', 'Gerencial creado exitosamente', buttons=QMessageBox.Ok)
                    VentanaCrearGerencial.destroy(self)
                    os.execl(sys.executable, sys.executable, * sys.argv)
                    
    def _cancelar(self):
        """Evento al hacer click en el boton cancelar"""
        VentanaCrearGerencial.destroy(self)