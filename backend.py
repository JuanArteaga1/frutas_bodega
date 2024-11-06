import mysql.connector
from datetime import datetime
from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from flask import Flask, request, jsonify


# Configuración de la aplicación Flask
app = Flask(__name__)
CORS(app)
# Configuración de la base de datos MySQL
bd = mysql.connector.connect(
    user="root",
    password="133724",
    host="localhost",
    database="administracion_bodega"
)
cursor = bd.cursor()
# Ruta para agregar frutas
#@app.route('/administrar_datos', methods=['POST'])
def administrar_datos():
    datos = request.json
    if datos.get('tipo') == 'entrada':
        agregar_fruta(datos) 
        return jsonify({"status": "agregar producto"}), 200
    elif datos.get('tipo') == 'proveedor':
        agregar_proveedor(datos)
        return jsonify({"status": "agregar proveedor"}), 200
    elif datos.get('tipo') == 'empleado':
        agregar_empleado(datos)
        return jsonify({"status": "agregar empleado"}), 200 
@app.route('/administrar_datos', methods=['DELETE'])
def administrar_datos_eliminar():
    datos = request.json
    if datos.get('tipo') == 'eliminar_producto':
        eliminarproducto(datos)
        return jsonify({"status": "eliminar producto"}), 200 
    elif datos.get('tipo') == 'eliminar_proveedor':
        eliminar_proveedor(datos)
        return jsonify({"status": "eliminar proveedor"}), 200
    elif datos.get('tipo') == 'eliminar_empleado':
        eliminar_empleado(datos)
        return jsonify({"status": "eliminar empleado"}), 200
@app.route('/administrar_datos', methods=['PUT'])
def administrar_datos_actualizar():
    datos = request.json
    if datos.get('tipo') == 'actualizar_producto':
        actualizar_producto(datos)
        return jsonify({"status": "actualizar producto"}), 200
    elif datos.get('tipo') == 'actualizar_proveedores':
        actualizar_proveedor(datos)
        return jsonify({"status": "actualizar proveedor"}), 200
    elif datos.get('tipo') == 'actualizar_empleado':
        actualizar_empleado(datos)
        return jsonify({"status": "actializar empleado"}), 200
#@app.route('/administrar_datos', methods=['POST'])  
def administrar_datos_sacar():
    datos = request.json
    if datos.get('tipo') == 'salida':
        sacar_frutas(datos)
        return jsonify({"status": "sacar prodcuto"}), 200





def sacar_frutas(datos):
    id_producto = int(datos.get('id_producto'))
    cantidad_a_sacar = int(datos.get('cantidad'))
    fecha_hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Asegurar formato correcto para la fecha

    # Verificar si el producto existe en la tabla 'productos'
    cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (id_producto,))
    producto_existente = cursor.fetchone()

    if producto_existente:
        # Obtener la cantidad actual del inventario para ese producto (último registro)
        cursor.execute("""
            SELECT cantidad_actual 
            FROM inventario  
            WHERE id_producto = %s 
            ORDER BY id_inventario DESC 
            LIMIT 1
        """, (id_producto,))
        
        cantidad_movimiento = cursor.fetchone()

        # Verificar que no haya resultados pendientes
        cursor.fetchall()  # Consumir cualquier resultado pendiente (aunque esto no debería ser necesario si no hay otras consultas)

        if cantidad_movimiento and int(cantidad_movimiento[0]) >= cantidad_a_sacar:  # Acceder al valor correcto en la tupla
            cantidad_actual = int(cantidad_movimiento[0])
            nueva_cantidad = cantidad_actual - cantidad_a_sacar

            # Actualizar el inventario con la nueva cantidad y registrar el movimiento
            cursor.execute(
                "INSERT INTO inventario(id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
                (id_producto, nueva_cantidad, fecha_hoy, -cantidad_a_sacar)  # 'cantidad_a_sacar' es negativa para representar salida
            )

            # Confirmar la transacción
            bd.commit()

            print("Movimiento de salida registrado correctamente.")
        else:
            print("No hay suficiente cantidad para realizar la salida.")
    else:
        print("El producto no existe en la base de datos.")
