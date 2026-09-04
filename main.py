from database import crear_base_datos
from items import anadir_item, mostrar_items, buscar_items, eliminar_item
from dispositivos import anadir_dispositivo, mostrar_dispositivos, eliminar_dispositivo
from ubicaciones import anadir_ubicacion, mostrar_ubicaciones, donde_esta, que_hay_en, eliminar_ubicacion
from utils import pedir_entero, pausar, mostrar_menu


def menu_items():
    while True:
        mostrar_menu(
            "--- ELEMENTOS ---",
            [
                "Añadir elemento",
                "Mostrar biblioteca",
                "Buscar elemento",
                "Eliminar elemento",
                "Volver al menú principal"
            ]
        )

        opcion = pedir_entero("Selecciona una opción: ")

        if opcion == 1:
            anadir_item()
            pausar()
        elif opcion == 2:
            mostrar_items()
            pausar()
        elif opcion == 3:
            buscar_items()
            pausar()
        elif opcion == 4:
            eliminar_item()
            pausar()
        elif opcion == 5:
            return
        else:
            print("Opción no válida.")


def menu_dispositivos():
    while True:
        mostrar_menu(
            "--- DISPOSITIVOS ---",
            [
                "Añadir dispositivo",
                "Mostrar dispositivos",
                "Eliminar dispositivo",
                "Volver al menú principal"
            ]
        )
        
        opcion = pedir_entero("Selecciona una opción: ")

        if opcion == 1:
            anadir_dispositivo()
            pausar()
        elif opcion == 2:
            mostrar_dispositivos()
            pausar()
        elif opcion == 3:
            eliminar_dispositivo()
            pausar()
        elif opcion == 4:
            return
        else:
            print("Opción no válida.")


def menu_ubicaciones():
    while True:
        mostrar_menu(
            "--- UBICACIONES ---",
            [
                "Añadir ubicación",
                "Mostrar ubicaciones",
                "Eliminar ubicación",
                "¿Dónde está?",
                "¿Qué hay en un dispositivo?",
                "Volver al menú principal"
            ]
        )

        opcion = pedir_entero("Selecciona una opción: ")

        if opcion == 1:
            anadir_ubicacion()
            pausar()
        elif opcion == 2:
            mostrar_ubicaciones()
            pausar()
        elif opcion == 3:
            eliminar_ubicacion()
            pausar()
        elif opcion == 4:
            donde_esta()
            pausar()
        elif opcion == 5:
            que_hay_en()
            pausar()
        elif opcion == 6:
            return
        else:
            print("Opción no válida.")


def menu():
    #  Creo un bucle que muestra indefinidamente el menú hasta que el usuario decida salir.
    while True:
        mostrar_menu(
            "--- MI BIBLIOTECA ---",
            [
                "Gestionar elementos",
                "Gestionar dispositivos",
                "Gestionar ubicaciones",
                "Salir"
            ]
        )

        opcion = pedir_entero("Selecciona una opción: ")

        if opcion == 1:
            menu_items()
        elif opcion == 2:
            menu_dispositivos()
        elif opcion == 3:
            menu_ubicaciones()
        elif opcion == 4:
            print("Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


crear_base_datos()
menu()
