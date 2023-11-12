import numpy as np

FILAS = 6
COLUMNAS = 7
JUGADOR_1 = 1
JUGADOR_2 = 2
VACIO = 0

def crear_tablero():
    return np.zeros((FILAS, COLUMNAS), dtype=int)

def movimiento_valido(tablero, col):
    return tablero[FILAS - 1][col] == VACIO

def colocar_ficha(tablero, col, jugador):
    for fila in range(FILAS):
        if tablero[fila][col] == VACIO:
            tablero[fila][col] = jugador
            break

def imprimir_tablero(tablero):
    for fila in reversed(range(FILAS)):
        for col in range(COLUMNAS):
            print(tablero[fila][col], end=' ')
        print()

def ganador(tablero, jugador):
    # Verificar horizontal
    for fila in range(FILAS):
        for col in range(COLUMNAS - 3):
            if tablero[fila][col] == jugador and tablero[fila][col + 1] == jugador and tablero[fila][col + 2] == jugador and tablero[fila][col + 3] == jugador:
                return True

    # Verificar vertical
    for col in range(COLUMNAS):
        for fila in range(FILAS - 3):
            if tablero[fila][col] == jugador and tablero[fila + 1][col] == jugador and tablero[fila + 2][col] == jugador and tablero[fila + 3][col] == jugador:
                return True

    # Verificar diagonal (pendiente positiva)
    for fila in range(FILAS - 3):
        for col in range(COLUMNAS - 3):
            if tablero[fila][col] == jugador and tablero[fila + 1][col + 1] == jugador and tablero[fila + 2][col + 2] == jugador and tablero[fila + 3][col + 3] == jugador:
                return True

    # Verificar diagonal (pendiente negativa)
    for fila in range(3, FILAS):
        for col in range(COLUMNAS - 3):
            if tablero[fila][col] == jugador and tablero[fila - 1][col + 1] == jugador and tablero[fila - 2][col + 2] == jugador and tablero[fila - 3][col + 3] == jugador:
                return True

    return False

def tablero_lleno(tablero):
    return not any(tablero[0][col] == VACIO for col in range(COLUMNAS))

def evaluar_ventana(ventana, jugador):
    puntaje = 0
    oponente = JUGADOR_1 if jugador == JUGADOR_2 else JUGADOR_2

    if ventana.count(jugador) == 4:
        puntaje += 100
    elif ventana.count(jugador) == 3 and ventana.count(VACIO) == 1:
        puntaje += 5
    elif ventana.count(jugador) == 2 and ventana.count(VACIO) == 2:
        puntaje += 2

    if ventana.count(oponente) == 3 and ventana.count(VACIO) == 1:
        puntaje -= 4

    return puntaje

def evaluar_tablero(tablero, jugador):
    puntaje = 0

    # Evaluar horizontal
    for fila in range(FILAS):
        for col in range(COLUMNAS - 3):
            ventana = list(tablero[fila, col:col + 4])
            puntaje += evaluar_ventana(ventana, jugador)

    # Evaluar vertical
    for col in range(COLUMNAS):
        for fila in range(FILAS - 3):
            ventana = list(tablero[fila:fila + 4, col])
            puntaje += evaluar_ventana(ventana, jugador)

    # Evaluar diagonal (pendiente positiva)
    for fila in range(FILAS - 3):
        for col in range(COLUMNAS - 3):
            ventana = list(tablero[fila:fila + 4, col:col + 4].diagonal())
            puntaje += evaluar_ventana(ventana, jugador)

    # Evaluar diagonal (pendiente negativa)
    for fila in range(3, FILAS):
        for col in range(COLUMNAS - 3):
            ventana = list(np.fliplr(tablero[fila - 3:fila + 1, col:col + 4]).diagonal())
            puntaje += evaluar_ventana(ventana, jugador)

    return puntaje

def minimax(tablero, profundidad, maximizar_jugador):
    if profundidad == 0 or ganador(tablero, JUGADOR_1) or ganador(tablero, JUGADOR_2) or tablero_lleno(tablero):
        return evaluar_tablero(tablero, JUGADOR_2) if maximizar_jugador else evaluar_tablero(tablero, JUGADOR_1)

    if maximizar_jugador:
        max_eval = float('-inf')
        for col in range(COLUMNAS):
            if movimiento_valido(tablero, col):
                temp_tablero = tablero.copy()
                colocar_ficha(temp_tablero, col, JUGADOR_2)
                eval = minimax(temp_tablero, profundidad - 1, False)
                max_eval = max(max_eval, eval)
        return max_eval

    else:
        min_eval = float('inf')
        for col in range(COLUMNAS):
            if movimiento_valido(tablero, col):
                temp_tablero = tablero.copy()
                colocar_ficha(temp_tablero, col, JUGADOR_1)
                eval = minimax(temp_tablero, profundidad - 1, True)
                min_eval = min(min_eval, eval)
        return min_eval

def obtener_mejor_movimiento(tablero):
    mejor_val = float('-inf')
    mejor_movimiento = -1

    for col in range(COLUMNAS):
        if movimiento_valido(tablero, col):
            temp_tablero = tablero.copy()
            colocar_ficha(temp_tablero, col, JUGADOR_2)
            movimiento_eval = minimax(temp_tablero, 4, False)
            if movimiento_eval > mejor_val:
                mejor_val = movimiento_eval
                mejor_movimiento = col

    return mejor_movimiento + 1

def main():
    tablero = crear_tablero()
    fin_del_juego = False
    turno = 0

    while not fin_del_juego:
        imprimir_tablero(tablero)

        if turno % 2 == 0:
            col = int(input("\nJugador 1, elige una columna (1-7): ")) - 1
            if movimiento_valido(tablero, col):
                colocar_ficha(tablero, col, JUGADOR_1)
            else:
                print("\nMovimiento inválido. Intenta de nuevo.")
                continue
        else:
            col = obtener_mejor_movimiento(tablero)
            colocar_ficha(tablero, col, JUGADOR_2)
            print(f"\nJugador 2 colocó una ficha en la columna {col + 1}")

        if ganador(tablero, JUGADOR_1):
            print("\n¡Jugador 1 gana!")
            fin_del_juego = True
        elif ganador(tablero, JUGADOR_2):
            print("\n¡Jugador 2 gana!")
            fin_del_juego = True
        elif tablero_lleno(tablero):
            print("\n¡Es un empate!")
            fin_del_juego = True

        turno += 1

    imprimir_tablero(tablero)

if __name__ == "__main__":
    main()
