import mysql.connector
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify

# Configuración de la aplicación Flask
app = Flask(__name__)
# Configuración de la base de datos MySQL
bd = mysql.connector.connect(
    user="root",
    password="123456",
    host="localhost",
    database="administracion_bodega"
)
cursor = bd.cursor()

# Ruta para agregar frutas
@app.route('/administrar_datos', methods=['POST'])
def administrar_datos_endpoint():
    datos = request.json    

    #gestionar producto
    if datos.get('tipo') == 'entrada':
        agregar_fruta(datos) 
        return jsonify({"status": "agregar producto"}), 200 
    elif datos.get('tipo') == 'eliminar_producto':
        eliminarproducto(datos)
        return jsonify({"status": "eliminar producto"}), 200 
    elif datos.get('tipo') == 'actualizar_producto':
        actualizar_producto(datos)
        return jsonify({"status": "actualizar producto"}), 200
    elif datos.get('tipo') == 'salida':
        sacar_frutas(datos)
        return jsonify({"status": "sacar prodcuto"}), 200


    #gestionar proveedor
    elif datos.get('tipo') == 'proveedor':
        agregar_proveedor(datos)
        return jsonify({"status": "agregar proveedor"}), 200 
    elif datos.get('tipo') == 'actualizar_proveedores':
        print("hola")
        actualizar_proveedor(datos)
        return jsonify({"status": "actualizar proveedor"}), 200
    elif datos.get('tipo') == 'eliminar_proveedor':
        print("hola1")
        eliminar_proveedor(datos)
        return jsonify({"status": "eliminar proveedor"}), 200
    
    #gestionar empleado
    elif datos.get('tipo') == 'empleado':
        agregar_empleado(datos)
        return jsonify({"status": "agregar empleado"}), 200 
    elif datos.get('tipo') == 'actualizar_empleado':
        actualizar_empleado(datos)
        return jsonify({"status": "actializar empleado"}), 200
    elif datos.get('tipo') == 'eliminar_empleado':
        eliminar_empleado(datos)
        return jsonify({"status": "eliminar empleado"}), 200

    elif datos.get('tipo') == 'inicio_sesion':
        resul = inicio_seccion(datos)
        return jsonify({"status": resul}), 200   
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
    apellido = str(datos.get('apellido'))
    direccion = str(datos.get('direccion'))
    email = str(datos.get('email'))
    telefono = str(datos.get('telefono'))
    contraseña_empleado = str(datos.get('contraseña'))# Captura la contraseña desde el formulario
    cursor.execute("SELECT id_empleados FROM empleados WHERE id_empleados = %s", (identificacion,))
    empleado_existente = cursor.fetchone()
    if empleado_existente == None:  
        cursor.execute("""
            INSERT INTO empleados (id_empleados, id_jerarquia, nombre, apellido, email, telefono, direccion, contraseña) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (identificacion, numero_jerarquia, nombre_empleado, apellido, email, telefono, direccion, contraseña_empleado))
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
    id_producto = int(datos.get('id_producto'))
    cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (id_producto,))
    producto_existente = cursor.fetchone()
    if producto_existente:
        cursor.execute("DELETE FROM inventario WHERE id_producto = %s", (id_producto,))
        bd.commit()
        cursor.execute("DELETE FROM productos  WHERE id_producto = %s", (id_producto,))
        bd.commit()
def actualizar_producto(datos):
    print("entro")
    id_producto = int(datos.get('id_producto'))
    nuevo_nombre = str(datos.get('nombre'))
    nuevo_precio = int(datos.get('precio'))
    nuevo_origen = str(datos.get('origen'))
    cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (id_producto,))
    producto_existente = cursor.fetchone()
    if producto_existente:
        print("entro")
        cursor.execute("""UPDATE productos SET nombre = %s, precio = %s, origen = %s  WHERE id_producto = %s""", (nuevo_nombre, nuevo_precio, nuevo_origen, id_producto))
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
    
# Ruta para obtener los nombres y apellidos de los empleados
@app.route('/nombre_empleados', methods=['POST'])
def nombre_empleados():
    cursor.execute("select nombre, apellido from empleados")
    resultados = cursor.fetchall()
    columnas = [i[0] for i in cursor.description]
    df =  pd.DataFrame(resultados, columns=columnas)
    nombre_apellidos = df.to_dict(orient='records')
    for item in nombre_apellidos:
        nombre = item['nombre']
        apellido = item['apellido']
        print(f'nombre: {nombre}, apellido: {apellido}')
    cursor.close()
    return jsonify(nombre_apellidos)
    






if __name__ == '__main__':
    app.run(debug=True) # Inicia la aplicación Flask en modo de depuración
    

print("hola")