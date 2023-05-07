from psycopg2 import pool
import sys

class Conexion:
    _DATABASE = 'HORARIO'
    _USERNAME = 'postgres'
    _PASSWORD = 'contrasenia'
    _DB_PORT = '5432'
    _HOST = '127.0.0.1'
    _MIN_CON = 1
    _MAX_CON = 5
    _POOL = None

    @classmethod
    def ObtenerPool(cls):
        if(cls._POOL is None):
            try:
                cls._POOL = pool.SimpleConnectionPool(cls._MIN_CON, cls._MAX_CON,
                                                        host = cls._HOST,
                                                        user = cls._USERNAME,
                                                        password = cls._PASSWORD,
                                                        port = cls._DB_PORT,
                                                        database = cls._DATABASE)
                return cls._POOL
            except Exception as e:
                print(f'Ocurrio un error al obtener el pool: {e}')
                sys.exit()
        else:
            return cls._POOL

    @classmethod
    def ObtenerConexion(cls):
        conexion =cls.ObtenerPool().getconn()
        return conexion

    @classmethod
    def LiberarConexion(cls, conexion):
        cls.ObtenerPool().putconn(conexion)

    @classmethod
    def CerrarConexiones(cls):
        cls.ObtenerPool().closeall()