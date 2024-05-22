from flask import Flask, jsonify, request, session
import bcrypt
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


app.secret_key = 'principe2002' # Esta linea es obligatorio por que si no, no funciona las sesiones

# <------| API'S |------> 
@app.route('/login', methods=['POST'])
def get_data():      
    # Recibir la informacion que se envio desde la ruta '/acceso-login' (Front-End)
    email = request.json.get('email')
    password = request.json.get('password')
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM usuarios WHERE correo = '{email}'")
    account = cur.fetchone()
    cur.close()
    password_verify = ''
    if account:
        password_verify = bcrypt.checkpw(password.encode('utf-8'), account['password'].encode('utf-8'))
    ###
    sending_data = {}
    code_request = 0
    status_request = 'unauthorized'

    #if bcrypt.checkpw(password,pwd):
    
    if password_verify: 
        code_request = 200
        status_request = 'success'

        session['logueado'] = True
        session['id'] = account['id']
        session['id_rol'] = account['id_rol']

        #Nuevo
        sending_data['logueado'] = True  
        sending_data['id_rol'] = account['id_rol'] 

        if sending_data['id_rol']==1:
            session['admin'] = True
            sending_data['admin'] = True

        elif sending_data['id_rol']==2:
            session['admin'] = False
            sending_data['admin'] = False
    else:
        sending_data['logueado'] = False
        code_request = 401
        status_request = 'unauthorized'


    return jsonify({'status': status_request, 'code': code_request, 'data': sending_data}), code_request

## Registro

@app.route('/registro', methods=['POST', 'POST'])
def post_data(): 
    # Recibir la informacion que se envio desde la ruta '/acceso-login' (Front-End)
        email = request.json.get('email')
        password = request.json.get('password')
        # pwd = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_encriptada = bcrypt.hashpw(password.encode('utf-8'),salt)
        nombre = request.json.get('nombre')
        apellido = request.json.get('apellido')
        fecha_nacimiento = request.json.get('fecha_nacimiento')

        # Expresión regular para verificar si la contraseña contiene al menos un carácter especial
        registroExitoso = False
        codigoPeticion = 401
        mensaje = ''
        code_request = 200
        status_request = 'unauthorized'

        if email and password and nombre and apellido and fecha_nacimiento:

            if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                if len(password) <= 8:
                    registroExitoso = True
                    codigoPeticion = 200
                    mensaje = 'Registro exitoso'
                    status_request = 'success'
                    #Realizar la insercion a la base de datos 
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO usuarios (correo, password, nombre, apellido, fecha_nacimiento, id_rol) VALUES (%s, %s, %s, %s, %s, '2')",
                                    (email, password_encriptada.decode('utf-8'), nombre, apellido, fecha_nacimiento))
                    mysql.connection.commit()
                    cur.close()
                else:
                    mensaje= 'La password no debe exceder los 8 caracteres' 

            else:
                mensaje= 'La password debe contener un caracter especial'
        else: 
            mensaje = 'Todos los campos son obligatorios'
            
        return jsonify({'status': status_request, 'code': code_request, 'data': {
            'mensaje': mensaje,
            'registro': registroExitoso
        }}), code_request

#----------------------------- Listar mascotas -----------------------------------------------------

# @app.route('/admin', methods=['POST'])
# def listar_mascotas():
#     id = request.json.get('id')
#     nombre = request.json.get('nombre')
#     edad = request.json.get('edad')
#     descripcion = request.json.get('descripcion')
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM mascotas WHERE ")
#     cur.execute(f"SELECT * FROM usuarios WHERE correo = '{email}'")
#     datos = cursor.fetchall()
#     mascotas = []
#     for fila in datos:
#         mascota = {'id': fila[0], 'nombre': fila[1], 'edad': fila[2], 'descripcion': fila[3]}
#         mascotas.append(mascota)
#     return jsonify({'mascotas': mascotas, 'mensaje': "Mascotas listadas."})

# @app.route('/admin', methods=['POST'])
# def admin():
#     cursor = MySQL.connection.cursor()
#     cursor.execute("SELECT * FROM mascotas")
#     datos = cursor.fetchall()
#     # Convertir los datos a diccionario
#     mascotas = []
#     fila = [column[0] for column in cursor.description]
#     for fila in datos:
#         mascota = {'id': fila[0], 'nombre': fila[1], 'edad': fila[2], 'descripcion': fila[3]}
#         mascotas.append(mascota)
#     cursor.close()
         
if __name__ == "__main__":
    app.run(debug=True)