from datetime import datetime
import jwt
from gestor_jwt import token_required
from flask_mysqldb import MySQL
from flask import jsonify
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify


DATABASE = {
    'host': "containers-us-west-59.railway.app",
    'user': 'root',
    'password': "mzj8vF2N8BRe4h8m8cyB",
    'database': "railway"
}

class Users:
    def __init__(self, iduser, DNI, Name, LastName, Email, Password, secret, Rol):
        self.iduser = iduser
        self.DNI = DNI
        self.Name = Name
        self.Lastname = LastName
        self.Email = Email
        self.Password = Password
        self.secret = secret
        self.Rol = Rol

    @classmethod
    def login(cls, Email, Password):
        conn = None
        try:
            conn = MySQL.connect(**DATABASE)
            c = conn.cursor()
            c.execute("SELECT * FROM user WHERE Email=?", (Email, ))
            result = c.fetchone()

            if result and result[4] == Password:
                secret = str(datetime.now().timestamp())
                user = {
                    "iduser": result[0],
                    "Name": result[1],
                    "Lastname": result[2],
                    "Email": result[3],
                    "Password": result[4],
                    "secret": secret,
                    "Rol": result[6]
                }
                token = Users.generate_token(user, secret)
                return user, token
            else:
                return ({"error": "Credenciales inválidas"}), 401

        except MySQL.Error as e:
            return ({"SQLError": str(e)}, 500)
        finally:
            if conn is not None:
                conn.close()
                
    @staticmethod
    def generate_token(user, secret):
        token = jwt.encode({"Email": user["Email"], "Password": user["Password"], "secret": user["secret"], "Rol": user["Rol"]}, secret)
        return token.decode('utf-8')
   

   

    @classmethod
    def post_user(cls, user):
        conn = None
        try:
            conn = mysql.connector.connect(**DATABASE)
            c = conn.cursor()
            c.execute('''
                INSERT INTO user (DNI, Name, Lastname, Email, Password)
                VALUES (%s, %s, %s, %s, %s)
            ''', (user["DNI"], user["Name"], user["Lastname"], user["Email"], user["Password"]))
            conn.commit()
            return jsonify({'message': 'user created successfully'}), 200
        except mysql.connector.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            if conn:
                conn.close()



    @classmethod
    @token_required
    def get_user_by_id(cls, user_id):
        try:
            conn = MySQL.connect(**DATABASE)
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE iduser=?", (user_id,))
            result = c.fetchone()
            if result:
                user = {
                    "iduser": result[0],
                    "Name": result[1],
                    "Lastname": result[2],
                    "Email": result[3],
                    "Password": result[4],
                    "secret": result[5],
                    "Rol": result[6]
                }
                return user
        except MySQL.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

