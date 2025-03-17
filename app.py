from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.alumno import Alumno
from models.asignatura import Asignatura
from models.calificacion import Calificacion
import os

app = Flask(__name__)
app.config.from_object('config.Config')

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

# Rutas para alumnos
@app.route('/alumnos')
def lista_alumnos():
    alumnos = Alumno.get_all()
    return render_template('alumnos/lista.html', alumnos=alumnos)

@app.route('/alumnos/nuevo', methods=['GET', 'POST'])
def nuevo_alumno():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        telefono = request.form['telefono']
        
        alumno = Alumno(None, nombre, apellidos, email, telefono)
        alumno.save()
        
        flash('Alumno registrado correctamente', 'success')
        return redirect(url_for('lista_alumnos'))
    
    return render_template('alumnos/form.html')

@app.route('/alumnos/editar/<int:id>', methods=['GET', 'POST'])
def editar_alumno(id):
    alumno = Alumno.get_by_id(id)
    
    if request.method == 'POST':
        alumno.nombre = request.form['nombre']
        alumno.apellidos = request.form['apellidos']
        alumno.email = request.form['email']
        alumno.telefono = request.form['telefono']
        
        alumno.save()
        
        flash('Alumno actualizado correctamente', 'success')
        return redirect(url_for('lista_alumnos'))
    
    return render_template('alumnos/form.html', alumno=alumno)

@app.route('/alumnos/eliminar/<int:id>')
def eliminar_alumno(id):
    Alumno.delete(id)
    flash('Alumno eliminado correctamente', 'success')
    return redirect(url_for('lista_alumnos'))

# Rutas para calificaciones
@app.route('/calificaciones')
def lista_calificaciones():
    calificaciones = Calificacion.get_all_with_details()
    return render_template('calificaciones/lista.html', calificaciones=calificaciones)

@app.route('/calificaciones/nueva', methods=['GET', 'POST'])
def nueva_calificacion():
    if request.method == 'POST':
        alumno_id = request.form['alumno_id']
        asignatura_id = request.form['asignatura_id']
        nota = request.form['nota']
        fecha_evaluacion = request.form['fecha_evaluacion']
        observaciones = request.form['observaciones']
        
        calificacion = Calificacion(None, alumno_id, asignatura_id, nota, fecha_evaluacion, observaciones)
        calificacion.save()
        
        flash('Calificación registrada correctamente', 'success')
        return redirect(url_for('lista_calificaciones'))
    
    alumnos = Alumno.get_all()
    asignaturas = Asignatura.get_all()
    return render_template('calificaciones/form.html', alumnos=alumnos, asignaturas=asignaturas)

@app.route('/calificaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_calificacion(id):
    calificacion = Calificacion.get_by_id(id)
    
    if request.method == 'POST':
        calificacion.alumno_id = request.form['alumno_id']
        calificacion.asignatura_id = request.form['asignatura_id']
        calificacion.nota = request.form['nota']
        calificacion.fecha_evaluacion = request.form['fecha_evaluacion']
        calificacion.observaciones = request.form['observaciones']
        
        calificacion.save()
        
        flash('Calificación actualizada correctamente', 'success')
        return redirect(url_for('lista_calificaciones'))
    
    alumnos = Alumno.get_all()
    asignaturas = Asignatura.get_all()
    return render_template('calificaciones/form.html', calificacion=calificacion, alumnos=alumnos, asignaturas=asignaturas)

@app.route('/calificaciones/eliminar/<int:id>')
def eliminar_calificacion(id):
    Calificacion.delete(id)
    flash('Calificación eliminada correctamente', 'success')
    return redirect(url_for('lista_calificaciones'))

@app.route('/informes/alumno/<int:id>')
def informe_alumno(id):
    alumno = Alumno.get_by_id(id)
    calificaciones = Calificacion.get_by_alumno(id)
    return render_template('informes/alumno.html', alumno=alumno, calificaciones=calificaciones)

if __name__ == '__main__':
    app.run(debug=True,port=80)
