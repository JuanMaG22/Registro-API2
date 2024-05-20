from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb

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
    _email = request.json.get('email')
    _password = request.json.get('password')

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_email, _password))

    account = cur.fetchone()

    ###
    sending_data = {}
    code_request = 0
    status_request = ''

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

#@app.route('/registro', methods= ["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True)