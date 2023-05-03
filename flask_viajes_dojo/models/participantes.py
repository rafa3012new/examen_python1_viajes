import os
from flask import flash
from flask_viajes_dojo.config.mysqlconnection import connectToMySQL
from flask_viajes_dojo.models import modelo_base
from flask_viajes_dojo.models import usuarios
from flask_viajes_dojo.utils.regex import REGEX_CORREO_VALIDO
from datetime import datetime


class Participante(modelo_base.ModeloBase):

    modelo = 'participantes'
    campos = ['id_viaje', 'id_participante']

    def __init__(self, data):
        self.id = data['id_viaje']
        self.destino = data['id_participante']
        self.nombre_participante = data['nombre_participante']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']