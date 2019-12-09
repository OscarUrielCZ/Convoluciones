from tkinter import *
from tkinter import messagebox as MessageBox
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from secuencia import Secuencia

def _quit(root):
    root.quit()
    root.destroy()

def valido(*args):
    for arg in args:
        if arg == '':
            return False
    return True

def obtener_secuencia(secuencia):
    secuencia = secuencia.split(',')
    return list(map(lambda numero: float(numero.strip()), secuencia))

def obtener_tipo(periodica):
    if periodica == 1:
        return 'p'
    return 'np'

def mostrarconvolusion(secuencia1, periodica1, origen1, secuencia2, periodica2, origen2):
    global fder, fgra, fig, canvas, res
    if not valido(secuencia1, origen1, secuencia2, origen2):
        MessageBox.showerror("Error", "Algunos campos están vacios")
        return

    secuencia1 = obtener_secuencia(secuencia1)
    secuencia2 = obtener_secuencia(secuencia2)
    t1 = obtener_tipo(periodica1) 
    t2 = obtener_tipo(periodica2) 

    sec1 = Secuencia(secuencia1, int(origen1)-1, t1)
    sec2 = Secuencia(secuencia2, int(origen2)-1, t2)

    conv = sec1.convolusion(sec2)
    res.set(conv.resultado())
    conv.graficar(fig)
    fgra.destroy()
    fgra = Frame(fder)
    fgra.pack()

    canvas = FigureCanvasTkAgg(fig, master=fgra)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, fgra)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

def mostrar_grafica(secuencia, periodica, origen):
    if not valido(secuencia, origen):
        MessageBox.showerror("Error", "Algunos campos están vacios")
        return

    secuencia1 = obtener_secuencia(secuencia)
    t1 = obtener_tipo(periodica) 
    sec = Secuencia(secuencia1, int(origen)-1, t1)
    sec.desplegar_grafica()

def mostrar_info():
    MessageBox.showinfo('Instrucciones', 'Para secuencias periodicas, sólo ingresa los elementos del periodo.\nEl origen es la posicíon del elemento donde n=0')

def main():
    global fder, fgra, fig, canvas, res
    root = Tk()
    root.title('Convoluciones')

    fizq = Frame(root)
    fder = Frame(root)
    farr = Frame(fizq)
    faba = Frame(fizq)
    fsec11 = Frame(farr)
    fsec12 = Frame(farr)
    fsec13 = Frame(farr)
    fsec21 = Frame(farr)
    fsec22 = Frame(farr)
    fsec23 = Frame(farr)
    sec1 = Entry(fsec11)
    sec2 = Entry(fsec21)
    or1 = Entry(fsec12)
    or2 = Entry(fsec22)
    fgra = Frame(fder)
    fres = Frame(fizq)

    per1 = IntVar()
    per2 = IntVar()
    fig = Figure(figsize=(5, 4), dpi=100)
    res = StringVar()

    # Información
    fizq.pack(side='left')
    fder.pack(side='left')
    farr.pack()
    fsec11.pack()
    fsec12.pack()
    fsec13.pack()
    Label(farr, text=' ', font=('Helvetica', 6)).pack()
    Label(farr, text='*', font=('Helvetica', 20)).pack()
    fsec21.pack()
    fsec22.pack()
    fsec23.pack()
    faba.pack()
    fgra.pack()
    # Primera secuencia
    Label(fsec11, text='Primera secuencia').pack()
    Label(fsec11, text='Elementos:').pack(side='left')
    sec1.pack(side='left')
    Label(fsec12, text='      Origen:').pack(side='left')
    or1.pack(side='left')
    Checkbutton(fsec13, text='Periodica', variable=per1, onvalue=1, offvalue=0).pack(side='left')
    Button(fsec13, text='Mostrar gráfica', command=lambda: mostrar_grafica(sec1.get(), per1.get(), or1.get())).pack(side='left')
    # Segunda secuencia
    Label(fsec21, text='Segunda secuencia').pack()
    Label(fsec21, text='Elementos:').pack(side='left')
    sec2.pack(side='left')
    Label(fsec22, text='      Origen:').pack(side='left')
    or2.pack(side='left')
    Checkbutton(fsec23, text='Periodica', variable=per2, onvalue=1, offvalue=0).pack(side='left')
    Button(fsec23, text='Mostrar gráfica', command=lambda: mostrar_grafica(sec2.get(), per2.get(), or2.get())).pack(side='left')
    # Resultado
    Label(fizq, text='=', font=('Helvetica', 16)).pack()
    fres.pack()
    Label(fres, textvariable=res, font=('Helvetica', 12)).pack()
    
    # Gráfica
    canvas = FigureCanvasTkAgg(fig, master=fgra)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    # Botón
    Label(fizq, text=' ').pack()
    Button(fizq, text='Convolusionar', command=lambda: \
        mostrarconvolusion(sec1.get(), per1.get(), or1.get(), sec2.get(), per2.get(), or2.get())).pack()
    Button(fizq, text='  Información  ', command=lambda:mostrar_info()).pack()
    Button(fizq, text='         Salir         ', command=lambda:_quit(root)).pack()

    root.mainloop()

fder = None
fgra = None
res = None
fig = None
canvas = None

if __name__ == '__main__':
    main()