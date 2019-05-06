import algoritmos

class Ponto:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Curva:
    def __init__(self,*pontos,cor_borda=None,cor_interna=None):
        self.pontos = list(pontos)
    def borda(self):
        return algoritmos.curva(self.pontos,0.0001)

class Circulo:
    def __init__(self,centro:tuple,raio:tuple,cor_borda=None,cor_interna=None):
        self.centro = centro
        self.raio = raio
        self.cor_borda=cor_borda
        self.cor_interna=cor_interna
    def borda(self):
        return algoritmos.circulo(self.centro,self.raio)

class Poligono:
    def __init__(self,*pontos,cor_borda=None,cor_interna=None):
        self.vertices = list(pontos)
        self.cor_borda = cor_borda
    def borda(self):
        if len(self.vertices)==1:
            return self.vertices
        else:
            v = self.vertices
            borda = []
            for i in range(len(v)-1):
                borda.extend(algoritmos.bresenham(v[i],v[i+1]))
            return borda