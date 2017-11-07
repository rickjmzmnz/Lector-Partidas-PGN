import chess
import chess.pgn
import chess.svg
import types

"""
Abre un archivo pgn
Se obtiene la informacion del archivo
Y se regresa en una lista
"""
def abrePGN(partida):
    evento = partida.headers["Event"]
    lugar = partida.headers["Site"]
    fecha = partida.headers["Date"]
    ronda = partida.headers["Round"]
    blanco = partida.headers["White"]
    negro = partida.headers["Black"]
    resultado = partida.headers["Result"]
    tablero = partida.board()
    moves = partida.main_line()
    movimientos = partida.board().variation_san(moves)

    return [partida,evento,lugar,fecha,ronda,blanco,negro,resultado,tablero,movimientos]

"""
Se obtiene la representacion del tablero en formato svg
"""
def obtenSvg(tablero):
    svg = chess.svg.board(board=tablero)
    return svg

"""
Dado un tablero y una jugada
Se realiza la jugada en el tablero
"""
def siguienteJugada(jugada,tablero):
    tablero.push(jugada)

"""
Dado un tablero, se regresa a la jugada anterior
"""
def anteriorJugada(tablero):
    tablero.pop()

"""
Dada una partida de un archivo pgn
Se obtiene cada jugada de ella
Y se regresan en una lista
"""
def obtenJugadas(partida):
    temp = partida
    
    longi = 0
    for move in temp.main_line():
        longi += 1
 
    lista = [None] * longi
    pos = 0
    for move in partida.main_line():
        lista[pos] = move
        pos += 1

    return lista

"""
Cuenta el numero de partidas de un archivo
"""
def cuentaPartidas(pgn):
    lista = []
    bandera = True
    juego = None

    while(bandera):
        juego = chess.pgn.read_game(pgn)
        if(juego != None):
            lista.append(juego)
        else:
            bandera = False

    return lista
    
