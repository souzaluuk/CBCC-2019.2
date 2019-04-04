# implementação do algoritmo de bresenham
from figuras import Pixel, Reta

p1 = Pixel(0,0)
p2 = Pixel(10,1)

reta = Reta(p1.get[:-1],p2.get[:-1])
print('p1:',p1)
print('p2:',p2)
print()
print('delta x:',reta.deltax) # 0-3
print('delta y:',reta.deltay) # 9-3
print('m:',reta.m) # deltay/deltax
print()
print('composição da reta(bresenham):')

for pixel in reta.bresenham:
    print(pixel)

print()
print(reta.pixel_a)
print(reta.pixel_b)
