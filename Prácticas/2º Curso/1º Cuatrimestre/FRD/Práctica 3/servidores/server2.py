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

@app.route('/echo', methods=['POST'])
def echo():
    # Obtén los datos del cuerpo de la solicitud en formato JSON
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    # Validar si los datos recibidos son un diccionario
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid format, expected a JSON object'}), 400

    # Responder con los mismos pares campo-valor
    response = {campo: valor for campo, valor in data.items()}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)