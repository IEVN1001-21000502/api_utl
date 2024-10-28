from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)

con = MySQL(app)

@app.route("/")
def index():
    return "hola"


@app.route("/alumnos/<mat>", methods = ["GET"])
def lista_alumnos(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is None:
            return jsonify({'alumno': None, 'mensaje': 'Alumno no encontrado', 'exito': False}), 404
        else:
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno encontrado', 'exito': True})
    except Exception as ex:
        return jsonify({'message': "error {}".format(ex), 'exito': False}), 500


def leer_alumno_bd(matricula):
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM alumnos WHERE matricula = %s'
        cursor.execute(sql, [matricula])
        datos = cursor.fetchone()
        if datos is not None:
            alumno = {"matricula": datos[0], "nombre": datos[1], "apaterno": datos[2], "amaterno": datos[3], "correo": datos[4]}
            return alumno
        else:
            return None
    except Exception as ex:
        raise Exception("Error al leer alumno: {}".format(ex))


def pagina_no_encontrada(error):
    return "<h1>PAGINA NO ENCONTRADA 404</h1>", 404

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)