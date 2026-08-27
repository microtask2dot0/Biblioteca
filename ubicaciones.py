import sqlite3
from database import conectar
from items import obtener_items, seleccionar_item, formatear_item
from dispositivos import obtener_dispositivos
from utils import seleccionar_id, agrupar_por_tipo, pedir_entero, pedir_confirmacion
from models import Item, Ubicacion

def anadir_ubicacion():

    while True:
        print()
        print("¿Cómo quieres seleccionar el item?")
        print("1. Buscar por título")
        print("2. Mostrar todos")
        print("3. Volver")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "3":
            return

        if opcion == "1":
            titulo = input("Título del item: ").strip()

            if not titulo:
                print("Debes introducir un título.")
                continue

            items = obtener_items(titulo, "titulo")

        elif opcion == "2":
            items = obtener_items()

        else:
            print("Opción no válida.")
            continue

        if not items:
            print("No se encontraron items.")
            continue

        item_id = seleccionar_item(items)

        if item_id is None:
            continue

        break

    dispositivos = obtener_dispositivos()

    if not dispositivos:
        print("No hay dispositivos registrados.")
        return

    print()
    print("¿En qué dispositivo está?")

    dispositivo_id = seleccionar_id(
        dispositivos,
        "Selecciona el ID del dispositivo: "
    )

    while True:
        ruta = input("Ruta o ubicación: ").strip()

        if ruta:
            break

        print("Debes introducir una ruta o ubicación.")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO ubicaciones (
                item_id,
                dispositivo_id,
                ruta
            )
            VALUES (?, ?, ?)
        """, (item_id, dispositivo_id, ruta))

        conexion.commit()
        print("Ubicación añadida correctamente.")
    except sqlite3.IntegrityError:
        conexion.rollback()
        print("Error: Ya existe una ubicación con el mismo item, dispositivo y ruta.")
    finally: # si el INSERT funciona, si se produce IntegrityError o si ocurre otro error, la conexión se cierra.
        conexion.close()

def obtener_ubicaciones():
    conexion = conectar()
    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # Hago un select que me traiga el id de la tabla ubicaciones, el titulo del item de la tabla items, 
    # el nombre del dispositivo de la tabla dispositivos y la ruta de la tabla ubicaciones. Para esto 
    # hago un join entre las tablas ubicaciones, items y dispositivos.
    # cursor.execute("""
    #     SELECT u.id, i.titulo, d.nombre, u.ruta
    #     FROM ubicaciones u
    #     JOIN items i ON u.item_id = i.id
    #     JOIN dispositivos d ON u.dispositivo_id = d.id
    #     ORDER BY i.titulo, d.nombre
    # """)
    
    cursor.execute("""
        SELECT
        id,
        item_id,
        dispositivo_id,
        ruta
        FROM ubicaciones
        ORDER BY id
    """)

    filas = cursor.fetchall()
    conexion.close()

    ubicaciones = []

    for fila in filas:
        ubicacion = Ubicacion(
            fila[0],
            fila[1],
            fila[2],
            fila[3]
        )

        ubicaciones.append(ubicacion)

    return ubicaciones

def obtener_datos_ubicacion(ubicacion):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            i.titulo,
            d.nombre
        FROM ubicaciones u
        JOIN items i
            ON u.item_id = i.id
        JOIN dispositivos d
            ON u.dispositivo_id = d.id
        WHERE u.id = ?
    """, (ubicacion.id,))

    datos = cursor.fetchone()

    conexion.close()

    return datos

# def buscar_ubicaciones_por_item(item_id):
#     conexion = conectar()
#     cursor = conexion.cursor()

#     cursor.execute("""
#          SELECT u.id, d.nombre, u.ruta
#          FROM ubicaciones u
#          JOIN dispositivos d ON u.dispositivo_id = d.id
#          WHERE u.item_id = ?
#          ORDER BY d.nombre
#     """, (item_id,))

#     ubicaciones = cursor.fetchall()
#     conexion.close()

#     return ubicaciones

