from cursorpool.CursorPool import CursorPool
from PySide6.QtWidgets import QMessageBox

from datetime import datetime

def ValidaEnteros(numero):
    """Valida el ingreso de un número entero
    return: True si es entero y False si no lo es"""
    try:
        NUMERO = int(numero)
        return True
    except:
        return False

def ValidaRUT(rut):
    """Valida un rut
    return
    True: Si el rut está correcto
    False: Si no cumple con los requisitos de un rut
    """

    lista_rut = []; lista_rut_enteros = []
    rut_ = rut[:-2]

    rut_entero = ValidaEnteros(rut_)

    if(rut_entero):
        if(7 <= len(rut_) <= 8):
            for digito in rut_:
                lista_rut_enteros.append(int(digito))
            lista_rut_enteros.reverse()

            ponderador = 2
            suma_producto = 0
            for digito in lista_rut_enteros:
                producto = ponderador * digito
                ponderador += 1
                suma_producto += producto
                if(ponderador == 8):
                    ponderador = 2

            lista_rut.reverse()

            resto = (suma_producto % 11)

            diferencia = 11 - resto

            if(diferencia == 11):
                digito = 0
            elif(diferencia == 10):
                digito = 'k'
            else:
                digito = diferencia
            if(digito == int(rut[-1])):
                return True
            else:
                return False       
        else:
            return False
    else:
        return False

def creacion_tabla():
    """Creación tablas"""

    with CursorPool() as cursor:
        try:
            cursor.execute("""CREATE TABLE "CARGO" (
                            id_cargo int not null,
                            nombre_cargo text,
                            PRIMARY KEY(id_cargo));""")
        except Exception as e:
            print(e)

    with CursorPool() as cursor:
        try:
            cursor.execute("""CREATE TABLE "EMPLEADO" (
                            rut_empleado text not null,
                            nombre_empleado text,
                            apellido_empleado text,
                            horas_contrato integer,
                            id_cargo int not null,
                            rut_jefe text not null,
                            PRIMARY KEY(rut_empleado),
                            FOREIGN KEY(rut_jefe) REFERENCES "EMPLEADO"(rut_empleado),
                            FOREIGN KEY(id_cargo) REFERENCES "CARGO"(id_cargo));""")
        except Exception as e:
            print(e)

    with CursorPool() as cursor:
        try:
            cursor.execute("""CREATE TABLE "HORASEXTRAS" (
                            rut_empleado text not null,
                            fecha date not null,
                            horas decimal(6,3),
                            turno_extra boolean,
                            PRIMARY KEY(rut_empleado, fecha),
                            FOREIGN KEY(rut_empleado) REFERENCES "EMPLEADO"(rut_empleado));""")
        except Exception as e:
            print(e)
    
    with CursorPool() as cursor:
        try:
            cursor.execute("""CREATE TABLE "CREDENCIALES" (
                            contraseña text not null,
                            rut_empleado text not null,
                            PRIMARY KEY(contraseña, rut_empleado),
                            FOREIGN KEY(rut_empleado) REFERENCES "EMPLEADO"(rut_empleado));""")
        except Exception as e:
            print(e)

    with CursorPool() as cursor:
        try:
            cursor.execute("""INSERT INTO "CARGO" VALUES(1, 'gerente'), (2, 'sub gerente 1'), (3, 'sub gerente 2'), (4, 'crew');""")
        except Exception as e:
            print(e)

def cantidad_de_colaboradores():
    """Rescata la cantidad de colaboradores registrados en el sistema
    
    return: Largo de la lista obtenida"""
    with CursorPool() as cursor:
        cursor.execute("""select * from "EMPLEADO" where id_cargo in(
        select id_cargo from "CARGO" where upper(nombre_cargo) = 'CREW')""")
        total_colaboradores  = cursor.fetchall()

        return len(total_colaboradores)
    
def cantidad_de_gerenciales():
    """Rescata la cantidad de gerenciales registrados en el sistema
    
    return: Largo de la lista obtenida"""
    with CursorPool() as cursor:
        cursor.execute("""select * from "EMPLEADO" where id_cargo in(
        select id_cargo from "CARGO" where upper(nombre_cargo) IN ('GERENTE', 'SUB GERENTE 1', 'SUB GERENTE 2'))""")
        total_gerenciales  = cursor.fetchall()

        return len(total_gerenciales)
    

