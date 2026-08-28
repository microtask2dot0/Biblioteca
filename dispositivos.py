from database import conectar
from utils import seleccionar_id, pedir_confirmacion
from models import Dispositivo

def anadir_dispositivo():
    conexion = conectar()
    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    while True:
        nombre = input("Ingrese el nombre del dispositivo: ").strip()

        if nombre:
            break

        print("El nombre del dispositivo es obligatorio.")

    while True:
        tipo = input("Ingrese el tipo de dispositivo (eReader, PC, etc.): ").strip()

        if tipo:
            break

        print("El tipo de dispositivo es obligatorio.")

    cursor.execute("""INSERT INTO dispositivos (nombre, tipo) VALUES (?, ?)""", (nombre, tipo))
    conexion.commit()
    conexion.close()
    print("Dispositivo añadido correctamente.")

# Siempre conviene separar la lógica de la base de datos de la lógica de la interfaz de usuario. Por eso, en lugar de mostrar 
# los dispositivos directamente en la función mostrar_dispositivos(), he creado una función separada llamada obtener_dispositivos() 
# que se encarga de recuperar los datos de la base de datos y devolverlos a la función mostrar_dispositivos(). 
# Esto permite que la función mostrar_dispositivos()  se enfoque únicamente en la presentación de los datos, mientras que la función 
# obtener_dispositivos() se encarga de la interacción con la base de datos.
# Esto hace que el código sea más modular y fácil de mantener.

def obtener_dispositivos():
    conexion = conectar()
    # Creo un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM dispositivos ORDER BY nombre")
    filas = cursor.fetchall()
    
    conexion.close()

    dispositivos = []

    for fila in filas:
        dispositivo = Dispositivo(
            fila[0],
            fila[1],
            fila[2]
        )

        dispositivos.append(dispositivo)

    return dispositivos

def mostrar_dispositivos():
    dispositivos = obtener_dispositivos()
    
    if not dispositivos:
        print("No hay dispositivos registrados.")
        return

    for dispositivo in dispositivos:
        print(dispositivo)
        print("________________________")
        print()

def borrar_dispositivo(dispositivo_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM dispositivos
        WHERE id = ?
    """, (dispositivo_id,))

    conexion.commit()
    conexion.close()

def eliminar_dispositivo():
    dispositivos = obtener_dispositivos()

    if not dispositivos:
        print("No hay dispositivos registrados.")
        return

    print()
    print("Dispositivos:")

    dispositivo_id = seleccionar_id(
        dispositivos,
        "Selecciona el ID del dispositivo: "
    )

    if dispositivo_id is None:
        return

    for dispositivo in dispositivos:
        if dispositivo.id == dispositivo_id:
            print()
            print(dispositivo)
            break

    if not pedir_confirmacion(
        "¿Seguro que quieres eliminar este dispositivo? (s/n): "
    ):
        print("Operación cancelada.")
        return

    borrar_dispositivo(dispositivo_id)

    print("Dispositivo eliminado correctamente.")