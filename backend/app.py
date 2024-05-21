from flask import Flask, jsonify, request, session
import bcrypt
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
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
    pwd = password.encode('utf-8')
    # pwd = password.encode('utf-8')
    # salt = bcrypt.gensalt()
    # password_encriptada = bcrypt.hashpw(pwd, salt)
    # salt = bcrypt.gensalt()
    # encript = bcrypt.hashpw(password_encriptada,sal)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (email, password))
    account = cur.fetchone()
    ###
    sending_data = {}
    code_request = 0
    status_request = ''

    #if bcrypt.checkpw(password,pwd):
    
    if account:
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
        # salt = bcrypt.gensalt()
        # password_encriptada = bcrypt.hashpw(pwd, salt)
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
                                    (email, password, nombre, apellido, fecha_nacimiento))
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
         
if __name__ == "__main__":
    app.run(debug=True)