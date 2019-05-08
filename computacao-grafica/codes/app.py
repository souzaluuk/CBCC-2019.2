import tkinter as tk
from tkinter.colorchooser import askcolor
from algoritmos import bresenham, circulo, curva, preenchrecursivo, preenchscanline
from elementos import *
#
#No manjaro, necessário usar:
# `pacman -S tk`
#
class App(tk.Tk):
    w_bt = 10 # largura dos botões
    frame_buffer_aux = [] # frame_buffer auxiliar
    forma_aux = None
    formas = []
    def __init__(self, escala=10, largura=600, altura=700, titulo='CG-2019.2'):
        super().__init__()
        # MODOS = LIVRE, LINHA, CIRCULO, BEZIER, PREE_REC, PREE_SCAN, CORTE_LINHA, TRANSLAD
        self.title(titulo)
        self.escala = escala
        self.altura = altura//escala # quantidade de linhas (y)
        self.largura = largura//escala # quantidade de colunas (x)
        self.ferramentas = None
        self.canvas = None
        self.frame_buffer = None
        self.lista_box = None
        self.entrada_xy = None
        self.cor = '#000000'
        self.modo = 'LINHA' # modo inicial

    def limpa_buffer(self):
        # inicializa frame buffer
        self.frame_buffer = [['#ffffff' for x in range(self.largura)] for y in range(self.altura)]
        self.forma_aux = None
        self.pinta_buffer()

    def show(self):
        self.canvas = self.cria_canvas() # cria canvas na tela do app
        self.limpa_buffer() # inicializa frame_buffer
        self.cria_eventos() # criação dos eventos de botões e cliques no canvas
        self.ferramentas = self.cria_ferramentas() # cria caixa de ferramentas na tela do app
        largura = (self.largura*self.escala)+((1+self.w_bt)*10) # largura da janela total
        altura = self.altura*self.escala # altura da janela total
        self.geometry("%dx%d+0+0" % (largura,altura)) # dimensões totais da tela do app
        self.resizable(False,False) # não redimensiona a janela
        self.mainloop()

    def cria_ferramentas(self):
        frame_ferramenta = tk.Frame(self) # frame para adicionar auxiliares ao Canvas
        frame_ferramenta.grid(row=0,column=1) # organiza ao lado do canvas (mesma linha, coluna 1)
        # eventos para label_ponto
        label_ponto = tk.Label(frame_ferramenta,text='(00,00)',height=2)
        label_ponto.pack()
        def motion_mouse(event):
            x,y = self.xyscala(event.x,event.y)
            x = '0'+str(x) if x < 10 else str(x)
            y = '0'+str(y) if y < 10 else str(y)
            label_ponto['text'] = '('+x+','+y+')'
        def leave_mouse(event): label_ponto['text']='(00,00)'
        self.canvas.bind('<Motion>',motion_mouse) # executa ao mover mouse sobre o canvas
        self.canvas.bind('<Leave>',leave_mouse) # executa ao retirar o mouse do canvas
        # lista formas
        tk.Label(frame_ferramenta,text='Polígonos:').pack()
        self.lista_box = tk.Listbox(frame_ferramenta,w=self.w_bt,height=6)
        self.lista_box.pack()

        bt_add = tk.Button(frame_ferramenta,text='+',command=self.add_forma,width=self.w_bt//2)
        bt_rm = tk.Button(frame_ferramenta,text='-',command=self.rm_forma,width=self.w_bt//2)
        self.lista_box.bind('<Double-Button-1>',lambda e: self.pinta_forma())

        bt_add.pack()
        bt_rm.pack()
        label_cor = tk.Label(frame_ferramenta,bg=self.cor,width=self.w_bt) # instância do label
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
        botoes = list()
        botoes.append(tk.Button(pai,text='Limpar',command=self.limpa_buffer,width=w_bt))
        #botoes.append(tk.Button(pai,text='Livre',command=lambda: self.muda_opcao('LIVRE'),width=w_bt))
        botoes.append(tk.Button(pai,text='Linha',command=lambda: self.muda_opcao('LINHA'),width=w_bt))
        botoes.append(tk.Button(pai,text='Círculo',command=lambda: self.muda_opcao('CIRCULO'),width=w_bt))
        botoes.append(tk.Button(pai,text='Bezier',command=lambda: self.muda_opcao('BEZIER'),width=w_bt))
        botoes.append(tk.Button(pai,text='Pre. Rec',command=lambda: self.muda_opcao('PREE_REC'),width=w_bt))
        botoes.append(tk.Button(pai,text='Pre. Scan',command=lambda: self.muda_opcao('PREE_SCAN'),width=w_bt))
        botoes.append(tk.Button(pai,text='Corte Linha',command=lambda: self.muda_opcao('CORTE_LINHA'),width=w_bt))
        botoes.append(tk.LabelFrame(pai))

        conj_translacao = botoes[-1]
        tk.Button(conj_translacao,text='Translação',command=lambda: self.muda_opcao('TRANSLAD'),width=w_bt-1).pack()
        tk.Label(conj_translacao,text=' (  X  ,  Y  ) ').pack()
        
        frame_aux = tk.Frame(conj_translacao)
        frame_aux.pack()
        self.entrada_xy = dict()
        self.entrada_xy['x'] = tk.StringVar()
        self.entrada_xy['y'] = tk.StringVar()
        tk.Entry(frame_aux,width=w_bt//2,textvariable=self.entrada_xy['x']).grid(row=0,column=0)
        tk.Entry(frame_aux,width=w_bt//2,textvariable=self.entrada_xy['y']).grid(row=0,column=1)

        for botao in botoes:
            botao.pack()
        return botoes
    
    def cria_canvas(self):
        # guarda parâmetros para criação do canvas
        largura = self.largura
        altura = self.altura
        escala = self.escala
        # instância do canvas
        canvas = tk.Canvas(self,width=(largura*escala)-2,height=(altura*escala))
        canvas.grid(row=0)
        return canvas

    def add_frame_buffer(self,x,y,cor):
        if self.largura>x>=0<=y<self.altura:
            self.frame_buffer[y][x] = cor # y -> linha ; x -> coluna

    def pinta_coord(self,coord):
        # exemplo de coord [(x0,y0),(x1,y1),...,(xn,yn)]
        escala = self.escala
        for pixel in filter(lambda p: self.largura>p[0]>=0<=p[1]<self.altura,coord):
            x,y = pixel
            cor = self.frame_buffer[y][x] # y -> linha ; x -> coluna
            x = x*escala
            y = y*escala
            xfim = x+escala
            yfim = y+escala
            self.canvas.create_rectangle(
                x+1,y+1,xfim-1,yfim-1,fill=cor,outline=cor
            )
    
    def marca_pixel(self,x,y):
        escala = self.escala
        x = x*escala
        y = y*escala
        xfim = x+escala
        yfim = y+escala
        self.canvas.create_rectangle(
            x+1,y+1,xfim-1,yfim-1,outline=self.cor
        )

    def pinta_buffer(self):
        escala = self.escala
        largura = self.largura
        altura = self.altura
        fb = self.frame_buffer
        for y in range(altura):
            for x in range(largura):
                cor = fb[y][x]
                xesc = x*escala
                yesc = y*escala
                xfim = xesc+escala
                yfim = yesc+escala
                self.canvas.create_rectangle(
                    xesc+1,yesc+1,xfim-1,yfim-1,fill=cor,outline=cor
                )
    
    def xyscala(self,x,y):
        x //= self.escala
        y //= self.escala
        return x,y
    
    def add_forma(self):
        if self.forma_aux:
            self.forma_aux.cor_borda = self.cor
            self.formas.append(self.forma_aux)
            self.forma_aux = None
            self.lista_box.insert(tk.END,'Poligono'+str(len(self.formas)))

    def rm_forma(self):
        index = self.lista_box.curselection()
        if index:
            index = index[0]
            self.lista_box.delete(index)
            self.formas.pop(index)
    
    def pinta_forma(self):
        index = self.lista_box.curselection()
        if index:
            index = index[0]
            forma = self.formas[index]
            for x,y in forma.borda():
                self.add_frame_buffer(x,y,forma.cor_borda)
            self.pinta_coord(forma.borda())

    def cria_eventos(self):
        modo = self.modo
        f_event = None
        self.forma_aux = None
        self.canvas.unbind('<Double-Button-1>')
        self.canvas.unbind('<B1-Motion>')
        if modo=='LIVRE':
            def f(event):
                x,y = self.xyscala(event.x,event.y) # converte de acordo com escala
                if self.largura>x>=0<=y<self.altura:
                    self.add_frame_buffer(x,y,self.cor) # adiciona cor no pixel indicado
                    self.pinta_coord([(x,y)]) # pinta diretamente o pixel
            self.canvas.bind('<B1-Motion>',f)
            f_event = f
        elif modo=='LINHA':
            # adiciona os pontos e finaliza ao chegar no ponto inicial ou ao dar double-clik
            def f(event):
                x,y = self.xyscala(event.x,event.y) # captura x e y do canvas e converte de acordo com nossa escala
                if not self.forma_aux: # se a forma auxiliar for None (Nula)
                    self.forma_aux = Poligono((x,y)) # realiza instância de uma Linha com a coordenada inicial
                    self.add_frame_buffer(x,y,self.cor) # adiciona cor ao pixel no frame buffer
                    self.pinta_coord([(x,y)]) # pinta no Canvas a coordenada informada
                elif (x,y) != self.forma_aux.coords[-1]: # se o último vértice for diferente do novo clicado
                    for x,y in bresenham(self.forma_aux.coords[-1],(x,y)):
                        self.add_frame_buffer(x,y,self.cor) # adiciona cor ao pixel no frame buffer
                    self.pinta_coord(bresenham(self.forma_aux.coords[-1],(x,y)))
                    self.forma_aux.coords.append((x,y)) # adiciona vértice à linha
                if len(self.forma_aux.coords)>1 and self.forma_aux.coords[0] == self.forma_aux.coords[-1]:
                    self.forma_aux.fechado = True
                    self.add_forma() # adiciona e reseta self.forma_aux
            f_event = f
        elif modo=='CIRCULO':
            def f(event):
                x,y = self.xyscala(event.x,event.y) # converte de acordo com escala
                if not self.forma_aux:
                    #self.forma_aux = Circulo((x,y),None)
                    self.forma_aux = Poligono((x,y))
                else:
                    #self.forma_aux.raio = (x,y)
                    self.forma_aux = Circulo(self.forma_aux.coords[0],(x,y))
                    self.forma_aux.cor_borda = self.cor
                    for x,y in self.forma_aux.borda():
                        self.add_frame_buffer(x,y,self.forma_aux.cor_borda)
                        self.pinta_coord([(x,y)])
                    self.add_forma()
            f_event = f
        elif modo=='BEZIER':
            def f(event):
                x,y = self.xyscala(event.x,event.y) # converte de acordo com escala
                self.marca_pixel(x,y)
                if not self.forma_aux:
                    self.forma_aux = Curva((x,y))
                else:
                    self.forma_aux.coords.append((x,y))

                if len(self.forma_aux.coords)>1 and self.forma_aux.coords[-2]==self.forma_aux.coords[-1]:
                    self.forma_aux.coords.pop(-1)
                    self.forma_aux.cor_borda = self.cor
                    for x,y in self.forma_aux.borda():
                        self.add_frame_buffer(x,y,self.forma_aux.cor_borda)
                        self.pinta_coord([(x,y)])
                    self.add_forma()
            f_event = f
        elif modo=='PREE_REC':
            def f(event):
                x,y = self.xyscala(event.x,event.y) # converte de acordo com escala
                preenchrecursivo(self.frame_buffer,(x,y),self.cor)
                self.pinta_buffer()
            f_event = f
        elif modo=='PREE_SCAN':
            index =  self.lista_box.curselection()
            if index:
                index = index[0]
                preenchscanline(self.frame_buffer,self.formas[index],self.cor)
                self.pinta_buffer()
            else:
                print('selecione uma figura')
        elif modo=='CORTE_LINHA':
            def f(event):
                x,y = self.xyscala(event.x,event.y) # captura x e y do canvas e converte de acordo com nossa escala
                self.marca_pixel(x,y)
                if not self.forma_aux: # se a forma auxiliar for None (Nula)
                    self.forma_aux = Poligono((x,y)) # realiza instância de uma Linha com a coordenada inicial
                else:
                    self.forma_aux.coords.append((x,y))
                    self.forma_aux.coords.sort()
                    p_min,p_max = self.forma_aux.coords
                    self.forma_aux = None
                    index =  self.lista_box.curselection()
                    if index:
                        index = index[0]
                        linha = self.formas[index]
                        self.limpa_buffer()
                        nova_linha = Poligono(None)
                        nova_linha.coords = algoritmos.cohen_Sutherland(linha.coords,p_min,p_max)
                        for x,y in nova_linha.borda():
                            self.add_frame_buffer(x,y,self.cor)
                        self.pinta_buffer()
                    else:
                        print('selecione uma figura')
            f_event = f
        elif modo=='TRANSLAD':
            index =  self.lista_box.curselection()
            if index:
                index = index[0]
                linha = self.formas[index]
                self.limpa_buffer()
                ponto_t = int(self.entrada_xy['x'].get()),int(self.entrada_xy['y'].get())
                linha.coords = algoritmos.translate(linha,ponto_t)
                for x,y in linha.borda():
                    self.add_frame_buffer(x,y,self.cor)
                self.pinta_coord(linha.borda())
            else:
                print('selecione uma figura')
        # substitui evento modo de pintura atual
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>',f_event)

app = App(escala=5)
app.show()
