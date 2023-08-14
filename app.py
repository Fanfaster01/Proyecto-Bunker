from flask import Flask, request, render_template
from static.src.proveedores import proveedores_bp

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

app.register_blueprint(proveedores_bp, url_prefix='/proveedores')

@app.route('/registrarVentas', methods=['GET'])
def registrarVentas():
    return render_template('registrar_ventas.html')

if __name__ == '__main__':
    app.run(debug=True)

