class Item:

    def __init__(
        self,
        id,
        titulo,
        tipo,
        valoracion=0,
        genero=None,
        autor=None,
        notas=None
    ):
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.valoracion = valoracion
        self.genero = genero
        self.autor = autor
        self.notas = notas

class Dispositivo:

    def __init__(
        self,
        id,
        nombre,
        tipo
    ):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo

class Ubicacion:

    def __init__(
        self,
        id,
        item_id,
        dispositivo_id,
        ruta
    ):
        self.id = id
        self.item_id = item_id
        self.dispositivo_id = dispositivo_id
        self.ruta = ruta