def agregar_fruta(datos):
    nombre = str(datos.get('nombre'))
    precio = int(datos.get('precio'))
    origen = str(datos.get('origen'))
    cantidad = int(datos.get('cantidad'))
    fecha_hoy = datetime.now()
    cursor.execute("SELECT nombre FROM productos WHERE nombre = %s and precio = %s", (nombre,precio))
    producto_existente = cursor.fetchone()
    if producto_existente == None:
        cursor.callproc('ingresar_producto',(nombre,precio,origen,cantidad,fecha_hoy,cantidad))
    else:
        cursor.execute("SELECT cantidad_actual FROM inventario WHERE nombre = %s", (nombre,))
        cantidad_movimiento = cursor.fetchone()
        if cantidad_movimiento:
            cantidad_movimiento = cantidad_movimiento[0] + cantidad
            cursor.execute(
                "INSERT INTO inventario(id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
                ( cantidad_movimiento, fecha_hoy, cantidad))
    bd.commit()
def agregar_proveedor(datos):
    identificacion = int(datos.get('id_proveedor'))
    nombre_proveedor = str(datos.get('nombre'))
    telefono = str(datos.get('telefono'))
    direccion = str(datos.get('direccion'))
    email = str(datos.get('email'))
    cursor.execute("SELECT id_proveedores FROM proveedores WHERE id_proveedores = %s", (identificacion,))
    proveedor_existente = cursor.fetchone()
    if proveedor_existente == None:
        cursor.execute("INSERT INTO proveedores (id_proveedores, nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s)",
                    (identificacion, nombre_proveedor, email, telefono, direccion))
        bd.commit()
