from flask import Flask, render_template, request, redirect, flash
from google.cloud import storage, firestore
import json
import random
import datetime
import time


today = datetime.date.today().strftime('%Y-%m-%d')
todayUTC = int(time.time())

# Crea una aplicación de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '000000'


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Definición: Endpoint para la página de inicio de la web. Contiene un formulario.

    Form: Nombre - Nombre insertado por el usuario.
    Form: Correo electrónico - email insertado por el usuario.

    Return: index.html
    """
    if request.method == "POST":
        # Creamos un cliente de cloud storage para acceder al bucket
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('bucket-juan-ejercicio-final')

        # Comprobamos que se han introducido los datos
        nombre = request.form.get("nombre")
        if len(nombre) == 0:
            flash("¡Introduce un nombre!")
            return render_template("index.html")
        
        email = request.form.get("email")
        if len(email) == 0:
            flash("¡Introduce un correo electrónico!")
            return render_template("index.html", nom=nombre)

        # Comprobamos que el usuario no existe en la base de datos
        db = firestore.Client()
        docs = db.collection(u'firestore-juan-ejercicio-final').stream()

        docs_dict = []
        for doc in docs:
            docs_dict.append(doc.to_dict())

        existe = False

        for d in docs_dict:
            if d['email'] == email:
                existe = True

        if existe == True:
            flash("¡Este correo electrónico ya ha sido registrado!")
            return render_template("index.html", nom=nombre, mail=email)
        else:
            # Creamos un diccionario con los datos del usuario
            usuario = {
                'ID': random.randint(100000, 999999),
                'nombre': nombre,       # Dato procedente de la web
                'email': email,         # Dato procedente de la web
                'registro': today       # Dato procedente de la variable creada arriba
            }

            try:
                # Guardamos los datos del usuario en un archivo JSON en cloud storage
                blob = bucket.blob(f'usuarios{todayUTC}.json')
                blob.upload_from_string(data=json.dumps(usuario),content_type='application/json')
                time.sleep(5)
                return redirect("/data")
            except:
                flash("¡Ha ocurrido un error! No se han almacenado los datos.")
                return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/data")
def data():
    """
    Definición: Endpoint para la página de la tabla de usuarios.

    Items - diccionario de datos extraídos de la base de datos

    return: data.html
    """

    # Configurar conexión con dynamoDB
    db = firestore.Client()
    doc_ref = db.collection(u'firestore-juan-ejercicio-final').stream()

    # Obtener los elementos de la tabla
    items = []
    for doc in doc_ref:
        items.append(doc.to_dict())
    print(items)

    return render_template("data.html", items=items)


if __name__ == '__main__':
    # Ejecuta la aplicación
    app.run(host="0.0.0.0", port=5000, debug=False)
