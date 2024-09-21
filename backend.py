import mysql.connector
import datetime
#si sale error  instalar "pip install mysql-connector-python" en la terminal
bd = mysql.connector.connect(
    user="root",
    password="133724",
    host="localhost",
    database="administracion_bodega"


)
cursor = bd.cursor()
cursor.execute("select * from jerarquias")
result = cursor.fetchall()

for jerarquias in result:
    print(jerarquias)

def iniciar_sesion():
    nombre_usuario = input("Ingresa tu nombre de usuario: ")
    contraseña = input("Ingresa tu contraseña: ")
    agregar_fruta()



# Agregar fruta
def agregar_fruta():
    
    id = 1#input("ingrese id: ")
    fruta = "pera" #input("Ingresa el nombre de la fruta: ")
    origen = "pasto"#input("ingrese de donde viene la fruta: ")
    precio = 1200#input("ingrese el precio de la fruta: ")
    cantidad = 12#int(input("Ingresa la cantidad en KG: "))
    fecha_hoy = datetime.date.today()
    cursor.execute(
        "INSERT INTO productos (id_producto, nombre, precio, origen) VALUES (%s, %s, %s, %s)",
        (id, fruta, precio, origen)
    )
    cursor.execute(
        "INSERT INTO inventario (id_producto, cantidad_actual, fecha_movimiento, cantidad_movimiento) VALUES (%s, %s, %s, %s)",
        (id, cantidad, fecha_hoy, cantidad)
    )
    bd.commit()

    print(f"Se han agregado {cantidad} KG {fruta}(s) al inventario.")

# Eliminar fruta
def eliminar_fruta():
    id = input("ingrese id: ")
    fruta = input("Ingresa el nombre de la fruta: ")
    cantidad = int(input("Ingresa la cantidad a eliminar en KG: "))


# Ver inventario
def ver_inventario():
    return 0

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
        print("2. +++++ sacar fruta ++++++")
        print("3. +++++ Ver inventario ++++++")
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
    


