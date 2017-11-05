import chess
import chess.pgn
import chess.svg
import types

def abrePGN(pgn):
    #Abrir archivo pgn
    #pgn = open("Kasparov.pgn")
    print(type(pgn))
    
    #Leer cada partida del archivo
    first = chess.pgn.read_game(pgn)
    second = chess.pgn.read_game(pgn)

    #print first
    #print(first.headers["Event"])
    #print second

    #Obtiene el tablero
    board = first.board()

    #Hace los movimientos de la partida
    for move in first.main_line():
        board.push(move)
        #print(board)
        #print("\n")

    #Genera el svg del tablero
    svg = chess.svg.board(board=board)
    return svg

