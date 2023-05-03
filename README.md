#El nombre de la base de datos es viajes_dojo

Se debe crear las tablas y db desde la carpeta db, alli se encuentran los script de las tablas y el diagrama de modelo

con el Archivo .env puede modificarse el user y password de la db mysql


#Esta version de Viajes Dojo hace uso de:

#Front End

HTML, CSS, JAVASRIPT Y BOOTSTRAP

#Back End

PYTHON, FLASK y MYSQL 

Hace uso del Modelo Vista Controlador (MVC)

#Archivos de Modelo:
base.py
usuarios.py

#Archivos de Vista (Templates, Static)

Templates:

base.html
main.html
form.html
detail.html
login.html
_menu.html

Static

viajes.css
viajes.js
archios de bootstrap...
utilidad toaster.css y js para modificar a apariencia de los mensajes flash llamada toastr


#Archivo Controlador
Controller.py

Hace uso de archivo .env, pero no se incluye debido a la seguridad de Github
por lo que se crea un archivo .env.example que despues se reombrara...
para que funcione la app el archivo .env.
El contenido del archivo .env es el que sigue a continuacion:

APP_SECRET_KEY="user_login"
BASEDATOS_HOST="localhost"
BASEDATOS_USER="root"
BASEDATOS_PASSWORD="root"
BASEDATOS_NOMBRE="user_login"
NOMBRE_SISTEMA="Sistema de Viajes"


por ello se utiliza el archivo de git ignore

