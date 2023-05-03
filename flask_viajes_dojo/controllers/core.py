import os
from flask import redirect, render_template, request, flash, session, url_for
from flask_viajes_dojo import app
from flask_bcrypt import Bcrypt
from flask_viajes_dojo.models.usuarios import Usuario
from flask_viajes_dojo.models.viajes import Viaje
from flask_viajes_dojo.models.participantes import Participante
from datetime import datetime, timedelta

bcrypt = Bcrypt(app)

@app.route("/")
def index():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")

    datos_mis_viajes = []

    if 'idusuario' in session:
        data = {"id_participante":int(session['idusuario'])}
        datos_mis_viajes = Viaje.get_all_misviajes(data)
        datos_otros_viajes = Viaje.get_all_otrosviajes(data)

    return render_template("main.html", sistema=nombre_sistema, mis_viajes = datos_mis_viajes, otros_viajes = datos_otros_viajes)

@app.route("/login")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    return render_template("login.html")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    #validaciones del objeto usuario
    if not Usuario.validar(request.form):
        return redirect('/login')

    pass_hash = bcrypt.generate_password_hash(request.form['password_reg'])

    data = {
        'usuario' : request.form['user'],
        'nombre' : request.form['name'],
        'apellido' : request.form['lastname'],
        'email' : request.form['email'],
        'password' : pass_hash,
    }

    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/login")

    flash("Usuario creado correctamente", "success")
    return redirect("/login")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identification'])

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['idusuario'] = usuario.id
    session['usuario'] = usuario.nombre + " " + usuario.apellido


    return redirect('/')

@app.route('/logout')
def logout():
    print("log out!")
    session.clear()
    return redirect('/login')


@app.route("/crearviaje")
def crearviaje():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    operacion = "Nuevo Viaje"


    if 'rollback_destino' in session:
        data = {
        'id':'',
        'destino':session['rollback_destino'],
        'descripcion':session['rollback_descripcion'],
        'fecha_inicio':session['rollback_fecha_inicio'],
        'fecha_fin' : session['rollback_fecha_fin'],
        }
        session.pop('rollback_destino')
        session.pop('rollback_descripcion')
        session.pop('rollback_fecha_inicio')
        session.pop('rollback_fecha_fin')
    else:
        data = {
        'id':'',
        'destino':'',
        'descripcion':'',
        'fecha_inicio':(datetime.today()+timedelta(days=+1)).strftime("%Y-%m-%d"),
        'fecha_fin' : (datetime.today()+timedelta(days=+2)).strftime("%Y-%m-%d"),
        }

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")

    return render_template('form.html',operacion=operacion,datos_viaje=data)



@app.route("/procesar_viaje", methods=["POST"])
def procesar_viaje():

    fecha = datetime.date
    date_format = '%Y-%m-%d %H:%M:%S'

    if type(request.form['fecha_inicio']) is str:
        fecha_inicio = datetime.strptime(request.form['fecha_inicio'] + " 00:00:00",date_format)

    if type(request.form['fecha_fin']) is str:
        fecha_fin = datetime.strptime(request.form['fecha_fin'] + " 00:00:00",date_format)

    data ={
            'destino':request.form['destino'],
            'descripcion':request.form['descripcion'],
            'planificador':session['idusuario'],
            'fecha_inicio':fecha_inicio,
            'fecha_fin':fecha_fin
           }


    validar = Viaje.validar(data)

    if not validar:
        if request.form['operacion'] == 'Nuevo Viaje':
            session['rollback_destino'] = request.form['destino']
            session['rollback_descripcion'] = request.form['descripcion']
            session['rollback_fecha_inicio'] = request.form['fecha_inicio']
            session['rollback_fecha_fin'] = request.form['fecha_fin']
            return redirect('/crearviaje')

    try:
        if request.form['operacion'] == 'Nuevo Viaje':

            id_viaje = Viaje.save(data)

            data2={
            'id_participante':int(session['idusuario']),
            'id_viaje':int(id_viaje)
            }

            Participante.save(data2)
            #falta grabar en participantes al creador
        if  request.form['operacion'] == 'Editar Viaje':
            data['id'] = int(request.form['id'])
            Viaje.update(data)
        flash("Viaje almacenada con exito!","success")
        print("Viaje guardado con exito!",flush=True)
    except Exception as error:
        print(f"error al guardar el viaje, valor del error : {error}",flush=True)

    return redirect('/')


@app.route("/unirse_viaje/<id>")
def unirse_viaje(id):

    data={
       'id_participante':int(session['idusuario']),
       'id_viaje':int(id)
         }

    Participante.save(data)

    return redirect('/')



@app.route("/detalle_viaje/<id_viaje>/<id_usuario>")
def detalle_viaje(id_viaje,id_usuario):

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    data = {"id_viaje":int(id_viaje),
            "id_participante":int(id_usuario)
            }

    datos_viaje = Viaje.get_viaje_con_participantes(data)

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")
    return render_template('detail.html',sistema=nombre_sistema, viaje=datos_viaje)