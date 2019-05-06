import algoritmos

class Ponto:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Curva:
    def __init__(self,*pontos):
        self.pontos = list(pontos)
    def borda(self):
        return algoritmos.curva(self.pontos,0.0001)

class Circulo:
    def __init__(self,centro:tuple,raio:tuple):
        self.centro = centro
        self.raio = raio
    def borda(self):
        return algoritmos.circulo(self.centro,self.raio)

class Linha:
    def __init__(self,*pontos):
        self.vertices = list(pontos)
    def borda(self):
        if len(self.vertices)==1:
            return self.vertices
        else:
            v = self.vertices
            borda = []
            for i in range(len(v)-1):
                borda.extend(algoritmos.bresenham(v[i],v[i+1]))
            return borda