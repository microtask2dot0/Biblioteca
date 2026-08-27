quiero hacer un programa que me indique qué libros, películas, fotos y música tengo y en qué dispositivos los tengo guardado. quiero que la aplicación sea local y también accesible desde otros dispositivos

Sí. Y es un proyecto muy bueno para aprender programación porque combina base de datos + backend + interfaz web + acceso desde otros dispositivos.

Por lo que describes, yo lo plantearía así:

🏗️ Arquitectura recomendada

&#x20; ┌──────────────────┐

&#x20; │ Móvil / PC / │

&#x20; │ Tablet │

&#x20; └────────┬─────────┘

&#x20; │

&#x20; navegador

&#x20; │

&#x20; ▼

&#x20; ┌─────────────────────┐

&#x20; │ Aplicación web │

&#x20; │ (interfaz) │

&#x20; └──────────┬──────────┘

&#x20; │

&#x20; ▼

&#x20; ┌─────────────────────┐

&#x20; │ Backend │

&#x20; │ Python │

&#x20; └──────────┬──────────┘

&#x20; │

&#x20; ▼

&#x20; ┌─────────────────────┐

&#x20; │ SQLite │

&#x20; │ Base datos │

&#x20; └─────────────────────┘

La idea sería que los archivos multimedia sigan donde están. La aplicación solamente guarda información sobre ellos.

Por ejemplo:

Obra Tipo Dispositivo Ubicación

Dune Libro Kindle /Books/Dune.pdf

Blade Runner Película PC /Movies/Blade Runner.mkv

Abbey Road Música NAS /Music/Beatles/

Foto vacaciones Foto HDD /Fotos/2025/

📚 La base de datos

Podríamos empezar con algo sencillo:

items

\-----

id

title

type

author

year

genre

description

devices

\--------

id

name

type

location

copies

\------

id

item_id

device_id

path

format

notes

La separación entre obra y copia es importante.

Por ejemplo, tienes:

"El Señor de los Anillos"

pero quizá tienes una copia:

El Señor de los Anillos

&#x20; ├── PC → C:\\Libros\\ESDLA.epub

&#x20; ├── Kindle → Kindle

&#x20; └── NAS → /books/tolkien/ESDLA.pdf

Así puedes saber qué tienes y dónde lo tienes.

🐍 Para ti, usaría Python

Como estás aprendiendo Python en freeCodeCamp, puedes aprovecharlo.

Mi stack inicial sería:

Python

FastAPI → servidor/backend

SQLite → base de datos

HTML + CSS + JavaScript → interfaz

SQLAlchemy → comunicación con la base de datos

Y más adelante podríamos añadir:

búsqueda

filtros por tipo

portadas

carátulas

etiquetas

préstamos

duplicados

importación automática de carpetas

usuarios

copias de seguridad

acceso desde móvil

API

estadísticas

🌐 ¿Cómo hacer que sea local pero accesible desde otros dispositivos?

Hay una solución muy interesante:

Ejecutas la aplicación en tu ordenador/NAS y los demás dispositivos acceden mediante el navegador.

Por ejemplo:

PC/NAS

└── Aplicación

&#x20; ├── Base de datos

&#x20; └── Servidor web

&#x20; │

&#x20; └── Wi-Fi de casa

&#x20; ├── 📱 móvil

&#x20; ├── 💻 portátil

&#x20; └── 📺 tablet

Desde el móvil entrarías, por ejemplo, en:

http://192.168.1.50:8000

Y tendrías tu biblioteca.

No necesitas inicialmente publicar nada en Internet.

🔐 Y si posteriormente quieres acceder desde fuera de casa

Ahí podemos añadir una solución como Tailscale o una VPN, en lugar de abrir directamente puertos de tu router a Internet.

Eso te permitiría algo como:

&#x20; INTERNET

&#x20; │

&#x20; conexión privada

&#x20; │

&#x20; ▼

&#x20; 🖥️ Tu servidor