def nombre_apellido_colaborador():
    """Obtiene el nombre y el apellido de los colaboradores registrados en el sistema

    return: Lista con string Nombre Apellido"""

    with CursorPool() as cursor:
        cursor.execute("""select nombre_empleado, apellido_empleado from "EMPLEADO" where id_cargo in(
        select id_cargo from "CARGO" where upper(nombre_cargo) = 'CREW')""")
        lista = cursor.fetchall()
        lista_datos = []
        for elemento in lista:
            lista_datos.append(f'{elemento[0]} {elemento[1]}')

        return lista_datos
    
def nombre_apellido_gerencial():
    """Obtiene el nombre y el apellido de los gerenciales registrados en el sistema

    return: Lista con string Nombre Apellido"""

    with CursorPool() as cursor:
        cursor.execute("""select nombre_empleado, apellido_empleado from "EMPLEADO" where id_cargo in(
        select id_cargo from "CARGO" where upper(nombre_cargo) IN ('GERENTE', 'SUB GERENTE 1', 'SUB GERENTE 2'))""")
        lista = cursor.fetchall()
        lista_datos = []
        for elemento in lista:
            lista_datos.append(f'{elemento[0]} {elemento[1]}')

        return lista_datos

def obtener_horas_contrato_colaboradores(nombre):
    """Obtiene las horas pactadas por contrato de un colabordor

    nombre: Nombre del colaborador a buscar
    
    return: Las horas pacatadas por contrato del colaborador"""

    nombre_colaborador = nombre.split()


    with CursorPool() as cursor:
        cursor.execute("""select horas_contrato from "EMPLEADO" where nombre_empleado = %s and apellido_empleado = %s""",
                        (nombre_colaborador[0], nombre_colaborador[1]))

        # Rescato solo el primer valor de la tupla (horas)
        horas = cursor.fetchone()[0]

        return horas

def obtener_horas_contrato_gerenciales(nombre):
    """Obtiene las horas pactadas por contrato de un gerencial

    nombre: Nombre del gerencial a buscar
    
    return: Las horas pacatadas por contrato del gerencial"""

    nombre_gerencial = nombre.split()

    with CursorPool() as cursor:
        cursor.execute("""select horas_contrato from "EMPLEADO" where nombre_empleado = %s and apellido_empleado = %s""",
                        (nombre_gerencial[0], nombre_gerencial[1]))

        # Rescato solo el primer valor de la tupla (horas)
        horas = cursor.fetchone()[0]

        return horas

def calcular_horas_semanales_colaborador(ventana, posicion, texto, line_edit, diccionario_entrada,
                                        diccionario_salida, j, label_horas):
    """Realiza el cálculo de las horas totales que debe trabajar un colaborador en función de la hora ingresada de salida y entrada para cada día
    
    ventana: Ventana principal donde se mostrarán las alertas
    posicion: Posición que ocupa el conbobox interactuado
    texto: Texto del combobox a recuperar
    line_edit: Line edit que muestra la suma total de horas ingresadas para un colaborador
    diccionario_entrada: Diccionario que almacena todas las capturas ingresadas de las horas de entrada
    diccionario_salida: Diccionario que almacena todas las capturas ingresadas de las horas de salida
    j: Posición del Line edit
    label_horas: Label que contiene las horas pactadas por contrato de un colaborador
    """

    if(label_horas[0].text() != ''):
        horas = 0; minutos = 0; segundos = 0

        if(posicion % 2 != 0):
            diccionario_entrada[posicion] = [texto, j]
        else:
            diccionario_salida[posicion] = [texto, j]

        for clave in diccionario_salida.keys():
            if(int(clave / 15) == j):
                try:
                    if(diccionario_salida[clave][0] == 'LIBRE'):
                        segundos += 0
                    else:
                        hora_salida = datetime(1,1,1, int(diccionario_salida[clave][0][:2]), int(diccionario_salida[clave][0][3:]))

                        hora_entrada = datetime(1,1,1, int(diccionario_entrada[clave - 1][0][:2]), int(diccionario_entrada[clave - 1][0][3:]))

                        if(hora_salida > hora_entrada):

                            delta_hora = hora_salida - hora_entrada
                            if(delta_hora.seconds - 1800 > 12 * 3600):
                                QMessageBox.warning(ventana, 'ERROR',
                                        'La jornada de trabajo no puede exceder las 12 horas diarias',
                                        buttons=QMessageBox.Ok)
                            else:
                                segundos += delta_hora.seconds - 1800
                        else:
                            QMessageBox.warning(ventana, 'ERROR',
                                        'La hora de salida debe ser mayor a la de entrada',
                                        buttons=QMessageBox.Ok)
                except:
                    pass
        try:
            if((segundos / 3600 ) > int(label_horas[0].text())):
                QMessageBox.warning(ventana, 'ERROR',
                                        'La jornada semanal no puede exceder las horas pactadas por contrato',
                                        buttons=QMessageBox.Ok)
            else:
                horas += int(segundos / 3600)
                minutos += int((segundos / 3600 - horas) * 60)
                if(minutos == 0):
                    if(0 <= horas <= 9):
                        line_edit[0].setText(f'0{horas}:0{minutos}')
                    else:
                        line_edit[0].setText(f'{horas}:0{minutos}')
                else:
                    if(0 <= horas <= 9):
                        line_edit[0].setText(f'0{horas}:{minutos}')
                    else:
                        line_edit[0].setText(f'{horas}:{minutos}')
        except:
            pass
    else:
        QMessageBox.critical(ventana, 'ERROR',
                                        'Debe seleccionar un trabajador antes de ingresar horas',
                                        buttons=QMessageBox.Ok)

