from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
import requests
import re
 # Este objeto es necesario para el envio de información para el backend

app = Flask(__name__, template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
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
    return render_template('admin.html')   

@app.route('/gato')
def despues():
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


# ACCESO---LOGIN
"""
@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
       
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol']=account['id_rol']
            
            if session['id_rol']==1:
                return render_template("admin.html")
            elif session ['id_rol']==2:
                return render_template("usuario.html")
        else:
            return render_template('index.html',mensaje="Usuario O Contraseña Incorrectas")            
"""

#registro---
# @app.route('/registro')
# def registro():
#     return render_template('registro.html')  

# @app.route('/crear-registro', methods= ["GET", "POST"])
# def crear_registro(): 
    
#     if request.method == 'POST':
#         correo = request.form['txtCorreo']
#         password = request.form['txtPassword']
#         nombre = request.form['txtNombre']
#         apellido = request.form['txtApellido']
#         fecha_nacimiento = request.form['txtFecha']

#         # Expresión regular para verificar si la contraseña contiene al menos un carácter especial
#         if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
#             if len(password) <= 8:
#                 # Realizar la inserción en la base de datos
#                 cur = mysql.connection.cursor()
#                 cur.execute("INSERT INTO usuarios (correo, password, nombre, apellido, fecha_nacimiento, id_rol) VALUES (%s, %s, %s, %s, %s, '2')",
#                             (correo, password, nombre, apellido, fecha_nacimiento))
#                 mysql.connection.commit()
#                 cur.close()

#                 return render_template("index.html", mensaje2="Usuario Registrado Exitosamente")
#             else:
#                 return render_template("registro.html", mensaje="La contraseña no debe exceder los 8 caracteres")
#         else:
#             return render_template("registro.html", mensaje="La contraseña debe contener un caracter especial")
    
#     return render_template("index.html",mensaje2="Usuario Registrado Exitosamente")
# #--------------------------------------------------


if __name__=='__main__':
    app.secret_key="juan_hds"

    #Nos crea de manera local al momento de correr
    app.run(debug=True, host='0.0.0.0', port=3000, threaded=True)