&#x20; │

&#x20; ┌─────────┼─────────┐

&#x20; ▼ ▼ ▼

&#x20; 📱 móvil 💻 PC 📱 tablet

Es una evolución mucho más segura que exponer directamente la aplicación a Internet.

🚀 Pero te recomiendo empezar MUCHO más pequeño

Como estás aprendiendo Python, no intentaría construir todo esto de golpe.

Podemos hacerlo por etapas:

Fase 1: Python + SQLite

→ Crear y consultar tu biblioteca.

Fase 2: FastAPI

→ Convertirla en una aplicación web.

Fase 3: HTML/CSS/JavaScript

→ Crear una interfaz bonita.

Fase 4: dispositivos

→ Registrar PC, Kindle, discos duros, NAS, etc.

Fase 5: acceso desde móvil/tablet

→ Acceso dentro de tu red local.

Fase 6: acceso remoto

→ VPN/Tailscale.

Fase 7: automatización

→ Que la aplicación pueda escanear carpetas y detectar automáticamente libros, películas, música y fotos.

De hecho, esta última parte puede ser muy interesante: podrías decirle a la aplicación que tu disco tiene /Peliculas, /Musica, /Libros y /Fotos, y que ella construya automáticamente el inventario.

Si quieres hacerlo como proyecto para aprender Python desde tu nivel actual,

puedo guiarte paso a paso y construirlo contigo, empezando por la primera versión mínima con SQLite, sin saltarnos conceptos.

sí por favor, guíame paso a paso y construirlo contigo, empezando por la primera versión mínima con SQLite, sin saltarnos conceptos.

¡Perfecto! Vamos a hacerlo como un proyecto real, pero a tu nivel actual. Y no voy a darte todo el programa de golpe: iremos construyéndolo y entendiendo qué hace cada pieza.

🗺️ Nuestro camino

Vamos a llegar aproximadamente a esto:

FASE 1 → Python + SQLite

&#x20; ↓

FASE 2 → Crear nuestra base de datos

&#x20; ↓

FASE 3 → Añadir libros, películas, música y fotos

&#x20; ↓

FASE 4 → Consultar y buscar

&#x20; ↓

FASE 5 → FastAPI

&#x20; ↓

FASE 6 → Interfaz web

&#x20; ↓

FASE 7 → Acceso desde móvil/tablet

&#x20; ↓

FASE 8 → Escanear automáticamente tus dispositivos

Hoy nos vamos a quedar en FASE 1.

🟢 Paso 1 — Crear nuestro proyecto

Crea una carpeta en tu ordenador llamada:

mi_biblioteca

Dentro vamos a tener inicialmente:

mi_biblioteca/

└── biblioteca.py

Nuestro primer objetivo es extremadamente sencillo:

Crear una base de datos SQLite y guardar un libro dentro.

No vamos a hacer todavía páginas web, usuarios, imágenes ni nada más.

🟢 Paso 2 — ¿Qué es SQLite?

SQLite es una base de datos que vive en un archivo.

Por ejemplo, nuestra aplicación terminará teniendo:

mi_biblioteca/

├── biblioteca.py

└── biblioteca.db

biblioteca.db será nuestra base de datos.

Una de las ventajas de SQLite para este proyecto es que no necesitas instalar un servidor de bases de datos.

Python además incluye el módulo sqlite3, así que para empezar no necesitamos instalar ninguna biblioteca externa.

🟢 Paso 3 — Nuestro primer programa

Abre biblioteca.py y escribe:

import sqlite3

conexion = sqlite3.connect("biblioteca.db")

print("Base de datos creada correctamente.")

conexion.close()

Guarda el archivo y ejecútalo:

python biblioteca.py

Si todo funciona, deberías ver:

Base de datos creada correctamente.

Y aparecerá un nuevo archivo:

mi_biblioteca/

├── biblioteca.py

└── biblioteca.db

🧠 ¿Qué acabamos de hacer?

