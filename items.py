from database import conectar
from utils import pedir_entero, normalizar_texto, pedir_confirmacion
from models import Item

def pedir_valoracion():
    while True:
        valor = input("Valoración (0-5): ")

        try:
            valor = int(valor)
        except ValueError:
            print("La valoración debe ser un número.")
            continue

        if 0 <= valor <= 5:
            return valor

        print("La valoración debe estar entre 0 y 5.")

# Función para añadir un registro a la tabla items
def anadir_item():

    # Creo la conexión a la base de datos llamando a la función conectar 
    # de la biblioteca database.py
    conexion = conectar()

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # Solicito al usuario que ingrese los datos del nuevo item.

    while True:
        titulo = input("Ingrese el título: ").strip()
        if titulo:
            break

        print("El título es obligatorio.")

    while True:
        tipo = normalizar_texto(
            input("Ingrese el tipo (Libro, Revista, etc.): ")
        )

        if tipo:
            break

        print("El tipo es obligatorio.")

    valoracion = pedir_valoracion()
    genero = normalizar_texto(input("Ingrese el género: "))
    autor = input("Ingrese el autor: ").strip()
    notas = input("Ingrese las notas: ").strip()

    # Inserto el nuevo item en la tabla items.
    # Esto se hace así (sin añadir directamente en VALUES los datos introducidos por el usuario) porque es imortante hacerlo así.
    cursor.execute("""INSERT INTO items (titulo, tipo, valoracion, genero, autor, notas) VALUES (?, ?, ?, ?, ?, ?)""", (titulo, tipo, valoracion, genero, autor, notas))
    conexion.commit()  # Guardo los cambios en la base de datos
    conexion.close() # Cierro la conexión
    print("Item añadido correctamente.")

def obtener_items(texto=None, campo=None): # Con texto=None hago que el parámetro texto sea opcional. Si no se pasa ningún valor, será None por defecto. 
                                           # El argumento campo sirve para decir por cuál de los campos se quiere hacer la búsqueda. Si no se pasa ningún valor, será None por defecto y se buscará en todos los campos.

    # Creo la conexión a la base de datos llamando a la función conectar 
    # de la biblioteca database.py
    conexion = conectar()

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # Como en SQL no se puede usar un parámetro para indicar el nombre 
    # de una columna, hago un diccionario que me permita mapear 
    # los nombres de los campos permitidos a los nombres de las 
    # columnas de la tabla items.
    campos_permitidos = {
        "titulo": "titulo",
        "tipo": "tipo",
        "genero": "genero",
        "autor": "autor",
        "notas": "notas"
    }

    if texto and campo in campos_permitidos:

        texto = f"%{texto.strip()}%"
        columna = campos_permitidos[campo]

        cursor.execute(f"""
            SELECT
                id,
                titulo,
                tipo,
                valoracion,
                genero,
                autor,
                notas
            FROM items
            WHERE {columna} LIKE ?
            ORDER BY titulo
        """, (texto,))

    elif texto:

        texto = f"%{texto.strip()}%"

        cursor.execute("""
            SELECT
                id,
                titulo,
                tipo,
                valoracion,
                genero,
                autor,
                notas
            FROM items
            WHERE titulo LIKE ?
               OR tipo LIKE ?
               OR genero LIKE ?
               OR autor LIKE ?
               OR notas LIKE ?
            ORDER BY titulo
        """, (texto, texto, texto, texto, texto))

    else:
        cursor.execute("""
            SELECT
                id,
                titulo,
                tipo,
                valoracion,
                genero,
                autor,
                notas
            FROM items
            ORDER BY titulo
        """)

    #items = cursor.fetchall() # Con cursor.fetchall() obtengo todos los registros de la consulta y los guardo en la variable items. 
    
    filas = cursor.fetchall()
    conexion.close()

    items = []

    for fila in filas:
        # Lo siguiente que hago es convertir el registro obtenido y que se ha guardado en la tupla llamada filas en un objeto llamado item.
        # Cuando se leen los registros en SQLite, estos se devuelve en tuplas y para que se puedan pasar sus datos a un objeto 
        # hay que hacerlo así.
        item = Item(
            fila[0],
            fila[1],
            fila[2],
            fila[3],
            fila[4],
            fila[5],
            fila[6]
        )

        items.append(item)

    return items

