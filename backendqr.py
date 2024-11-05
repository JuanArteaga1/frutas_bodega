#Importar la libreria de Google
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from flask import Flask, request, jsonify,send_from_directory

#Crear el servidor de Google
import mysql.connector
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

# Configuración de la conexión
app = Flask(__name__)
bd = mysql.connector.connect(
    user="root",
    password="133724",
    host="localhost",
    database="administracion_bodega"
)
cursor = bd.cursor()

# Autenticación con Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'ivory-amphora-436523-h5-3835099dbf3e.json'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

def datos(id):
    cursor.execute("SELECT nombre, origen, precio FROM productos WHERE id_producto = %s", (id,))
    resultado = cursor.fetchone()
    resultado  # Comprueba si se obtuvo algún resultado
    nombre, origen, precio = resultado
    return nombre, origen, precio 
    

def agregar_texto_a_pdf(pdf_path, output_path, nombre, x, y, origen, xx, yy, precio=None, xxx=None, yyy=None, cantidad=None, xxxx=None, yyyy=None):
    # Leer el PDF existente
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Crear un nuevo PDF en memoria
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(x, y, nombre)
    can.drawString(xx, yy, origen)
    
    # Solo dibujar el precio si no es None
    if precio is not None and xxx is not None and yyy is not None:
        can.drawString(xxx, yyy, precio)
    
    # Solo dibujar la cantidad si no es None
    if cantidad is not None and xxxx is not None and yyyy is not None:
        can.drawString(xxxx, yyyy, cantidad)
    
    can.save()

    # Mover a la posición del inicio del buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Combinar el PDF existente con el nuevo PDF
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        if i == 0:  # Solo agregar texto a la primera página
            page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    # Guardar el nuevo PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)


def subir_a_drive(filepath, filename):
    file_metadata = {
        'name': filename,
        'mimeType': 'application/pdf',
        'parents': ['1SE_XkndZNtQnsvRunKBD4yi3cC1MJwDw']  # Asegúrate de que sea la ID correcta
    }
    media = MediaFileUpload(filepath, mimetype='application/pdf')
    try:
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        link = {file.get('webViewLink')}
        return link
    except HttpError as error:
        print(f"Ocurrió un error al subir el archivo a Google Drive: {error}")


@app.route('/main', methods=['POST'])
def main():
    dato = request.json 
    print("entro")
    opcion = dato.get('opcion')
    nombre1, origen1, precio1 = datos(dato.get('base'))
    # Archivo para almacenar el contador
    contador_path = "contador.txt"
    # Leer el contador desde el archivo o inicializarlo
    if os.path.exists(contador_path):
        with open(contador_path, "r") as f:
            contenido = f.read().strip()
            # Verificar si el contenido es un número válido
            if contenido.isdigit():
                contador = int(contenido)
            else:
                contador = 0  # Inicializa el contador si el contenido no es válido
        
        nombre1, origen1, precio1 = datos()
        
    if opcion == '1':
        pdf_path = "D:\\git proyectos\\frutas-bodega\\entrada\\INFORME DE ENTRADA.pdf"
        # Variables para INFORME DE ENTRADA
        nombre = nombre1
        x = 210
        y = 602
        origen = origen1
        xx = 210
        yy = 540
        precio = str(precio1)
        xxx = 210
        yyy = 478
        cantidad = "60"
        xxxx = 215
        yyyy = 417

    elif opcion == "2":
        pdf_path = "D:\\git proyectos\\frutas-bodega\salida\\INFORME DE SALIDA.pdf"
        # Variables para INFORME DE SALIDA
        nombre = nombre1
        x = 210
        y = 602
        origen = origen1
        xx = 210
        yy = 540
        cantidad = "60"
        xxxx = 210
        yyyy = 478
        precio = None  # No se utiliza en el informe de salida
        xxx, yyy = (None, None)  # No se usarán

    else:
        print("Opción no válida.")

    # Generar el nuevo PDF
    contador += 1
    output_path = f"D:\\git proyectos\\frutas-bodega\\ {'entrada' if opcion == '1' else 'salida'} ({contador}).pdf"
    agregar_texto_a_pdf(pdf_path, output_path, nombre, x, y, origen, xx, yy, precio, xxx, yyy, cantidad, xxxx, yyyy)

    # Guardar el nuevo contador
    with open(contador_path, "w") as f:
        f.write(str(contador))

    print(f"PDF generado: {output_path}\n")
    # Subir el PDF generado a Google Drive
    link = subir_a_drive(output_path, f"INFORME DE {'ENTRADA' if opcion == '1' else 'SALIDA'} ({contador}).pdf")
    return jsonify({link})


if __name__ == '__main__':
    app.run(debug=True) 