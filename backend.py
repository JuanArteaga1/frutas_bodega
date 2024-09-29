import mysql.connector
from datetime import datetime
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
    datos = request.json
    agregar_fruta(datos)

# Función para agregar fruta a la base de datos
def agregar_fruta(datos):
    id_producto = int(datos.get('id_producto'))
    nombre = str(datos.get('nombre'))
    precio = int(datos.get('precio'))
    origen = str(datos.get('origen'))
    cantidad = int(datos.get('cantidad'))
    fecha_hoy = datetime.now().now().date()
    cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (id_producto,))
    producto_existente = cursor.fetchone()
    if producto_existente:
        cursor.execute("SELECT cantidad_actual FROM inventario WHERE id_producto = %s", (id_producto,))
        cantidad_movimiento = cursor.fetchone()
        if cantidad_movimiento:
            cantidad_movimiento = cantidad_movimiento[0] + cantidad
            cursor.execute(
                "INSERT INTO inventario(id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
                (id_producto, cantidad_movimiento, fecha_hoy, cantidad))
        else:
            cursor.execute(
                    "INSERT INTO inventario(id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
                    (id_producto, cantidad, fecha_hoy, cantidad))
        
    else:
        cursor.execute(
            "INSERT INTO productos (id_producto, nombre, precio, origen) VALUES (%s, %s, %s, %s)",
            (id_producto, nombre, precio, origen)
    )
        cursor.execute(
                "INSERT INTO inventario(id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
                (id_producto, cantidad, fecha_hoy, cantidad))
        
        
    

    bd.commit()

if __name__ == '__main__':
    app.run(debug=True)  # Inicia la aplicación Flask en modo de depuración
