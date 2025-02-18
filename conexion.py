import pymysql

try:
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="1097781666",
        database="sakila",
        port=3307
    )
    
    print("Conexión exitosa a la base de datos Sakila")
    conexion.close()
    print("Conexión cerrada")

except pymysql.MySQLError as err:
    print(f"Error: {err}")