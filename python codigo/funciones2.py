import json
from datetime import datetime


ARCHIVO = "horario.json"
ARCHIVO_REPORTE = "reporte_horario.json"

def cargar_horario():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        horario_vacio = []
        guardar_horario(horario_vacio)
        return horario_vacio

    except json.JSONDecodeError:
        print("ERROR: El archivo horario.json está dañado.")
        print("Se iniciará un horario vacío.")

        horario_vacio = []
        guardar_horario(horario_vacio)
        return horario_vacio


def guardar_horario(horario):
    with open(ARCHIVO, "w", encoding="utf-8") as file:
        json.dump(
            horario,
            file,
            indent=4,
            ensure_ascii=False
        )


def mostrar_menu():
    print("\n" + "=" * 50)
    print("       GENERADOR DE HORARIOS PARA ESTUDIANTES")
    print("=" * 50)
    print("1. Registrar una materia o actividad")
    print("2. Ver horario semanal")
    print("3. Modificar una materia o actividad")
    print("4. Eliminar una materia o actividad")
    print("5. Hacer reporte del horario")
    print("6. Salir")
    print("=" * 50)



def convertir_hora(hora):
    return datetime.strptime(hora, "%H:%M")


def validar_hora(hora):
    try:
        convertir_hora(hora)
        return True
    except ValueError:
        return False


def pedir_hora(mensaje):
    """
    Solicita una hora hasta que el usuario
    ingrese una hora válida en formato HH:MM.
    """

    while True:
        hora = input(mensaje).strip()

        if validar_hora(hora):
            return hora

        print("ERROR: La hora no es válida.")
        print("Use el formato HH:MM. Ejemplo: 08:30")


def validar_dia(dia):
    dias_validos = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes"
    ]

    return dia.strip().lower() in dias_validos


def pedir_dia(mensaje):
    """
    Solicita un día hasta que el usuario
    ingrese un día válido.
    """

    while True:
        dia = input(mensaje).strip()

        if validar_dia(dia):
            return dia

        print("ERROR: El día no es válido.")
        print(
            "Use: Lunes, Martes, Miercoles, "
            "Jueves o Viernes."
        )



def hay_conflicto(nueva_materia, horario, materia_excluir=None):

    for materia in horario:


        if materia is materia_excluir:
            continue

        if (
            materia["dia"].strip().lower()
            == nueva_materia["dia"].strip().lower()
        ):

            hora_inicio_existente = convertir_hora(
                materia["hora_inicio"]
            )

            hora_fin_existente = convertir_hora(
                materia["hora_fin"]
            )

            hora_inicio_nueva = convertir_hora(
                nueva_materia["hora_inicio"]
            )

            hora_fin_nueva = convertir_hora(
                nueva_materia["hora_fin"]
            )

            if (
                hora_inicio_nueva < hora_fin_existente
                and
                hora_fin_nueva > hora_inicio_existente
            ):
                return True

    return False


def registrar_materia(horario):

    print("\n" + "-" * 50)
    print("REGISTRAR MATERIA O ACTIVIDAD")
    print("-" * 50)

    materia = input(
        "Ingrese el nombre de la materia o actividad: "
    ).strip()

    if not materia:
        print("ERROR: El nombre no puede estar vacío.")
        return

    dia = pedir_dia(
        "Ingrese el día de la semana "
        "(Lunes, Martes, Miercoles, Jueves, Viernes): "
    )

    hora_inicio = pedir_hora(
        "Ingrese la hora de inicio (formato HH:MM): "
    )

    hora_fin = pedir_hora(
        "Ingrese la hora de fin (formato HH:MM): "
    )

    if convertir_hora(hora_inicio) >= convertir_hora(hora_fin):
        print(
            "ERROR: La hora de inicio debe ser menor "
            "que la hora de fin."
        )
        return

    ubicacion = input(
        "Ingrese la ubicación de la materia o actividad: "
    ).strip()

    if not ubicacion:
        ubicacion = "Sin ubicación"

    nueva_materia = {
        "materia": materia,
        "dia": dia,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "ubicacion": ubicacion
    }

    if hay_conflicto(nueva_materia, horario):

        print(
            "ERROR: Existe un conflicto de horario."
        )

        print(
            "La materia o actividad no fue registrada."
        )

        return

    horario.append(nueva_materia)

    guardar_horario(horario)

    print(
        "\nMateria o actividad registrada "
        "exitosamente."
    )

def ver_horario(horario):

    if not horario:
        print(
            "\nNo hay materias o actividades registradas."
        )
        return

    dias = [
        "Lunes",
        "Martes",
        "Miercoles",
        "Jueves",
        "Viernes"
    ]

    print("\n" + "=" * 60)
    print("                 HORARIO SEMANAL")
    print("=" * 60)

    for dia in dias:

        print(f"\n{dia}:")
        print("-" * 60)

        materias_dia = [
            materia
            for materia in horario
            if materia["dia"].strip().lower()
            == dia.lower()
        ]

        if not materias_dia:

            print("  No hay materias o actividades.")

        else:

            materias_dia = sorted(
                materias_dia,
                key=lambda x: convertir_hora(
                    x["hora_inicio"]
                )
            )

            for materia in materias_dia:

                print(
                    f"  {materia['hora_inicio']} - "
                    f"{materia['hora_fin']}: "
                    f"{materia['materia']} "
                    f"en {materia['ubicacion']}"
                )

    print("\n" + "=" * 60)


