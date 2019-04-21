# módulo de aplicação dos arlgoritmos da disciplina de Computação Gráfica
from formas import Pixel, Reta

def calcula_m(p1:tuple,p2:tuple):
    '''Retorna a divisão de delta y por delta x'''
    x1,y1 = p1
    x2,y2 = p2
    delta_x = x2-x1
    delta_y = y2-y1
    return delta_y/delta_x if delta_x!=0 else delta_y

def reflexao(p1:tuple,p2:tuple):
    '''Objetiva 'mover' a reta para o primeiro octante'''
    valor_m = calcula_m(p1,p2) # guarda o valor de 'm'
    if  > 1 or m < -1:
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
        Objetiva 'mover' a reta para de volta ao local de origem
        for pixel in lista_pixels: # troca para os pixels da lista
            if self.trocay:
                pixel.y = -pixel.y
            if self.trocax:
                pixel.x = -pixel.x
            if self.trocaxy:
                pixel.x,pixel.y = pixel.y,pixel.x
        self.trocay = self.trocax = self.trocaxy = Falses

def bresenham(pixel_a:Pixel,pixel_b:Pixel):
    '''Utilizando o algoritmo de bresenham e retorna uma lista com os pixels que compõem o objeto reta'''
    p1 = pixel_a.get[0][:-1] # ignora cor
    p2 = pixel_b.get[0][:-1] # ignora cor

    p1,p2 = reflexao(p1,p2) # retorna reflexão

    x1,y1 = p1
    x2,y2 = p2

    return [(x1,y1),(x2,y2)]

p1 = Pixel(0,0)
p2 = Pixel(5,5)

print(bresenham(p1,p2))

exit()
'''    reflexao(p1,p2) # realiza reflexão
    pixels = [] # inicializa lista de pixels

    m = self.m # guarda o valor de 'm'

    xa,ya = p1
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

    def deltax(self):
        Retorna a variação de xa e xb
        xa,xb = self.pixel_a.x, self.pixel_b.x
        return xb-xa
    @property
    def deltay(self):
        Retorna a variação de ya e yb
        ya,yb = self.pixel_a.y, self.pixel_b.y
        return yb-ya
    @property
    def m(self):
        Retorna a divisão de delta y por delta x
        return self.deltay/self.deltax if self.deltax!=0 else self.deltay
    @property
    def bresenham(self):
        Utilizando o algoritmo de bresenham e retorna uma lista com os pixels que compõem o objeto reta
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

'''