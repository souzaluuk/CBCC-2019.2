# definindo um ponto/pixel
class Ponto:
    '''Classe que representa um ponto ou pixel'''
    def __init__(self,x,y,cor=None):
        self.x=x
        self.y=y
        self.cor=cor
    @property
    def cartesiano(self):
        '''Retorna ponto cartesiano como tupla: (x,y)'''
        return (self.x,self.y)
    @property
    def pixel(self):
        '''Retorna pixel como tupla (x,y,cor)'''
        return (self.x,self.y,self.cor)

class Reta:
    '''Classe que representa uma reta'''
    trocax = trocay = trocaxy = False # usados nas reflexões
    def __init__(self,ponto_a,ponto_b):
        self.ponto_a=ponto_a
        self.ponto_b=ponto_b
    @property
    def deltax(self):
        '''Retorna a variação de xa e xb'''
        xa,xb = self.ponto_a.x, self.ponto_b.x
        return xb-xa
    @property
    def deltay(self):
        '''Retorna a variação de ya e yb'''
        ya,yb = self.ponto_a.y, self.ponto_b.y
        return yb-ya
    @property
    def m(self):
        '''Retorna a divisão de delta y por delta x'''
        return self.deltay/self.deltax if self.deltax!=0 else self.deltay
    @property
    def bresenham(self):
        '''Utilizando a lógica do algoritmo de bresenham e retorna uma lista com os Pontos que compõem o objeto reta'''
        self.reflexao(self.ponto_a,self.ponto_b) # realiza reflexão
        pontos = []
        m = self.m
        e = m - 0.5 # o valor de 'e' será alterado
        xa,ya = self.ponto_a.cartesiano # retorna (x,y)
        xb,yb = self.ponto_b.cartesiano # retorna (x,y)
        #print((xa,ya),e)
        pontos.append(Ponto(xa,ya))
        while xa < xb:
            if e >= 0:
                ya = ya + 1
                e = e - 1
            xa = xa + 1
            e = e + m
            #print((xa,ya),e)
            pontos.append(Ponto(xa,ya))
        self._reflexao(self.ponto_a,self.ponto_b,pontos) # inversa da reflexão
        return pontos

    def reflexao(self,p1,p2):
        '''Objetiva 'mover' a reta para o primeiro octante'''
        if self.m > 1 or self.m < -1:
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
    
    def _reflexao(self,p1,p2,lista_pontos):
        '''Objetiva 'mover' a reta para de volta ao local de origem'''
        if self.trocay:
            p1.y = -p1.y
            p2.y = -p2.y
        if self.trocax:
            p1.x = -p1.x
            p2.x = -p2.x
        if self.trocaxy:
            p1.x,p1.y = p1.y,p1.x
            p2.x,p2.y = p2.y,p2.x
        
        for ponto in lista_pontos: # troca para os pontos da lista
            if self.trocay: ponto.y = -ponto.y
            if self.trocax: ponto.x = -ponto.x
            if self.trocaxy: ponto.x,ponto.y = ponto.y,ponto.x
        self.trocay = self.trocax = self.trocaxy = False
