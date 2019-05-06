import elementos

def cohen_Sutherland(linha, p_min:tuple, p_max:tuple):
    dentro_janela = 0  # 0000
    esquerda_janela = 1  # 0001
    direita_janela = 2  # 0010
    baixo_janela = 4  # 0100
    cima_janela = 8  # 1000

    p1,p2 = linha
    
    x1, y1 = p1
    x2, y2 = p2

    x_min,y_min = p_min
    x_max,y_max = p_max

    def define_bit(x, y):
        bit = dentro_janela
        if x < x_min:  # para a esquerda da janela
            bit |= esquerda_janela
        elif x > x_max:  # para a direita da janela
            bit |= direita_janela
        if y < y_min:  # para baixo da janela
            bit |= baixo_janela
        elif y > y_max:  # para cima da janela
            bit |= cima_janela
        return bit

    #define o bit equivalente a área que o extremo da linha está
    bit1 = define_bit(x1,y1)
    bit2 = define_bit(x2,y2)

    linha_aceita = False

    while True:
        # Se os dois extremos estiverem dentro do retangulo
        if bit1 == 0 and bit2 == 0:
            linha_aceita = True
            break
        # Se os dois extremos estiverem fora do retangulo
        elif (bit1 & bit2) != 0:
            break
        # Algum segmento da linha está dentro do retangulo
        else:
            # Pelo menos um dos pontos está fora
            x = 1.0
            y = 1.0
            if bit1 != 0:
                bit_fora = bit1
            else:
                bit_fora = bit2

            # Encontrar o ponto de interseção
            if bit_fora & cima_janela:
                # ponto sobre a janela
                x = x1 + (x2 - x1) * \
                    (y_max - y1) / (y2 - y1)
                y = y_max
            elif bit_fora & baixo_janela:
                # ponto abaixo da janela
                x = x1 + (x2 - x1) * \
                    (y_min - y1) / (y2 - y1)
                y = y_min
            elif bit_fora & direita_janela:
                # ponto a direita da janela
                y = y1 + (y2 - y1) * \
                    (x_max - x1) / (x2 - x1)
                x = x_max
            elif bit_fora & esquerda_janela:
                # ponto a esquerda da janela
                y = y1 + (y2 - y1) * \
                    (x_min - x1) / (x2 - x1)
                x = x_min
            #Substitui com o ponto de interseção encontrado
            if bit_fora == bit1:
                x1 = x
                y1 = y
                bit1 = define_bit(x1, y1)
            else:
                x2 = x
                y2 = y
                bit2 = define_bit(x2, y2)
    if linha_aceita:
        #print("Linha aceita de %.2f,%.2f para %.2f,%.2f" % (x1, y1, x2, y2))
        x1 = round(x1)
        x2 = round(x2)
        y1 = round(y1)
        y2 = round(y2)
        return ((x1,y1),(x2,y2))
    else:
        #print("Linha rejeitada")
        return None

def preenchscanline(fb,poligono,cor):
    borda = list(poligono.borda())
    if not poligono.fechado:
        borda.extend(bresenham(borda[-1],borda[0]))
    xmin = min(map(lambda p:p[0],borda))
    xmax = max(map(lambda p:p[0],borda))
    ymin = min(map(lambda p:p[1],borda))
    ymax = max(map(lambda p:p[1],borda))

    scanlines = {}
    
    for y in range(ymin,ymax+1):
        scanlines[y] = list()
        for x in range(xmin,xmax+1):
            if (x,y) in borda:
                scanlines[y].append(x)
                if borda.count((x,y))>1:
                    if not type(poligono) == elementos.Poligono:
                        pass
                        #scanlines[y].append(x)
                    else:
                        if (x,y) in poligono.vertices:
                            index = poligono.vertices.index((x,y))
                            conjunto_teste = poligono.vertices[index-1:index+2]
                            if conjunto_teste:
                                if max(conjunto_teste,key=lambda p:p[1]) == poligono.vertices[index] or min(conjunto_teste,key=lambda p:p[1]) == poligono.vertices[index]:
                                    scanlines[y].pop(-1)
    for y in scanlines:
        linhas = scanlines[y]
        for x in range(len(linhas)-1):
            x0,xs = linhas[x], linhas[x+1]
            for i in range(x0+1,xs):
                fb[y][i] = cor

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
    coord = []
    t=0
    while t<1:
        for r in range(1, n+1):
            for i in range(0, n-r):
                pts[i] = soma(mult(pts[i],(1-t)),mult(pts[i+1],t))
        xfim,yfim = pts[0]
        if not (round(xfim),round(yfim)) in coord:
            coord.append((round(xfim),round(yfim)))
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
    coords_fim.extend([(-y,x) for x,y in coords])
    coords_fim.extend([(y,-x) for x,y in coords])
    coords_fim.extend([(x,-y) for x,y in coords])
    coords_fim.extend([(-x,-y) for x,y in coords])
    coords_fim.extend([(-y,-x) for x,y in coords])
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