Esta línea:

import sqlite3

le dice a Python:

"Quiero utilizar SQLite."

Esta:

conexion = sqlite3.connect("biblioteca.db")

hace algo muy interesante.

Le dice:

"Conéctate a biblioteca.db."

Si el archivo no existe, SQLite lo crea automáticamente.

Y finalmente:

conexion.close()

cierra la conexión con la base de datos.

🟢 Paso 4 — Crear nuestra primera tabla

Ahora vamos a crear una tabla llamada items.

De momento tendrá solamente cuatro columnas:

items

\--------------------------------

id

titulo

tipo

dispositivo

Por ejemplo:

1 | Dune | libro | Kindle

2 | Blade Runner | pelicula | PC

3 | Abbey Road | musica | NAS

4 | Vacaciones 2025 | foto | HDD

Modifica biblioteca.py para que quede así:

import sqlite3

conexion = sqlite3.connect("biblioteca.db")

cursor = conexion.cursor()

cursor.execute("""

&#x20; CREATE TABLE IF NOT EXISTS items (

&#x20; id INTEGER PRIMARY KEY AUTOINCREMENT,

&#x20; titulo TEXT NOT NULL,

&#x20; tipo TEXT NOT NULL,

&#x20; dispositivo TEXT NOT NULL

&#x20; )

""")

conexion.commit()

print("Tabla creada correctamente.")

conexion.close()

Ejecuta otra vez:

python biblioteca.py

Deberías obtener:

Tabla creada correctamente.

🧠 Ahora hay cuatro conceptos importantes

1\. conexion

conexion = sqlite3.connect("biblioteca.db")

Es nuestra conexión con la base de datos.

2\. cursor

cursor = conexion.cursor()

El cursor nos permite ejecutar instrucciones SQL.

3\. execute()

cursor.execute(...)

Le estamos diciendo a SQLite:

"Ejecuta esta instrucción."

4\. commit()

conexion.commit()

Esto confirma los cambios.

Piensa en commit() como:

💾 Guardar los cambios en la base de datos.

🟢 Paso 5 — Nuestro primer libro

Ahora viene algo más divertido.

Vamos a insertar un libro.

Añade antes de conexion.commit():

cursor.execute("""

&#x20; INSERT INTO items (titulo, tipo, dispositivo)

&#x20; VALUES (?, ?, ?)

""", ("Dune", "libro", "Kindle"))

Por tanto, el programa completo queda:

import sqlite3

conexion = sqlite3.connect("biblioteca.db")

cursor = conexion.cursor()

cursor.execute("""

&#x20; CREATE TABLE IF NOT EXISTS items (

&#x20; id INTEGER PRIMARY KEY AUTOINCREMENT,

&#x20; titulo TEXT NOT NULL,

&#x20; tipo TEXT NOT NULL,

&#x20; dispositivo TEXT NOT NULL

&#x20; )

""")

cursor.execute("""

&#x20; INSERT INTO items (titulo, tipo, dispositivo)

&#x20; VALUES (?, ?, ?)

""", ("Dune", "libro", "Kindle"))

conexion.commit()

print("Libro añadido correctamente.")

conexion.close()

Ejecuta:

python biblioteca.py

Y debería aparecer:

Libro añadido correctamente.

🎉 Acabas de guardar tu primer elemento en tu propia base de datos.

⚠️ Pero hay algo importante

Si ejecutas el programa cinco veces, ahora mismo tendrás cinco Dune.

Eso es normal.

Más adelante solucionaremos esto y también crearemos funciones como:

añadir_libro()

añadir_pelicula()

añadir_musica()

añadir_foto()

buscar()

listar()

Pero todavía no lo hagamos.

Quiero que primero entiendas lo que acabamos de construir.

🎯 Tu ejercicio ahora

Haz solamente estos pasos:

Crea mi_biblioteca.

Crea biblioteca.py.

Escribe el código anterior.

Ejecútalo.

