from db import get_connection

class Asignatura:
    def __init__(self, id=None, nombre=None, descripcion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM asignaturas ORDER BY nombre"
                cursor.execute(sql)
                result = cursor.fetchall()
                
                asignaturas = []
                for row in result:
                    asignaturas.append(cls(**row))
                return asignaturas
        finally:
            connection.close()
    
    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM asignaturas WHERE id = %s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                
                if result:
                    return cls(**result)
                return None
        finally:
            connection.close()
