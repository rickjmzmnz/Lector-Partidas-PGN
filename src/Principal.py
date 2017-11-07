from __future__ import division
from Tkinter import *
from PIL import ImageTk, Image
from Lector import *
import tkFileDialog
import tkMessageBox
import cairo
import rsvg
import os
import io
import types

class Interfaz(Frame):

    """
    Constructor de la clase
    Se crea el canvas donde se pondra el tablero
    Se crean los botones y etiquetas de la interfaz
    """
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.pack(fill=BOTH,expand=True)
        self.creaCanvas()
        self.creaBotones()
        self.creaListbox()
        self.creaEtiquetas()
        self.acciones()
        self.listaPartidas = None
        self.partida = None
        self.tablero = None
        self.jugadas = None
        self.numeroJugada = 0

    """
    Dibuja el canvas donde se colocara el tablero
    """
    def creaCanvas(self):
        self.canvas = Canvas(self, bg="white",width=400,height=400)
        self.canvas.place(x=500,y=10)

    """
    Se crean los botones para las diferentes acciones de la interfaz
    """
    def creaBotones(self):
        botonAbrir = Button(self,text="Cargar archivo",command=self.cuentaPartidas)
        botonAbrir.place(x=10,y=10)

        botonSalir = Button(self,text="Salir",command=self.salir)
        botonSalir.place(x=150,y=10)

        botonSig = Button(self,text="Siguiente jugada",command=self.siguienteMovimiento)
        botonSig.place(x=650,y=430)

        botonAnt = Button(self,text="Anterior jugada",command=self.anteriorMovimiento)
        botonAnt.place(x=500,y=430)

    """
    Crea el listbox donde se van a mostrar todas las partidas del archivo cargado
    """
    def creaListbox(self):
        scrollbar = Scrollbar(self,orient=VERTICAL)
        scrollbar2 = Scrollbar(self,orient=HORIZONTAL)
        self.listbox = Listbox(self,yscrollcommand=scrollbar.set,xscrollcommand=scrollbar2.set,height=18,width=36)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.place(x=475,y=10)
        scrollbar2.config(command=self.listbox.xview)
        scrollbar2.place(x=220,y=285)
        self.listbox.place(x=220,y=10)

    """
    Carga la partida que sea seleccionada en la lista de partidas cargadas
    """
    def acciones(self):
        self.listbox.bind("<Double-Button-1>",self.cargaPartida)
            
    """
    Se colocan las etiquetas para detallar la informacion
    Del archivo PGN que se cargue
    """
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

        jugada = Label(self,text="Jugada:")
        jugada.place(x=800,y=430)

        self.jugadaPart = Label(self,text="-")
        self.jugadaPart.place(x=850,y=430)

    """
    La partida seleccionada de la lista es cargada y se obtiene toda la informacion de ella
    """
    def cargaPartida(self,evento):
        selec = self.listbox.curselection()
        indice = selec[0]
        partida = self.listaPartidas[indice]
    
        lista = abrePGN(partida)

        self.partida = None
        self.tablero = None
        self.jugadas = None
        self.numeroJugada = 0
        
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

    """
    Carga todas las partidas dentro de un archivo pgn
    """
    def cuentaPartidas(self):
        self.listbox.delete(0,END)
        archivo = tkFileDialog.askopenfilename()
        pgn = open(archivo)
        self.listaPartidas = cuentaPartidas(pgn)
        for i in range(len(self.listaPartidas)):
            partida = self.listaPartidas[i]
            self.listbox.insert(END,partida)


    """
    Funcion para poder ajustar una cadena larga a la interfaz
    """
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

    """
    Realiza el siguiente movimiento de la partida
    """
    def siguienteMovimiento(self):
        if self.canvas.find_all() != ():
            if (self.numeroJugada < len(self.jugadas)):
                jugada = self.jugadas[self.numeroJugada]
                self.jugadaPart.config(text=str(jugada))
                self.numeroJugada += 1
                siguienteJugada(jugada,self.tablero)
                svg = obtenSvg(self.tablero)
                self.svgToImage(svg,"tablero")
                imagen = Image.open("tablero.png")
                imagenTk = ImageTk.PhotoImage(imagen)
                self.canvas.image = imagenTk
                self.canvas.create_image(imagenTk.width()/2,imagenTk.height()/2,anchor=CENTER,image=imagenTk,tags="tab")
            else:
                tkMessageBox.showwarning("Error","La partida ha terminado")
        else:
            tkMessageBox.showwarning("Error","Carga una partida PGN")

    """
    Se regresa a un movimiento anterior de la partida
    """
    def anteriorMovimiento(self):
        if self.canvas.find_all() != ():
            if(self.numeroJugada > 0):
                self.numeroJugada += (-1)
                jugada = self.jugadas[self.numeroJugada]
                self.jugadaPart.config(text=str(jugada))
                anteriorJugada(self.tablero)
                svg = obtenSvg(self.tablero)
                self.svgToImage(svg,"tablero")
                imagen = Image.open("tablero.png")
                imagenTk = ImageTk.PhotoImage(imagen)
                self.canvas.image = imagenTk
                self.canvas.create_image(imagenTk.width()/2,imagenTk.height()/2,anchor=CENTER,image=imagenTk,tags="tab")
            else:
                tkMessageBox.showwarning("Error","Ya no hay jugada previa")
        else:
            tkMessageBox.showwarning("Error","Carga una partida PGN")

    """
    Convierte un archivo SVG a uno PNG
    """
    def svgToImage(self,svg,nombre):
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 640,480)
        ctx = cairo.Context(img)
        handle= rsvg.Handle(None, str(svg))
        handle.render_cairo(ctx)
        img.write_to_png(nombre+".png")

    """
    Borra el archivo png del tablero generado por el programa
    Y se sale del programa
    """
    def salir(self):
        try:
            os.remove("tablero.png")
            os._exit(0)
        except OSError:
            os._exit(0)

"""
Main del programa
Crea una ventana y manda a llamar al constructor de la clase
Para poder interactuar con las acciones que se puedan realizar
"""
if __name__=="__main__":
    root = Tk()
    root.geometry("920x500")
    root.title("Lector PGN")
    root.wm_state("normal")
    app = Interfaz(root)
    root.mainloop()
