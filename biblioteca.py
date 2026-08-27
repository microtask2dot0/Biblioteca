# Indico que voy a usar SQLite
from database import conectar

# Creo la conexión a la base de datos llamando a la función conectar 
# de la biblioteca database.py
conexion = conectar()
# Función para comrobar si la base de datos biblioteca.db existe y si no, crearla.
def crear_base_datos():
    # Me conecto  a la base de datos biblioteca.db (si no existe, se crea)
    conexion = sqlite3.connect("biblioteca.db")

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # SQLite necesita que se activen explícitamente las claves foráneas en cada conexión. Esto se hace con el comando PRAGMA foreign_keys = ON.
    cursor.execute("PRAGMA foreign_keys = ON") # Se le dice que compruebe las relaciones entre las tablas y que no permita insertar datos que violen esas relaciones. Esto es importante para mantener la integridad de los datos en la base de datos.

    # Si la tablas items, dispositivos y ubicaciones no existen, las creo. Con el método execute() puedo ejecutar comandos SQL. 
    # En este caso, creo la tablas:
    # items con los campos id, titulo y tipo, valoracion, genero, autor y notas
    # dispositivos con los campos id, nombre y tipo
    # ubicaciones con los campos id, item_id, dispositivo_id y ruta. Además, establezco las claves foráneas para que item_id haga referencia a id de la tabla items y dispositivo_id haga referencia a id de la tabla dispositivos.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valoracion INTEGER DEFAULT 0,
            genero TEXT,
            autor TEXT,
            notas  TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    #  FOREIGN KEY (item_id) REFERENCES items(id) y  FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id) son claves foráneas 
    # que establecen una relación entre la tabla ubicaciones y las tablas items y dispositivos. Esto significa que cada registro 
    # en la tabla ubicaciones debe tener un item_id que exista en la tabla items y un dispositivo_id que exista en la tabla dispositivos.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ubicaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            dispositivo_id INTEGER NOT NULL,
            ruta TEXT,
            FOREIGN KEY (item_id) REFERENCES items(id),
            FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id)
        )
    """)

    conexion.commit()  # Guardo los cambios en la base de datos
    # Cierro la conexión a la base de datos
    conexion.close()

    print("Base de datos y tablas creadas correctamente (si no existían).")

def menu():
    #  Creo un bucle que muestra indefinidamente el menú hasta que el usuario decida salir.
    while True:
        print("\nMi biblioteca:")
        print("\n1. Añadir elemento")
        print("2. Mostrar biblioteca")
        print("3. Buscar elemento")
        print("4. Añadir dispositivo")
        print("5. Mostrar dispositivos")
        print("6. Añadir ubicación")
        print("7. Mostrar ubicaciones")
        print("8. Salir")
        opcion = input("¿Qué quieres hacer? (1/2/3/4/5/6/7/8): ")

        if opcion == "1":
            anadir_item()
        elif opcion == "2":
            mostrar_items()
        elif opcion == "3":
            buscar_items()
        elif opcion == "4":
            anadir_dispositivo()
        elif opcion == "5":
            mostrar_dispositivos()
        elif opcion == "6":
            anadir_ubicacion()
        elif opcion == "7":
            mostrar_ubicaciones()
        elif opcion == "8":
            print("Hasta luego!")
            # Salgo del bucle
            break
        else:
            print("Opción no válida. Intente de nuevo.")

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

# Función para mostrar todos los registros de la tabla items
def mostrar_items():
    # Me conecto  a la base de datos biblioteca.db (si no existe, se crea)
    conexion = sqlite3.connect("biblioteca.db")

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # SQLite necesita que se activen explícitamente las claves foráneas en cada conexión. Esto se hace con el comando PRAGMA foreign_keys = ON.
    cursor.execute("PRAGMA foreign_keys = ON")

    # Leo todos los registros de la tabla items y los imprimo en pantalla.
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall() # Con cursor.fetchall() obtengo todos los registros de la consulta y los guardo en la variable items. 
    # Se imprime en pantalla la lista de tuplas con los registros de la tabla items.
    for item in items:
        print(f"ID: {item[0]}, Título: {item[1]}, Tipo: {item[2]},  Valoración: {item[3]}, Género: {item[4]}, Autor: {item[5]}, Notas: {item[6]}" )

# Función para añadir un registro a la tabla items
def anadir_item():
    # Me conecto  a la base de datos biblioteca.db (si no existe, se crea)
    conexion = sqlite3.connect("biblioteca.db")

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # SQLite necesita que se activen explícitamente las claves foráneas en cada conexión. Esto se hace con el comando PRAGMA foreign_keys = ON.
    cursor.execute("PRAGMA foreign_keys = ON")

    # Solicito al usuario que ingrese los datos del nuevo item.
    titulo = input("Ingrese el título: ")
    tipo = input("Ingrese el tipo (Libro, Revista, etc.): ")
    #dispositivo = input("Ingrese el dispositivo donde se encuentra el item (Kindle, PC, etc.): ")
    valoracion = pedir_valoracion()
    genero = input("Ingrese el género: ")
    autor = input("Ingrese el autor: ")
    notas = input("Ingrese las notas: ")

    # Inserto el nuevo item en la tabla items.
    # Esto se hace así (sin añadir directamente en VALUES los datos introducidos por el usuario) porque es imortante hacerlo así.
    #cursor.execute("""INSERT INTO items (titulo, tipo, dispositivo, valoracion, genero, autor, notas) VALUES (?, ?, ?, ?, ?, ?, ?)""", (titulo, tipo, dispositivo, valoracion, genero, autor, notas))
    cursor.execute("""INSERT INTO items (titulo, tipo, valoracion, genero, autor, notas) VALUES (?, ?, ?, ?, ?, ?)""", (titulo, tipo, valoracion, genero, autor, notas))
    conexion.commit()  # Guardo los cambios en la base de datos
    print("Item añadido correctamente.")

def buscar_items():
    texto = input("¿Qué quieres buscar? ")

    conexion = sqlite3.connect("biblioteca.db")

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # SQLite necesita que se activen explícitamente las claves foráneas en cada conexión. Esto se hace con el comando PRAGMA foreign_keys = ON.
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("SELECT * FROM items WHERE titulo LIKE ?", ('%' + texto + '%',))
    resultados = cursor.fetchall()
    conexion.close()

    for item in resultados:
        print(f"ID: {item[0]}, Título: {item[1]}, Tipo: {item[2]},  Valoración: {item[3]}, Género: {item[4]}, Autor: {item[5]}, Notas: {item[6]}")

def anadir_dispositivo():
    conexion = sqlite3.connect("biblioteca.db")

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # SQLite necesita que se activen explícitamente las claves foráneas en cada conexión. Esto se hace con el comando PRAGMA foreign_keys = ON.
    cursor.execute("PRAGMA foreign_keys = ON")

    nombre = input("Ingrese el nombre del dispositivo: ")
    tipo = input("Ingrese el tipo de dispositivo (eReader, PC, etc.): ")

    cursor.execute("""INSERT INTO dispositivos (nombre, tipo) VALUES (?, ?)""", (nombre, tipo))
    conexion.commit()
    conexion.close()
    print("Dispositivo añadido correctamente.")

def mostrar_dispositivos():
    conexion = sqlite3.connect("biblioteca.db")

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # SQLite necesita que se activen explícitamente las claves foráneas en cada conexión. Esto se hace con el comando PRAGMA foreign_keys = ON.
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("SELECT * FROM dispositivos")
    dispositivos = cursor.fetchall()
    conexion.close()

    for dispositivo in dispositivos:
        print(f"ID: {dispositivo[0]}, Nombre: {dispositivo[1]}, Tipo: {dispositivo[2]}")

    conexion.close()

def anadir_ubicacion():
    conexion = sqlite3.connect("biblioteca.db")

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # SQLite necesita que se activen explícitamente las claves foráneas en cada conexión. Esto se hace con el comando PRAGMA foreign_keys = ON.
    cursor.execute("PRAGMA foreign_keys = ON")

    item_id = input("Ingrese el ID del item: ")
    dispositivo_id = input("Ingrese el ID del dispositivo: ")
    ruta = input("Ingrese la ruta del item en el dispositivo: ")

    cursor.execute("""INSERT INTO ubicaciones (item_id, dispositivo_id, ruta) VALUES (?, ?, ?)""", (item_id, dispositivo_id, ruta))
    conexion.commit()
    conexion.close()
    print("Ubicación añadida correctamente.")

def mostrar_ubicaciones():
    conexion = sqlite3.connect("biblioteca.db")

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # SQLite necesita que se activen explícitamente las claves foráneas en cada conexión. Esto se hace con el comando PRAGMA foreign_keys = ON.
    cursor.execute("PRAGMA foreign_keys = ON")

    # Hago un select que me traiga el id de la tabla ubicaciones, el titulo del item de la tabla items, 
    # el nombre del dispositivo de la tabla dispositivos y la ruta de la tabla ubicaciones. Para esto 
    # hago un join entre las tablas ubicaciones, items y dispositivos.
    cursor.execute("""
        SELECT u.id, i.titulo, d.nombre, u.ruta
        FROM ubicaciones u
        JOIN items i ON u.item_id = i.id
        JOIN dispositivos d ON u.dispositivo_id = d.id
    """)
    ubicaciones = cursor.fetchall()
    conexion.close()

    for ubicacion in ubicaciones:
        print(f"ID: {ubicacion[0]}, Título del item: {ubicacion[1]}, Nombre del dispositivo: {ubicacion[2]}, Ruta: {ubicacion[3]}")

crear_base_datos()  # Llamo a la función crear_base_datos() para crear la base de datos y la tabla items si no existen.

menu()  # Llamo a la función menu() para mostrar el menú de opciones al usuario.    
