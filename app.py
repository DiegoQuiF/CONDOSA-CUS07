from flask import Flask, render_template, request, redirect
import pyodbc


app = Flask(__name__)


#CONEXIÓN CON LA BASE DE DATOS
def connection():
    s = 'LAPTOP-3H729AV9\SQLEXPRESS'    #Nombre del servidor
    d = 'E_CONDOSA'  #DataBase, va igual
    u = ''      #usuario de la BD
    p = ''      #contraseña de la BD
    #línea de conexión con autentificación de windows
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+s+';DATABASE='+d+';Trusted_Connection=yes;'
    #línea de conexión con usuario de sql server
    #cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn


#PÁGINA PRINCIPAL
@app.route("/")
def main():
    return render_template("index.html")

@app.route('/cuadroCostos')
def cuadroCostos():
    return render_template("cuadroCostos.html")

@app.route('/descargarRecibo')
def descargarRecibo():
    return render_template("descargarRecibo.html")

#INICIA LA APP
if(__name__=="__main__"):
    app.run(debug=True, port=5000)