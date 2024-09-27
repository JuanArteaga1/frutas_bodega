import mysql.connector
import datetime

# Conexión a la base de datos
bd = mysql.connector.connect(
    user="root",
    password="133724",
    host="localhost",
    database="administracion_bodega"
)

cursor = bd.cursor()

# Verificar jerarquías
cursor.execute("SELECT * FROM jerarquias")
result = cursor.fetchall()
for jerarquias in result:
    print(jerarquias)

def iniciar_sesion():
    nombre_usuario = input("Ingresa tu nombre de usuario: ")
    contraseña = input("Ingresa tu contraseña: ")
    # Aquí podrías agregar una verificación de usuario y contraseña si es necesario
    gestionar_inventario()

# Agregar fruta
def agregar_fruta():
    id = int(input("Ingresa el ID: "))  # Asegúrate de que el ID sea único
    fruta = input("Ingresa el nombre de la fruta: ")
    origen = input("Ingresa de dónde viene la fruta: ")
    precio = float(input("Ingresa el precio de la fruta: "))  # Convertir a float para manejar decimales
    cantidad = int(input("Ingresa la cantidad en KG: "))
    fecha_hoy = datetime.date.today()
    
    # Insertar en la tabla de productos
    cursor.execute(
        "INSERT INTO productos (id_producto, nombre, precio, origen) VALUES (%s, %s, %s, %s)",
        (id, fruta, precio, origen)
    )
    
    # Insertar en la tabla de inventario
    cursor.execute(
        "INSERT INTO inventario (id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
        (id, cantidad, fecha_hoy, cantidad)
    )
    
    bd.commit()
    print(f"Se han agregado {cantidad} KG de {fruta}(s) al inventario.")

# Eliminar fruta
def eliminar_fruta():
    id = int(input("Ingresa el ID de la fruta a eliminar: "))
    cantidad = int(input("Ingresa la cantidad a eliminar en KG: "))
    
    # Verificar si la fruta existe en el inventario
    cursor.execute("SELECT cantidad_actual FROM inventario WHERE id_producto = %s", (id,))
    result = cursor.fetchone()
    
    if result:
        cantidad_actual = result[0]
        if cantidad_actual >= cantidad:
            nueva_cantidad = cantidad_actual - cantidad
            cursor.execute(
                "UPDATE inventario SET cantidad_actual = %s WHERE id_producto = %s",
                (nueva_cantidad, id)
            )
            bd.commit()
            print(f"Se han eliminado {cantidad} KG de la fruta con ID {id}.")
        else:
            print("No hay suficiente cantidad en el inventario para eliminar.")
    else:
        print("La fruta no se encuentra en el inventario.")

# Ver inventario
def ver_inventario():
    cursor.execute("SELECT * FROM inventario")
    inventario = cursor.fetchall()
    print("\n--- Inventario Actual ---")
    for item in inventario:
        print(f"ID: {item[0]}, Cantidad Actual: {item[1]}, Fecha de Movimiento: {item[2]}, Cantidad Movida: {item[3]}")
    print("--------------------------")

# Menú principal
def main():
    while True:
        print("\n---    PECHENES    ---")
        print("\n--- Autenticación de Usuarios ---")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Elige una opción: ")
        if opcion == '2':
            iniciar_sesion()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

def gestionar_inventario():
    while True:
        print("\n*--- Inventario de Frutas ---*")
        print("1. +++++  Agregar fruta ++++++")
        print("2. +++++  Eliminar fruta ++++++")
        print("3. +++++  Ver inventario ++++++")
        print("4. ++++++++++ Salir ++++++++++")
        opcion = input("Elige una opción: ")
        if opcion == '1':
            agregar_fruta()
        elif opcion == '2':
            eliminar_fruta()
        elif opcion == '3':
            ver_inventario()
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == '__main__':
    main()

print("Fin del programa")
