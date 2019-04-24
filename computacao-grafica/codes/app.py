import tkinter as tk
from tkinter.colorchooser import askcolor
#
#No manjaro, necessário usar:
# `pacman -S tk`
#
class App(tk.Tk):
    def __init__(self, escala=10, largura=600, altura=600, titulo='CG-2019.2'):
        super().__init__()
        # MODOS = LIVRE, LINHA, CIRCULO, CURVA, PREE_REC, PREE_SCAN
        self.title(titulo)
        self.altura = altura
        self.largura = largura
        self.escala = escala
        self.ferramentas = None
        self.canvas = None
        self.frame_buffer = []
        self.cor = 'black'
        self.modos = None

    def show(self):
        self.canvas = self.cria_canvas() # cria canvas na tela do app
        self.ferramentas = self.cria_ferramentas() # cria caixa de ferramentas na tela do app
        self.geometry("%dx%d+0+0" % (self.largura+int(self.largura*0.13), self.altura)) # dimensões totais da 
        self.resizable(False,False)
        self.mainloop()

    def cria_ferramentas(self):
        frame_ferramenta = tk.Frame(self)
        frame_ferramenta.grid(row=0,column=1)
        label_ponto = tk.Label(frame_ferramenta,text='(00,00)')
        label_ponto.pack()
        # eventos para label_ponto
        def motion_mouse(event):
            x,y = self.xyscala(event.x,event.y)
            x = '0'+str(x) if x < 10 else str(x)
            y = '0'+str(y) if y < 10 else str(y)
            label_ponto['text'] = '('+x+','+y+')'
        def leave_mouse(event):
            label_ponto['text']='(00,00)'
        def press_mouse(event): 
            x,y = self.xyscala(event.x,event.y)
            self.frame_buffer.append((x,y,self.cor))
            #self.pinta_pixel(x,y,self.cor)
            self.pinta_buffer()
        self.canvas.bind('<Motion>',motion_mouse) # liga função ao evento
        self.canvas.bind('<Leave>',leave_mouse)
        self.canvas.bind('<Button-1>',press_mouse)
        # instância do label que muda a cor
        label_cor = tk.Label(frame_ferramenta,text='      ',bg=self.cor)
        # evento para mudança de cor
        def muda_cor(event):
            _,hex = askcolor(color=self.cor) # método nativo da lib tkinter
            if hex: # se retornar uma cor, e não None (em caso de cancalemento da escolha)
                self.cor = hex
                label_cor.configure(bg=self.cor)
        label_cor.bind('<Button-1>',muda_cor)
        label_cor.pack()
        # limpar tela
        def limpar_tela(event):
            self.frame_buffer = []
            self.canvas.delete('all')
            for x in range(0,self.largura,self.escala):
                self.canvas.create_line(x,0,x,self.altura)
            for y in range(0,self.altura,self.escala):
                self.canvas.create_line(0,y,self.largura,y)

        limpar = tk.Button(frame_ferramenta,text='Limpar',width=6)
        limpar.bind('<Button-1>',limpar_tela)
        limpar.pack()

        self.cria_botoes_modos(frame_ferramenta)
        return {
            'ponto':label_ponto,
            'cor':label_cor
        }
    
    def cria_botoes_modos(self,pai):
        w = 6
        botoes = [
            tk.Button(pai,text='Linha',command=None,width=w),
            tk.Button(pai,text='Círculo',command=None,width=w),
            tk.Button(pai,text='Bezier',command=None,width=w),
            tk.Button(pai,text='Pre. Rec',command=None,width=w),
            tk.Button(pai,text='Pre. Scan',command=None,width=w),
        ]
        for botao in botoes:
            botao.pack()
        return botoes
    def cria_canvas(self):
        # guarda parâmetros para criação do canvas
        escala = self.escala
        largura = self.largura
        altura = self.altura
        # instância do canvas
        canvas = tk.Canvas(self,width=largura,height=altura,bg='white')
        canvas.grid(row=0)
        # pintura da grade de pixels
        for x in range(0,largura,escala):
            canvas.create_line(x,0,x,altura)
        for y in range(0,altura,self.escala):
            canvas.create_line(0,y,largura,y)
        return canvas
    
    def pinta_pixel(self,x,y,cor):
        x *= self.escala
        y *= self.escala
        xfim = x+self.escala
        yfim = y+self.escala
        self.canvas.create_rectangle(x,y,xfim,yfim,fill=cor)
    def pinta_buffer(self):
        for pixel in self.frame_buffer:
            x,y,cor = pixel
            self.pinta_pixel(x,y,cor)
    
    def xyscala(self,x,y):
        x //= self.escala
        y //= self.escala
        return x,y

app = App(escala=20)
app.show()
exit()