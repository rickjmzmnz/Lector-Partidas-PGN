import chess
import chess.pgn
import chess.svg
import types

def abrePGN(pgn):
    partida = chess.pgn.read_game(pgn)
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
    
def obtenListaMov(partida):
    
    temp = partida
    longi = 0
    #Hace los movimientos de la partida
    for move in temp.main_line():
        longi += 1

    lista = [None] * longi
    pos = 0
    for move in first.main_line():
        lista[pos] = move
        pos += 1

def obtenSvg(tablero):
    svg = chess.svg.board(board=tablero)
    return svg

def siguienteJugada(jugada,tablero):
    tablero.push(jugada)

def anteriorJugada(tablero):
    tablero.pop()
    
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
    
    
def prueba(pgn):
    #Abrir archivo pgn
    #pgn = open("Kasparov.pgn")
    
    #Leer cada partida del archivo
    first = chess.pgn.read_game(pgn)
    second = chess.pgn.read_game(pgn)

    #print first
    #print(first.headers["Event"])
    #print second

    #Obtiene el tablero
    board = first.board()
    moves = first.main_line()
    allMoves = first.board().variation_san(moves)
    print(allMoves)

    """
    nodo = first
    while not nodo.is_end():
        nodoSig = nodo.variations[0]
        print(nodo.board().san(nodoSig.move))
        nodo = nodoSig
    """
    #move = (first.main_line().next())
    #print((first.main_line().next()))

    temp = first
    
    longi = 0
    #Hace los movimientos de la partida
    for move in temp.main_line():
        #print(move)
        #board.push(move)
        #print(board)
        #print("\n")
        longi += 1

    print(longi)
        
    lista = [None] * longi
    print(len(lista))
    pos = 0
    for move in first.main_line():
        lista[pos] = move
        pos += 1

    print(lista)
        
    #Genera el svg del tablero
    svg = chess.svg.board(board=board)
    return svg

