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
@app.route('/administrar_datos', methods=['POST'])
def administrar_datos_endpoint():
    datos = request.json
    if datos.get('tipo') == 'entrada':
        agregar_fruta(datos)
    elif datos.get('tipo') == 'salida':
        print("")
    elif datos.get('tipo') == 'proveedor':
        agregar_proveedor(datos)
    elif datos.get('tipo') == 'empleado':
        agregar_empleado(datos)
    elif datos.get('tipo') == 'salida':
        sacar_fruta(datos)
# Función para agregar fruta a la base de datos
def agregar_fruta(datos):
    id_producto = int(datos.get('id_producto'))
    nombre = str(datos.get('nombre'))
    precio = int(datos.get('precio'))
    origen = str(datos.get('origen'))
    cantidad = int(datos.get('cantidad'))
    fecha_hoy = datetime.now()
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

def agregar_proveedor(datos):
    cedula = int(datos.get('id_proveedor'))
    nombre_proveedor = str(datos.get('nombre'))
    telefono = str(datos.get('telefono'))
    direccion = str(datos.get('direccion'))
    email = str(datos.get('email'))
    cursor.execute("INSERT INTO proveedores (id_proveedores, nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s)",
                (cedula, nombre_proveedor, email, telefono, direccion))
    bd.commit()
def agregar_empleado(datos):
    cedula = int(datos.get('id_empleado'))
    jerarquia = 1
    nombre_empleado = str(datos.get('nombre'))
    apellido = str(datos.get('apellido'))
    direccion = str(datos.get('direccion'))
    email = str(datos.get('email'))
    telefono = str(datos.get('telefono'))
    contraseña_empleado = str(datos.get('contraseña'))  # Captura la contraseña desde el formulario
    cursor.execute("""
        INSERT INTO empleados (id_empleados, id_jerarquia, nombre, apellido, email, telefono, direccion, contraseña) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (cedula, jerarquia, nombre_empleado, apellido, email, telefono, direccion, contraseña_empleado))
    bd.commit()
def sacar_fruta(datos):
    id_producto = int(datos.get('id_producto'))
    cantidad = int(datos.get('cantidad'))
    fecha_hoy = datetime.now()
    cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (id_producto,))
    producto_existente = cursor.fetchone()
    if producto_existente:
        cursor.execute("SELECT cantidad_actual FROM inventario WHERE id_producto = %s", (id_producto,))
        cantidad_movimiento = cursor.fetchone()
        if cantidad_movimiento:
            cantidad_movimiento = cantidad_movimiento[0] - cantidad
            cursor.execute(
                "INSERT INTO inventario(id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
                (id_producto, cantidad_movimiento, fecha_hoy, cantidad))
        else:
            cursor.execute(
                    "INSERT INTO inventario(id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
                    (id_producto, cantidad, fecha_hoy, cantidad))
    else:
        cursor.execute(
                "INSERT INTO inventario(id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
                (id_producto, cantidad, fecha_hoy, cantidad))

    bd.commit()

if __name__ == '__main__':
    app.run(debug=True)  # Inicia la aplicación Flask en modo de depuración
