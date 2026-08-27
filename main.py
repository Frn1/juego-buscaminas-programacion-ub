# pyright: strict, reportImplicitRelativeImport=false

import interfaz
from tablero import Board


def main():
    board: Board | None = None

    while True:
        print("-------------------------")
        print("ESCUADRÓN ANTIBOMBAS")
        print("-------------------------")
        print("[1] Generar campo minado")
        print("[0] Salir")
        print("-------------------------")

        option: int = interfaz.request_integer(
            "Seleccione una opción: ",
            "Por favor, ingresá un número.",
            "Opción inválida, elegí 0 o 1.",
            0,
            1,
        )

        if option == 0:
            print("¡Hasta la próxima, escuadrón!")
            break
        elif option == 1:
            size: int = interfaz.request_integer(
                "¿De qué tamaño armo el campo (nxn) entre 10 y 40? ",
                "Por favor, ingresá un número.",
                "El tamaño debe estar entre 10 y 40",
                10,
                40,
            )
            max_mines: int = size * size - 1
            number_mines: int = interfaz.request_integer(
                "¿Cuantas minas debe haber en el campo? ",
                "Por favor, ingresá un número.",
                f"El tamaño debe estar entre 1 y {max_mines}.",
                1,
                max_mines,
            )
            board = Board(size, size, number_mines)
            print(f"¡Campo con {number_mines} explosivos!")
            play(board)
            board = None


def play(board: Board):
    while True:
        interfaz.show_board(board)

        print("\n[1] Revelar celda")
        print("[2] Marcar/desmarcar celda con bandera")
        print("[0] Abandonar partida")

        opcion: int = interfaz.request_integer(
            "Seleccione una opción: ",
            "Por favor, ingresá un número.",
            "Opción inválida.",
            0,
            2,
        )

        if opcion == 0:
            print("Partida abandonada.")
            return
        elif opcion == 1:
            revealed_mine = interfaz.reveal_cell(board)
            if revealed_mine:
                interfaz.show_board(board)
                return
            if board.won():
                interfaz.show_board(board)
                print("¡Campo desminado con éxito! ¡GANASTE!")
                return
        elif opcion == 2:
            interfaz.flag_cell(board)


if __name__ == "__main__":
    main()
