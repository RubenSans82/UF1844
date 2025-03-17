from db import get_connection
from models.alumno import Alumno
from models.asignatura import Asignatura

class Calificacion:
    def __init__(self, id=None, alumno_id=None, asignatura_id=None, nota=None, fecha_evaluacion=None, observaciones=None):
        self.id = id
        self.alumno_id = alumno_id
        self.asignatura_id = asignatura_id
        self.nota = nota
        self.fecha_evaluacion = fecha_evaluacion
        self.observaciones = observaciones
        self.alumno = None
        self.asignatura = None
    
    def save(self):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                if self.id is None:
                    # Insertar nueva calificación
                    sql = """INSERT INTO calificaciones 
                          (alumno_id, asignatura_id, nota, fecha_evaluacion, observaciones) 
                          VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (self.alumno_id, self.asignatura_id, self.nota, 
                                         self.fecha_evaluacion, self.observaciones))
                    self.id = connection.insert_id()
                else:
                    # Actualizar calificación existente
                    sql = """UPDATE calificaciones 
                          SET alumno_id=%s, asignatura_id=%s, nota=%s, fecha_evaluacion=%s, observaciones=%s 
                          WHERE id=%s"""
                    cursor.execute(sql, (self.alumno_id, self.asignatura_id, self.nota, 
                                         self.fecha_evaluacion, self.observaciones, self.id))
            connection.commit()
        finally:
            connection.close()
    
    @classmethod
    def get_all_with_details(cls):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT c.*, a.nombre as alumno_nombre, a.apellidos as alumno_apellidos, 
                           as2.nombre as asignatura_nombre
                    FROM calificaciones c
                    JOIN alumnos a ON c.alumno_id = a.id
                    JOIN asignaturas as2 ON c.asignatura_id = as2.id
                    ORDER BY a.apellidos, a.nombre, as2.nombre
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                
                calificaciones = []
                for row in result:
                    calificacion = cls(
                        id=row['id'],
                        alumno_id=row['alumno_id'],
                        asignatura_id=row['asignatura_id'],
                        nota=row['nota'],
                        fecha_evaluacion=row['fecha_evaluacion'],
                        observaciones=row['observaciones']
                    )
                    # Crear objetos simplificados para alumno y asignatura
                    calificacion.alumno = Alumno(
                        id=row['alumno_id'],
                        nombre=row['alumno_nombre'],
                        apellidos=row['alumno_apellidos']
                    )
                    calificacion.asignatura = Asignatura(
                        id=row['asignatura_id'],
                        nombre=row['asignatura_nombre']
                    )
                    calificaciones.append(calificacion)
                return calificaciones
        finally:
            connection.close()
    
    @classmethod
    def get_by_id(cls, id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM calificaciones WHERE id = %s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                
                if result:
                    return cls(**result)
                return None
        finally:
            connection.close()
    
    @classmethod
    def get_by_alumno(cls, alumno_id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT c.*, as2.nombre as asignatura_nombre, as2.descripcion as asignatura_descripcion
                    FROM calificaciones c
                    JOIN asignaturas as2 ON c.asignatura_id = as2.id
                    WHERE c.alumno_id = %s
                    ORDER BY as2.nombre
                """
                cursor.execute(sql, (alumno_id,))
                result = cursor.fetchall()
                
                calificaciones = []
                for row in result:
                    calificacion = cls(
                        id=row['id'],
                        alumno_id=row['alumno_id'],
                        asignatura_id=row['asignatura_id'],
                        nota=row['nota'],
                        fecha_evaluacion=row['fecha_evaluacion'],
                        observaciones=row['observaciones']
                    )
                    calificacion.asignatura = Asignatura(
                        id=row['asignatura_id'],
                        nombre=row['asignatura_nombre'],
                        descripcion=row['asignatura_descripcion']
                    )
                    calificaciones.append(calificacion)
                return calificaciones
        finally:
            connection.close()
    
    @classmethod
    def delete(cls, id):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM calificaciones WHERE id = %s"
                cursor.execute(sql, (id,))
            connection.commit()
        finally:
            connection.close()
