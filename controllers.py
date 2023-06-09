from flask import Flask, render_template, request, redirect
import psycopg2

# CONEXIÓN CON LA BASE DE DATOS
def connection():
    user = 'modulo4'
    password = 'modulo4'
    database = 'sigcon'
    host = '137.184.120.127'
    server = 'postgresql'

    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )
        return conn
    except psycopg2.Error as error:
        print('Error al conectar con la base de datos:', error)

# Función para obtener los datos de la tabla recibo_estado desde la base de datos
def obtener_datos_recibo_estado():
    conn = connection()
    cursor = conn.cursor()

    try:
        consulta = 'SELECT * FROM recibo_estado'
        cursor.execute(consulta)
        datos_recibo_estado = cursor.fetchall()  # Obtener todos los resultados

        return datos_recibo_estado
    except psycopg2.Error as error:
        print('Error al obtener datos de recibo_estado:', error)
    finally:
        cursor.close()
        conn.close()



# Función para obtener los datos de la tabla mant_recibo desde la base de datos
def obtener_datos_mant_recibo():
    conn = connection()
    cursor = conn.cursor()

    try:
        consulta = 'SELECT * FROM mant_recibo'
        cursor.execute(consulta)
        datos_mant_recibo = cursor.fetchall()  # Obtener todos los resultados

        return datos_mant_recibo
    except psycopg2.Error as error:
        print('Error al obtener datos de mant_recibo:', error)
    finally:
        cursor.close()
        conn.close()