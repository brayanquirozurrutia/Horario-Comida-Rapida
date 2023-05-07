import sys
import os

from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QMessageBox, QWidget, QLineEdit, QGridLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

from funciones.Funciones import ValidaRUT, empleado_registrado, eliminar_colaborador


class VentanaEliminarColaborador(QMainWindow):
    """Crea una ventana para poder eliminar un colaborador"""
    def __init__(self):
        super().__init__()
        # Asignamos título
        self.setWindowTitle('Elimianción de Colaborador')
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
        titulo = QLabel('Eliminación de colaborador')
        # Posiciomos
        self.layout_principal.addWidget(titulo)
        # Centramos y agrandamos
        titulo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        titulo.setFont(QFont('Arial', 15))
        # Creamos un espacio intermedio entre el título y las entradas de datos
        label_intermedio = QLabel()
        # Lo posicionamos
        self.layout_principal.addWidget(label_intermedio)

        # Creamos un grid layout
        self.grid_layout = QGridLayout()

        # Publicamos el grid layout en el layou principal
        self.layout_principal.addLayout(self.grid_layout)

        # Creamos los componentes
        # Creamos el label
        label_rut = QLabel('RUT')
        # Posicionamos label
        self.grid_layout.addWidget(label_rut, 0, 0)
        # Creamos entrada de datos
        self.line_edit_rut = QLineEdit()
        # Asignamos placeholder al rut
        self.line_edit_rut.setPlaceholderText('12345678-5')
        # Posicionamos el Line Edit
        self.grid_layout.addWidget(self.line_edit_rut, 0, 1)
        # Creamos un label para hacer espacio
        label_intermedio_2 = QLabel()
        # Posicionamos
        self.grid_layout.addWidget(label_intermedio_2, 1, 0)

        # Creamos otro grid layout para los botones
        self.grid_layout_2 = QGridLayout()
        # Loa gregamos al layout principal
        self.layout_principal.addLayout(self.grid_layout_2)

        # Creamos botón Aceptar y cancelar
        self.boton_eliminar = QPushButton('Eliminar')
        self.boton_cancelar = QPushButton('Cancelar')
        # Los posicionamos
        self.grid_layout_2.addWidget(self.boton_eliminar, 0, 0)
        self.grid_layout_2.addWidget(self.boton_cancelar, 0, 1)

        # Nos conectamos a las señales de los botones crear y cancelar
        self.boton_eliminar.clicked.connect(self._aceptar)
        self.boton_cancelar.clicked.connect(self._cancelar)

    def _aceptar(self):
        """Evento al hacer click en el boton crear"""
        # Creamos un cantador auxiliar para validar las entradas de datos
        self.contador = 0

        # Recuperamos los valores
        rut = self.line_edit_rut.displayText()

        # Validamos los campos
        if(len(rut) == 0):
            QMessageBox.warning(self, 'ERROR', 'Debe ingresar un RUT, vuelva a intentarlo', buttons=QMessageBox.Ok)
        else:
            # Aumentamos sontador
            self.contador +=1

        # Validamos un rut correcto
        rut_validado = ValidaRUT(rut)
        if(rut_validado == False):
            QMessageBox.warning(self, 'RUT ERROR', 'Debe ingresar un rut válido sin puntos y con guion', buttons=QMessageBox.Ok)
        else:
            self.contador +=1

        # Verificamos si se respetan las condiciones
        if(self.contador == 2):
            # Verificamos existencia del rut en el sistema
            gerencial_registrado = empleado_registrado(rut)

            if(gerencial_registrado != None):
                # Corroboramos los datos y preguntamos si se desea elimnar
                self.pregunta = QMessageBox.question(self, 'Eliminar Colaborador', f'RUT: {rut}\n\n¿Confirma eliminación de colaborador?',
                buttons=QMessageBox.Yes | QMessageBox.No)
                
                # Verificamos respuesta
                if(self.pregunta == QMessageBox.Yes):
                    eliminar_colaborador(rut)
                    QMessageBox.information(self, 'Eliminación de Colaborador', 'Colaborador eliminado exitosamente', buttons=QMessageBox.Ok)
                    VentanaEliminarColaborador.destroy(self)
                    os.execl(sys.executable, sys.executable, * sys.argv)
            else:
                QMessageBox.warning(self, 'RUT ERROR', f'El RUT {rut} no existe en el sistema', buttons=QMessageBox.Ok)
    
    def _cancelar(self):
        """Evento al hacer click en el boton cancelar"""
        VentanaEliminarColaborador.destroy(self)