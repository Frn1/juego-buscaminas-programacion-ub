# pyright: strict, reportImplicitRelativeImport=false

from tablero import Board, CellState


def request_integer(msj: str, parse_error_message: str, range_error_message: str, minimum: int, maximum: int):
    while True:
        entrada = input(msj)
        try:
            numero = int(entrada)
        except ValueError:
            print(parse_error_message)
            continue

        if numero < minimum or numero > maximum:
            print(range_error_message)
            continue

        return numero


def show_board(board: Board):
    print("    ", end="")
    for x in range(board.width()):
        print(f"{x + 1:>02} ", end="")
    print()
    print("    ", end="")
    for _ in range(board.width()):
        print("-- ", end="")
    print()
    for y in range(board.height()):
        linea = f"{y + 1:>02} |"
        for x in range(board.width()):
            cell_state = board.get_cell_state(x, y)

            if cell_state == CellState.UNREVEALED:
                simbolo = "."
            elif cell_state == CellState.FLAG:
                simbolo = "B"
            else:  # REVELADA
                if board.is_mine(x, y):
                    simbolo = "M"
                else:
                    count = board.count_neighbouring_mines(x, y)
                    simbolo = str(count) if count != 0 else " "

            linea = linea + " " + simbolo + " "
        linea += f"| {y + 1:>02}"
        print(linea)
    print("    ", end="")
    for _ in range(board.width()):
        print("-- ", end="")
    print()
    print("    ", end="")
    for x in range(board.width()):
        print(f"{x + 1:>02} ", end="")
    print()


def request_coordinate(length: int, message: str) -> int:
    valor = request_integer(
        message,
        "Por favor, ingresá un número entero.",
        f"El valor debe estar entre 1 y {length}.",
        1,
        length,
    )
    return valor - 1  # el usuario cuenta desde 1, la lista desde 0


def reveal_cell(board: Board) -> bool:
    x = request_coordinate(board.width(), f"Columna a escanear [1 - {board.width()}]: ")
    y = request_coordinate(board.height(), f"Fila a escanear [1 - {board.height()}]: ")

    if board.get_cell_state(x, y) == CellState.REVEALED:
        print("Esa celda ya estaba revelada, elegí otra.")
        return False

    revealed_a_mine = board.change_cell_state(x, y, CellState.REVEALED)

    if revealed_a_mine:
        print("¡ZONA COMPROMETIDA! BOOM. Fin del juego.")
    else:
        print("¡Zona segura!")
        # Revelar todas las celdas alrededor de la posicion seleccionada si es 0
        positions_to_reveal: list[tuple[int, int]] = [(x, y)]
        while positions_to_reveal:
            (center_x, center_y) = positions_to_reveal.pop()
            if board.count_neighbouring_mines(center_x, center_y) != 0:
                continue
            for new_position in board.get_neighbour_positions(center_x, center_y):
                (new_x, new_y) = new_position
                if board.get_cell_state(new_x, new_y) != CellState.UNREVEALED:
                    continue
                _ = board.change_cell_state(new_x, new_y, CellState.REVEALED)
                positions_to_reveal.append(new_position)


    return revealed_a_mine


def flag_cell(board: Board):
    x = request_coordinate(board.width(), f"Columna a escanear [1 - {board.width()}]: ")
    y = request_coordinate(board.height(), f"Fila a escanear [1 - {board.height()}]: ")

    current_state: CellState = board.get_cell_state(x, y)

    if current_state == CellState.REVEALED:
        print("Esa celda ya está revelada, no se puede marcar.")
    elif current_state == CellState.FLAG:
        _ = board.change_cell_state(x, y, CellState.UNREVEALED)
    else:
        _ = board.change_cell_state(x, y, CellState.FLAG)
