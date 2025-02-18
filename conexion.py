import pymysql
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Función para ejecutar una consulta y obtener los resultados
def ejecutar_consulta(query):
    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="1097781666",
            database="sakila",
            port=3307
        )

        print("Conexión exitosa a la base de datos Sakila")

        cursor = conexion.cursor()
        
        # Ejecutar la consulta
        cursor.execute(query)
        
        # Obtener los resultados
        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()
        
        return resultados

    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return []

# Consultas SQL
consulta_1 = """
SELECT 
    c.customer_id, 
    c.first_name || ' ' || c.last_name AS customer_name, 
    r.rental_id, 
    r.rental_date, 
    i.inventory_id, 
    f.film_id, 
    f.title, 
    fc.category_id
FROM customer c
INNER JOIN rental r ON c.customer_id = r.customer_id
INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
INNER JOIN film_category fc ON f.film_id = fc.film_id
WHERE r.rental_date BETWEEN '2005-06-01' AND '2005-07-01';
"""

# Función para obtener la ruta de la carpeta de Descargas
def obtener_ruta_descargas():
    # Para sistemas basados en Unix (Linux/MacOS)
    if os.name == 'posix':
        descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
    # Para sistemas Windows
    elif os.name == 'nt':
        descargas = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    return descargas

# Función para generar el PDF
def generar_pdf():
    # Obtener los datos de la consulta 1
    datos = ejecutar_consulta(consulta_1)
    
    # Verificar si hay resultados
    if not datos:
        messagebox.showinfo("Resultado", "No se encontraron resultados para esta consulta.")
        return
    
    # Obtener la ruta de la carpeta de Descargas
    ruta_descargas = obtener_ruta_descargas()
    
    # Ruta completa del archivo PDF
    pdf_file = os.path.join(ruta_descargas, "consulta_resultado.pdf")
    
    # Crear el archivo PDF
    pdf = canvas.Canvas(pdf_file, pagesize=letter)
    pdf.setFont("Helvetica", 10)
    
    # Título
    pdf.drawString(200, 750, "Resultados de la Consulta de Alquileres (Junio-Julio 2005)")
    
    # Escribir los datos en el PDF
    y_position = 730
    for fila in datos:
        texto = f"Customer ID: {fila[0]} | Customer Name: {fila[1]} | Rental ID: {fila[2]} | Rental Date: {fila[3]} | Inventory ID: {fila[4]} | Film ID: {fila[5]} | Title: {fila[6]} | Category ID: {fila[7]}"
        pdf.drawString(30, y_position, texto)
        y_position -= 15  # Para la siguiente fila

        # Si no cabe más en la página, añadir una nueva página
        if y_position < 100:
            pdf.showPage()
            y_position = 750
    
    # Guardar el PDF
    pdf.save()
    messagebox.showinfo("Éxito", f"PDF generado correctamente y guardado en: {pdf_file}")

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Generador de Reportes en PDF")

# Botón para generar el PDF
btn_generar_pdf = tk.Button(root, text="Generar PDF", command=generar_pdf)
btn_generar_pdf.pack(pady=20)

# Ejecutar la interfaz gráfica
root.mainloop()


