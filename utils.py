# Valida que el usuario introduzca un número entero y lo devuelve. Si el usuario introduce un valor no válido, 
# se le pedirá que lo intente de nuevo.
def pedir_entero(mensaje):
    while True:
        valor = input(mensaje)

        try:
            return int(valor)
        except ValueError:
            print("Debes introducir un número entero.")

# Valida que un ID exista.
def seleccionar_id(elementos, mensaje):


    if not elementos:
        return None

    ids_disponibles = []

    for elemento in elementos:
        ids_disponibles.append(elemento.id)
        print(f"{elemento.id}. {elemento.nombre}")

    while True:
        id_seleccionado = pedir_entero(mensaje)

        if id_seleccionado in ids_disponibles:
            return id_seleccionado

        print("El ID seleccionado no existe.")

# Función para agrupar elementos por un atributo específico. Devuelve un diccionario donde las claves son los valores del atributo
# y los valores son listas de elementos que comparten ese valor.
def agrupar_por_tipo(elementos):
    # Al hacer una consulta a la base de datos, obtengo una lista de tuplas, 
    # donde cada tupla representa un elemento y contiene varios atributos y paso las tuplas a un diccionario.
    grupos = {} # Creo un diccionario vacío para almacenar los grupos
    for elemento in elementos:
        tipo = elemento.tipo
        if tipo not in grupos:# Compruebo si el tipo ya existe como clave en el diccionario. Si no existe, creo una nueva lista para ese tipo.
            grupos[tipo] = []

        grupos[tipo].append(elemento)
    return grupos

def normalizar_texto(texto):
    # Normaliza el texto a minúsculas y elimina espacios al inicio y al final
    return texto.strip().lower()

def pausar():
    input("Presione ENTER para volver al menú principal...")

def pedir_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()

        if respuesta == "s":
            return True

        if respuesta == "n":
            return False

        print("Debes responder 's' o 'n'.")