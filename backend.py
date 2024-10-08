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
    print("datos")
    datos = request.json
    if datos.get('tipo') == 'entrada':
        agregar_fruta(datos) 
        return jsonify({"status": "Fruta agregada con éxito"}), 200 
    elif datos.get('tipo') == 'proveedor':
        agregar_proveedor(datos)
        return jsonify({"status": "Fruta agregada con éxito"}), 200 
    elif datos.get('tipo') == 'empleado':
        agregar_empleado(datos)
        return jsonify({"status": "Fruta agregada con éxito"}), 200 
    elif datos.get('tipo') == 'salida':
        sacar_frutas(datos)
        return jsonify({"status": "Fruta agregada con éxito"}), 200 
    elif datos.get('tipo') == 'eliminarproducto':
        eliminarproducto(datos)
        return jsonify({"status": "Fruta agregada con éxito"}), 200 
    elif datos.get('tipo') == 'actulizar_producto':
        actualizar_producto(datos)
        return jsonify({"status": "Fruta agregada con éxito"}), 200 
    elif datos.get('tipo') == 'actualizar_proveedores':
        eliminar_proveedor(datos)
        return jsonify({"status": "Fruta agregada con éxito"}), 200 


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
def eliminar_proveedor(datos):
    nombre_empleado = "juan"#str(datos.get('nombre'))
    identificacion = 1#int(datos.get('id_empleado'))
    cursor.execute("SELECT id_proveedores FROM proveedores WHERE id_proveedores = %s", (identificacion,))
    proveedor_existente = cursor.fetchone()
    if proveedor_existente:
        cursor.execute("DELETE FROM proveedores WHERE id_producto = %s", (identificacion,))
        bd.commit()
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
def eliminarproducto(datos):
    id_producto = int(datos.get('id_producto'))
    cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (id_producto,))
    producto_existente = cursor.fetchone()
    if producto_existente:
        cursor.execute("DELETE FROM inventario WHERE id_producto = %s", (id_producto,))
        bd.commit()
        cursor.execute("DELETE FROM productos  WHERE id_producto = %s", (id_producto,))
        bd.commit()
def actualizar_producto():
    print("entro")
    id_producto = 1#int(datos.get('id_producto'))
    nuevo_nombre = "pera"#str(datos.get('nombre'))
    nuevo_precio = 3000#int(datos.get('precio'))
    nuevo_origen = "popayan"#str(datos.get('origen'))
    cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (id_producto,))
    producto_existente = cursor.fetchone()
    if producto_existente:
        print("entro")
        cursor.execute("""UPDATE productos SET nombre = %s, precio = %s, origen = %s  WHERE id_producto = %s""", (nuevo_nombre, nuevo_precio, nuevo_origen, id_producto))
        bd.commit()  

def actualizar_proveedor(datos):
    identificacion = 1#int(datos.get('id_proveedor'))
    nombre_proveedor = "pedrp" #str(datos.get('nombre'))
    telefono = "3160807017"#str(datos.get('telefono'))
    direccion = "tu casa" #str(datos.get('direccion'))
    email = "jara@jara.com"#str(datos.get('email'))
    cursor.execute("SELECT id_proveedores FROM proveedores WHERE id_proveedores = %s", (identificacion,))
    proveedor_existente = cursor.fetchone()
    if proveedor_existente:
        cursor.execute("""UPDATE proveedores SET nombre = %s, email = %s, telefono = %s, direccion = %s  WHERE id_proveedores = %s""", (nombre_proveedor, email, telefono, direccion, identificacion))
        bd.commit()  





if __name__ == '__main__':
    app.run(debug=True) # Inicia la aplicación Flask en modo de depuración
    