def modificar_materia(horario):

    if not horario:
        print(
            "\nNo hay materias o actividades registradas."
        )
        return

    print("\n" + "-" * 50)
    print("MODIFICAR MATERIA O ACTIVIDAD")
    print("-" * 50)

    nombre_materia = input(
        "Ingrese el nombre de la materia o actividad "
        "a modificar: "
    ).strip()

    for materia in horario:

        if (
            materia["materia"].strip().lower()
            == nombre_materia.lower()
        ):

            print("\nMateria encontrada.")
            print(f"Nombre: {materia['materia']}")
            print(f"Día: {materia['dia']}")
            print(
                f"Hora: {materia['hora_inicio']} - "
                f"{materia['hora_fin']}"
            )
            print(f"Ubicación: {materia['ubicacion']}")

            print("\nIngrese los nuevos datos:")

            nuevo_dia = pedir_dia(
                "Ingrese el nuevo día de la semana: "
            )

            nueva_hora_inicio = pedir_hora(
                "Ingrese la nueva hora de inicio "
                "(formato HH:MM): "
            )

            nueva_hora_fin = pedir_hora(
                "Ingrese la nueva hora de fin "
                "(formato HH:MM): "
            )

            if (
                convertir_hora(nueva_hora_inicio)
                >= convertir_hora(nueva_hora_fin)
            ):
                print(
                    "ERROR: La hora de inicio debe ser "
                    "menor que la hora de fin."
                )
                return

            nueva_ubicacion = input(
                "Ingrese la nueva ubicación: "
            ).strip()

            if not nueva_ubicacion:
                nueva_ubicacion = "Sin ubicación"

            materia_modificada = {
                "materia": materia["materia"],
                "dia": nuevo_dia,
                "hora_inicio": nueva_hora_inicio,
                "hora_fin": nueva_hora_fin,
                "ubicacion": nueva_ubicacion
            }
            if hay_conflicto(
                materia_modificada,
                horario,
                materia
            ):

                print(
                    "ERROR: Existe un conflicto de horario."
                )

                print(
                    "La materia no fue modificada."
                )

                return

            materia["dia"] = nuevo_dia
            materia["hora_inicio"] = nueva_hora_inicio
            materia["hora_fin"] = nueva_hora_fin
            materia["ubicacion"] = nueva_ubicacion

            guardar_horario(horario)

            print(
                "\nMateria modificada exitosamente."
            )

            return

    print(
        "\nNo se encontró una materia o actividad "
        "con ese nombre."
    )

def eliminar_materia(horario):

    if not horario:
        print(
            "\nNo hay materias o actividades registradas."
        )
        return

    print("\n" + "-" * 50)
    print("ELIMINAR MATERIA O ACTIVIDAD")
    print("-" * 50)

    nombre_materia = input(
        "Ingrese el nombre de la materia o actividad "
        "a eliminar: "
    ).strip()

    dia = pedir_dia(
        "Ingrese el día de la materia o actividad "
        "a eliminar: "
    )

    for i in range(len(horario)):

        if (
            horario[i]["materia"].strip().lower()
            == nombre_materia.lower()
            and
            horario[i]["dia"].strip().lower()
            == dia.strip().lower()
        ):

            horario.pop(i)

            guardar_horario(horario)

            print(
                f"\nLa materia {nombre_materia} del día "
                f"{dia} ha sido eliminada exitosamente."
            )

            return

    print(
        "\nNo se encontró una materia o actividad "
        "con ese nombre y día."
    )



def generar_reporte(horario):

    if not horario:
        print(
            "\nNo hay materias o actividades "
            "para generar el reporte."
        )
        return

    dias = [
        "Lunes",
        "Martes",
        "Miercoles",
        "Jueves",
        "Viernes"
    ]

    reporte = []

    for dia in dias:

        materias_dia = [
            materia
            for materia in horario
            if materia["dia"].strip().lower()
            == dia.lower()
        ]

        materias_dia = sorted(
            materias_dia,
            key=lambda x: convertir_hora(
                x["hora_inicio"]
            )
        )

        eventos = []

        for materia in materias_dia:

            eventos.append({
                "materia": materia["materia"],
                "hora_inicio": materia["hora_inicio"],
                "hora_fin": materia["hora_fin"],
                "ubicacion": materia["ubicacion"]
            })

        reporte.append({
            "dia": dia,
            "eventos": eventos
        })

    with open(
        ARCHIVO_REPORTE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            reporte,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print("             REPORTE DEL HORARIO SEMANAL")
    print("=" * 60)

    contador = 0

    for dia in reporte:

        print(f"\n{dia['dia']}:")
        print("-" * 60)

        if not dia["eventos"]:

            print("  No hay materias o actividades.")

        else:

            for evento in dia["eventos"]:

                print(
                    f"  - {evento['materia']} "
                    f"({evento['hora_inicio']} - "
                    f"{evento['hora_fin']}) "
                    f"en {evento['ubicacion']}"
                )

        contador += 1

        if (
            contador == 2
            and dia != reporte[-1]
        ):

            input(
                "\nPresione ENTER para continuar..."
            )

            contador = 0

    print("\n" + "=" * 60)
    print("Reporte generado exitosamente.")
    print(
        f"Archivo guardado como: "
        f"{ARCHIVO_REPORTE}"
    )
    print("=" * 60)

def main():


    horario = cargar_horario()

    while True:

        mostrar_menu()

        opcion = input(
            "Seleccione una opción: "
        ).strip()

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

            print(
                "\nGracias por utilizar el "
                "Generador de Horarios."
            )

            print("Programa finalizado.")
            break

        else:

            print(
                "\nERROR: Opción no válida."
            )

            print(
                "Seleccione una opción del 1 al 6."
            )



if __name__ == "__main__":
    main()
