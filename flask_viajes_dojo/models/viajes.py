import os
from flask import flash
from flask_viajes_dojo.config.mysqlconnection import connectToMySQL
from flask_viajes_dojo.models import modelo_base
from flask_viajes_dojo.models import usuarios
from flask_viajes_dojo.models import participantes
from flask_viajes_dojo.utils.regex import REGEX_CORREO_VALIDO
from datetime import datetime


class Viaje(modelo_base.ModeloBase):

    modelo = 'viajes'
    campos = ['destino', 'descripcion', 'planificador','fecha_inicio','fecha_fin']

    def __init__(self, data):
        self.id = data['id']
        self.destino = data['destino']
        self.descripcion = data['descripcion']
        self.planificador = data['planificador']
        self.nombre_planificador = data['nombre_planificador'] 
        self.fecha_inicio = data['fecha_inicio']
        self.fecha_fin = data['fecha_fin']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.participantes = []


    #si da tiempo
    @classmethod
    def buscar(cls, dato):
        query = "select * from viajes where id = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    #si da tiempo
    @classmethod
    def update(cls,data):
        query = 'UPDATE viajes SET destino = %(destino)s, descripcion = %(descripcion)s, fecha_inicio = %(fecha_inicio)s, fecha_fin = %(fecha_fin)s WHERE id = %(id)s;'
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        return resultado


    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del campo {campo} no puede ser menor o igual a {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):


        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid


        if 'destino' in data:
            is_valid = cls.validar_largo(data, 'destino', 3)
            if is_valid == False: no_create = False

        if 'descripcion' in data:
            is_valid = cls.validar_largo(data, 'descripcion', 3)
            if is_valid == False: no_create = False

        if 'fecha_inicio' in data and 'fecha_fin' in data:
            is_valid = data['fecha_inicio'] > datetime.now()
            if is_valid == False:
                flash("La fecha de inicio del viaje debe ser una fecha futura","error")
                no_create = False


            is_valid = data['fecha_fin'] > datetime.now()
            if is_valid == False:
                flash("La fecha de fin del viaje debe ser una fecha futura","error")
                no_create = False


            is_valid = data['fecha_fin'] > data['fecha_inicio']
            if is_valid == False:
                flash("La fecha de fin de viaje debe ser mayor que la fecha de inicio","error")
                no_create = False


        return no_create

    @classmethod
    def get_all_misviajes(cls,data):


        #SE ARMA LA CONSULTA
        query = "select (\"\") as nombre_planificador, v.id, v.destino, v.descripcion, v.fecha_inicio, v.fecha_fin, v. planificador , v.created_at, v.updated_at, CONCAT(u.nombre, \" \", u.apellido) as nombre_participante from viajes v left join participantes p on v.id = p.id_viaje left join usuarios u on p.id_participante = u.id where p.id_participante = %(id_participante)s;"


        #SE EJECUTA LA CONSULTA
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)

        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        viajes = []
        for result in results:
            result['fecha_inicio'] = result['fecha_inicio'].strftime("%Y-%m-%d")
            result['fecha_fin'] = result['fecha_fin'].strftime("%Y-%m-%d")
            viajes.append(cls(result))

        return viajes
 

    @classmethod
    def get_all_otrosviajes(cls,data):
        #SE ARMA LA CONSULTA
        query = "select v.id, v.destino, v.descripcion, v.fecha_inicio, v.fecha_fin, v.planificador, CONCAT(u.nombre, \" \", u.apellido) as nombre_planificador , v.created_at, v.updated_at from viajes v left join participantes p on v.id = p.id_viaje left join usuarios u on v.planificador = u.id where v.id not in (select id_viaje from participantes where id_participante = %(id_participante)s) group by v.id;"

        #SE EJECUTA LA CONSULTA
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        viajes = []
        for result in results:
            result['fecha_inicio'] = result['fecha_inicio'].strftime("%Y-%m-%d")
            result['fecha_fin'] = result['fecha_fin'].strftime("%Y-%m-%d")
            viajes.append(cls(result))

        return viajes


    @classmethod
    def get_viaje_con_participantes(cls,data):
        #SE ARMA LA CONSULTA
        query = "select v.id, v.destino, v.descripcion, v.fecha_inicio, v.fecha_fin, v.planificador, CONCAT(u.nombre,\" \", u.apellido) as nombre_planificador , v.created_at, v.updated_at from viajes v left join usuarios u on v.planificador = u.id where v.id =  %(id_viaje)s;"

        # print("query viajes ",query,flush=True)


        #SE EJECUTA LA CONSULTA
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)

        # print("query viajes ",results,flush=True)

        resultado = results[0]

        resultado['fecha_inicio'] =  resultado['fecha_inicio'].strftime("%Y-%m-%d")
        resultado['fecha_fin'] =  resultado['fecha_fin'].strftime("%Y-%m-%d")


        #SE CONVIERTE EN OBJETO PYTHON TODA LA CONSULTA
        viaje = cls(resultado)


        #SE ARMA LA CONSULTA del 1 a MUCHOS
        query1 = "select p.id_viaje, p.id_participante, CONCAT(u.nombre, \" \", u.apellido) as nombre_participante, p.created_at, p.updated_at from participantes p left join usuarios u on p.id_participante = u.id where p.id_viaje = %(id_viaje)s and p.id_participante <> %(id_participante)s;"


        #SE EJECUTA LA CONSULTA
        results1 = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query1, data)


        if results1:
             for result1 in results1:

                participante_data = {
                      "id_viaje" : result1["id_viaje"],
                      "id_participante" : result1["id_participante"],
                      "nombre_participante": result1["nombre_participante"],
                      "created_at": result1["created_at"],
                      "updated_at": result1["updated_at"]
                }

                viaje.participantes.append(participantes.Participante(participante_data))


        return viaje