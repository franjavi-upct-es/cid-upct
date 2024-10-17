from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/ip')
def obtener_ip():
    direccion_ip = request.remote_addr
    respuesta = {"ip": direccion_ip}
    return jsonify(respuesta)

@app.route('/md5/<string:texto>')
def obtener_md5(texto):
    md5_resumen = hashlib.md5(texto.encode('utf-8')).hexdigest()
    respuesta = {"md5": md5_resumen}
    return jsonify(respuesta)

@app.route('/echo/<string:campo1>/<string:valor1>/<string:campo2>/<string:valor2>')
def echo(campo1, valor1, campo2, valor2):
    respuesta = {
        campo1: valor1,
        campo2: valor2
    }
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True)