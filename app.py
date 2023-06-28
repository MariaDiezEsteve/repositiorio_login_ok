from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from config import config
from models.model_user import *


app = Flask(__name__, template_folder="src/templates")

app.secret_key = 'B!1w8NAt1T^%kvhUI*S^'

db = MySQL(app)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["Email"]
        password = request.form["Password"]
        if email and password:
            print ('@#@#@# get_logged_user', email, password)
            return render_template('home.html')
        user, token = Users.login(email, password)
        if user:
            return jsonify({'user': user, 'token': token})    
        return jsonify({'message': 'Error en el login ROUTER'})
    else:        
        return render_template('login.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = {
            "DNI": request.form["DNI"],
            "Name": request.form["Name"],
            "Lastname": request.form["Lastname"],
            "Email": request.form["Email"],
            "Password": request.form["Password"]
        }
        
        print("user", user)
        users = Users.post_user(user)
        print(users)
        return render_template('eiii.html')
    else:
        return render_template('registro.html')
          

@app.route("/home")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)