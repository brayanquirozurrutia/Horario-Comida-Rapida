from conexion.Conexion import Conexion

class CursorPool:
    def __init__(self):
        self._conexion = None
        self._cursor = None
    
    def __enter__(self):
        self._conexion = Conexion.ObtenerConexion()
        self._cursor = self._conexion.cursor()

        return self._cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if(exc_val):
            self._conexion.rollback()
            print(f'Ocurrio una excepción: {exc_val} - {exc_type} - {exc_tb}')
        else:
            self._conexion.commit()
        self._cursor.close()
        Conexion.LiberarConexion(self._conexion)