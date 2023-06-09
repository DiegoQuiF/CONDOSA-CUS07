from flask import Flask, render_template, request, redirect
from controllers import obtener_datos_recibo_estado, obtener_datos_mant_recibo, connection
import psycopg2

app = Flask(__name__)


#PÁGINA PRINCIPAL a
@app.route("/")
def main():
    predios = []
    periodos = []
    consulta1 = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predios from tipo_predio TP, predio PR where TP.id_tipo_predio = PR.id_tipo_predio;"
    consulta2 = "select 'Último periodo' as periodos;"
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute(consulta1)
        for row in cursor.fetchall():
            predios.append({"id_predio":row[0], "predios":row[1]})
        
        cursor.execute(consulta2)
        for row in cursor.fetchall():
            periodos.append({"periodos":row[0]})
    except psycopg2.Error as error:
        print('error al extrear los datos de la consulta: ', error)
    finally:
        cursor.close()
        conn.close()
    return render_template("index.html", predios = predios, periodos = periodos)

@app.route('/cuadroCostos')
def cuadroCostos():
    return render_template("cuadroCostos.html")

@app.route('/reciboTotal')
def reciboTotal():
    return render_template("reciboTotal.html")

@app.route('/descargarRecibo')
def descargarRecibo():
    datos_recibo = obtener_datos_recibo_estado()
    return render_template("descargarRecibo.html", datos_recibo=datos_recibo)

@app.route('/recibo_estado')
def mostrar_recibo_estado():
    datos_recibo_estado = obtener_datos_recibo_estado()
    return render_template("recibo_estado.html", datos_recibo_estado=datos_recibo_estado)

@app.route('/mant_recibo')
def mostrar_mant_recibo():
    datos_mant_recibo = obtener_datos_mant_recibo()
    return render_template("mant_recibo.html", datos_mant_recibo=datos_mant_recibo)


# INICIA LA APP
if __name__ == "__main__":
    app.run(debug=True, port=5000)
