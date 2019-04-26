# Definições padrões:
COR_PADRAO='#000000'

class Elemento:
    def __init__(self):
        '''Interface modelo dos elementos que serão manipuladas'''
        # implementar construtor para cada filho
        if type(self) is Elemento:
            raise Exception('Utilze apenas como interface')
        else:
            raise Exception('Implemente o método __init__ (construtor)')
    @property
    def get(self):
        '''Implementar este módulo em todos os objetos filhos para retorno de lista de pixles'''
        raise Exception('Implemente o método get')

class Pixel(Elemento):
    '''Classe que representa um pixel'''
    def __init__(self,x,y,cor=COR_PADRAO):
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
        return [(self.x,self.y,self.cor)]

class Linha(Elemento):
    '''Classe que representa uma linha'''
    trocax = trocay = trocaxy = False # flags para reflexões
    def __init__(self,ponto_a,ponto_b,cor_linha=COR_PADRAO): # recebe tuplas
        '''Construtor da linha'''
        xa,ya = ponto_a
        xb,yb = ponto_b
        self.cor_linha=cor_linha
        self.pixel_a=Pixel(xa,ya,cor_linha)
        self.pixel_b=Pixel(xb,yb,cor_linha)
    @property
    def get(self):
        '''Retorna uma lista com os pontos da linha'''
        return self.pixel_a.get+self.pixel_b.get

class Poligono(Elemento):
    def __init__(self,*pontos,fechado=False): # pontoss devem ser tuplas que representem cada vértice
        '''Construtor do Polígono'''
        self.pontos = pontos
        self.fechado = fechado
    @property
    def get(self):
        '''Retorna uma lista com os pixels'''
        pixels = []
        for ponto in self.pontos:
            x,y = ponto
            pixels.append(Pixel(x,y).get)
        if self.fechado:
            pixels.append(pixels[0])
        return pixels
