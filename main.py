from tablero import Tablero
import interfaz


def main():
    tablero = None

    while True:
        print("-------------------------")
        print("ESCUADRÓN ANTIBOMBAS")
        print("-------------------------")
        print("[1] Generar campo minado")
        print("[2] Jugar")
        print("[0] Salir")
        print("-------------------------")

        opcion = interfaz.validarNumero(
            "Seleccione una opción: ",
            "Por favor, ingresá un número.",
            "Opción inválida, elegí 0, 1 o 2.",
            0, 2
        )

        if opcion == 0:
            print("¡Hasta la próxima, escuadrón!")
            break
        elif opcion == 1:
            size = interfaz.validarNumero(
                "¿De qué tamaño armo el campo (nxn) entre 5 y 8? ",
                "Por favor, ingresá un número.",
                "El tamaño debe estar entre 5 y 8.",
                5, 8
            )
            num_minas = size
            tablero = Tablero(size, num_minas)
            print(f"¡Campo minado generado con {num_minas} explosivos!")
        elif opcion == 2:
            if tablero is None:
                print("Primero tenés que generar un campo minado (opción 1).")
            else:
                jugar(tablero)
                tablero = None


def jugar(tablero):
    while True:
        interfaz.mostrarTablero(tablero)

        print("\n[1] Revelar celda")
        print("[2] Marcar/desmarcar celda con bandera")
        print("[0] Abandonar partida")

        opcion = interfaz.validarNumero(
            "Seleccione una opción: ",
            "Por favor, ingresá un número.",
            "Opción inválida.",
            0, 2
        )

        if opcion == 0:
            print("Partida abandonada.")
            return
        elif opcion == 1:
            juego_continua = interfaz.revelarCelda(tablero)
            if not juego_continua:
                interfaz.mostrarTablero(tablero)
                return
            if tablero.haGanado():
                interfaz.mostrarTablero(tablero)
                print("¡Campo desminado con éxito! ¡GANASTE!")
                return
        elif opcion == 2:
            interfaz.marcarCelda(tablero)


if __name__ == "__main__":
    main()