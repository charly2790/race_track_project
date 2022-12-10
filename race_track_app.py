from flask import Flask

from flask import render_template,request

app = Flask(__name__)

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

if __name__=='__main__':
    #Necesario para correr la aplicación
    app.run(debug=True)