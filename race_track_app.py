#Imports
from flask import Flask

from flask import render_template, request, redirect, send_from_directory

from flaskext.mysql import MySQL

from datetime import datetime

import os

app = Flask(__name__)

#-------- MySQL -----------
#Configurar los datos para la conexión con la base de datos
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'

app.config['MYSQL_DATABASE_USER']='root'

app.config['MYSQL_DATABASE_PASSWORD']=''

app.config['MYSQL_DATABASE_BD']='race_track'

mysql.init_app(app)

#--------------------------
#Agrego un acceso al diccionario con el path de la carpeta
CARPETA = os.path.join("uploads")
app.config['CARPETA']=CARPETA
#--------------------------


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        print(request.form['email'])
        print(request.form['password'])
        #Se crea un usuario con los datos provistos en el formulario
        # user = User(0,request.form['email'],request.form['password'])
        # logged_user = ModelUser.login(db,user)
        # if logged_user != None:
        #     print("logged not none")
        #     if logged_user.password:
        #         print("logged true")
        #         return redirect(url_for('home'))
        #     else:
        #         print("logged none")
        #         flash("Contraseña incorrecta")
        # else:
        #     print("logged none")
        #     flash("Usuario no registrado")
        #     render_template('auth/login.html')
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/createRace')
def create():
    return render_template('carreras/createRace.html')

@app.route('/insert_carrera', methods=['POST'])
def insert_carrera():
    nombre = request.form['nombreCarreraText']
    fecha = request.form['fechaDatetime']
    direccion = request.form['lugarCarreraText']
    distancia = request.form['distanciaText']
    logo = request.files['logoFile']

    now = datetime.now()
    timeFormated = now.strftime("%Y%m%d%H%M%S")

    if logo.filename != '':
        nuevoNombreLogo= timeFormated+'-'+nombre+os.path.splitext(logo.filename)[1]
        logo.save("uploads/"+nuevoNombreLogo)

    datos = (nombre, distancia, fecha, direccion, nuevoNombreLogo)
    sql= "INSERT INTO `race_track`.`carreras` \
         (`nombre_carrera`, `distancia`, `fecha_carrera`,`lugar`,`logo_carrera`) \
         VALUES(%s, %s, %s, %s, %s);"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect("/listRaces")

@app.route('/uploads/<nombreLogo>')
def uploads(nombreLogo):
    return send_from_directory(app.config['CARPETA'],nombreLogo)

@app.route('/listRaces')
def listar_carreras():
    sql = "SELECT * FROM `race_track`.`carreras` ORDER BY id_carrera DESC;"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    db_carreras = cursor.fetchall()

    conn.commit()
    return render_template('carreras/listRaces.html', carreras = db_carreras)

@app.route('/editRace/<int:idCarrera>')
def edit(idCarrera):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `race_track`.`carreras` WHERE id_carrera = %s", (idCarrera))
    db_carrera = cursor.fetchall()
    conn.commit()
    return render_template('carreras/editRace.html', carrera = db_carrera)

@app.route('/udpate_carrera', methods=['POST'])
def update_carrera():
    nombre = request.form['nombreCarreraText']
    fecha = request.form['fechaDatetime']
    direccion = request.form['lugarCarreraText']
    distancia = request.form['distanciaText']
    logo = request.files['logoFile']
    idCarrera = request.form['idText']

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    timeFormated = now.strftime("%Y%m%d%H%M%S")

    cursor.execute("SELECT logo_carrera FROM `race_track`.`carreras` WHERE id_carrera = %s", (idCarrera))
    filaLogo = cursor.fetchall()

    if logo.filename != '':
        nuevoNombreLogo= timeFormated+'-'+nombre.replace(' ','_')+os.path.splitext(logo.filename)[1]
        logo.save("uploads/"+nuevoNombreLogo)
        os.remove(os.path.join(app.config['CARPETA'],filaLogo[0][0]))
    else:
        nuevoNombreLogo = filaLogo[0][0]

    datos = (nombre, distancia, fecha, direccion, nuevoNombreLogo, idCarrera)
    sql= "UPDATE race_track.carreras SET nombre_carrera=%s, distancia=%s, fecha_carrera=%s, \
          lugar=%s, logo_carrera=%s WHERE id_carrera = %s;"

    cursor.execute(sql, datos)
    conn.commit()

    return redirect("/listRaces")

if __name__=='__main__':
    #Necesario para correr la aplicación
    app.run(debug=True)