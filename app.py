import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
DB_NAME = "consultas.db"

# func dbb
def init_db():
    """Crea la tabla si no existe al arrancar el servicio"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor_a REAL,
            valor_b REAL,
            resultado REAL,
            fecha TEXT
        )
    ''')
    conn.commit()
    conn.close()

def guardar_consulta(a, b, resultado):
    """Inserta los datos en la base de datos"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO historial (valor_a, valor_b, resultado, fecha) VALUES (?, ?, ?, ?)",
        (a, b, resultado, fecha_actual)
    )
    conn.commit()
    conn.close()

@app.route('/sumar', methods=['GET'])
def sumar_numeros():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)

    if a is None or b is None:
        return jsonify({"error": "Por favor, proporciona los parametros a y b"}), 400

    resultado = a + b 
    guardar_consulta(a, b, resultado) 
    
    return jsonify({
        "operacion": "suma",
        "a": a,
        "b": b,
        "resultado": resultado,
        "mensaje": "Guardado en historial"
    })

@app.route('/historial', methods=['GET'])
def ver_historial():
    """Este ahora sí funcionará porque pertenece a la misma 'app'"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historial ORDER BY id DESC")
        filas = cursor.fetchall()
        conn.close()
        
        historial_limpio = []
        for f in filas:
            historial_limpio.append({
                "id": f[0],
                "a": f[1],
                "b": f[2],
                "resultado": f[3],
                "fecha": f[4]
            })
            
        return jsonify(historial_limpio)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. Bloque de ejecución ÚNICO
if __name__ == '__main__':
    init_db()  # Inicializamos la BD
    print("Servidor corriendo en el puerto 5001...")
    app.run(host='0.0.0.0', port=5001)