Comprueba que aparece biblioteca.db.

Cuando lo tengas, dime qué salida te aparece al ejecutar python biblioteca.py, y seguimos con el siguiente paso: leer el Dune que acabamos de guardar desde SQLite.

Ahora viene una decisión importante de diseño

Hasta ahora nuestra tabla es:

items

\--------------------------------

id

titulo

tipo

dispositivo

Pero piensa en lo que quieres conseguir finalmente.

Un mismo libro podría estar en:

Kindle

PC

NAS

disco duro externo

Y una película podría estar en:

PC

NAS

disco externo

Por tanto, guardar:

titulo | dispositivo

en la misma tabla no es una buena estructura.

Necesitamos separar qué tenemos de dónde lo tenemos.

🟢 Paso 15 — Nuestro nuevo modelo

Vamos a empezar a pensar como diseñadores de bases de datos.

Tendremos una tabla:

items

\--------------------------------

id

titulo

tipo

autor

año

genero

Y otra:

dispositivos

\--------------------------------

id

nombre

tipo

Por ejemplo:

items

1 | Dune | libro

2 | Blade Runner | pelicula

3 | Abbey Road | musica

4 | Vacaciones | foto

dispositivos

1 | Kindle | ebook

2 | PC | ordenador

3 | NAS | almacenamiento

4 | HDD 1 | disco

Y finalmente necesitaremos una tercera tabla:

ubicaciones

\--------------------------------

id

item_id

dispositivo_id

ruta

Que nos permitirá decir:

Dune

&#x20;├── Kindle

&#x20;└── NAS

Blade Runner

&#x20;└── PC

Abbey Road

&#x20;└── NAS

Esto es muchísimo más potente.

🚨 Pero no borres nada todavía

Aquí quiero hacer algo deliberadamente distinto a los pasos anteriores.

No vamos a modificar todavía tu base de datos.

Primero quiero que entiendas por qué necesitamos tres tablas.

Este concepto se llama relaciones entre tablas, y es uno de los conceptos más importantes de bases de datos.

Por ejemplo:

&#x20; ITEMS

&#x20; ┌─────────────┐

&#x20; │ Dune │

&#x20; │ Blade Runner│

&#x20; │ Abbey Road │

&#x20; └──────┬──────┘

&#x20; │

&#x20; │

&#x20; UBICACIONES

&#x20; │

&#x20; │

&#x20; ┌──────┴──────┐

&#x20; │ │

&#x20; ▼ ▼

&#x20; DISPOSITIVOS DISPOSITIVOS

&#x20; Kindle NAS

Más adelante aprenderemos que esto se implementa mediante claves primarias y claves foráneas.

No necesitas dominarlo todavía.

**TODO**

Crear clases

Ver cómo hacer que obtener_items() devuelva objetos Item en lugar de tuplas

Eso sí, hay una mejora que veremos después: obtener_datos_ubicacion() hace una consulta por cada ubicación. No es grave para nuestra aplicación, pero no es la forma más eficiente si tuviéramos cientos de ubicaciones.

Podemos hacer que la consulta cree:

Item
Ubicacion

para cada resultado.

Es decir, cada resultado podría ser:

(item, ubicacion)

Esto sigue siendo una tupla de Python, sí, pero no es una tupla de datos de SQLite. Son dos objetos de nuestro modelo agrupados.

Sin embargo, hay otra posibilidad todavía más limpia: crear una clase que represente precisamente esta relación.

Pero no quiero que creemos otra clase todavía

1 Dune Libro 1 CI-FI Frank Herbert No me gustó la película
2 It Libro 5 Terror Stephen King Mi primer libro de este autor
3 Dune Película 0 CI-Fi No sé quién es Muy mala
4 Dune Videojuego 2 CI-Fi
5 El señor de los anillos 1 libro 5 épico No lo recuerdo Mu chulo el libro
6 La tienda libro 3 terror Stephen King Es un poco desagradable

27/08/26
