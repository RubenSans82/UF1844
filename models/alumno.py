from db import get_connection

class Alumno:
    def __init__(self, id=None, nombre=None, apellidos=None, dni=None, email=None, telefono=None, fecha_registro=None):
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni  # Added DNI field
        self.email = email
        self.telefono = telefono
        self.fecha_registro = fecha_registro
    
    def save(self):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                if self.id is None:
                    # Insertar nuevo alumno
                    sql = "INSERT INTO alumnos (nombre, apellidos, dni, email, telefono) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.nombre, self.apellidos, self.dni, self.email, self.telefono))
                    self.id = connection.insert_id()
                else:
                    # Actualizar alumno existente
                    sql = "UPDATE alumnos SET nombre=%s, apellidos=%s, dni=%s, email=%s, telefono=%s WHERE id=%s"
                    cursor.execute(sql, (self.nombre, self.apellidos, self.dni, self.email, self.telefono, self.id))
            connection.commit()
        finally:
            connection.close()
    
    @classmethod
    def get_all(cls):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM alumnos ORDER BY apellidos, nombre"
                cursor.execute(sql)
                result = cursor.fetchall()
                
                alumnos = []
                for row in result:
                    alumnos.append(cls(**row))
                return alumnos
        finally:
            connection.close()
    
    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM alumnos WHERE id = %s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                
                if result:
                    return cls(**result)
                return None
        finally:
            connection.close()
    
    @classmethod
    def delete(cls, id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM alumnos WHERE id = %s"
                cursor.execute(sql, (id,))
            connection.commit()
        finally:
            connection.close()
