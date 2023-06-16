from flask import Flask, render_template, request, redirect
from controllers import obtener_datos_recibo_estado, obtener_datos_mant_recibo, connection
import psycopg2

app = Flask(__name__)


#PÁGINA PRINCIPAL, lista de predios
@app.route("/")
def main():
    predios = []
    #Consulta para sacar los predios:
    consultaPredios = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predio from tipo_predio TP, predio PR where TP.id_tipo_predio = PR.id_tipo_predio;"

    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute(consultaPredios)
        for row in cursor.fetchall():
            predios.append({"id_predio":row[0], "predio":row[1]})
    except psycopg2.Error as error:
        print('error al extrear los datos de la consulta: ', error)
    finally:
        cursor.close()
        conn.close()

    return render_template("index.html", predios = predios)

#Datos Predio seleccionado
@app.route("/<int:id>")
def condominio(id):
    predios = []
    prediosi = []
    #Consulta para sacar los predios:
    consultaPredios = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predio from tipo_predio TP, predio PR where TP.id_tipo_predio = PR.id_tipo_predio;"
    #Consulta para sacar al predio seleccionado y su presidente:
    consultaPredio_Presidente = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predio, CONCAT(PE.apellido_paterno, ' ', PE.apellido_materno, ', ', PE.nombres) as presidente from tipo_predio TP, predio PR, persona PE where TP.id_tipo_predio = PR.id_tipo_predio and PE.id_persona = PR.id_persona and PR.id_predio = "+str(id)+";"

    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute(consultaPredios)
        for row in cursor.fetchall():
            predios.append({"id_predio":row[0], "predio":row[1]})

        cursor.execute(consultaPredio_Presidente)
        for row in cursor.fetchall():
            prediosi.append({"id_predio":row[0], "predio":row[1], "presidente":row[2]})
    except psycopg2.Error as error:
        print('error al extrear los datos de la consulta: ', error)
    finally:
        cursor.close()
        conn.close()

    return render_template("index_CD.html", prediosi = prediosi, predios = predios)

#Predio con el cuadro de casas pertenecientes al predio
@app.route('/<int:id>/cuadroCostos')
def cuadroCostos(id):
    prediosi = []
    cuadro = []
    #Consulta para sacar al predio seleccionado y su presidente:
    consultaPredio_Presidente = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predio, CONCAT(PE.apellido_paterno, ' ', PE.apellido_materno, ', ', PE.nombres) as presidente from tipo_predio TP, predio PR, persona PE where TP.id_tipo_predio = PR.id_tipo_predio and PE.id_persona = PR.id_persona and PR.id_predio = "+str(id)+";"
    #Consulta para sacar las abitaciones, con su bloque, con su estado, area, area_cochera, area_total, monto_minimo y monto por area.
    consultaCuadroHabitaciones = "select CA.numero, PM.descripcion as bloque, CE.descripcion as estado, CA.area, (select sum(area) from estacionamiento where id_casa = CA.id_casa) as area_cochera, ((select sum(area) from estacionamiento where id_casa = CA.id_casa) + CA.area) as area_total, 'xxx.xx' as montominimo, 'xxx.xx' as montoxarea from casa CA, predio_mdu PM, casa_estado CE where CA.id_predio = "+str(id)+" and CA.id_predio_mdu = PM.id_predio_mdu and CE.id_estado = CA.id_estado;"

    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute(consultaPredio_Presidente)
        for row in cursor.fetchall():
            prediosi.append({"id_predio":row[0], "predio":row[1], "presidente":row[2]})

        cursor.execute(consultaCuadroHabitaciones)
        for row in cursor.fetchall():
            cuadro.append({"numero":row[0], "bloque":row[1], "estado":row[2], "area":row[3], "area_cochera":row[4], "area_total":row[5], "montominimo":row[6], "montoxarea":row[7]})
    except psycopg2.Error as error:
        print('error al extrear los datos de la consulta: ', error)
    finally:
        cursor.close()
        conn.close()

    return render_template("cuadroCostos.html", prediosi = prediosi, cuadro = cuadro)

