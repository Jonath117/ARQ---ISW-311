from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sumar', methods=['GET'])
def sumar_numeros():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)

    if a is None or b is None:
        return jsonify({"error": "Por favor, proporciona los parametros a y b"}), 400

    resultado = a + b  
    
    return jsonify({
        "operacion": "suma",
        "a": a,
        "b": b,
        "resultado": resultado
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)