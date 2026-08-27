import random

from enum import Enum


class Celda(Enum):
    DESCONOCIDA = 0
    BANDERA = 1
    REVELADA = 2

class Tablero:
    def __init__(self, size, num_minas):
        self.size = size
        self.num_minas = num_minas
        self.minas_colocadas = False
        self.minas = []

        for fila in range(size):
            fila_minas = []
            for columna in range(size):
                fila_minas.append(False)
            self.minas.append(fila_minas)

        # Matriz de estados: el estado visible de cada celda
        self.estados = []
        for fila in range(size):
            fila_estados = []
            for columna in range(size):
                fila_estados.append(Celda.DESCONOCIDA)
            self.estados.append(fila_estados)

    def colocarMinas(self, x_evitar, y_evitar):
        # Pone minas al azar,
        # sin repeticion y evitando la celda que tocó el jugador.
        minas_puestas = 0
        while minas_puestas < self.num_minas:
            fila = random.randint(0, self.size - 1)
            columna = random.randint(0, self.size - 1)

            es_la_posicion_evitada = (fila == x_evitar and columna == y_evitar)
            ya_tiene_mina = self.minas[fila][columna]

            if not es_la_posicion_evitada and not ya_tiene_mina:
                self.minas[fila][columna] = True
                minas_puestas += 1

        self.minas_colocadas = True

    def hayMina(self, x, y):
        return self.minas[x][y]

    def getState(self, x, y):
        return self.estados[x][y]

    def dentroDelTablero(self, x, y):
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def contarMinasAlrededor(self, x, y):
        # Revisamos las 8 celdas vecinas una por una,
        # comprobando siempre que existan antes de mirarlas.
        contador = 0

        if self.dentroDelTablero(x - 1, y - 1) and self.minas[x - 1][y - 1]:
            contador += 1
        if self.dentroDelTablero(x - 1, y) and self.minas[x - 1][y]:
            contador += 1
        if self.dentroDelTablero(x - 1, y + 1) and self.minas[x - 1][y + 1]:
            contador += 1
        if self.dentroDelTablero(x, y - 1) and self.minas[x][y - 1]:
            contador += 1
        if self.dentroDelTablero(x, y + 1) and self.minas[x][y + 1]:
            contador += 1
        if self.dentroDelTablero(x + 1, y - 1) and self.minas[x + 1][y - 1]:
            contador += 1
        if self.dentroDelTablero(x + 1, y) and self.minas[x + 1][y]:
            contador += 1
        if self.dentroDelTablero(x + 1, y + 1) and self.minas[x + 1][y + 1]:
            contador += 1

        return contador

    def cambiarEstado(self, x, y, nuevoEstado):
        # Devuelve True si el juego sigue, False si pisaste una mina.
        estadoActual = self.estados[x][y]

        # Una celda revelada no se puede volver a cambiar
        if estadoActual == Celda.REVELADA:
            return True

        # DESCONOCIDA solo puede pasar a BANDERA o a REVELADA
        if estadoActual == Celda.DESCONOCIDA:
            if nuevoEstado != Celda.BANDERA and nuevoEstado != Celda.REVELADA:
                return True

        # BANDERA solo puede volver a DESCONOCIDA
        if estadoActual == Celda.BANDERA:
            if nuevoEstado != Celda.DESCONOCIDA:
                return True

        # Recién colocamos las minas cuando se revela la primera celda
        if nuevoEstado == Celda.REVELADA and not self.minas_colocadas:
            self.colocarMinas(x, y)

        self.estados[x][y] = nuevoEstado

        if nuevoEstado == Celda.REVELADA and self.hayMina(x, y):
            return False

        return True

    def haGanado(self):
        # Ganás cuando las celdas sin revelar son exactamente las minas
        celdas_sin_revelar = 0
        for fila in range(self.size):
            for columna in range(self.size):
                if self.estados[fila][columna] != Celda.REVELADA:
                    celdas_sin_revelar += 1

        return celdas_sin_revelar == self.num_minas