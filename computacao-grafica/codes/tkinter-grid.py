from tkinter import *

def cria_canvas(pai, width, height, escala):
    tela = Canvas(
            pai,
            width=width,
            height=height,
            bg='#ffffff')
    desenha_grade(tela,escala)
    tela.pack()
    return tela

def desenha_grade(canvas,escala):
    width = int(canvas['width'])
    height = int(canvas['height'])
    for x in range(0,width,escala):
        canvas.create_line(x,0,x,height)
    for y in range(0,height,escala):
        canvas.create_line(0,y,width,y)

def pinta_pixel(tela,x,y,escala):
    x *= escala
    y *= escala
    xfim = x+escala
    yfim = y+escala
    tela.create_rectangle(x,y,xfim,yfim,fill='black')

def xyscala(x,y,escala):
    x //= escala
    y //= escala
    return x,y

def main():
    escala = 10
    width = 500
    height = 500

    janela = Tk()
    janela.title('CG-2019.2')
    janela.resizable(False,False)

    frame_pixels = Frame(janela)
    frame_pixels.grid(row=0,column=0)

    frame_infos = Frame(janela,bd=5)
    frame_infos.grid(row=0,column=1)

    tela = cria_canvas(frame_pixels,width,height,escala)

    label_ponto = Label(frame_infos,text='(x,y)')
    label_ponto.pack()

    def motion_mouse(event):
        x,y = xyscala(event.x,event.y,escala)
        label_ponto['text'] = str((x,y))

    def leave_mouse(event):
        label_ponto['text']='(x,y)'

    def press_mouse(event):
        x,y = xyscala(event.x,event.y,escala)
        pinta_pixel(tela,x,y,escala)

    tela.bind('<Motion>',motion_mouse)
    tela.bind('<Leave>',leave_mouse)
    tela.bind('<ButtonPress>',press_mouse)

    from classes import Poligono
    quadrado = Poligono((1,1),(1,15),(15,15),(15,1))

    def pinta_reta(reta):
        for ponto in reta.cartesiano:
            x,y = ponto
            pinta_pixel(tela,x,y,escala)

    for reta in quadrado.retas: pinta_reta(reta)
    janela.mainloop()

main()
