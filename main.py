from database import crear_base_datos
from items import anadir_item, mostrar_items, buscar_items, eliminar_item
from dispositivos import anadir_dispositivo, mostrar_dispositivos, eliminar_dispositivo
from ubicaciones import anadir_ubicacion, mostrar_ubicaciones, donde_esta, que_hay_en, eliminar_ubicacion
from utils import pedir_entero, pausar


def menu_items():
    while True:
        print("\n--- ELEMENTOS ---")
        print("\n1. Añadir elemento")
        print("2. Mostrar biblioteca")
        print("3. Buscar elemento")
        print("4. Eliminar elemento")
        print("5. Volver al menú principal")
        print(" ")

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
        print("\n--- DISPOSITIVOS ---")
        print("\n1. Añadir dispositivo")
        print("2. Mostrar dispositivos")
        print("3. Eliminar dispositivo")
        print("4. Volver al menú principal")
        print(" ")

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
        print("\n--- UBICACIONES ---")
        print("\n1. Añadir ubicación")
        print("2. Mostrar ubicaciones")
        print("3. Eliminar ubicación")
        print("4. ¿Dónde está?")
        print("5. ¿Qué hay en un dispositivo?")
        print("6. Volver al menú principal")
        print(" ")

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
        print("\n=============")
        print("Mi biblioteca")
        print("=============")
        print("\n1. Gestionar elementos")
        print("2. Gestionar dispositivos")
        print("3. Gestionar ubicaciones")
        print("4. Salir")
        print("")

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
