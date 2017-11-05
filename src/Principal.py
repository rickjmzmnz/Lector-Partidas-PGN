from __future__ import division
from Tkinter import *
from PIL import ImageTk, Image
from Lector import *
import tkFileDialog
import chess
import chess.pgn
import cairo
import rsvg
import os
import io
import types

class Interfaz(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.pack(fill=BOTH,expand=True)
        self.creaCanvas()
        self.creaBotones()
        self.creaEtiquetas()
        self.partida = None
        self.tablero = None
        self.jugadas = None
        self.numeroJugada = 0
        
    def creaCanvas(self):
        self.canvas = Canvas(self, bg="white",width=400,height=400)
        self.canvas.place(x=500,y=10)
        
    def creaBotones(self):
        botonAbrir = Button(self,text="Cargar archivo",command=self.cargaArchivo)
        botonAbrir.place(x=10,y=10)

        botonSalir = Button(self,text="Salir",command=self.salir)
        botonSalir.place(x=150,y=10)

        botonSig = Button(self,text="Siguiente jugada",command=self.siguienteMovimiento)
        botonSig.place(x=500,y=430)

        botonAnt = Button(self,text="Anterior jugada",command=self.anteriorMovimiento)
        botonAnt.place(x=650,y=430)


    def creaEtiquetas(self):
        info = Label(self,text="Informacion de la partida")
        info.place(x=10,y=60)

        evento = Label(self,text="Evento:")
        evento.place(x=10,y=90)

        self.eventoPart = Label(self,text="-")
        self.eventoPart.place(x=90,y=90)
        
        lugar = Label(self,text="Lugar:")
        lugar.place(x=10,y=120)

        self.lugarPart = Label(self,text="-")
        self.lugarPart.place(x=90,y=120)
        
        fecha = Label(self,text="Fecha:")
        fecha.place(x=10,y=150)

        self.fechaPart = Label(self,text="-")
        self.fechaPart.place(x=90,y=150)

        ronda = Label(self,text="Ronda:")
        ronda.place(x=10,y=180)

        self.rondaPart = Label(self,text="-")
        self.rondaPart.place(x=90,y=180)

        blancas = Label(self,text="Blancas:")
        blancas.place(x=10,y=210)

        self.blancasPart = Label(self,text="-")
        self.blancasPart.place(x=90,y=210)

        negras = Label(self,text="Negras:")
        negras.place(x=10,y=240)

        self.negrasPart = Label(self,text="-")
        self.negrasPart.place(x=90,y=240)

        resultado = Label(self,text="Resultado:")
        resultado.place(x=10,y=270)

        self.resultadoPart = Label(self,text="-")
        self.resultadoPart.place(x=90,y=270)

        movimientos = Label(self,text="Movimientos:")
        movimientos.place(x=10,y=300)

        self.movimientosPart = Label(self,text="-")
        self.movimientosPart.place(x=90,y=300)
        
    def cargaArchivo(self):
        archivo = tkFileDialog.askopenfilename()
        pgn = open(archivo)
        lista = abrePGN(pgn)
        
        self.partida = lista[0]
        cadenaEvento = lista[1]
        cadenaLugar = lista[2]
        cadenaFecha = lista[3]
        cadenaRonda = lista[4]
        cadenaBlancas = lista[5]
        cadenaNegras = lista[6]
        cadenaResultado = lista[7]
        self.tablero = lista[8]
        cadenaMov = lista[9]
        cadenaMov = self.ajustaCadena(cadenaMov)
        
        self.eventoPart.config(text=cadenaEvento)
        self.lugarPart.config(text=cadenaLugar)
        self.fechaPart.config(text=cadenaFecha)
        self.rondaPart.config(text=cadenaRonda)
        self.blancasPart.config(text=cadenaBlancas)
        self.negrasPart.config(text=cadenaNegras)
        self.resultadoPart.config(text=cadenaResultado)
        self.movimientosPart.config(text=cadenaMov)

        svg = obtenSvg(self.tablero)
        self.svgToImage(svg,"tablero")
        imagen = Image.open("tablero.png")
        imagenTk = ImageTk.PhotoImage(imagen)
        self.canvas.image = imagenTk
        self.canvas.create_image(imagenTk.width()/2,imagenTk.height()/2,anchor=CENTER,image=imagenTk,tags="tab")

        self.jugadas = obtenJugadas(self.partida)
        print(self.jugadas)

    def ajustaCadena(self,cadena):
        nueva = ""
        partida = cadena.split()
        inicio = 0
        fin = 15
        for i in range(0,len(partida),15):
            intervalo = partida[inicio:fin]
            for j in range(len(intervalo)):
                nueva = nueva + intervalo[j] + " "
            nueva = nueva + "\n"
            inicio = fin 
            fin = fin + 15
        return nueva
        
    def siguienteMovimiento(self):
        if (self.numeroJugada < len(self.jugadas)):
            svg = obtenSvg(self.tablero)
            self.svgToImage(svg,"actual")
            jugada = self.jugadas[self.numeroJugada]
            self.numeroJugada += 1
            siguienteJugada(jugada,self.tablero)
            svg = obtenSvg(self.tablero)
            self.svgToImage(svg,"tablero")
            imagen = Image.open("tablero.png")
            imagenTk = ImageTk.PhotoImage(imagen)
            self.canvas.image = imagenTk
            self.canvas.create_image(imagenTk.width()/2,imagenTk.height()/2,anchor=CENTER,image=imagenTk,tags="tab")
            print(self.numeroJugada)

    def anteriorMovimiento(self):
        if(self.numeroJugada > 0):
            self.numeroJugada += (-1)
            anteriorJugada(self.tablero)
            svg = obtenSvg(self.tablero)
            self.svgToImage(svg,"tablero")
            imagen = Image.open("tablero.png")
            imagenTk = ImageTk.PhotoImage(imagen)
            self.canvas.image = imagenTk
            self.canvas.create_image(imagenTk.width()/2,imagenTk.height()/2,anchor=CENTER,image=imagenTk,tags="tab")
            print(self.numeroJugada)
    
    """
    Funcion para guardar el diagrama
    """
    def guardarTableroActual(self):
        diagrama = Image.new("RGB",(400,400),"white")
        nombre = "actual.png"
        ps = self.canvas.postscript()
        im = Image.open(io.BytesIO(ps.encode('utf-8')))
        im.save(nombre)
            
    def svgToImage(self,svg,nombre):
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 640,480)
        ctx = cairo.Context(img)
        handle= rsvg.Handle(None, str(svg))
        handle.render_cairo(ctx)
        img.write_to_png(nombre+".png")

        
    def salir(self):
        os._exit(0)
        
if __name__=="__main__":
    root = Tk()
    root.geometry("1000x500")
    root.title("Lector PGN")
    root.wm_state("normal")
    app = Interfaz(root)
    root.mainloop()
