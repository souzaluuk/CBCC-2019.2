import tkinter as tk
from tkinter.colorchooser import askcolor
from algoritmos import bresenham, circulo, curva
#
#No manjaro, necessário usar:
# `pacman -S tk`
#
class App(tk.Tk):
    w_bt = 6
    frame_buffer_aux = []
    def __init__(self, escala=10, largura=600, altura=600, titulo='CG-2019.2'):
        super().__init__()
        # MODOS = LIVRE, LINHA, CIRCULO, CURVA, PREE_REC, PREE_SCAN
        self.title(titulo)
        self.altura = altura
        self.largura = largura
        self.escala = escala
        self.ferramentas = None
        self.canvas = None
        self.cor = 'black'
        self.frame_buffer = None
        self.modo = 'LIVRE'

    def limpa_buffer(self):
        # inicializa frame buffer
        self.frame_buffer = [['white' for x in range(self.largura//self.escala)] for y in range(self.altura//self.escala)]
        self.frame_buffer_aux = []
        self.pinta_buffer([(x,y) for x in range(self.largura//self.escala) for y in range(self.altura//self.escala)])

    def show(self):
        self.canvas = self.cria_canvas() # cria canvas na tela do app
        self.limpa_buffer() # inicializa frame_buffer
        self.cria_eventos() # criação dos eventos de botões e cliques no canvas
        self.ferramentas = self.cria_ferramentas() # cria caixa de ferramentas na tela do app
        self.geometry("%dx%d+0+0" % (self.largura+int(self.largura*0.13), self.altura)) # dimensões totais da 
        self.resizable(False,False)
        self.mainloop()

    def cria_eventos(self):
        modo = self.modo
        f_event = None
        self.frame_buffer_aux = []
        if modo=='LIVRE':
            def f(event):
                x,y = self.xyscala(event.x,event.y) # converte de acordo com escala
                self.add_frame_buffer(x,y,self.cor) # adiciona cor no pixel indicado
                self.pinta_buffer([(x,y)]) # pinta diretamente o pixel
            f_event = f
        elif modo=='LINHA':
            # pintando linha a cada novo clique ( para finalizar uma linha)
            # para finalização de uma linha deve-se mudar o modo de pintura, ou clicar em linha novamente
            def f(event):
                x,y = self.xyscala(event.x,event.y) # converte de acordo com escala
                if self.frame_buffer_aux: # caso haja algo no buffer auxiliar
                    x0,y0 = self.frame_buffer_aux[-1]
                    self.frame_buffer_aux = bresenham((x0,y0),(x,y))
                    for x,y in self.frame_buffer_aux:
                        self.add_frame_buffer(x,y,self.cor)
                else: # se buffer auxiliar vazio
                    self.frame_buffer_aux.append((x,y))
                    self.add_frame_buffer(x,y,self.cor)
                self.pinta_buffer(self.frame_buffer_aux)
            f_event = f
        elif modo=='CIRCULO':
            # pintando linha a cada novo clique ( para finalizar uma linha)
            # para finalização de uma linha deve-se mudar o modo de pintura, ou clicar em linha novamente
            def f(event):
                x,y = self.xyscala(event.x,event.y) # converte de acordo com escala
                if self.frame_buffer_aux: # caso haja algo no buffer auxiliar
                    x0,y0 = self.frame_buffer_aux[-1]
                    self.frame_buffer_aux = list(
                        filter(
                            lambda p: self.largura//self.escala>p[0]>=0<=p[1]<self.altura//self.escala,
                            circulo((x0,y0),(x,y))
                        )
                    )
                    for x,y in self.frame_buffer_aux:
                        self.add_frame_buffer(x,y,self.cor)
                    self.pinta_buffer(self.frame_buffer_aux)
                    self.frame_buffer_aux=[]
                else: # se buffer auxiliar vazio
                    self.frame_buffer_aux.append((x,y)) # armazena a posição do raio
            f_event = f
        elif modo=='BEZIER':
            def f(event):
                x,y = self.xyscala(event.x,event.y) # converte de acordo com escala
                self.frame_buffer_aux.append((x,y))
                if len(self.frame_buffer_aux)==4:
                    print('buffer:',self.frame_buffer_aux)
                    self.frame_buffer_aux = curva(self.frame_buffer_aux)
                    for x,y in self.frame_buffer_aux:
                        self.add_frame_buffer(x,y,self.cor)
                    self.pinta_buffer(self.frame_buffer_aux) # sempre após o add_frame_buffer
                    self.frame_buffer_aux = []
            f_event = f
        # substitui evento modo de pintura atual
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>',f_event)

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
        self.canvas.bind('<Motion>',motion_mouse) # liga função ao evento
        self.canvas.bind('<Leave>',leave_mouse)
        #self.canvas.bind('<Button-1>',self.clica_canvas)
        # instância do label que muda a cor
        label_cor = tk.Label(frame_ferramenta,bg=self.cor,width=self.w_bt)
        # evento para mudança de cor
        def muda_cor(event):
            _,hex = askcolor(color=self.cor) # método nativo da lib tkinter
            if hex: # se retornar uma cor, e não None (em caso de cancalemento da escolha)
                self.cor = hex
                label_cor.configure(bg=self.cor)
        label_cor.bind('<Button-1>',muda_cor)
        label_cor.pack()

        botoes = self.cria_botoes_modos(frame_ferramenta)
        return {
            'ponto':label_ponto,
            'cor':label_cor,
            'botoes':botoes
        }

    def muda_opcao(self,modo):
        self.modo = modo
        self.cria_eventos()

    def cria_botoes_modos(self,pai):
        w_bt = self.w_bt
        botoes = [
            tk.Button(pai,text='Limpar',command=self.limpa_buffer,width=w_bt),
            tk.Button(pai,text='Livre',command=lambda: self.muda_opcao('LIVRE'),width=w_bt),
            tk.Button(pai,text='Linha',command=lambda: self.muda_opcao('LINHA'),width=w_bt),
            tk.Button(pai,text='Círculo',command=lambda: self.muda_opcao('CIRCULO'),width=w_bt),
            tk.Button(pai,text='Bezier',command=lambda: self.muda_opcao('BEZIER'),width=w_bt),
            tk.Button(pai,text='Pre. Rec',command=lambda: self.muda_opcao('scanline'),width=w_bt),
            tk.Button(pai,text='Pre. Scan',command=lambda: self.muda_opcao('recursivo'),width=w_bt),
        ]
        for botao in botoes:
            botao.pack()
        return botoes
    def cria_canvas(self):
        # guarda parâmetros para criação do canvas
        largura = self.largura
        altura = self.altura
        # instância do canvas
        canvas = tk.Canvas(self,width=largura-2,height=altura)
        canvas.grid(row=0)
        return canvas

    def add_frame_buffer(self,x,y,cor):
        self.frame_buffer[x][y] = cor

    def pinta_buffer(self,coord):
        # exemplo de coord [(x0,y0),(x1,y1),...,(xn,yn)]
        escala = self.escala
        for pixel in coord:
            x,y = pixel
            cor = self.frame_buffer[x][y]
            x = x*escala
            y = y*escala
            xfim = x+escala
            yfim = y+escala
            self.canvas.create_rectangle(
                x+1,y+1,xfim-1,yfim-1,fill=cor,outline=cor
            )
    
    def xyscala(self,x,y):
        x //= self.escala
        y //= self.escala
        return x,y

app = App(escala=20)
app.show()
exit()