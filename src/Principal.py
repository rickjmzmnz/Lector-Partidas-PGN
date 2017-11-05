from Tkinter import *
from PIL import ImageTk, Image
from Lector import *
import tkFileDialog
import cairo
import rsvg
import os
import types

class Interfaz(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.pack(fill=BOTH,expand=True)
        self.creaBotones()

    def creaBotones(self):
        botonAbrir = Button(self,text="Cargar archivo",command=self.cargaArchivo)
        botonAbrir.place(x=10,y=10)

        botonSalir = Button(self,text="Salir",command=self.salir)
        botonSalir.place(x=150,y=10)
        
    def cargaArchivo(self):
        archivo = tkFileDialog.askopenfilename()
        pgn = open(archivo)
        svg = abrePGN(pgn)
        self.svgToImage(svg)

    def svgToImage(self,svg):
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 640,480)
        ctx = cairo.Context(img)
        handle= rsvg.Handle(None, str(svg))
        handle.render_cairo(ctx)
        img.write_to_png("svg.png")

        
    def salir(self):
        os._exit(0)
        
if __name__=="__main__":
    root = Tk()
    root.geometry("500x500")
    root.title("Lector PGN")
    root.wm_state("normal")
    app = Interfaz(root)
    root.mainloop()
