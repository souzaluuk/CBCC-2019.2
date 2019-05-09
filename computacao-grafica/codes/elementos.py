import algoritmos

class Ponto:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Curva:
    def __init__(self,*ponto_controle,cor_borda=None,fechado=False):
        self.coords = list(ponto_controle)
        self.fechado = fechado
    def borda(self):
        return algoritmos.curva(self.coords,0.001)

class Circulo:
    def __init__(self,centro,raio:tuple,cor_borda=None,fechado=True):
        self.coords = [centro]
        x1,y1 = centro # centro do circulo
        x2,y2 = raio # ponto que será base para o raio
        self.raio = round(((x2-x1)**2 + (y2-y1)**2)**0.5) # arrendondamento da distância entre os dois pontos
        self.cor_borda = cor_borda
        self.fechado = fechado
    def borda(self):
        return algoritmos.circulo(self.coords[0],self.raio)

class Poligono:
    def __init__(self,*coords,cor_borda=None,fechado=False):
        self.coords = list(coords)
        self.cor_borda = cor_borda
        self.fechado = fechado
    def borda(self):
        if len(self.coords)==1:
            return self.coords
        else:
            v = self.coords
            borda = []
            for i in range(len(v)-1):
                borda.extend(algoritmos.bresenham(v[i],v[i+1]))
            return borda

class Cubo:
    def __init__(self,poligono_a,poligono_b):
        self.poligono_a = poligono_a
        self.poligono_b = poligono_b
    def borda(self):
        borda = []
        borda.extend(self.poligono_a.borda()) # z -> 2
        borda.extend(self.poligono_b.borda()) # z -> 1
        for p1,p2 in zip(self.poligono_a.coords,self.poligono_b.coords):
            borda.extend(algoritmos.bresenham(p1,p2))
        return borda