# Definições padrões:
COR='#000000'

class Pixel:
    '''Classe que representa um pixel ou pixel'''
    def __init__(self,x,y,cor=COR):
        '''Construtor do Pixel'''
        self.x=x
        self.y=y
        self.cor=cor
    def __str__(self):
        '''Para uso em caso de transformação em string'''
        return str(self.get)
    @property
    def get(self):
        '''Retorna pixel como tupla: (x,y,cor)'''
        return (self.x,self.y,self.cor)

class Reta:
    '''Classe que representa uma reta'''
    trocax = trocay = trocaxy = False # flags para reflexões
    def __init__(self,ponto_a,ponto_b,cor_reta=COR): # recebe tuplas
        '''Construtor da Reta'''
        xa,ya = ponto_a
        xb,yb = ponto_b
        self.cor_reta=cor_reta
        self.pixel_a=Pixel(xa,ya,cor_reta)
        self.pixel_b=Pixel(xb,yb,cor_reta)
    @property
    def deltax(self):
        '''Retorna a variação de xa e xb'''
        xa,xb = self.pixel_a.x, self.pixel_b.x
        return xb-xa
    @property
    def deltay(self):
        '''Retorna a variação de ya e yb'''
        ya,yb = self.pixel_a.y, self.pixel_b.y
        return yb-ya
    @property
    def m(self):
        '''Retorna a divisão de delta y por delta x'''
        return self.deltay/self.deltax if self.deltax!=0 else self.deltay
    @property
    def bresenham(self):
        '''Utilizando o algoritmo de bresenham e retorna uma lista com os pixels que compõem o objeto reta'''
        self.reflexao(self.pixel_a,self.pixel_b) # realiza reflexão
        pixels = []
        m = self.m # guarda o valor de 'm'
        e = m - 0.5 # primeiro valor de 'e'
        xa,ya = self.pixel_a.get[:-1] # retorna (x,y)
        xb,yb = self.pixel_b.get[:-1] # retorna (x,y)
        pixels.append(self.pixel_a)
        while xa < xb-1:
            if e >= 0:
                ya += 1
                e -= 1
            xa += 1
            e += m
            pixels.append(Pixel(xa,ya,self.cor_reta))
        pixels.append(self.pixel_b)
        self._reflexao(self.pixel_a,self.pixel_b,pixels) # inversa da reflexão
        return pixels

    def reflexao(self,p1,p2):
        '''Objetiva 'mover' a reta para o primeiro octante'''
        m = self.m # guarda o valor de 'm'
        if m > 1 or m < -1:
            p1.x,p1.y = p1.y,p1.x # troca 'x' com 'y'
            p2.x,p2.y = p2.y,p2.x # troca 'x' com 'y'
            self.trocaxy = True
        if p1.x > p2.x:
            p1.x = -p1.x
            p2.x = -p2.x
            self.trocax = True
        if p1.y > p2.y:
            p1.y = -p1.y
            p2.y = -p2.y
            self.trocay = True

    def _reflexao(self,p1,p2,lista_pixels):
        '''Objetiva 'mover' a reta para de volta ao local de origem'''
        for pixel in lista_pixels: # troca para os pixels da lista
            if self.trocay:
                pixel.y = -pixel.y
            if self.trocax:
                pixel.x = -pixel.x
            if self.trocaxy:
                pixel.x,pixel.y = pixel.y,pixel.x
        self.trocay = self.trocax = self.trocaxy = False

class Poligono:
        def __init__(self,*pontos,fechado=True): # pontoss devem ser tuplas que representem cada vértice
            '''Construtor do Polígono'''
            self.pontos = pontos
            self.fechado = fechado
        @property
        def retas(self):
            reta = []
            for x in range(len(self.pontos)-1):
                x1,y1 = self.pontos[x]
                x2,y2 = self.pontos[x+1]
                reta.append(Reta((x1,y1),(x2,y2)))
            x1,y1 = self.pontos[-1]
            x2,y2 = self.pontos[0]
            if self.fechado:
                reta.append(Reta((x1,y1),(x2,y2)))
            return reta
        @property
        def pixels(self):
            retas = self.retas
            pixels = []
            for reta in retas:
                pixels += reta.bresenham
            return pixels
