from flask import Flask, request, jsonify
app = Flask(__name__)

# Cambia el nombre del endpoint a '/agregar_fruta'
@app.route('/agregar_fruta', methods=['POST'])
def receive_product():
    data = request.json  # Obtén los datos en formato JSON
    print(f"Datos recibidos: {data}")
    
    # Procesa los datos como lo necesites
    return jsonify({"message": "Producto recibido correctamente", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