#Predio con el cuadro de casas pertenecientes al predio luego de confirmar los pagos.
@app.route('/<int:id>/cuadroCostos/descargarRecibo')
def descargarRecibo(id):
    prediosi = []
    cuadro = []
    #Consulta para sacar al predio seleccionado y su presidente:
    consultaPredio_Presidente = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as predio, CONCAT(PE.apellido_paterno, ' ', PE.apellido_materno, ', ', PE.nombres) as presidente from tipo_predio TP, predio PR, persona PE where TP.id_tipo_predio = PR.id_tipo_predio and PE.id_persona = PR.id_persona and PR.id_predio = "+str(id)+";"
    #Consulta para sacar las abitaciones, con su bloque, con su estado, area, area_cochera, area_total, monto_minimo y monto por area.
    consultaCuadroHabitaciones = "select CA.numero, PM.descripcion as bloque, CE.descripcion as estado, CA.area, (select sum(area) from estacionamiento where id_casa = CA.id_casa) as area_cochera, ((select sum(area) from estacionamiento where id_casa = CA.id_casa) + CA.area) as area_total, 'xxx.xx' as montominimo, 'xxx.xx' as montoxarea from casa CA, predio_mdu PM, casa_estado CE where CA.id_predio = "+str(id)+" and CA.id_predio_mdu = PM.id_predio_mdu and CE.id_estado = CA.id_estado;"
    
    conn = connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(consultaPredio_Presidente)
        for row in cursor.fetchall():
            prediosi.append({"id_predio":row[0], "predio":row[1], "presidente":row[2]})

        cursor.execute(consultaCuadroHabitaciones)
        for row in cursor.fetchall():
            cuadro.append({"numero":row[0], "bloque":row[1], "estado":row[2], "area":row[3], "area_cochera":row[4], "area_total":row[5], "montominimo":row[6], "montoxarea":row[7]})
            #print(row[0])
    except psycopg2.Error as error:
        print('error al extrear los datos de la consulta: ', error)
    finally:
        cursor.close()
        conn.close()
   
    return render_template("descargarRecibo.html", cuadro = cuadro, prediosi = prediosi)

#PAGINA DEL RECIBO
@app.route('/<int:id>/cuadroCostos/descargarRecibo/<int:id2>')
def reciboTotal(id, id2):
    
    datosPredio = []
    datosPersona = []
    #DATOS DEL PREDIO Y EL RECIBO
    consultaRecibo_Predio = "select PR.id_predio, CONCAT(TP.nomre_predio, ' \"', PR.descripcion, '\"') as nombre_predio, PR.ruc, MR.n_recibo, MR.periodo, PR.direccion from tipo_predio TP, predio PR, mant_recibo MR where TP.id_tipo_predio = PR.id_tipo_predio and PR.id_predio = "+str(id)+";"    
    #DATOS DE LA PERSONA 
    consultaRecibo_Persona = "select PD.id_predio, CA.numero, CONCAT(PE.nombres, ' ', PE.apellido_paterno, ' ', PE.apellido_materno) as nombreCompleto, CA.area, CA.participacion, PMDU.descripcion  from persona PE, propietario PR, casa CA,predio PD, predio_mdu PMDU where PR.id_persona = PE.id_persona and PR.id_casa = CA.id_casa and PD.id_predio = CA.id_predio and PMDU.id_predio_mdu = CA.id_predio and CA.numero = "+str(id2)+" ;"
    
    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute(consultaRecibo_Predio)
        for row in cursor.fetchall():
            datosPredio.append({"id_predio":row[0], "nombre_predio":row[1], "ruc":row[2], "num_recibo":row[3], "periodo":row[4], "direccion":row[5]})
        cursor.execute(consultaRecibo_Persona)
        for row in cursor.fetchall():
            datosPersona.append({"id_predio":row[0], "num_casa":row[1], "nombres_apellidos":row[2], "area_casa":row[3], "participacion":row[4], "desc_mdu":row[5]})
        #DATOS PARA EL RECIBO   
        nombre_predio = datosPredio[0]["nombre_predio"]
        ruc = datosPredio[0]["ruc"]
        num_recibo = datosPredio[0]["num_recibo"]
        periodo = datosPredio[0]["periodo"]
        direccion = datosPredio[0]["direccion"]
        


    except psycopg2.Error as error:
        print('error al extrear los datos de la consulta: ', error)

    finally:
        cursor.close()
        conn.close()
        
    return render_template("reciboTotal.html", datosPersona=datosPersona,nombre_predio = nombre_predio, ruc = ruc, num_recibo=num_recibo, periodo=periodo, direccion=direccion)

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
