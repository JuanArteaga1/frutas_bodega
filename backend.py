import mysql.connector
import datetime
from flask import Flask, request, jsonify

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos MySQL
bd = mysql.connector.connect(
    user="root",
    password="133724",
    host="localhost",
    database="administracion_bodega"
)
cursor = bd.cursor()

# Ruta para agregar frutas
@app.route('/agregar_fruta', methods=['POST'])
def agregar_fruta_endpoint():
    datos = request.json  # Obtener los datos JSON de la solicitud
    if datos:
        result = agregar_fruta(datos)  # Procesar los datos
        return jsonify({"message": "Producto recibido correctamente", "status": "success"})
    else:
        return jsonify({"message": "No se recibieron datos", "status": "error"}), 400

# Función para agregar fruta a la base de datos
def agregar_fruta(datos):
    id_producto = int(datos.get('id_producto'))
    nombre = str(datos.get('nombre'))
    precio = int(datos.get('precio'))
    origen = str(datos.get('origen'))
    cantidad = int(datos.get('cantidad')) # Asumiendo que `cantidad` también debe ser insertado
    cursor.execute(
        "INSERT INTO productos (id_producto, nombre, precio, origen) VALUES (%s, %s, %s, %s)",
        (id_producto, nombre, precio, origen)
    )
    bd.commit()
    return "True"

if __name__ == '__main__':
    app.run(debug=True)  # Inicia la aplicación Flask en modo de depuración
