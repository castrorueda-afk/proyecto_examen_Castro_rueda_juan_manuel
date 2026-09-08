from funciones import (
    cargar_horario,
    registrar_materia,
    ver_horario,
    modificar_materia,
    eliminar_materia,
    generar_reporte
)


def mostrar_menu():
    print("      GENERADOR DE HORARIOS PARA ESTUDIANTES")
    print("1. Registrar una materia o actividad")
    print("2. Ver horario semanal")
    print("3. Modificar una materia o una actividad")
    print("4. Eliminar una materia o una actividad")
    print("5. Hacer reporte del horario")
    print("6. Salir")

def main():

    horario = cargar_horario()

    while True:

        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_materia(horario)

        elif opcion == "2":
            ver_horario(horario)

        elif opcion == "3":
            modificar_materia(horario)

        elif opcion == "4":
            eliminar_materia(horario)

        elif opcion == "5":
            generar_reporte(horario)

        elif opcion == "6":
            print("\nSaliendo del programa...")
            break

        else:
            print("\nERROR: Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
