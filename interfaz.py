from tablero import Celda


def validarNumero(msj, msE, msE2, mini, maxi):
    while True:
        entrada = input(msj)
        try:
            numero = int(entrada)
        except ValueError:
            print(msE)
            continue

        if numero < mini or numero > maxi:
            print(msE2)
            continue

        return numero


def mostrarTablero(tablero):
    for fila in range(tablero.size):
        linea = ""
        for columna in range(tablero.size):
            estado = tablero.getState(fila, columna)

            if estado == Celda.DESCONOCIDA:
                simbolo = "#"
            elif estado == Celda.BANDERA:
                simbolo = "B"
            else:  # REVELADA
                if tablero.hayMina(fila, columna):
                    simbolo = "M"
                else:
                    simbolo = str(tablero.contarMinasAlrededor(fila, columna))

            linea = linea + simbolo + " "
        print(linea)


def pedirCoordenada(tablero, mensaje):
    valor = validarNumero(
        mensaje,
        "Por favor, ingresá un número entero.",
        f"El valor debe estar entre 1 y {tablero.size}.",
        1, tablero.size
    )
    return valor - 1  # el usuario cuenta desde 1, la lista desde 0


def revelarCelda(tablero):
    fila = pedirCoordenada(tablero, f"Fila a escanear [1 - {tablero.size}]: ")
    columna = pedirCoordenada(tablero, f"Columna a escanear [1 - {tablero.size}]: ")

    if tablero.getState(fila, columna) == Celda.REVELADA:
        print("Esa celda ya estaba revelada, elegí otra.")
        return True

    juego_continua = tablero.cambiarEstado(fila, columna, Celda.REVELADA)

    if juego_continua:
        print("¡Zona segura!")
    else:
        print("¡ZONA COMPROMETIDA! BOOM. Fin del juego.")

    return juego_continua


def marcarCelda(tablero):
    fila = pedirCoordenada(tablero, f"Fila a marcar [1 - {tablero.size}]: ")
    columna = pedirCoordenada(tablero, f"Columna a marcar [1 - {tablero.size}]: ")

    estado_actual = tablero.getState(fila, columna)

    if estado_actual == Celda.REVELADA:
        print("Esa celda ya está revelada, no se puede marcar.")
    elif estado_actual == Celda.BANDERA:
        tablero.cambiarEstado(fila, columna, Celda.DESCONOCIDA)
    else:
        tablero.cambiarEstado(fila, columna, Celda.BANDERA)