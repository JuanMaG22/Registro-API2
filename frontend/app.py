from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
import requests
import re
 # Este objeto es necesario para el envio de información para el backend

app = Flask(__name__, template_folder='template')

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')   

@app.route('/admin')
def admin():
    # Recolectando información del formulario de mascotas por vía POST
    _id = request.json.get['txtId']
    _nombre = request.json.get['txtNombre']
    _edad = request.json.get['txtEdad']
    _descripcion = request.json.get['txtDescripcion']

    # Enviar datos a la API en formato JSON
    response = requests.post('http://127.0.0.1:5000/admin', json={"id": _id, "nombre": _nombre, "edad": _edad, "descripcion": _descripcion})

    # Recibiendo la respuesta de la API
    datos = response.json()['datos']
    if datos['mascotas']:
        return render_template("admin.html")  
 
@app.route('/adoptar')
def adoptar():
    return render_template('adoptar.html')  

@app.route('/acceso-login', methods=['POST'])
def login():
    # Recolectando información del formulario de login por via POST
    email = request.form['txtCorreo']   
    password = request.form['txtPassword']

    # Mandando informacion a la api con la ruta '/login' ubicada en 'backend/app.py'
    response = requests.post('http://127.0.0.1:5000/login', json={"email": email, "password": password})

    # Recibiendo la respuesta de la api
    data = response.json()['data']

    # Utilizando la clave 'logueado' para saber si las credenciales que introdujo el usuario son correctas
    if data['logueado']:
        
        # Utilizando la clase 'admin' para saber si la cuenta ingresado por el usuario es administrador o no
        if data['admin']:
            return render_template("admin.html") # Renderizar la plantilla 'admin.html' si la cuenta del usuario es admin
        
        else:
            return render_template("usuario.html") # Renderizar la plantilla 'usuario.html' si la cuenta del usuario no es admin

    else: 
        # Renderizar la plantilla 'index.html' si las credenciales que introdujo el usuario no son correctas y además imprimir un mensaje en dicha plantilla
        return render_template('index.html', mensaje = 'Usuario O Contraseña Incorrectas')  

#Registro
@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear-registro', methods= ["GET", "POST"])
def crear_registro():

    # Recolectando información del formulario de login por via POST
    _email = request.form['txtCorreo']
    _password = request.form['txtPassword']
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _fecha_nacimiento = request.form['txtFecha']

 # Mandando informacion a la api con la ruta '/login' ubicada en 'backend/app.py'
    response = requests.post('http://127.0.0.1:5000/registro', json={"email": _email, "password": _password, "nombre": _nombre, 
                                                                  "apellido": _apellido, "fecha_nacimiento": _fecha_nacimiento})
    # Recibiendo la respuesta de la api
    data = response.json()['data']
    if data['registro']:
        return render_template("index.html",mensaje2= data['mensaje'])
    else:
        return render_template("registro.html", mensaje= data['mensaje'] )

# ------------------ Listar Mascotas ------------------------
"""@app.route('/mascotas', methods=['GET'])
def listar_mascotas():
    # Recolectando información del formulario de mascotas por vía POST
    _id = request.json.get['txtId']
    _nombre = request.json.get['txtNombre']
    _edad = request.json.get['txtEdad']
    _descripcion = request.json.get['txtDescripcion']

    # Enviar datos a la API en formato JSON
    response = requests.post('http://127.0.0.1:5000/mascotas', json={"id": _id, "nombre": _nombre, "edad": _edad, "descripcion": _descripcion})

    # Recibiendo la respuesta de la API
    datos = response.json()['datos']
    if datos['mascotas']:
        return render_template("index.html", mensaje2=datos['mensaje'])
    else:
        return render_template("mascotas.html", mensaje=datos['mensaje'])
"""

if __name__=='__main__':
    app.secret_key="juan_hds"

    #Nos crea de manera local al momento de correr
    app.run(debug=True, host='0.0.0.0', port=3000, threaded=True)