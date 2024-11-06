# Importar las librerías necesarias
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import mysql.connector
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from googleapiclient.errors import HttpError
import io
import os

# Configuración de la conexión a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        user="root",
        password="123456789",
        host="localhost",
        database="administracion_bodega"
    )

# Configuración de Google Drive
def autenticar_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = 'ivory-amphora-436523-h5-3835099dbf3e.json'
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

# Obtener datos del producto
def obtener_datos_producto(cursor, producto_id=10):
    cursor.execute("SELECT nombre, origen, precio FROM productos WHERE id_producto = %s", (producto_id,))
    resultado = cursor.fetchone()
    return resultado if resultado else (None, None, None)

# Agregar texto a un PDF
def agregar_texto_a_pdf(pdf_path, output_path, nombre, x, y, origen, xx, yy, precio=None, xxx=None, yyy=None, cantidad=None, xxxx=None, yyyy=None):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(x, y, nombre)
    can.drawString(xx, yy, origen)
    
    if precio is not None and xxx is not None and yyy is not None:
        can.drawString(xxx, yyy, precio)
    if cantidad is not None and xxxx is not None and yyyy is not None:
        can.drawString(xxxx, yyyy, cantidad)
    
    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        if i == 0:
            page.merge_page(new_pdf.pages[0])
        writer.add_page(page)
    
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

# Seleccionar plantilla
def seleccionar_plantilla():
    print("Seleccione una plantilla:")
    print("1. INFORME DE ENTRADA")
    print("2. INFORME DE SALIDA")
    print("3. Salir")
    return input("Ingrese el número de la opción deseada (1, 2 o 3): ")

# Subir PDF a Google Drive
def subir_a_drive(drive_service, filepath, filename):
    file_metadata = {
        'name': filename,
        'mimeType': 'application/pdf',
        'parents': ['1SE_XkndZNtQnsvRunKBD4yi3cC1MJwDw']
    }
    media = MediaFileUpload(filepath, mimetype='application/pdf')
    try:
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        print(f"Archivo '{filename}' subido a Google Drive con ID: {file.get('id')}")
        print(f"Link de visualización: {file.get('webViewLink')}")
    except HttpError as error:
        print(f"Ocurrió un error al subir el archivo a Google Drive: {error}")

# Cargar el contador o inicializarlo
def cargar_contador(contador_path):
    if os.path.exists(contador_path):
        with open(contador_path, "r") as f:
            contenido = f.read().strip()
            return int(contenido) if contenido.isdigit() else 0
    return 0

# Guardar el contador actualizado
def guardar_contador(contador_path, contador):
    with open(contador_path, "w") as f:
        f.write(str(contador))

# Programa principal
def main():
    bd = conectar_bd()
    cursor = bd.cursor()
    drive_service = autenticar_drive()
    contador_path = "contador.txt"
    contador = cargar_contador(contador_path)

    while True:
        opcion = seleccionar_plantilla()
        if opcion == "3":
            print("Saliendo del programa...")
            break

        nombre1, origen1, precio1 = obtener_datos_producto(cursor)
        if not nombre1:
            print("No se encontró el producto especificado.")
            continue

        pdf_path, nombre, x, y, origen, xx, yy, precio, xxx, yyy, cantidad, xxxx, yyyy = '', nombre1, 210, 602, origen1, 210, 540, None, None, None, None, None

        if opcion == "1":
            pdf_path = "C:\\Users\\danyr\\Documents\\Universidad\\Codigo_Qr\\INFORME DE ENTRADA.pdf"
            precio, xxx, yyy = str(precio1), 210, 478
            cantidad, xxxx, yyyy = "60", 215, 417
        elif opcion == "2":
            pdf_path = "C:\\Users\\danyr\\Documents\\Universidad\\Codigo_Qr\\INFORME DE SALIDA.pdf"
            cantidad, xxxx, yyyy = "60", 210, 478

        contador += 1
        output_path = f"C:\\Users\\danyr\\Documents\\Universidad\\Codigo_Qr\\INFORME DE {'ENTRADA' if opcion == '1' else 'SALIDA'} ({contador}).pdf"
        agregar_texto_a_pdf(pdf_path, output_path, nombre, x, y, origen, xx, yy, precio, xxx, yyy, cantidad, xxxx, yyyy)

        guardar_contador(contador_path, contador)
        print(f"PDF generado: {output_path}\n")

        subir_a_drive(drive_service, output_path, f"INFORME DE {'ENTRADA' if opcion == '1' else 'SALIDA'} ({contador}).pdf")

if __name__ == "__main__":
    main()
