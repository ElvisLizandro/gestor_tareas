from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurar la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir el modelo de la tabla 'Tarea'
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    completado = db.Column(db.Boolean, default=False)

# Crear la base de datos
with app.app_context():
    db.create_all()

#Ruta de prueba
@app.route('/')
def index():
    tareas = Tarea.query.all() # Obtener todas las tareas
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form['titulo']
    nueva_tarea = Tarea(titulo=titulo)
    db.session.add(nueva_tarea)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/completar/<int:id>')
def completar(id):
    tarea = Tarea.query.get(id)
    if tarea:
        tarea.completado = not tarea.completado
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    tarea = Tarea.query.get(id)
    if tarea:
        db.session.delete(tarea)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)