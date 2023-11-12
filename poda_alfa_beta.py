# Importación de bibliotecas necesarias
from termcolor import colored
import random
import math

# Definición de constantes para el juego
FILAS = 6
COLUMNAS = 7

JUGADOR = 1
IA = -1
VACIO = 0

# Direcciones en las que se pueden buscar secuencias de fichas
DIRECCIONES = [(0, 1), (1, 0), (1, 1), (1, -1)]

# Función para crear un tablero vacío
def crear_tablero():
    return [[VACIO] * COLUMNAS for _ in range(FILAS)]

# Función para imprimir el tablero en la consola
def imprimir_tablero(tablero):
    for fila in tablero:
        print("[", end=" ")
        for col in fila:
            if col == VACIO:
                print(colored("o", "white"), end=" ")  # Ficha vacía
            elif col == JUGADOR:
                print(colored("O", "yellow"), end=" ")  # Ficha del Jugador 1
            elif col == IA:
                print(colored("O", "red"), end=" ")  # Ficha del Jugador 2 (IA)
        print("]")

# Función para soltar una ficha en una columna específica
def soltar_ficha(tablero, col, pieza):
    fila = obtener_fila_libre(tablero, col)
    if fila is not None:
        tablero[fila][col] = pieza
        return True
    return False

# Función para obtener la fila libre en una columna específica
def obtener_fila_libre(tablero, col):
    for fila in reversed(range(FILAS)):
        if tablero[fila][col] == VACIO:
            return fila
    return None

# Función para contar las fichas consecutivas en una dirección específica
def conteo_consecutivas(tablero, pieza, consecutivas):
    count = 0
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if tablero[i][j] == pieza:
                count += sum(verificar_en_direccion(tablero, i, j, pieza, consecutivas, direccion) for direccion in DIRECCIONES)
    return count

# Función para verificar las fichas en una dirección específica
def verificar_en_direccion(tablero, fila, col, pieza, consecutivas, direccion):
    dr, dc = direccion
    consecutivas_actuales = 0
    for _ in range(consecutivas):
        if 0 <= fila < FILAS and 0 <= col < COLUMNAS and tablero[fila][col] == pieza:
            consecutivas_actuales += 1
            fila += dr
            col += dc
        else:
            break
    return 1 if consecutivas_actuales == consecutivas else 0

# Función de evaluación de la posición actual del tablero
def funcion_evaluacion(tablero):
    ai_cuatro = conteo_consecutivas(tablero, IA, 4)
    ai_tres = conteo_consecutivas(tablero, IA, 3)
    ai_dos = conteo_consecutivas(tablero, IA, 2)
    jugador_cuatro = conteo_consecutivas(tablero, JUGADOR, 4)
    jugador_tres = conteo_consecutivas(tablero, JUGADOR, 3)
    jugador_dos = conteo_consecutivas(tablero, JUGADOR, 2)
    return (ai_cuatro * 10 + ai_tres * 5 + ai_dos * 2) - (jugador_cuatro * 10 + jugador_tres * 5 + jugador_dos * 2)

# Función para verificar si hay un estado de victoria en el tablero
def estado_victoria(tablero, pieza):
    for fila in range(FILAS):
        for col in range(COLUMNAS-3):
            if all(tablero[fila][col + i] == pieza for i in range(4)):
                return True

    for col in range(COLUMNAS):
        for fila in range(FILAS-3):
            if all(tablero[fila + i][col] == pieza for i in range(4)):
                return True

    for fila in range(FILAS-3):
        for col in range(COLUMNAS-3):
            if all(tablero[fila + i][col + i] == pieza for i in range(4)):
                return True

    for fila in range(3, FILAS):
        for col in range(COLUMNAS-3):
            if all(tablero[fila - i][col + i] == pieza for i in range(4)):
                return True

    return False