def empleado_registrado(rut):
    """Busca un empleado por su rut dentro de la tabla empleado
    rut: RUT del empleado a buscar
    return: Datos del empleado si lo encuentra y None si no existe"""
    with CursorPool() as cursor:
        try:
            cursor.execute("""SELECT * FROM "EMPLEADO" WHERE rut_empleado = %s;""",(rut,))

            gerencial  = cursor.fetchone()
            return gerencial
        
        except Exception as e:
            print(e)

def jefe():
    """Busca el rut del jefe correspondiente en la tabla empleado
    return: Rut del jefe"""
    with CursorPool() as cursor:
        try:
            cursor.execute("""SELECT rut_empleado from "EMPLEADO" where rut_empleado = rut_jefe;""")
            rut_jefe = cursor.fetchone()
            return rut_jefe[0]
        
        except Exception as e:
            print(e)
    
def crear_trabajador(rut, nombre, apellido, horas_contrato, id_cargo, rut_jefe):
    """Inserta una tupla de tabla empleado
    nombre: Nombre del trabajador
    apellido: Apellido del trabajador
    horas_cotnrato: Horas del contrato
    id_cargo: Id del cargo asignado
    rut_jefe: RUT del jefe asociado"""
    with CursorPool() as cursor:
        try:
            cursor.execute("""INSERT INTO "EMPLEADO" VALUES(%s, %s, %s, %s, %s, %s);""", (rut, nombre, apellido, horas_contrato, id_cargo, rut_jefe))
        except Exception as e:
            print(e)

def empleado_es_jefe(rut):
    """Comprueba si un rut es de jefe
    rut: RUT a corroborar"""
    with CursorPool() as cursor:
        try:
            cursor.execute("""SELECT rut_jefe FROM "EMPLEADO" where rut_empleado = %s;""", (rut,))
            rut_ = cursor.fetchone()
            return rut_[0]
        except Exception as e:
            print(e)

def eliminar_gerencial(rut):
    """Elimina una tupla de la tabla empleado
    rut: RUT del gerencial a eliminar"""

    with CursorPool() as cursor:
        try:
            cursor.execute("""DELETE FROM "EMPLEADO" where rut_empleado = %s;""", (rut,))
        except Exception as e:
            print(e)

def eliminar_colaborador(rut):
    """Elimina una tupla de la tabla empleado
    rut: RUT del colaborador a eliminar"""

    with CursorPool() as cursor:
        try:
            cursor.execute("""DELETE FROM "EMPLEADO" where rut_empleado = %s;""", (rut,))
        except Exception as e:
            print(e)

def ingresar_horas_extras(rut, fecha, horas, turno_extra):
    """Ingresa una tupla de las horas extras realizadas por un trabajador en la tabla correspondiente
    rut: RUT del trabajador
    fecha: Fecha en la que realizaron las horas extras
    horas: Total de horas extras realizadas
    turno_extra: Valor booleano si las horas corresponden a un turno extra o no"""

    with CursorPool() as cursor:
        try:
            cursor.execute("""INSERT INTO "HORASEXTRAS" VALUES(%s, %s, %s, %s);""", (rut, fecha, horas, turno_extra))
        except Exception as e:
            print(e)

def ver_horas_extras(rut, fecha_inicial, fecha_final):
    """Busca las horas extras realizadas por un colaborador en cierto mes
    rut: RUT del empleado
    fecha_inicial: Fecha inicial de la búsqueda
    fecha_final: Fecha final de la búsqueda
    return: Horas realizadas por el trabajador en el rango de fechas indicada"""
    with CursorPool() as cursor:
        try:
            cursor.execute("""SELECT horas FROM "HORASEXTRAS" WHERE rut_empleado = %s AND fecha BETWEEN %s AND %s;""", (rut, fecha_inicial, fecha_final))
            horas = cursor.fetchone()
            return horas[0]
        except Exception as e:
            print(e)