import random
from collections.abc import Iterator
from enum import Enum
from typing import Final


class CellState(Enum):
    UNREVEALED = 0
    FLAG = 1
    REVEALED = 2

class AlreadyRevealedError(Exception):
    ...

class CannotRevealError(Exception):
    ...

class AlreadyFlaggedError(Exception):
    ...

class Board:
    __width: int
    __height: int
    __mines_to_add: int | None
    __mines: set[tuple[int, int]]
    __cell_rows: list[list[CellState]]

    def __init__(self, width: int, height: int, mines: int):
        if width <= 0 or height <= 0:
            raise ValueError
        self.__width = width
        self.__height = height
        self.__mines_to_add = mines
        self.__mines = set()

        # Matriz de estados: el estado visible de cada celda
        self.__cell_rows = []
        for _ in range(height):
            row: list[CellState] = []
            for _ in range(width):
                row.append(CellState.UNREVEALED)
            self.__cell_rows.append(row)

    def width(self) -> int:
        return self.__width

    def height(self) -> int:
        return self.__height

    def is_mine(self, x: int, y: int) -> bool:
        return (x, y) in self.__mines

    def get_cell_state(self, x: int, y: int) -> CellState:
        return self.__cell_rows[y][x]

    def __set_cell_state(self, x: int, y: int, new_state: CellState):
        self.__cell_rows[y][x] = new_state

    def distribute_mines(self):
        if self.__mines_to_add is None:
            raise Warning("Mines already distributed")

        # Nos aseguramos que haya suficientes espacios libres
        empty_spaces = 0
        for row in self.__cell_rows:
            for column in row:
                if column != CellState.REVEALED:
                    empty_spaces += 1
                if empty_spaces >= self.__mines_to_add:
                    break
        if empty_spaces < self.__mines_to_add:
            raise Warning("Not enough space in board")

        # Pone minas al azar, evitando celdas que ya fueron reveladas o lugares que ya tienen minas.
        mines_added = 0
        while mines_added < self.__mines_to_add:
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)

            not_revealed = self.get_cell_state(x, y) != CellState.REVEALED
            already_a_mine = self.is_mine(x, y)

            if not_revealed and not already_a_mine:
                self.__mines.add((x, y))
                mines_added += 1

        self.__mines_to_add = None

    def inside_board(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.__width and y >= 0 and y < self.__height

    __NEIGHBOUR_OFFSETS: Final[set[tuple[int, int]]] = {
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    }

    def get_neighbour_positions(self, x: int, y: int) -> Iterator[tuple[int, int]]:
        for offset in self.__NEIGHBOUR_OFFSETS:
            new_pos = (x + offset[0], y + offset[1])
            if not self.inside_board(new_pos[0], new_pos[1]):
                continue
            yield new_pos

    def count_neighbouring_mines(self, x: int, y: int) -> int:
        # Revisamos las 8 celdas vecinas una por una,
        # comprobando siempre que existan antes de mirarlas.
        count = 0

        for pos in self.get_neighbour_positions(x, y):
            if self.is_mine(pos[0], pos[1]):
                count += 1

        return count

    def change_cell_state(self, x: int, y: int, new_state: CellState):
        # Devuelve True si el juego sigue, False si pisaste una mina.
        current_state: CellState = self.get_cell_state(x, y)

        # Una celda revelada no se puede volver a cambiar
        if current_state == CellState.REVEALED:
            raise AlreadyRevealedError

        # DESCONOCIDA solo puede pasar a BANDERA o a REVELADA
        if (
            current_state == CellState.UNREVEALED
            and new_state != CellState.FLAG
            and new_state != CellState.REVEALED
        ):
            raise CannotRevealError

        # BANDERA solo puede volver a DESCONOCIDA
        if current_state == CellState.FLAG and new_state != CellState.UNREVEALED:
            raise AlreadyFlaggedError

        # Primero marcamos la nueva posicion..
        self.__set_cell_state(x, y, new_state)

        # y despues, si se intento revelar, distribuyo las minas.
        # La funcion va a evitar los lugares ya revelados.
        if not self.__mines and new_state == CellState.REVEALED:
            self.distribute_mines()

        # El juego termina si se revela una mina
        return new_state == CellState.REVEALED and self.is_mine(x, y)

    def won(self):
        # Ganás cuando las celdas sin revelar son exactamente las minas
        unrevealed_cells = 0
        for row in self.__cell_rows:
            for cell_state in row:
                if cell_state != CellState.REVEALED:
                    unrevealed_cells += 1

        return unrevealed_cells == len(self.__mines)