# Función para verificar si el juego ha llegado a un nodo terminal
def es_nodo_terminal(tablero):
    return estado_victoria(tablero, JUGADOR) or estado_victoria(tablero, IA) or not obtener_columnas_validas(tablero) or tablero_lleno(tablero)

# Nueva función para verificar si el tablero está lleno
def tablero_lleno(tablero):
    return all(not es_columna_valida(tablero, col) for col in range(COLUMNAS))

# Función para verificar si una columna específica es válida
def es_columna_valida(tablero, col):
    return obtener_fila_libre(tablero, col) is not None

# Función para obtener las columnas válidas en el tablero
def obtener_columnas_validas(tablero):
    return [col for col in range(1, COLUMNAS + 1) if es_columna_valida(tablero, col - 1)]

# Algoritmo Minimax para tomar decisiones en el juego
def minimax(tablero, profundidad, alfa, beta, jugador):
    columnas_validas = obtener_columnas_validas(tablero)
    nodo_terminal = es_nodo_terminal(tablero)

    if profundidad == 0 or nodo_terminal:
        if nodo_terminal:
            if estado_victoria(tablero, IA):
                return (None, 100000000000000)
            elif estado_victoria(tablero, JUGADOR):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, funcion_evaluacion(tablero))

    if jugador == IA:
        max_valor = -math.inf
        columna = random.choice(columnas_validas)

        for col in columnas_validas:
            tablero_copia = [fila[:] for fila in tablero]
            if soltar_ficha(tablero_copia, col - 1, IA):
                nuevo_puntaje = minimax(tablero_copia, profundidad-1, alfa, beta, JUGADOR)[1]
                if nuevo_puntaje > max_valor:
                    max_valor = nuevo_puntaje
                    columna = col
                alfa = max(alfa, max_valor)
                if alfa >= beta:
                    break

        return columna, max_valor
    else:
        min_valor = math.inf
        columna = random.choice(columnas_validas)

        for col in columnas_validas:
            tablero_copia = [fila[:] for fila in tablero]
            if soltar_ficha(tablero_copia, col - 1, JUGADOR):
                nuevo_puntaje = minimax(tablero_copia, profundidad-1, alfa, beta, IA)[1]
                if nuevo_puntaje < min_valor:
                    min_valor = nuevo_puntaje
                    columna = col
                beta = min(beta, min_valor)
                if alfa >= beta:
                    break

        return columna, min_valor

# Inicialización y muestra del tablero
tablero = crear_tablero()
print("\nTablero Inicial:\n")
imprimir_tablero(tablero)
print()

# Juego principal
fin_del_juego = False
turno = JUGADOR

while not fin_del_juego:
    if turno == JUGADOR:
        print("Turno del Jugador 1:\n")
        while True:
            try:
                col = int(input("Ingrese la columna (1-7): "))
                print()
                if 1 <= col <= COLUMNAS and es_columna_valida(tablero, col - 1):
                    soltar_ficha(tablero, col - 1, JUGADOR)
                    if estado_victoria(tablero, JUGADOR):
                        fin_del_juego = True
                        print("¡Gano el Jugador 1!\n")
                    turno = IA
                    break
                else:
                    print("*** Columna inválida, ingrese el número de columna nuevamente ***\n")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    else:
        print("Turno de Jugador 2:\n")
        col, _ = minimax(tablero, 4, -math.inf, math.inf, IA)
        if es_columna_valida(tablero, col - 1):
            soltar_ficha(tablero, col - 1, IA)
            if estado_victoria(tablero, IA):
                fin_del_juego = True
                print("¡Gano el Jugador 2!\n")
            turno = JUGADOR

    imprimir_tablero(tablero)
    print()

    # Verificar empate
    if tablero_lleno(tablero) and not estado_victoria(tablero, JUGADOR) and not estado_victoria(tablero, IA):
        fin_del_juego = True
        print("¡Empate!\n")

print("Fin del juego :)\n")