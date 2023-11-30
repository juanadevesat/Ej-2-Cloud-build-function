from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '000000'


@app.route("/", methods=["GET", "POST"])
def index():

    return "Hello, World!"


if __name__ == '__main__':
    # Ejecuta la aplicación
    app.run(host="0.0.0.0", port=5000, debug=False)