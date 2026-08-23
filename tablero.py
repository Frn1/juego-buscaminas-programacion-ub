from enum import Enum


class Celda(Enum):
    DESCONOCIDO = 0
    BANDERA = 1
    REVELADO = 2

class Tablero:
    size = -1


    def setSize(self, size):
        self.size = size

    def setMines

    def getState(self, x:int, y:int) -> Celda:
        pass
    def setState(self, x:int, y:int, celda:Celda):
        pass

