import sys
import os

from datetime import datetime, timedelta

from PySide6.QtWidgets import QMainWindow, QLabel, QCheckBox, QPushButton, QVBoxLayout, QMessageBox, QWidget, QLineEdit, QGridLayout, QDateEdit, QTimeEdit
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QIcon, QFont

from funciones.Funciones import ValidaRUT, empleado_registrado, ingresar_horas_extras


class VentanaCrearHorasExtras(QMainWindow):
    """Crea una ventana para poder ingresar horas extras"""
    def __init__(self):
        super().__init__()
        # Asignamos título
        self.setWindowTitle('Ingreso de Horas Extras')
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
        titulo = QLabel('Ingreso de horas extras')
        # Ponemos en negrita
        titulo.setStyleSheet("font-weight: bold")
        # Posiciomos
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
        # Publicamos el grid layout en el layout principal
        self.layout_principal.addLayout(self.grid_layout)

        # Creamos los componentes
        # Creamos los label
        label_rut = QLabel('RUT')
        label_fecha = QLabel('Fecha')
        label_hora_entrada = QLabel('Hora de entrada')
        label_hora_salida = QLabel('Hora de salida')
        label_turno_extra = QLabel('¿Es turno extra?')
        # Posicionamos label
        self.grid_layout.addWidget(label_rut, 0, 0)
        self.grid_layout.addWidget(label_fecha, 1, 0)
        self.grid_layout.addWidget(label_hora_entrada, 2, 0)
        self.grid_layout.addWidget(label_hora_salida, 3, 0)
        self.grid_layout.addWidget(label_turno_extra, 4, 0)
        # Creamos entradas de datos
        self.rut = QLineEdit()
        self.edit_fecha = QDateEdit()
        self.edit_entrada = QTimeEdit()
        self.edit_salida = QTimeEdit()
        self.turno_extra = QCheckBox()
        # Asignamos placeholder
        self.rut.setPlaceholderText('12345678-5')
        # Asignamos formato de horas
        self.edit_entrada.setDisplayFormat('hh:mm:ss')
        self.edit_salida.setDisplayFormat('hh:mm:ss')
        # Activamos edit de fecha
        self.edit_fecha.setKeyboardTracking(True)
        # Asignamos fecha de hoy al edit
        self.edit_fecha.setDate(QDate.currentDate())
        # Asignamos como fecha máxima el día de hoy
        self.edit_fecha.setMaximumDate(QDate.currentDate())
        # Posicionamos los Edit
        self.grid_layout.addWidget(self.rut, 0, 1)
        self.grid_layout.addWidget(self.edit_fecha, 1, 1)
        self.grid_layout.addWidget(self.edit_entrada, 2, 1)
        self.grid_layout.addWidget(self.edit_salida, 3, 1)
        # Posicionamos checkbox
        self.grid_layout.addWidget(self.turno_extra, 4, 1)
        # Creamos un label para hacer espacio
        label_intermedio_2 = QLabel()
        # Posicionamos
        self.grid_layout.addWidget(label_intermedio_2, 5, 0)

        # Creamos otro grid layout
        self.grid_layout_2 = QGridLayout()
        # Lo agregamos al layout principal
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
        rut = self.rut.displayText()
        fecha = self.edit_fecha.date().toString('dd-MM-yyyy')
        hora_entrada = self.edit_entrada.time()
        hora_salida = self.edit_salida.time()

        # Calculamos horas trabajadas
        # Entrada
        h_entrada = int(hora_entrada.toPython().hour)
        m_entrada = int(hora_entrada.toPython().minute)
        s_entrada = int(hora_entrada.toPython().second)
        # Salida
        h_salida = int(hora_salida.toPython().hour)
        m_salida = int(hora_salida.toPython().minute)
        s_salida = int(hora_salida.toPython().second)
        # Calculamos delta horas
        delta_horas = datetime(1, 1, 1, h_salida, m_salida, s_salida) - datetime(1, 1, 1, h_entrada, m_entrada, s_entrada)
        
        if(self.turno_extra.checkState() == Qt.Checked):
            turno_extra = True
            delta_horas -= timedelta(seconds=1800)
            delta_horas = delta_horas.seconds / 3600
            
        else:
            turno_extra = False
            delta_horas = delta_horas.seconds / 3600

        # Validamos que la hora de salida sea mayor a la de entrada 
        if(hora_salida > hora_entrada):
            self.contador += 1
        else:
            QMessageBox.warning(self, 'HORA ERROR', 'La hora de salida debe ser mayor a la de entrada',
                buttons=QMessageBox.Ok)
        
        # Validamos consistencia horario para turno extra
        if(turno_extra):
            if(hora_salida > hora_entrada.addSecs(1800)):
                    self.contador += 1
            else:
                QMessageBox.warning(self, 'HORA ERROR', 'La hora de salida debe contemplar la colación de 30 minutos',
                    buttons=QMessageBox.Ok)
        else:
            self.contador += 1
        
        # Validamos un rut correcto
        rut_validado = ValidaRUT(rut)
        if(rut_validado == False):
            QMessageBox.warning(self, 'RUT ERROR', 'Debe ingresar un rut válido, sin puntos y con guion', buttons=QMessageBox.Ok)
        else:
            self.contador +=1

        # Verificamos si se respetan las condiciones
        if(self.contador == 3):
            # Verificamos existencia del rut en el sistema
            gerencial_registrado = empleado_registrado(rut)

            if(gerencial_registrado == None):
                QMessageBox.warning(self, 'RUT ERROR', f'El rut {rut} no está registrado', buttons=QMessageBox.Ok)
            else:
                # Corroboramos el ingreso y preguntamos si se desea ingresar
                self.pregunta = QMessageBox.question(self, 'Ingresar Horas Extras', f'Fecha: {fecha}\nHora de entrada: {hora_entrada.toString("hh:mm:ss")}\nHora de salida: {hora_salida.toString("hh:mm:ss")}\nTurno extra: {turno_extra}\nHoras totales: {delta_horas} horas\n\n¿Confirma ingreso de horas extras?',
                buttons=QMessageBox.Yes | QMessageBox.No)
                
                # Verificamos respuesta
                if(self.pregunta == QMessageBox.Yes):
                    ingresar_horas_extras(rut, fecha, delta_horas, turno_extra)
                    QMessageBox.information(self, 'Ingresar Horas Extras', 'Horas registradas exitosamente', buttons=QMessageBox.Ok)
                    VentanaCrearHorasExtras.destroy(self)
                    os.execl(sys.executable, sys.executable, * sys.argv)
 
    def _cancelar(self):
        """Evento al hacer click en el boton cancelar"""
        VentanaCrearHorasExtras.destroy(self)