def agregar_empleado(datos):
    identificacion = int(datos.get('id_empleado'))
    jerarquia = str(datos.get('tipo1'))
    if jerarquia == 'administrador':
        numero_jerarquia = 2
    else :
        numero_jerarquia = 1    
    nombre_empleado = str(datos.get('nombre'))
    direccion = str(datos.get('direccion'))
    email = str(datos.get('email'))
    telefono = str(datos.get('telefono'))
    contraseña_empleado = str(datos.get('contraseña'))# Captura la contraseña desde el formulario
    cursor.execute("SELECT id_empleados FROM empleados WHERE id_empleados = %s", (identificacion,))
    empleado_existente = cursor.fetchone()
    if empleado_existente == None:  
        cursor.execute("""
            INSERT INTO empleados (id_empleados, id_jerarquia, nombre, email, telefono, direccion, contraseña) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (identificacion, numero_jerarquia, nombre_empleado, email, telefono, direccion, contraseña_empleado))
        bd.commit()
def eliminar_proveedor(datos):
    identificacion =int(datos.get('id_proveedor'))
    cursor.execute("SELECT id_proveedores FROM proveedores WHERE id_proveedores = %s", (identificacion,))
    proveedor_existente = cursor.fetchone()
    if proveedor_existente:
        cursor.execute("DELETE FROM proveedores WHERE id_proveedores = %s", (identificacion,))
        bd.commit()
def eliminar_empleado(datos):
    identificacion =int(datos.get('id_empleado'))
    cursor.execute("SELECT id_empleados FROM empleados WHERE id_empleados = %s", (identificacion,))
    proveedor_existente = cursor.fetchone()
    if proveedor_existente:
        cursor.execute("DELETE FROM empleados WHERE id_empleados = %s", (identificacion,))
        bd.commit()
def eliminarproducto(datos):
    nombre = str(datos.get('nombre'))
    cursor.execute("SELECT id_producto FROM productos WHERE nombre = %s", (nombre,))
    producto_existente = cursor.fetchone()
    if producto_existente:
        id_producto = producto_existente[0]  # Obtener el ID de producto
        cursor.execute("DELETE FROM inventario WHERE id_producto = %s", (id_producto,))
        bd.commit()
        cursor.execute("DELETE FROM productos WHERE nombre = %s", (nombre,))
        bd.commit()
def actualizar_producto(datos):
    nombre = str(datos.get('nombre'))
    nuevo_precio = int(datos.get('precio'))
    nuevo_origen = str(datos.get('origen'))
    print("entro")
    cursor.execute("""UPDATE productos SET precio = %s, origen = %s  WHERE nombre = %s""", ( nuevo_precio, nuevo_origen, nombre))
    bd.commit()
def actualizar_proveedor(datos):
    identificacion =int(datos.get('id_proveedor'))
    nombre_proveedor =str(datos.get('nombre'))
    telefono =str(datos.get('telefono'))
    direccion =str(datos.get('direccion'))
    email =str(datos.get('email'))
    cursor.execute("SELECT id_proveedores FROM proveedores WHERE id_proveedores = %s", (identificacion,))
    proveedor_existente = cursor.fetchone()
    if proveedor_existente:
        cursor.execute("""UPDATE proveedores SET nombre = %s, email = %s, telefono = %s, direccion = %s  WHERE id_proveedores = %s""", (nombre_proveedor, email, telefono, direccion, identificacion))
        bd.commit()  
def actualizar_empleado(datos):
    identificacion = int(datos.get('id_empleado'))
    nombre_empleado = str(datos.get('nombre'))
    apellido = str(datos.get('apellido'))
    direccion = str(datos.get('direccion'))
    email = str(datos.get('email'))
    telefono = str(datos.get('telefono'))
    cursor.execute("SELECT id_empleados FROM empleados WHERE id_empleados = %s", (identificacion,))
    empleado_existente = cursor.fetchone()
    if empleado_existente:
        cursor.execute("""UPDATE empleados SET nombre = %s, apellido = %s, email = %s, telefono = %s, direccion = %s  WHERE id_empleados = %s""", (nombre_empleado, apellido, email, telefono, direccion, identificacion))
        bd.commit() 
def inicio_seccion(datos):
    identificacion = str(datos.get('identificacion'))
    contraseña_empleado = (datos.get('contraseña'))
    cursor.execute("SELECT id_empleados,contraseña FROM empleados WHERE id_empleados = %s and contraseña = %s", (identificacion, contraseña_empleado,))
    empleado_existente = cursor.fetchone()
    if empleado_existente:
        return True
    else:
        return False
def obtener_datos():
    cursor.execute("SELECT id_producto, nombre, origen, precio FROM productos")
    resultados = cursor.fetchall()
    
    productos = []
    for fila in resultados:
        datos = {
            'nombre': fila[1],  # Nombre del producto con origen
        }
        productos.append(datos)

    return productos

def obtener_empleados():
    cursor.execute("SELECT nombre FROM empleados")
    resultados = cursor.fetchall()
    empleados = []
    
    for fila in resultados: 
        
        empleado = {
            'nombre': fila[0],  # Nombre completo del empleado
        }
        empleados.append(empleado)
    return empleados

def obtener_proveedores():
    cursor.execute("SELECT nombre FROM proveedores")
    resultados = cursor.fetchall()
    proveedores = []

    for fila in resultados:
        proveedor = {
            'nombre': fila[0],  # Nombre del proveedor
        }
        proveedores.append(proveedor)

    return proveedores

# Ruta para obtener los nombres y apellidos de los empleados

@app.route('/administrar_datos', methods=['GET'])
def administrar_datos():
    cursor.execute("SELECT id_producto, nombre, origen, precio FROM productos")
    resultados = cursor.fetchall()
    datos = []
    for fila in resultados:
        dato = {
            'id_producto': fila[0],
            'nombre': fila[1],
            'origen': fila[2],
            'precio': fila[3],
        }
        datos.append(dato)
    return jsonify(datos), 200





if __name__ == '__main__':
    app.run(debug=True) # Inicia la aplicación Flask en modo de depuración