def buscar_ubicaciones_por_item(item_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            item_id,
            dispositivo_id,
            ruta
        FROM ubicaciones
        WHERE item_id = ?
        ORDER BY id
    """, (item_id,))

    filas = cursor.fetchall()
    conexion.close()

    ubicaciones = []

    for fila in filas:
        ubicacion = Ubicacion(
            fila[0],
            fila[1],
            fila[2],
            fila[3]
        )

        ubicaciones.append(ubicacion)

    return ubicaciones

def mostrar_ubicaciones():
    ubicaciones = obtener_ubicaciones()

    if not ubicaciones:
        print("No hay ubicaciones registradas.")
        return

    for ubicacion in ubicaciones:

        datos = obtener_datos_ubicacion(ubicacion)

        print(
            f"ID: {ubicacion.id}\n"
            f"Item: {datos[0]}\n"
            f"Dispositivo: {datos[1]}\n"
            f"Ruta: {ubicacion.ruta}\n"
            "-----------------------------"
        )

def donde_esta():
    while True:
        titulo = input("Ingrese el título del item que desea buscar: ").strip()

        if titulo:
            break
        print("El título no puede estar vacío. Por favor, inténtelo de nuevo.")

    items = obtener_items(titulo, "titulo")  # Llamo a la función obtener_items() para obtener los items que coincidan con el título introducido.   

    if not items:
        print("No se encontraron items con ese título.")
        return

    item_id = seleccionar_item(items)

    if item_id is None:
        return

    item_seleccionado = None

    for item in items:
        if item.id == item_id:
            item_seleccionado = item
            break

    print()
    print("Elemento seleccionado:")
    formatear_item(item_seleccionado)
    
    ubicaciones = buscar_ubicaciones_por_item(item_id)

    if not ubicaciones:
        print("Ese elemento no tiene ubicaciones registradas.")
        return

    print()
    print("Ubicaciones:")
    for ubicacion in ubicaciones:

        datos = obtener_datos_ubicacion(ubicacion)

        print(
            f"ID: {ubicacion.id}\n"
            f"Dispositivo: {datos[1]}\n"
            f"Ruta: {ubicacion.ruta}\n"
            "-----------------------------"
        )

def buscar_items_por_dispositivo(dispositivo_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            items.id,
            items.titulo,
            items.tipo,
            items.valoracion,
            items.genero,
            items.autor,
            items.notas,
            ubicaciones.id,
            ubicaciones.item_id,
            ubicaciones.dispositivo_id,
            ubicaciones.ruta
        FROM ubicaciones
        JOIN items
            ON ubicaciones.item_id = items.id
        WHERE ubicaciones.dispositivo_id = ?
        ORDER BY items.titulo
    """, (dispositivo_id,))

    filas = cursor.fetchall()
    conexion.close()
    resultados = []

    for fila in filas:
        item = Item(
            fila[0],
            fila[1],
            fila[2],
            fila[3],
            fila[4],
            fila[5],
            fila[6]
        )

        ubicacion = Ubicacion(
            fila[7],
            fila[8],
            fila[9],
            fila[10]
        )

    #item.ruta = fila[7]
    #resultados.append(item, ubicacion)
        resultados.append((item, ubicacion)) # El método append sólo admite un parámetro. Como queremos pasar dos parámetros (item y ubicacion), 
                                             # tengo que convertir estos dos parámetros en una tupla, por eso al método append se le pasa estos 
                                             # dos parámetros entre paréntesis.
    return resultados

def que_hay_en():
    dispositivos = obtener_dispositivos()
    dispositivos.sort(key=lambda dispositivo: dispositivo.id) # Ordeno los dispositivos por ID de forma ascendente.

    if not dispositivos:
        print("No hay dispositivos registrados.")
        return

    print()
    print("¿En qué dispositivo quieres buscar?")

    dispositivo_id = seleccionar_id(
        dispositivos,
        "Selecciona el ID del dispositivo: "
    )

    resultados = buscar_items_por_dispositivo(dispositivo_id)

    if not resultados:
        print("No hay elementos registrados en este dispositivo.")
        return

    grupos = {}

    for item, ubicacion in resultados:
        tipo = item.tipo.lower()

        if tipo not in grupos:
            grupos[tipo] = []

        grupos[tipo].append((item, ubicacion))

    print()

    for tipo, elementos in grupos.items():
        print(tipo.capitalize())

        for item, ubicacion in elementos:
            print(
                f"  ID: {item.id} | "
                f"{item.titulo} → {ubicacion.ruta}"
            )

        print()