def obtener_item_por_id(item_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            titulo,
            tipo,
            valoracion,
            genero,
            autor,
            notas
        FROM items
        WHERE id = ?
    """, (item_id,))

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        return None

    # En el return convierto el registro obtenido y que se ha guardado en la tupla llamada fila en un objeto llamado item.
    # Cuando se leen los registros en SQLite, estos se devuelve en tuplas y para que se puedan pasar sus datos a un objeto 
    # hay que hacerlo así.
    return Item(
        fila[0],
        fila[1],
        fila[2],
        fila[3],
        fila[4],
        fila[5],
        fila[6]
    )

def formatear_item(item):
    print(
        f"ID: {item.id}\n"
        f"Título: {item.titulo}\n"
        f"Tipo: {item.tipo}\n"
        f"Valoración: {item.valoracion}\n"
        f"Género: {item.genero}\n"
        f"Autor: {item.autor}\n"
        f"Notas: {item.notas}\n"
        "-----------------------------"
    )

# Función para mostrar todos los registros de la tabla items
def mostrar_items():
    items = obtener_items() # Llamo a la función obtener_items() para obtener todos los items de la base de datos.

    if not items:
        print("No hay items registrados.")
        return

    for item in items:
        formatear_item(item)

def buscar_items():
    
    campos = {
        "1": "titulo",
        "2": "tipo",
        "3": "genero",
        "4": "autor",
        "5": "notas"
    }

    while True:
        print()
        print("¿Qué quieres hacer?")
        print("1. Buscar por título")
        print("2. Buscar por tipo")
        print("3. Buscar por género")
        print("4. Buscar por autor")
        print("5. Buscar por notas")
        print("6. Buscar en todos los campos")
        print("7. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "7":
            return

        if opcion not in campos and opcion != "6":
            print("Opción no válida.")
            continue

        texto = input("¿Qué quieres buscar? ").strip()

        if not texto:
            print("Debes introducir algo para buscar.")
            continue

        if opcion == "6":
            items = obtener_items(texto) # He añadido por mi cuenta que la llamada a la función obtener_items() reciba el texto introducido
            # por el usuario para que busque los items que contengan ese texto en el título y así conseguir que se pueda usar la función obtener_items
            # para obtener datos sin WHERE o con WHERE en el SELECT.
        else:
            items = obtener_items(texto, campos[opcion]) # En este caso en vez de buscar el texto en cualquier caso, como ocurre
            # en la llamada a la función obtener_items() anterior, aquí se busca el texto en el campo que el usuario ha seleccionado.
        
        if not items:
            print("No se encontraron resultados.")
            continue

        print()
        print(f"\nSe encontraron {len(items)} resultados.")
        print()
        print("Resultados:")

        for item in items:
            formatear_item(item)

def seleccionar_item(items=None):
    if items is None:
        items = obtener_items()

    if not items:
        print("No hay items registrados.")
        return None

    ids_disponibles = []

    items.sort(key=lambda item: item.id)  # Ordeno los items por ID de forma ascendente.
        
    print()
    
    for item in items:
        ids_disponibles.append(item.id)
        print(
            f"ID: {item.id} | "
            f"Título: {item.titulo} | "
            f"Tipo: {item.tipo} | "
            f"Autor: {item.autor or 'Sin autor'}"
        )

    while True:
        item_id = pedir_entero("Selecciona el ID del elemento: ")

        if item_id in ids_disponibles:
            return item_id

        print("El ID seleccionado no existe.")
        print(f"IDs disponibles: {', '.join(map(str, ids_disponibles))}") # Se mostraría 1, 2, 3, 4, 5  si esos fueran los IDs disponibles.
        # La función map() se utiliza para aplicar la función str() a cada elemento de la lista ids_disponibles, convirtiendo cada ID en una cadena de texto.
        # Luego, la función join() se utiliza para unir todas las cadenas de texto resultantes en una sola cadena, separadas por comas y espacios. 

def borrar_item(item_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM items
        WHERE id = ?
    """, (item_id,))

    conexion.commit()
    conexion.close()

def eliminar_item():

    item_id = seleccionar_item()

    if item_id is None:
        return

    item = obtener_item_por_id(item_id)

    if item is None:
        print("El item no existe.")
        return

    print()
    print("Item seleccionado:")
    formatear_item(item)

    if not pedir_confirmacion(
        "¿Seguro que quieres eliminar este item? (s/n): "
    ):
        print("Operación cancelada.")
        return

    borrar_item(item_id)

    print("Item eliminado correctamente.")
