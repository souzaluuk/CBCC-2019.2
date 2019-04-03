# implementação do algoritmo de bresenham
from classes import Ponto, Reta

#primeiro caso
#p1 = Ponto(0,3)
#p2 = Ponto(3,9)
#segundo caso
#p1 = Ponto(0,0)
#p2 = Ponto(5,3)
#terceiro caso
p1 = Ponto(5,5)
p2 = Ponto(0,0)

reta = Reta(p1.cartesiano,p2.cartesiano)
print('p1:',p1.cartesiano)
print('p2:',p2.cartesiano)
print()
print('delta x:',reta.deltax) # 0-3
print('delta y:',reta.deltay) # 9-3
print('m:',reta.m) # deltay/deltax
print()
print('composição da reta(bresenham):')

for ponto in reta.bresenham:
    print(ponto.cartesiano)
