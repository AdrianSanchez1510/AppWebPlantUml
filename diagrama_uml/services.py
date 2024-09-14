def obtener_tablas(cursor, nombre_esquema):
    query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{nombre_esquema}'"
    cursor.execute(query)
    return cursor.fetchall()

def generar_codigo_plantuml(tablas, columnas):
    codigo = "@startuml\n"
    for tabla in tablas:
        codigo += f"class {tabla['nombre']} {{\n"
        for columna in columnas.get(tabla['nombre'], []):
            codigo += f"  {columna['nombre']} : {columna['tipo']}\n"
        codigo += "}\n"
    codigo += "@enduml"
    return codigo

def obtener_imagen_plantuml(codigo_plantuml):
    url_plantuml = "http://www.plantuml.com/plantuml/png/"
    response = requests.post(url_plantuml, data=codigo_plantuml)
    if response.status_code == 200:
        return response.url
    else:
        return None
