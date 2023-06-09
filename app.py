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

@app.route("/<int:id>")
def condominio(id):
    predios = []
    periodos = []
    consulta1 = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predios from tipo_predio TP, predio PR where TP.id_tipo_predio = PR.id_tipo_predio and PR.id_predio = "+str(id)+";"
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
    return render_template("index_CD.html", predios = predios, periodos = periodos)

@app.route('/<int:id>/cuadroCostos')
def cuadroCostos(id):
    cuadros = []
    predios = []
    consulta1 = "select CA.numero, PM.descripcion as bloque, CE.descripcion as estado, CA.area, (select sum(area) from estacionamiento where id_casa = CA.id_casa) as area_cochera, ((select sum(area) from estacionamiento where id_casa = CA.id_casa) + CA.area) as area_total, 'xxx.xx' as montominimo, 'xxx.xx' as montoxarea from casa CA, predio_mdu PM, casa_estado CE where CA.id_predio = "+str(id)+" and CA.id_predio_mdu = PM.id_predio_mdu and CE.id_estado = CA.id_estado;"
    consulta2 = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predios from tipo_predio TP, predio PR where TP.id_tipo_predio = PR.id_tipo_predio and PR.id_predio = "+str(id)+";"
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute(consulta1)
        for row in cursor.fetchall():
            cuadros.append({"numero":row[0], "bloque":row[1], "estado":row[2], "area":row[3], "area_cochera":row[4], "area_total":row[5], "montominimo":row[6], "montoxarea":row[7]})
        
        cursor.execute(consulta2)
        for row in cursor.fetchall():
            predios.append({"id_predio":row[0], "predios":row[1]})
    except psycopg2.Error as error:
        print('error al extrear los datos de la consulta: ', error)
    finally:
        cursor.close()
        conn.close()
    return render_template("cuadroCostos.html", cuadros = cuadros, predios = predios)

@app.route('/<int:id>/cuadroCostos/descargarRecibo')
def descargarRecibo(id):
    cuadros = []
    predios = []
    consulta1 = "select CA.numero, PM.descripcion as bloque, CE.descripcion as estado, CA.area, (select sum(area) from estacionamiento where id_casa = CA.id_casa) as area_cochera, ((select sum(area) from estacionamiento where id_casa = CA.id_casa) + CA.area) as area_total, 'xxx.xx' as montominimo, 'xxx.xx' as montoxarea from casa CA, predio_mdu PM, casa_estado CE where CA.id_predio = "+str(id)+" and CA.id_predio_mdu = PM.id_predio_mdu and CE.id_estado = CA.id_estado;"
    consulta2 = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predios from tipo_predio TP, predio PR where TP.id_tipo_predio = PR.id_tipo_predio and PR.id_predio = "+str(id)+";"
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute(consulta1)
        for row in cursor.fetchall():
            cuadros.append({"numero":row[0], "bloque":row[1], "estado":row[2], "area":row[3], "area_cochera":row[4], "area_total":row[5], "montominimo":row[6], "montoxarea":row[7]})
        
        cursor.execute(consulta2)
        for row in cursor.fetchall():
            predios.append({"id_predio":row[0], "predios":row[1]})
    except psycopg2.Error as error:
        print('error al extrear los datos de la consulta: ', error)
    finally:
        cursor.close()
        conn.close()
    return render_template("descargarRecibo.html", cuadros = cuadros, predios = predios)


@app.route('/<int:id>/cuadroCostos/descargarRecibo/reciboTotal')
def reciboTotal(id):
    return render_template("reciboTotal.html")

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