# def buscar_items_por_dispositivo(dispositivo_id):
#     conexion = conectar()
#     cursor = conexion.cursor()

#     cursor.execute("""
#         SELECT
#             items.id,
#             items.titulo,
#             items.tipo,
#             items.valoracion,
#             items.genero,
#             items.autor,
#             items.notas,
#             ubicaciones.ruta
#         FROM ubicaciones
#         JOIN items
#             ON ubicaciones.item_id = items.id
#         WHERE ubicaciones.dispositivo_id = ?
#         ORDER BY items.titulo
#     """, (dispositivo_id,))

#     filas = cursor.fetchall()
#     conexion.close()
#     items = []

#     for fila in filas:
#         item = Item(
#             fila[0],
#             fila[1],
#             fila[2],
#             fila[3],
#             fila[4],
#             fila[5],
#             fila[6]
#         )

#     item.ruta = fila[7]
#     items.append(item)

#     return items

# def que_hay_en():
#     dispositivos = obtener_dispositivos()
#     dispositivos.sort(key=lambda dispositivo: dispositivo.id)  # Ordeno los dispositivos por ID de forma ascendente.

#     if not dispositivos:
#         print("No hay dispositivos registrados.")
#         return

#     print()
#     print("¿En qué dispositivo quieres buscar?")

#     dispositivo_id = seleccionar_id(
#         dispositivos,
#         "Selecciona el ID del dispositivo: "
#     )

#     resultados = buscar_items_por_dispositivo(dispositivo_id)

#     if not resultados:
#         print("No hay elementos registrados en este dispositivo.")
#         return

#     items = []
#     for item, ubicacion in resultados:
#         items.append(item)

#     grupos = agrupar_por_tipo(items)

#     print()

#     for tipo, elementos in grupos.items():
#         print(tipo.capitalize())

#         for elemento in elementos:
#             print(
#                 f"  ID: {elemento.id} | "
#                 f"{elemento.titulo} → {ubicacion.ruta}"
#             )
#             break

#         print()

# def seleccionar_ubicacion(ubicaciones):
#     if not ubicaciones:
#         return None

#     ids_disponibles = []

#     print()

#     for ubicacion in ubicaciones:
#         ids_disponibles.append(ubicacion[0])

#         print(
#             f"ID: {ubicacion[0]} | "
#             f"Dispositivo: {ubicacion[1]} | "
#             f"Ruta: {ubicacion[2]}"
#         )

#     while True:
#         ubicacion_id = pedir_entero(
#             "Selecciona el ID de la ubicación: "
#         )

#         if ubicacion_id in ids_disponibles:
#             return ubicacion_id

#         print("El ID seleccionado no existe.")

def seleccionar_ubicacion(ubicaciones):
    if not ubicaciones:
        return None

    ids_disponibles = []

    print()

    for ubicacion in ubicaciones:
        datos = obtener_datos_ubicacion(ubicacion)

        ids_disponibles.append(ubicacion.id)

        print(
            f"ID: {ubicacion.id} | "
            f"Dispositivo: {datos[1]} | "
            f"Ruta: {ubicacion.ruta}"
        )

    while True:
        ubicacion_id = pedir_entero(
            "Selecciona el ID de la ubicación: "
        )

        if ubicacion_id in ids_disponibles:
            return ubicacion_id

        print("El ID seleccionado no existe.")

def borrar_ubicacion(ubicacion_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM ubicaciones
        WHERE id = ?
    """, (ubicacion_id,))

    conexion.commit()
    conexion.close()

def eliminar_ubicacion():

    item_id = seleccionar_item()

    if item_id is None:
        return

    ubicaciones = buscar_ubicaciones_por_item(item_id)

    if not ubicaciones:
        print("Ese elemento no tiene ubicaciones registradas.")
        return

    ubicacion_id = seleccionar_ubicacion(ubicaciones)

    if ubicacion_id is None:
        return

    if not pedir_confirmacion(
        "¿Seguro que quieres eliminar esta ubicación? (s/n): "
    ):
        print("Operación cancelada.")
        return

    borrar_ubicacion(ubicacion_id)

    print("Ubicación eliminada correctamente.")