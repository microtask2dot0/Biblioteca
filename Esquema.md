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

FASE 5 → FastAPI

&#x20; ↓

FASE 6 → Interfaz web

&#x20; ↓

FASE 7 → Acceso desde móvil/tablet

&#x20; ↓

FASE 8 → Escanear automáticamente tus dispositivos

Hoy nos vamos a quedar en FASE 1.

**TODO**

Crear clases

27/08/26

28/08/26

03/09/2026
04/09/26
