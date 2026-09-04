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

    # El método __str__ es un método especial de Python que define cómo queremos que se represente un objeto cuando lo convertimos a texto.
    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Título: {self.titulo}\n"
            f"Tipo: {self.tipo}\n"
            f"Valoración: {self.valoracion}\n"
            f"Género: {self.genero}\n"
            f"Autor: {self.autor}\n"
            f"Notas: {self.notas}"
        )

    def tiene_valoracion(self):
        return self.valoracion > 0

    def es_del_tipo(self, tipo):
        return self.tipo.lower() == tipo.lower()

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

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Nombre: {self.nombre}\n"
            f"Tipo: {self.tipo}"
        )

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

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Item ID: {self.item_id}\n"
            f"Dispositivo ID: {self.dispositivo_id}\n"
            f"Ruta: {self.ruta}"
        )
