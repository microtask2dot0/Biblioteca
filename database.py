import sqlite3 # Importo la biblioteca que maneja SQLite

NOMBRE_BD = "biblioteca.db"
DATABASE_VERSION = 2


def conectar():
     # Me conecto  a la base de datos biblioteca.db (si no existe, 
     #se crea)
    conexion = sqlite3.connect(NOMBRE_BD)

    # SQLite necesita que se activen explícitamente las claves foráneas
    # en cada conexión. Esto se hace con el comando 
    # PRAGMA foreign_keys = ON.
    conexion.execute("PRAGMA foreign_keys = ON") # Se le dice que compruebe las relaciones entre las tablas y que no permita insertar datos que violen esas relaciones. Esto es importante para mantener la integridad de los datos en la base de datos.
    
    return conexion

# Función para comrobar si la base de datos biblioteca.db existe y si no, crearla.
def crear_base_datos():
    # Me conecto  a la base de datos biblioteca.db (si no existe, se crea)
    # Creo la conexión a la base de datos llamando a la función conectar 
    # de la biblioteca database.py
    conexion = conectar()

    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

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
            FOREIGN KEY (item_id)
                REFERENCES items(id)
                ON DELETE CASCADE,

            FOREIGN KEY (dispositivo_id)
                REFERENCES dispositivos(id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_ubicaciones_unicas
        ON ubicaciones (item_id, dispositivo_id, ruta)
    """)

    actualizar_base_datos(conexion)
    conexion.commit()  # Guardo los cambios en la base de datos
    # Cierro la conexión a la base de datos
    conexion.close()

    print("Base de datos y tablas creadas correctamente (si no existían).")

def obtener_version_db(conexion):
    cursor = conexion.cursor()

    cursor.execute("PRAGMA user_version") # Con esta sentencia veo la actual versión de la base de datos.

    return cursor.fetchone()[0] # Con fetchone obtenemos sólo la primera fila y con [0] se obtiene el primer valor de esa fila.
                                # El método fetchmany(n) devuelve n filas y hasta 5 filas.

def establecer_version_db(conexion, version):
    cursor = conexion.cursor()

    cursor.execute(f"PRAGMA user_version = {version}")

def migrar_v1_a_v2(conexion):
    cursor = conexion.cursor()

    print("Actualizando la base de datos a la versión 2...")

    cursor.execute("""
        ALTER TABLE ubicaciones
        RENAME TO ubicaciones_antigua
    """)

    cursor.execute("""
        CREATE TABLE ubicaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            dispositivo_id INTEGER NOT NULL,
            ruta TEXT,
            FOREIGN KEY (item_id)
                REFERENCES items(id)
                ON DELETE CASCADE,
            FOREIGN KEY (dispositivo_id)
                REFERENCES dispositivos(id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        INSERT INTO ubicaciones (
            id,
            item_id,
            dispositivo_id,
            ruta
        )
        SELECT
            id,
            item_id,
            dispositivo_id,
            ruta
        FROM ubicaciones_antigua
    """)

    cursor.execute("""
        DROP TABLE ubicaciones_antigua
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_ubicaciones_unicas
        ON ubicaciones (item_id, dispositivo_id, ruta)
    """)

    conexion.commit()

    print("Base de datos actualizada correctamente.")

def actualizar_base_datos(conexion):
    version = obtener_version_db(conexion)

    if version < DATABASE_VERSION:
        if version == 1:
            migrar_v1_a_v2(conexion)

        establecer_version_db(conexion, DATABASE_VERSION)
