from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ip')
def obtener_ip():
    direccion_ip = request.remote_addr
    respuesta = {"ip": direccion_ip}
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True)