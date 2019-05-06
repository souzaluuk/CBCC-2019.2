def preenchscanline(fb):
    for y in range(len(fb)):
        print(y,fb[y])
    return 0

def preenchrecursivo(fb,ponto:tuple,cor_nova:str):
    conjunto = [ ponto ]
    altura = len(fb)
    largura = len(fb[0])
    
    x,y = ponto
    cor_atual = fb[y][x] # cor_interna atual ***lembrando *** "y -> linha ; x -> coluna"
    while len(conjunto)>0:
        x,y = conjunto.pop() # ***lembrando *** "y -> linha ; x -> coluna"
        if not (0<=x<largura and 0<=y<altura):
            continue
        if fb[y][x] != cor_atual or cor_nova == cor_atual:
            continue
        fb[y][x] = cor_nova
        conjunto.append( (x-1,y) )
        conjunto.append( (x+1,y) )
        conjunto.append( (x,y-1) )
        conjunto.append( (x,y+1) )

def curva(controlPT,passo):
    n = len(controlPT)
    pts = [None] * (n + 1)
    for i in range(0, n):
        pts[i] = controlPT[i]
    def mult(p:tuple,n:float):
        x,y = p
        return (x*n,y*n)
    def soma(p1,p2):
        x1,y1 = p1
        x2,y2 = p2
        return (x1+x2,y1+y2)
    coord = set()
    t=0
    while t<1:
        for r in range(1, n+1):
            for i in range(0, n-r):
                pts[i] = soma(mult(pts[i],(1-t)),mult(pts[i+1],t))
        xfim,yfim = pts[0]
        coord.add((round(xfim),round(yfim)))
        t+=passo
    return coord

def circulo(ponto_centro:tuple,ponto_raio:tuple):
    x1,y1 = ponto_centro # centro do circulo
    x2,y2 = ponto_raio # ponto que será base para o raio
    raio = round(((x2-x1)**2 + (y2-y1)**2)**0.5) # arrendondamento da distância entre os dois pontos
    coords = [] # lista para guardar as coordenadas iniciais
    x,y = (0,raio) # ponto de partida na construção o círculo (deslocado para o centro)
    p = 1 - raio
    coords.append((x,y))
    while x<y-1:
        x+=1
        if p<0:
            p+=2*x+3
        else:
            y-=1
            p+=2*x-2*y+5
        coords.append((x,y))
    # realização das reflexões para os demais octantes
    coords_fim=coords[:] # cópia das coordenadas do primeiro octante
    coords_fim.extend([(y,x) for x,y in coords])
    coords_fim.extend([(y,-x) for x,y in coords])
    coords_fim.extend([(x,-y) for x,y in coords])
    coords_fim.extend([(-x,-y) for x,y in coords])
    coords_fim.extend([(-y,-x) for x,y in coords])
    coords_fim.extend([(-y,x) for x,y in coords])
    coords_fim.extend([(-x,y) for x,y in coords])
    coords_fim=[(x+x1,y+y1) for x,y in coords_fim] # desloca de volta para o ponto de origem
    return coords_fim

def bresenham(pixel_a:tuple,pixel_b:tuple):
    '''Utilizando o algoritmo de bresenham e retorna uma lista com os pixels(tuplas) que compõem uma reta'''
    # trocaxy = trocax = trocay = False # flags de troca para bresenham

    def calcula_m(p1:tuple,p2:tuple):
        '''Retorna a divisão de delta y por delta x'''
        x1,y1 = p1
        x2,y2 = p2
        delta_x = x2-x1
        delta_y = y2-y1
        return delta_y/delta_x if delta_x!=0 else delta_y

    def reflexao(p1:tuple,p2:tuple):
        '''Objetiva 'mover' a reta para o primeiro octante'''
        trocaxy = trocax = trocay = False
        valor_m = calcula_m(p1,p2) # guarda o valor de 'm'
        # converte para objetos pixels para que possa realizar trocas
        x1,y1 = p1 # instância pixel1
        x2,y2 = p2 # instância pixel2
        if  valor_m > 1 or valor_m < -1:
            x1,y1 = y1,x1 # troca 'x' com 'y'
            x2,y2 = y2,x2 # troca 'x' com 'y'
            trocaxy = True # ativa flag de troca para xy
        if x1 > x2:
            x1 = -x1 # inverte x de p1
            x2 = -x2 # inverte x de p2
            trocax = True # ativa flag de troca para x
        if y1 > y2:
            y1 = -y1 # inverte y de p1
            y2 = -y2 # inverte y de p2
            trocay = True # ativa flag de troca para y
        return (x1,y1),(x2,y2),trocaxy,trocax,trocay

    def _reflexao(lista_pixels,trocaxy,trocax,trocay):
        '''Objetiva 'mover' a reta para de volta ao local de origem'''
        for i in range(len(lista_pixels)): # troca para os pixels da lista
            x,y = lista_pixels[i]
            if trocay:
                y = -y
            if trocax:
                x = -x
            if trocaxy:
                x,y = y,x
            lista_pixels[i] = (x,y)
        trocay = trocax = trocaxy = False

    p1,p2,trocaxy,trocax,trocay = reflexao(pixel_a,pixel_b) # retorna reflexão com flags

    m = calcula_m(p1,p2) # guarda o cálculo de (x2-x1)/(y2-y1)
    x1,y1 = p1
    x2,_ = p2

    pixels = list() # lista de pixels que será retornada
    e = m - 0.5 # primeiro valor de 'e'

    pixels.append(p1)
    while x1 < x2-1:
        if e >= 0:
            y1 += 1
            e -= 1
        x1 += 1
        e += m
        pixels.append((x1,y1))
    pixels.append(p2)
    _reflexao(pixels,trocaxy,trocax,trocay)
    return pixels