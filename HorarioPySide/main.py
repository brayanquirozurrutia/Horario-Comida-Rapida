from functools import partial

from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QMessageBox, QWidget, QLineEdit, QGridLayout, QHBoxLayout, QComboBox, QCalendarWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon, QFont

import sys
import locale

from datetime import datetime, timedelta

from funciones.Funciones import cantidad_de_colaboradores, nombre_apellido_colaborador, obtener_horas_contrato_colaboradores, calcular_horas_semanales_colaborador, cantidad_de_gerenciales, nombre_apellido_gerencial, obtener_horas_contrato_gerenciales, creacion_tabla

from creargerencial.CrearGerencial import VentanaCrearGerencial
from eliminargerencial.EliminarGerencial import VentanaEliminarGerencial
from crearcolaborador.CrearColaborador import VentanaCrearColaborador
from eliminarcolaborador.EliminarColaborador import VentanaEliminarColaborador
from crearhorasextras.CrearHorasExtras import VentanaCrearHorasExtras
from verhorasextras.VerHorasExtras import VentanVerHorasExtras

class Horario(QMainWindow):
    def __init__(self):
        super().__init__()

        # Definimos nombre de la ventana
        self.setWindowTitle('iHorario')
        # Asignamos icono
        self.setIconSize(QSize(16, 16))
        self.setWindowIcon(QIcon("../Icono/iHorario.ico"))

        # Creamos un contenedor general para almacenar los layout
        self.contenedor_general = QWidget(self)
        # Publicamos el compoenente
        self.setCentralWidget(self.contenedor_general)

        # Creamos un layout principal vertical
        self.layout_principal = QVBoxLayout()
        # Publicamos el layout pricipal
        self.contenedor_general.setLayout(self.layout_principal)

        # Definimos la coordenada X e Y de la grilla para poder posicionar de mejor manera los widget
        self.row = 0
        self.column = 0

        # Creamos la estructura de la BBDD
        creacion_tabla()

        # Creamos el título
        self._crear_label_titulo()

        # Creamos el subtítulo (se debe mostrar al elegir la semana)
        self._crear_label_subtitulo()

        # Creamos un gridlayout
        self.grid_layout_colaboradores = QGridLayout()

        # Creamos los label con los nombres de los días de la semana y las etiquetas de entrada y salida
        self._label_dias_semana()

        # Mostramos los combobox con los nombres de los colaboradores
        self._nombres_colaboradores()

        # Creamos los label con las horas pactadas por contrato de un colaborador
        self._label_horas_contrato_colaborador()

        # Creamos Line Edit para mostrar la suma de horas semanales ingresadas
        self._total_horas_semana_colaborador()

        # Creamos los combobox de los rangos horarios de cada día de la semana
        self._combobox_dias_colaboradores()

        # Creamos un diccionario que para almacenar todas las horas de entrada seleccionadas
        self.diccionario_horas_seleccionadas_entrada = {}

        # Creamos un diccionario que para almacenar todas las horas de salida seleccionadas
        self.diccionario_horas_seleccionadas_salida = {}
        
        # Creamos una lista que almacenará los nombres seleccionados para evitar duplicidad al momento de seleccionarlos
        self.lista_nombres_colaboradores = []

        # Creamos una lista que almacenará los nombres seleccionados para evitar duplicidad al momento de seleccionarlos
        self.lista_nombres_gerenciales = []

        # Mostramos los combobox con los nombres de los gerenciales
        self._nombres_gerenciales()

        # Creamos los label con las horas pactadas por contrato de un gerencial
        self._label_horas_contrato_gerencial()

        # Creamos Line Edit para mostrar la suma de horas semanales ingresadas de los gerenciales
        self._total_horas_semana_gerencial()

        # Creamos los combobox de los rangos horarios de cada día de la semana para los gerenciales
        self._combobox_dias_gerenciales()

        # Creamso un layout horizontal para centrar los botones
        self.layout_horizontal = QHBoxLayout()

        # Creamos un grid layout para posicionar los botones
        self.grid_layout_botones = QGridLayout()
        # Creamos un grid layout para posicionar el calendario
        self.grid_layout_calendario = QGridLayout()

        # Creamos el botón para crear gerenciales
        self._crear_gerencial()

        # Creamos el botón para eliminar gerenciales
        self._eliminar_gerencial()

        # Creamos el botón para crear colaboradores
        self._crear_colaborador()

        # Creamos el botón para poder eliminar un colaborador
        self._eliminar_gcolaborador()

        # Creamos el botón para ingresar horas extras
        self._ingresar_horas_extras()

        # Creamos el botón para ver horas extras
        self._ver_horas_extras()

        # Creamos calendario para eligir semana de ingreso de horario
        self._elegir_semana()

        # Creamos el menú
        self._crear_menu()

    def _crear_label_titulo(self):
        """Crea un label usado como título"""

        # Creamos titulo principal
        self.label_titulo = QLabel('Horario semanal')
        # Agrandamos letra
        self.label_titulo.setFont(QFont('Arial', 25))
        # Ponemos negrita
        self.label_titulo.setStyleSheet("font-weight: bold")
        # Centramos el título
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # Creamos un espacio
        label = QLabel()
        # Publicamos titulo principal
        self.layout_principal.addWidget(self.label_titulo)
        # Publicamos espacio
        self.layout_principal.addWidget(label)
    
    def _crear_label_subtitulo(self):
        """Crea un label usado como subtítulo encargado de mostrar la semana seleccionada para hacer ingreso del horario"""
        # Creamos subtítulo con la semana actual
        self.label_subtitulo = QLabel('')
        # Agrandamos letra
        self.label_subtitulo.setFont(QFont('Arial', 20))
        # Ponemos negrita
        self.label_subtitulo.setStyleSheet("font-weight: bold")
        # Centramos el título
        self.label_subtitulo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # Creamos un espacio
        label = QLabel()
        # Publicamos el subtítulo
        self.layout_principal.addWidget(self.label_subtitulo)
        # Publicamos espacio
        self.layout_principal.addWidget(label)
    
    def _label_dias_semana(self):
        """Crea los label con los nombres de los días de la semana y los de entrada y salida"""
        
        # Creamos una lista con los nombres de los días de la semana
        lista_días_semana = [
            'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'
        ]

        # Creamos un diccionario con los label de los nombres de los días de la semana
        self.diccionario_label_dias_semana = {}
        # Seteamos posición inicial
        self.row = 0; self.column = 2
        for i in range(7):
            # Creamos los label
            self.diccionario_label_dias_semana[f'label_dia_semana_{i}'] = [QLabel(), i]
            # Le asignamos el valor
            self.diccionario_label_dias_semana[f'label_dia_semana_{i}'][0].setText(lista_días_semana[i])
            # Ponemos negrita
            self.diccionario_label_dias_semana[f'label_dia_semana_{i}'][0].setStyleSheet("font-weight: bold")
            # Posicionamos los label
            self.grid_layout_colaboradores.addWidget(self.diccionario_label_dias_semana[f'label_dia_semana_{i}'][0],
                                                    (self.row), (self.column), 1, 2, Qt.AlignmentFlag.AlignCenter)
            self.column += 2
        
        # Creamos los label de entrada y salida
        # Creamos un diccionario con los label de entrada y salida
        self.diccionario_label_entrada_salida= {}
        # Seteamos posición inicial
        self.row = 1; self.column = 2
        for i in range(14):
            # Creamos los label
            self.diccionario_label_entrada_salida[f'label_{i}'] = QLabel()
            # Ponemos negrita
            self.diccionario_label_entrada_salida[f'label_{i}'].setStyleSheet("font-weight: bold")
            # Le asignamos el valor
            if(i%2 == 0):
                self.diccionario_label_entrada_salida[f'label_{i}'].setText('Entrada')
            else:
                self.diccionario_label_entrada_salida[f'label_{i}'].setText('Salida')
            # Posicionamos los label
            self.grid_layout_colaboradores.addWidget(self.diccionario_label_entrada_salida[f'label_{i}'],
                                            (self.row), (self.column + i),1,1,Qt.AlignmentFlag.AlignCenter)
    
    def _rango_horario(self):
        """Obtiene el rango horario disponible para realizar labores"""

        # Creamos una hora seteada a las 00:00
        hora_base = datetime(1,1,1,0,0)
        # Creamos una lista que almacenará todas las medias horas de un día
        lista_horas = []
        for i in range(49):
            hora = hora_base + timedelta(0,1800*i)
            # Las agregamos a la lista en las dejamos en formato HH:MM
            lista_horas.append(hora.strftime("%H:%M"))
        
        return lista_horas

    # ------------------------------------------------------COLABORADORES------------------------------------------------------

    def _nombres_colaboradores(self):
        """Crea los combobox con los nombres de los colaboradores registrados en el sistema"""

        # Creamos una etiqueta con la palabra nombre
        label_nombre = QLabel('Nombre')
        # Ponemos negrita
        label_nombre.setStyleSheet("font-weight: bold")
        # La posicionamos
        self.grid_layout_colaboradores.addWidget(label_nombre, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Creamos un diccionario para almacenar los obtjetos del tipo combobox que almacenan los nombres de los colaboradores
        # Seteamos la posición
        self.row = 2
        self.diccionario_combobox_colaboradores = {}
        for i in range(cantidad_de_colaboradores()):
            # Creamos el combobox
            self.diccionario_combobox_colaboradores[f'combobox_{i}'] = [QComboBox(), i]
            # Posicionamos el combobox
            self.grid_layout_colaboradores.addWidget(self.diccionario_combobox_colaboradores[f'combobox_{i}'][0], (self.row+i), 0)
            # Le asignamos los valores a los combobox
            self.diccionario_combobox_colaboradores[f'combobox_{i}'][0].addItems(nombre_apellido_colaborador())
            # Ajustamos el tamaño
            self.diccionario_combobox_colaboradores[f'combobox_{i}'][0].setFixedWidth(130)
            # Rescatamos la señal de éste para mostrar las horas pactadas por contrato de un colaborador
            self.diccionario_combobox_colaboradores[f'combobox_{i}'][0].textActivated.connect(partial(self._muestra_horas_colaboradores,self.diccionario_combobox_colaboradores[f'combobox_{i}'][1]))
            # Rescatamos la señal para evitar que se seleccione 2 veces el mismo colaborador
            self.diccionario_combobox_colaboradores[f'combobox_{i}'][0].textActivated.connect(self._nombres_duplicados)

        # Agregamos el layout grid al layout horizontal
        self.layout_principal.addLayout(self.grid_layout_colaboradores)
    
    def _muestra_horas_colaboradores(self,posicion, nombre):
        """Cambia el texto de los label que almacenan las horas pactadas por contrato de un colaborador y muestra las horas del colaborador seleccionado
        
        posicion: posicion que ocupa el combobox seleccionado
        nombre: nombre del colaborador seleccionado en el combobox"""

        # Mostramos la etiqueta Horas contrato
        self.etiqueta_horas.setText('Horas contrato')
        # Ponemos negrita
        self.etiqueta_horas.setStyleSheet("font-weight: bold")
        # Damos ancho
        self.etiqueta_horas.setFixedWidth(90)

        # Ajustamos todo para que se vea más estético
        self.etiqueta_intermedia_2.setFixedWidth(90)

        # Rescatamos las horas de un colaborador en función de su nombre y apellido
        horas = obtener_horas_contrato_colaboradores(nombre)
        
        for valor in  self.diccionario_label_horas_colaboradores.values():
            if(valor[1] == posicion):
                valor[0].setText(f'{horas}')
    
    def _nombres_duplicados(self, texto):
        """Busca si un nombre ya se ha seleccionado para hacer ingreso de su horario y así, evitar duplicidad
        
        texto: Nombre del colaborador mostrado en el combobox"""
        # Buscamos si el texno no está almacenado y lo agregamos
        if(texto not in self.lista_nombres_colaboradores):
            self.lista_nombres_colaboradores.append(texto)
        else:
            # Si se ha seleccionado 2 veces, lanzamos el mensaje
            QMessageBox.information(self, 'Nombre duplicado',
                                        f'El colaborador {texto} ya se ha seleccionado\n\nseleccione otro nombre',
                                        buttons=QMessageBox.Ok)

    def _label_horas_contrato_colaborador(self):
        """Crea los label que rescatan las horas por contrado de un colaborador seleccionado"""
        # Creamos la etiqueta con la palabra Horas contrato
            # Se activa al seleccionar un colaborador
        self.etiqueta_horas = QLabel(' ')
        # La posicionamos
        self.grid_layout_colaboradores.addWidget(self.etiqueta_horas,1,1)

        # Creamos un diccionario para almacenar los label con las horas por contrato de cada trabajador
        self.diccionario_label_horas_colaboradores = {}
        # Seteamos la posición inicial
        self.row = 2; self.column = 1
        for i in range(cantidad_de_colaboradores()):
            # Creamos los label
            self.diccionario_label_horas_colaboradores[f'label_horas_contrato_{i}'] = [QLabel(), i]
            # Posicionamos los label
            self.grid_layout_colaboradores.addWidget(self.diccionario_label_horas_colaboradores[f'label_horas_contrato_{i}'][0],
                                                            (self.row + i), 1,1,1, Qt.AlignmentFlag.AlignCenter)
    
    def _combobox_dias_colaboradores(self):
        """Crea los combobox para ingresar las horas de trabajo diarias de entrada y salida"""
        # Calculamos la cantidad de combobox a crear
        total_combobox = 14 * cantidad_de_colaboradores()

        # Creamos un diccionario con los combobox a crear
        self.diccionario_combobox_horas = {}
        # Seteamos posición inicial
        self.row = 2; self.column = 2
        for i in range(1, total_combobox + 1):
            j = int(i /15)
            self.diccionario_combobox_horas[f'combobox_dias_{i}'] = [QComboBox(), i]
            # Le asignamos los valores
            self.diccionario_combobox_horas[f'combobox_dias_{i}'][0].addItem('LIBRE')
            self.diccionario_combobox_horas[f'combobox_dias_{i}'][0].addItems(self._rango_horario())
            # Los posicionamos
            self.grid_layout_colaboradores.addWidget(self.diccionario_combobox_horas[f'combobox_dias_{i}'][0],
                                                    self.row, self.column)
            self.column += 1
            # Lo conectamos a la señal
            self.diccionario_combobox_horas[f'combobox_dias_{i}'][0].textActivated.connect(partial(self._muestra_horas_totales_semana,self.diccionario_combobox_horas[f'combobox_dias_{i}'][1], self.diccionario_line_edit_horas_semana[f'line_edit_{j}'], j, 
                                                    self.diccionario_label_horas_colaboradores[f'label_horas_contrato_{j}']))

            # Cambiamos la fila cuando se llegue al domingo
            if(i%14 == 0):
                self.row += 1
                self.column = 2
    
    def _muestra_horas_totales_semana(self, posicion, line_edit, j, label_horas ,texto):
        """Muestra las horas trabajadas por un colaborador al ingresar su entrada y salida
        
        posición: Posición que ocupa el conbobox interactuado
        line_edit: Line edit que muestra la suma total de horas ingresadas para un colaborador
        j: Posición del Line edit
        label_horas: Label que contiene las horas pactadas por contrato de un colaborador
        texto: Texto del combobox a recuperar"""

        # Llamamos a la función encargada de calcular las horas trabajadas por un crew 
        calcular_horas_semanales_colaborador(self, posicion, texto, line_edit, self.diccionario_horas_seleccionadas_entrada, self.diccionario_horas_seleccionadas_salida, j, label_horas)
    
    def _total_horas_semana_colaborador(self):
        """Crea los line edit que almacenarán la suma de horas seleccionadas para la jornada semanal de un colaborador"""
        # Creamos una etiqueta con la palabra Horas semanales
        etiqueta_horas_semanales = QLabel('Horas semanales')
        # Ponemos negrita
        etiqueta_horas_semanales.setStyleSheet("font-weight: bold")
        # Posicionamos
        self.grid_layout_colaboradores.addWidget(etiqueta_horas_semanales, 1, 17)
        # Creamos un diccionario con los line edit de la suma totald de horas semanales
        self.diccionario_line_edit_horas_semana = {}
        # Seteamos posición inicial
        self.row = 2; self.column = 17
        for i in range(cantidad_de_colaboradores()):
            # Creamos el line Edit
            self.diccionario_line_edit_horas_semana[f'line_edit_{i}'] = [QLineEdit('00:00'), i]
            # Los posicionamos
            self.grid_layout_colaboradores.addWidget(self.diccionario_line_edit_horas_semana[f'line_edit_{i}'][0],
                                                    (self.row+i), self.column)
            # Lo hacemos de solo lectura
            self.diccionario_line_edit_horas_semana[f'line_edit_{i}'][0].setReadOnly(True)
    
    # ------------------------------------------------------GERENCIALES------------------------------------------------------
    
    def _nombres_gerenciales(self):
        """Crea los combobox con los nombres de los gerenciales registrados en el sistema"""
        # Creamos un gridlayout
        self.grid_layout_gerenciales = QGridLayout()

        # Creamos un diccionario para almacenar los obtjetos del tipo combobox que almacenan los nombres de los gerenciales
        # Seteamos la posición
        self.row = 1
        self.diccionario_combobox_gerenciales= {}
        for i in range(cantidad_de_gerenciales()):
            # Creamos el combobox
            self.diccionario_combobox_gerenciales[f'combobox_{i}'] = [QComboBox(), i]
            # Posicionamos el combobox
            self.grid_layout_gerenciales.addWidget(self.diccionario_combobox_gerenciales[f'combobox_{i}'][0], (self.row+i), 0)
            # Le asignamos los valores a los combobox
            self.diccionario_combobox_gerenciales[f'combobox_{i}'][0].addItems(nombre_apellido_gerencial())
            # Ajustamos el tamaño
            self.diccionario_combobox_gerenciales[f'combobox_{i}'][0].setFixedWidth(130)
            # Rescatamos la señal de éste para mostrar las horas pactadas por contrato de un colaborador
            self.diccionario_combobox_gerenciales[f'combobox_{i}'][0].textActivated.connect(partial(self._muestra_horas_gerenciales,self.diccionario_combobox_gerenciales[f'combobox_{i}'][1]))
            # Rescatamos la señal para evitar que se seleccione 2 veces el mismo colaborador
            self.diccionario_combobox_gerenciales[f'combobox_{i}'][0].textActivated.connect(self._nombres_duplicados_gerencial)

        # Agregamos el layout grid al layout horizontal
        self.layout_principal.addLayout(self.grid_layout_gerenciales)
    
    def _muestra_horas_gerenciales(self,posicion, nombre):
        """Cambia el texto de los label que almacenan las horas pactadas por contrato de un gerencial y muestra las horas del gerencial seleccionado
        
        posicion: posicion que ocupa el combobox seleccionado
        nombre: nombre del gerencial seleccionado en el combobox"""

        # Ajustamos ancho
        self.etiqueta_intermedia_2.setFixedWidth(90)
        # Seteamos texto
        self.etiqueta_horas.setText('Horas contrato')
        # Ponemos negrita
        self.etiqueta_horas.setStyleSheet("font-weight: bold")
        # Damos ancho
        self.etiqueta_horas.setFixedWidth(90)

        # Rescatamos las horas de un colaborador en función de su nombre y apellido
        horas = obtener_horas_contrato_gerenciales(nombre)
        
        for valor in  self.diccionario_label_horas_gerencial.values():
            if(valor[1] == posicion):
                valor[0].setText(f'{horas}')
    
    def _nombres_duplicados_gerencial(self, texto):
        """Busca si un nombre ya se ha seleccionado para hacer ingreso de su horario y así, evitar duplicidad
        
        texto: Nombre del gerencial mostrado en el combobox"""
        # Buscamos si el texno no está almacenado y lo agregamos
        if(texto not in self.lista_nombres_gerenciales):
            self.lista_nombres_gerenciales.append(texto)
        else:
            # Si se ha seleccionado 2 veces, lanzamos el mensaje
            QMessageBox.information(self, 'Nombre duplicado',
                                        f'El gerencial {texto} ya se ha seleccionado\n\nseleccione otro nombre',
                                        buttons=QMessageBox.Ok)
    
    def _label_horas_contrato_gerencial(self):
        """Crea los label que rescatan las horas por contrado de un gerencial seleccionado"""

        # Creamos la etiqueta intermedia para separar las horas pacatdas por contrato al seleccionar un gerencial y el combobox
        # Para ingresar jornada
            # Se activa al seleccionar un colaborador
        self.etiqueta_intermedia_2 = QLabel(' ')
        # La posicionamos
        self.grid_layout_gerenciales.addWidget(self.etiqueta_intermedia_2,0,1)

        # Creamos un diccionario para almacenar los label con las horas por contrato de cada gerencial
        self.diccionario_label_horas_gerencial = {}
        # Seteamos la posición inicial
        self.row = 1
        for i in range(cantidad_de_gerenciales()):
            # Creamos los label
            self.diccionario_label_horas_gerencial[f'label_horas_contrato_{i}'] = [QLabel(), i]
            # Ajustamos ancho
            # self.diccionario_label_horas_gerencial[f'label_horas_contrato_{i}'][0].setFixedWidth(80)
            # Posicionamos los label
            self.grid_layout_gerenciales.addWidget(self.diccionario_label_horas_gerencial[f'label_horas_contrato_{i}'][0],
                                                            (self.row + i), 1,1,1, Qt.AlignmentFlag.AlignCenter)
            
    def _combobox_dias_gerenciales(self):
        """Crea los combobox para ingresar las horas de trabajo diarias de entrada y salida de un gerencial"""
        # Calculamos la cantidad de combobox a crear
        total_combobox = 14 * cantidad_de_gerenciales()

        # Creamos un diccionario con los combobox a crear
        self.diccionario_combobox_horas_gerenciales = {}
        # Seteamos posición inicial
        self.row = 1; self.column = 2
        for i in range(1, total_combobox + 1):
            j = int(i /15)
            self.diccionario_combobox_horas_gerenciales[f'combobox_dias_{i}'] = [QComboBox(), i]
            # Le asignamos los valores
            self.diccionario_combobox_horas_gerenciales[f'combobox_dias_{i}'][0].addItem('LIBRE')
            self.diccionario_combobox_horas_gerenciales[f'combobox_dias_{i}'][0].addItems(self._rango_horario())
            # Los posicionamos
            self.grid_layout_gerenciales.addWidget(self.diccionario_combobox_horas_gerenciales[f'combobox_dias_{i}'][0],
                                                    self.row, self.column)
            self.column += 1
            # Lo conectamos a la señal
            # REVISAR ESTO
            self.diccionario_combobox_horas_gerenciales[f'combobox_dias_{i}'][0].textActivated.connect(partial(self._muestra_horas_totales_semana_gerencial,self.diccionario_combobox_horas_gerenciales[f'combobox_dias_{i}'][1], self.diccionario_line_edit_horas_semana_gerencial[f'line_edit_{j}'], j, 
                                                    self.diccionario_label_horas_gerencial[f'label_horas_contrato_{j}']))

            # Cambiamos la fila cuando se llegue al domingo
            if(i%14 == 0):
                self.row += 1
                self.column = 2
    
    def _muestra_horas_totales_semana_gerencial(self, posicion, line_edit, j, label_horas ,texto):
        """Muestra las horas trabajadas por un gerenciañ al ingresar su entrada y salida
        
        posición: Posición que ocupa el conbobox interactuado
        line_edit: Line edit que muestra la suma total de horas ingresadas para un gerencial
        j: Posición del Line edit
        label_horas: Label que contiene las horas pactadas por contrato de un gerencial
        texto: Texto del combobox a recuperar"""

        # Llamamos a la función encargada de calcular las horas trabajadas por un crew 
        calcular_horas_semanales_colaborador(self, posicion, texto, line_edit, self.diccionario_horas_seleccionadas_entrada, self.diccionario_horas_seleccionadas_salida, j, label_horas)

    def _total_horas_semana_gerencial(self):
        """Crea los line edit que almacenarán la suma de horas seleccionadas para la jornada semanal de un gerenciual"""
        # Creamos un diccionario con los line edit de la suma totald de horas semanales
        self.diccionario_line_edit_horas_semana_gerencial = {}
        # Seteamos posición inicial
        self.row = 1; self.column = 17
        for i in range(cantidad_de_gerenciales()):
            # Creamos el line Edit
            self.diccionario_line_edit_horas_semana_gerencial[f'line_edit_{i}'] = [QLineEdit('00:00'), i]
            # Los posicionamos
            self.grid_layout_gerenciales.addWidget(self.diccionario_line_edit_horas_semana_gerencial[f'line_edit_{i}'][0],
                                                    (self.row+i), self.column)
            # Lo hacemos de solo lectura
            self.diccionario_line_edit_horas_semana_gerencial[f'line_edit_{i}'][0].setReadOnly(True)

    # ------------------------------------------------------BOTONES------------------------------------------------------

    def _crear_gerencial(self):
        """Creamos un botón para agregar nuevos gerenciales"""
        # Creamos un espacio para separar los botones
        label_intermedio_vertical_1 = QLabel()
        # Lo posicionamos
        self.layout_principal.addWidget(label_intermedio_vertical_1)

        # Agregamos el layour horizontal al principal
        self.layout_principal.addLayout(self.layout_horizontal)

        # Creamos un espacio para centrar los botones
        label_intermedio_horizontal_1 = QLabel()
        # Lo posicionamos
        self.layout_horizontal.addWidget(label_intermedio_horizontal_1)

        # Agregamos el grid layout al layout principal
        self.layout_horizontal.addLayout(self.grid_layout_botones)

        # Creamos el botón
        self.boton_crear_gerencial = QPushButton('Crear gerencial')
        # Lo posicionamos
        self.grid_layout_botones.addWidget(self.boton_crear_gerencial, 1, 0)
        # Ajustamos tamaño
        # self.boton_crear_gerencial.setFixedWidth(120)
        # Rescatamos la señal
        self.boton_crear_gerencial.clicked.connect(self.nuevo_gerencial)

    def nuevo_gerencial(self):
        """Crea e instancia la ventana para ingresar nuevos gerenciales"""
        # Instanciamos
        self.ventana_nuevo_gerencial = VentanaCrearGerencial()
        # Mostramos
        self.ventana_nuevo_gerencial.show()
    
    def _eliminar_gerencial(self):
        """Creamos un botón para eliminar gerenciales"""

        # Creamos el botón
        self.boton_eliminar_gerencial = QPushButton('Eliminar gerencial')
        # Lo posicionamos
        self.grid_layout_botones.addWidget(self.boton_eliminar_gerencial, 1, 1)
        # Ajustamos tamaño
        # self.boton_eliminar_gerencial.setFixedWidth(120)
        # Rescatamos la señal
        self.boton_eliminar_gerencial.clicked.connect(self.borrar_gerencial)

    def borrar_gerencial(self):
        """Crea e instancia la ventana para eliminar gerenciales"""
        # Instanciamos
        self.ventana_eliminar_gerencial = VentanaEliminarGerencial()
        # Mostramos
        self.ventana_eliminar_gerencial.show()

    def _crear_colaborador(self):
        """Creamos un botón para agregar nuevos colaboradores"""
        # Creamos el botón
        self.boton_crear_colaborador = QPushButton('Crear colaborador')
        # Lo posicionamos
        self.grid_layout_botones.addWidget(self.boton_crear_colaborador, 2, 0)
        # Rescatamos la señal
        self.boton_crear_colaborador.clicked.connect(self.nuevo_colaborador)
    
    def nuevo_colaborador(self):
        """Crea e instancia la ventana para ingresar nuevos colaboradores"""
        # Instanciamos
        self.ventana_nuevo_colaborador = VentanaCrearColaborador()
        # Mostramos
        self.ventana_nuevo_colaborador.show()

    def _eliminar_gcolaborador(self):
        """Creamos un botón para eliminar gerenciales"""
        # Creamos el botón
        self.boton_eliminar_colaborador = QPushButton('Eliminar colaborador')
        # Lo posicionamos
        self.grid_layout_botones.addWidget(self.boton_eliminar_colaborador, 2, 1)
        # Rescatamos la señal
        self.boton_eliminar_colaborador.clicked.connect(self.borrar_colaborador)

        # Creamos un espacio para centrar los botones
        label_intermedio_horizontal_2 = QLabel()
        # Lo posicionamos
        self.layout_horizontal.addWidget(label_intermedio_horizontal_2)

    def borrar_colaborador(self):
        """Crea e instancia la ventana para eliminar colaboradores"""
        # Instanciamos
        self.ventana_eliminar_colaborador = VentanaEliminarColaborador()
        # Mostramos
        self.ventana_eliminar_colaborador.show()

    def _ingresar_horas_extras(self):
        """Ingresa horas extras de un trabajador"""
        # Creamos el botón
        self.boton_crear_hhee= QPushButton('Ingresar horas extras')
        # Lo posicionamos
        self.grid_layout_botones.addWidget(self.boton_crear_hhee, 3, 0)
        # Rescatamos la señal
        self.boton_crear_hhee.clicked.connect(self.ingresar_hhee)

    def ingresar_hhee(self):
        """Crea e instancia la ventana para crear las horas extras"""
        # Instanciamos
        self.ventana_crear_hhee = VentanaCrearHorasExtras()
        # Mostramos
        self.ventana_crear_hhee.show()
    
    def _ver_horas_extras(self):
        """Visualiza las horas extras trabajadas"""
        # Creamos el botón
        self.boton_ver_hhee= QPushButton('Ver horas extras')
        # Lo posicionamos
        self.grid_layout_botones.addWidget(self.boton_ver_hhee, 3, 1)
        # Rescatamos la señal
        self.boton_ver_hhee.clicked.connect(self.ver_hhee)

    def ver_hhee(self):
        """Crea e instancia la ventana para ver las horas extras"""
        # Instanciamos
        self.ventana_ver_hhee = VentanVerHorasExtras()
        # Mostramos
        self.ventana_ver_hhee.show()
        
    def _elegir_semana(self):
        """Creamos un calendario para poder elegir la semana a ingresar horario"""
        # Creamos un espacio para separar los botones del calendario
        label_intermedio_vertical_2 = QLabel()
        # Lo posicionamos
        self.layout_principal.addWidget(label_intermedio_vertical_2)
        # Agregamos el grid layout al layout principal
        self.layout_principal.addLayout(self.grid_layout_calendario)
        # Creamos calendario
        calendario = QCalendarWidget()
        # Quitamos número de la semana
        calendario.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        # Seteamos tamaño
        calendario.setFixedSize(350, 200)
        # Posicionamos
        self.grid_layout_calendario.addWidget(calendario,0,0)
        # Rescatamos la señal
        calendario.clicked.connect(self.mostrar_semana_elegida)

    def mostrar_semana_elegida(self, fecha):
        """Rescata la fecha seleccionada, para obtener el lunes y domingo correspondiente de la semana y mostrarlo en el label de subtítulo
        fecha: Fecha seleccionada del calendario"""

        # Obtenemos la fecha y la pasamos a datetime
        fecha_datetime= datetime(int(fecha.toString('dd-MM-yyyy')[6:]), int(fecha.toString('dd-MM-yyyy')[3:5]), (int(fecha.toString('dd-MM-yyyy')[:2])))
        # Obtenemos el número del día
        numero_semana = fecha_datetime.isocalendar().weekday
        # Calculamos la fecha de inicio de la semana
        fecha_inicio = datetime(int(fecha.toString('dd-MM-yyyy')[6:]), int(fecha.toString('dd-MM-yyyy')[3:5]), (int(fecha.toString('dd-MM-yyyy')[:2]))) - timedelta(days=(numero_semana - 1))
        # Calculamos la fecha final de la semana
        fecha_final = datetime(int(fecha.toString('dd-MM-yyyy')[6:]), int(fecha.toString('dd-MM-yyyy')[3:5]), (int(fecha.toString('dd-MM-yyyy')[:2]))) + timedelta(days=(7-numero_semana))
        # Convertimos las fechas al español
        locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))
        # Modificamos texto del subtítulo
        self.label_subtitulo.setText(f'Semana del {int(fecha_inicio.strftime("%d"))} {fecha_inicio.strftime("%B").capitalize()} al {int(fecha_final.strftime("%d"))} de {(fecha_final.strftime("%B")).capitalize()}')

    # ------------------------------------------------------BOTONES------------------------------------------------------
    def _crear_menu(self):
        """Crea un menú de acceso rápido"""
        # Creamos los botones del menú
        # Con el símbolo & se logra un acceso rápido a la opción
        boton_crear_gerencial  = QAction('&Crear Gerencial', self)
        boton_crear_colaborador = QAction('C&rear Colaborador', self)
        boton_eliminar_gerencial = QAction('&Eliminar gerencial', self)
        boton_eliminar_colaborador = QAction('E&liminar Colaborador', self)
        boton_crear_hhee = QAction('&Ingresar Horas Extras', self)
        boton_ver_hhee = QAction('&Ver Horas Extras', self)
        boton_salir = QAction('&Salir', self)
        boton_acerca = QAction('Acerca de', self)

        # Conectamos las señales de los botones
        boton_crear_gerencial.triggered.connect(self.nuevo_gerencial)
        boton_crear_colaborador.triggered.connect(self.nuevo_colaborador)
        boton_eliminar_gerencial.triggered.connect(self.borrar_gerencial)
        boton_eliminar_colaborador.triggered.connect(self.borrar_colaborador)
        boton_crear_hhee.triggered.connect(self.ingresar_hhee)
        boton_ver_hhee.triggered.connect(self.ver_hhee)
        boton_salir.triggered.connect(self.salir)
        boton_acerca.triggered.connect(self.acerca)

        # Creamos el menú
        menu = self.menuBar()
        # Agregamos las opciones al menu
        # Deja subrrayada la letra que posee el acceso
        menu_archivo = menu.addMenu('Archivo')
        menu_guardar = menu.addMenu('Guardar')
        menu_acerca = menu.addMenu('Acerca')
        menu_ayuda = menu.addMenu('Ayuda')
       
        # Agregamos sub menú
        # Opciones de creación
        sub_menu_crear = menu_archivo.addMenu('Crear')
        # Asignamos las opciones del sub menú crear
        sub_menu_crear.addAction(boton_crear_gerencial)
        sub_menu_crear.addAction(boton_crear_colaborador)
        # Añadimos un separador
        menu_archivo.addSeparator()
        # Opciones de eliminación
        sub_menu_eliminar = menu_archivo.addMenu('Eliminar')
        # Asignamos las opciones del sub menú eliminar
        sub_menu_eliminar.addAction(boton_eliminar_gerencial)
        sub_menu_eliminar.addAction(boton_eliminar_colaborador)
        # Añadimos un separador
        menu_archivo.addSeparator()
        # Opciones de horas extras
        sub_menu_hhee = menu_archivo.addMenu('Horas Extras')
        # Asignamos las opciones del sub menú horas extras
        sub_menu_hhee.addAction(boton_crear_hhee)
        sub_menu_hhee.addAction(boton_ver_hhee)
        # Añadimos un separador
        menu_archivo.addSeparator()
        # Opción salir
        menu_archivo.addAction(boton_salir)
        # Agregamos action al menú acerca
        menu_acerca.addAction(boton_acerca)

        # Creación de atajos para nuestro menú
        # Crear gerencial
        boton_crear_gerencial.setShortcut(Qt.CTRL | Qt.SHIFT | Qt.Key_C)
        # Crear colaborador
        boton_crear_colaborador.setShortcut(Qt.CTRL | Qt.Key_R)
        # Eliminar gerencial
        boton_eliminar_gerencial.setShortcut(Qt.CTRL | Qt.SHIFT | Qt.Key_E)
        # Eliminar colaborador
        boton_eliminar_colaborador.setShortcut(Qt.CTRL | Qt.Key_E)
        # Ingresar HHEE
        boton_crear_hhee.setShortcut(Qt.CTRL | Qt.Key_I)
        # Ver HHEE
        boton_ver_hhee.setShortcut(Qt.CTRL | Qt.Key_V)
        # Salir
        boton_salir.setShortcut(Qt.CTRL | Qt.Key_S)

    def salir(self):
        """Cierra la ventana principal"""
        pregunta = QMessageBox.question(self, 'Salir', '¿Desea salir?',
                buttons=QMessageBox.Yes | QMessageBox.No)
        
        if(pregunta == QMessageBox.Yes):
            Horario.destroy(self)
            sys.exit()

    def acerca(self):
        """Muestra información del Horario"""
        QMessageBox.information(self, 'Acerca de', f'iHorario V 1.0\n\nHecho con ♥ por Brayan Quiroz Urrutia',
                buttons=QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication([])

    horario = Horario()
    horario.show()

    sys.exit(app.exec())