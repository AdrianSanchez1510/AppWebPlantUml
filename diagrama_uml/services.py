import psycopg2
import pymysql
import pyodbc
import requests
from PIL import Image
from io import BytesIO
import zlib
import base64
import string
from zlib import compress

# Definir el alfabeto de PlantUML
plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = str.maketrans(base64_alphabet, plantuml_alphabet)

def conectar_base_datos(tipo_base_datos, host, puerto, usuario, password, nombre_base_datos):
    if tipo_base_datos == 'postgresql':
        conn = psycopg2.connect(
            host=host,
            port=puerto,
            user=usuario,
            password=password,
            dbname=nombre_base_datos
        )
    elif tipo_base_datos == 'mysql':
        conn = pymysql.connect(
            host=host,
            port=puerto,
            user=usuario,
            password=password,
            db=nombre_base_datos,
            charset='utf8mb4'
        )
    elif tipo_base_datos == 'sqlserver':
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host},{puerto};DATABASE={nombre_base_datos};UID={usuario};PWD={password}'
        )
    else:
        raise ValueError(f"Tipo de base de datos {tipo_base_datos} no soportado")
    
    return conn

def obtener_tablas_postgres_mysql(cursor):
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return cursor.fetchall()

def obtener_columnas_postgres_mysql(cursor, tabla):
    cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{tabla}'")
    return cursor.fetchall()

def obtener_tablas_sqlserver(cursor):
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'")
    return cursor.fetchall()

def obtener_columnas_sqlserver(cursor, tabla):
    cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{tabla}'")
    return cursor.fetchall()

def obtener_relaciones_postgres_mysql(cursor):
    cursor.execute("""
    SELECT
        tc.table_name, 
        kcu.column_name, 
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name
    FROM 
        information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
    WHERE constraint_type = 'FOREIGN KEY';
    """)
    return cursor.fetchall()

def obtener_relaciones_sqlserver(cursor):
    cursor.execute("""
    SELECT 
        fk.name AS fk_name, 
        tp.name AS table_name, 
        cp.name AS column_name, 
        tr.name AS foreign_table_name, 
        cr.name AS foreign_column_name
    FROM 
        sys.foreign_keys AS fk
        INNER JOIN sys.tables AS tp ON fk.parent_object_id = tp.object_id
        INNER JOIN sys.tables AS tr ON fk.referenced_object_id = tr.object_id
        INNER JOIN sys.foreign_key_columns AS fkc ON fk.object_id = fkc.constraint_object_id
        INNER JOIN sys.columns AS cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
        INNER JOIN sys.columns AS cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id;
    """)
    return cursor.fetchall()

def obtener_esquema(tipo_base_datos, host, puerto, usuario, password, nombre_base_datos):
    conn = conectar_base_datos(tipo_base_datos, host, puerto, usuario, password, nombre_base_datos)
    cursor = conn.cursor()

    if tipo_base_datos in ['postgresql', 'mysql']:
        tablas = obtener_tablas_postgres_mysql(cursor)
        columnas = {tabla[0]: obtener_columnas_postgres_mysql(cursor, tabla[0]) for tabla in tablas}
        relaciones = obtener_relaciones_postgres_mysql(cursor)
    elif tipo_base_datos == 'sqlserver':
        tablas = obtener_tablas_sqlserver(cursor)
        columnas = {tabla[0]: obtener_columnas_sqlserver(cursor, tabla[0]) for tabla in tablas}
        relaciones = obtener_relaciones_sqlserver(cursor)

    conn.close()
    return tablas, columnas, relaciones

def generar_codigo_plantuml(tablas, columnas, relaciones):
    codigo = "@startuml\n"
    
    # Definir tablas y columnas
    for tabla in tablas:
        codigo += f"class {tabla[0]} {{\n"
        for columna in columnas.get(tabla[0], []):
            codigo += f"  {columna[0]} : {columna[1]}\n"
        codigo += "}\n"
    
    # Definir relaciones (claves foráneas)
    for relacion in relaciones:
        codigo += f"{relacion[0]} --> {relacion[2]} : {relacion[1]} references {relacion[3]}\n"

    codigo += "@enduml"
    return codigo

def deflate_and_encode(plantuml_text):
    zlibbed_str = compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]  # Eliminar el encabezado de zlib y el final
    encoded = base64.b64encode(compressed_string).decode('utf-8')
    return encoded.translate(b64_to_plantuml)

def obtener_imagen_plantuml(codigo_plantuml):
    url_base = "http://www.plantuml.com/plantuml/png/"
    
    codigo_uml_codificado = deflate_and_encode(codigo_plantuml)
    
    url_completa = url_base + codigo_uml_codificado
    
    response = requests.get(url_completa)
    
    if response.status_code == 200 and response.headers['Content-Type'] == 'image/png':
        return response.content  # Devolver el contenido de la imagen en binario
    else:
        return None

def generar_diagrama_para_base_datos(tipo_base_datos, host, puerto, usuario, password, nombre_base_datos):
    tablas, columnas, relaciones = obtener_esquema(tipo_base_datos, host, puerto, usuario, password, nombre_base_datos)
    codigo_uml = generar_codigo_plantuml(tablas, columnas, relaciones)
    return obtener_imagen_plantuml(codigo_uml)
