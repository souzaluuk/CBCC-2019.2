def projecao_perspectiva(poligono,d):
    matriz = [[d,0,0,0],[0,d,0,0],[0,0,d,0],[0,0,1,0]]
    novos_pontos = []
    for i in range(len(poligono)):
        vetor_aux = []
        vetor_aux.append( (matriz[0][0]*poligono[i][0]) + (matriz[0][1]*poligono[i][1]) + (matriz[0][2]*poligono[i][2]) + (matriz[0][3]*poligono[i][3]) )
        vetor_aux.append( (matriz[1][0]*poligono[i][0]) + (matriz[1][1]*poligono[i][1]) + (matriz[1][2]*poligono[i][2]) + (matriz[1][3]*poligono[i][3]) )
        vetor_aux.append( (matriz[2][0]*poligono[i][0]) + (matriz[2][1]*poligono[i][1]) + (matriz[2][2]*poligono[i][2]) + (matriz[2][3]*poligono[i][3]) )
        vetor_aux.append( (matriz[3][0]*poligono[i][0]) + (matriz[3][1]*poligono[i][1]) + (matriz[3][2]*poligono[i][2]) + (matriz[3][3]*poligono[i][3]) )
        novos_pontos.append(vetor_aux)
    for i in range(len(poligono)):
        novos_pontos[i][0] = round(novos_pontos[i][0] / novos_pontos[i][3])
        novos_pontos[i][1] = round(novos_pontos[i][1] / novos_pontos[i][3])
        novos_pontos[i][2] = round(novos_pontos[i][2] / novos_pontos[i][3])
        novos_pontos[i][3] = round(novos_pontos[i][3] / novos_pontos[i][3])
    return novos_pontos

def  projecao_orto(poligono,x,y,z):
    matriz = [[x,0,0,0],[0,y,0,0],[0,0,z,0],[0,0,0,1]]
    novos_pontos = []
    for i in range(len(poligono)):
        vetor_aux = []
        vetor_aux.append( (matriz[0][0]*poligono[i][0]) + (matriz[0][1]*poligono[i][1]) + (matriz[0][2]*poligono[i][2]) + (matriz[0][3]*poligono[i][3]) )
        vetor_aux.append( (matriz[1][0]*poligono[i][0]) + (matriz[1][1]*poligono[i][1]) + (matriz[1][2]*poligono[i][2]) + (matriz[1][3]*poligono[i][3]) )
        vetor_aux.append( (matriz[2][0]*poligono[i][0]) + (matriz[2][1]*poligono[i][1]) + (matriz[2][2]*poligono[i][2]) + (matriz[2][3]*poligono[i][3]) )
        vetor_aux.append( (matriz[3][0]*poligono[i][0]) + (matriz[3][1]*poligono[i][1]) + (matriz[3][2]*poligono[i][2]) + (matriz[3][3]*poligono[i][3]) )
        novos_pontos.append(vetor_aux)
    return novos_pontos

def translate(figura, ponto_t):
    tx,ty = ponto_t
    pontos = list(figura.coords)
    for i in range(len(pontos)):
        x,y = pontos[i]
        pontos[i] = (x+tx,y+ty)
    return pontos

def rotate(figura, grau_rotacao,pivo=(0,0)):
    import math
    x_pivo,y_pivo = pivo
    grau_cos = math.cos(math.radians(grau_rotacao)) # cos do grau
    grau_sen = math.sin(math.radians(grau_rotacao)) # sen do grau
    novas_coords = list()
    for x,y in figura.coords:
        x_ = x_pivo + round((x-x_pivo)*grau_cos - (y-y_pivo)*grau_sen)
        y_ = y_pivo + round((y-y_pivo)*grau_cos + (x-x_pivo)*grau_sen)
        novas_coords.append((x_,y_))
    return novas_coords

def scale(figura, escala):
    coords = figura.coords
    escala_x,escala_y = escala
    min_x = min(coords,key=lambda ponto: ponto[0])[0]
    min_y = min(coords,key=lambda ponto: ponto[1])[1]
    novas_coords = list()
    for x,y in coords:
        x_ = min_x + ((x - min_x) * escala_x) if x!=0 else x
        y_ = min_x + ((y - min_y) * escala_y) if y!=0 else y
        novas_coords.append((round(x_),round(y_)))
    return novas_coords

def cohen_Sutherland(pontos_linha, p_min:tuple, p_max:tuple):
    dentro_janela = 0  # 0000
    esquerda_janela = 1  # 0001
    direita_janela = 2  # 0010
    baixo_janela = 4  # 0100
    cima_janela = 8  # 1000

    p1,p2 = pontos_linha
    
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

def preenchscanline(fb, poligono,cor):
    borda = poligono.borda()
    if not poligono.fechado:
        borda.extend(bresenham(borda[-1],borda[0]))
    
def preenchscanline(fb,poligono,cor):
    import elementos
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
                        if (x,y) in poligono.coords:
                            index = poligono.coords.index((x,y))
                            conjunto_teste = poligono.coords[index-1:index+2]
                            if conjunto_teste:
                                if max(conjunto_teste,key=lambda p:p[1]) == poligono.coords[index] or min(conjunto_teste,key=lambda p:p[1]) == poligono.coords[index]:
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
    #from functools import reduce
    coord_fim = list()
    for p1,p2 in zip(coord,coord[1:]):
        coord_fim.extend(bresenham(p1,p2))
    return coord_fim

def circulo(ponto_centro:tuple,raio:tuple):
    x1,y1 = ponto_centro # centro do circulo
    raio = raio
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

# Função para retornar o X do ponto de intersecção de duas linhas
def intersecoes_x(x1,y1,x2,y2,x3,y3,x4,y4):
    numerador = (x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)
    denominador = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
    return numerador/denominador

# Função para retornar o Y do ponto de intersecção de duas linhas
def intersecoes_y(x1,y1,x2,y2,x3,y3,x4,y4):
    numerador = (x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)
    denominador = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
    return  numerador/denominador

# Função que recorta todos as arestas e escreve um recorte de aresta da área recortada
# tamanho_poligono = quantidade de arestas do poligono

def recorte_poligono(pontos_poligono, tamanho_poligono, x1, y1, x2, y2):
    pontos_novos = [[0, 0], [0, 0], [0, 0], [0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]
    novo_tamanho_poligono = 0

    #(ix,iy),(kx,ky) são coordenadas dos pontos
    for i in range(tamanho_poligono):
        #I e K formam a linha no poligono
        k = (i+1) % tamanho_poligono
        ix = pontos_poligono[i][0]
        iy = pontos_poligono[i][1]
        kx = pontos_poligono[k][0]
        ky = pontos_poligono[k][1]
        print("i:", i)
        print("k:", k)
        print("ix:", ix)
        print("iy:", iy)
        print("kx:", kx)
        print("ky:", ky)
        #k = k % tamanho_poligono
        #calculando a posição do primeiro ponto escrito pela linha de corte
        i_posicao = (x2-x1) * (iy-y1) - (y2-y1) * (ix-x1)


        #calculando a posição do segundo ponto escrito pela linha de corte
        k_posicao = (x2-x1) * (ky-y1) - (y2-y1) * (kx-x1)


        print(i_posicao)
        print(k_posicao)

        #Se o dois estiverem dentro:
        if (i_posicao < 0 and k_posicao < 0):
            #apenas o segundo ponto é adicionado
            pontos_novos[novo_tamanho_poligono][0] = kx
            pontos_novos[novo_tamanho_poligono][1] = ky
            novo_tamanho_poligono = novo_tamanho_poligono +1
            print("caso 1")

        #Se apenas o ponto 1 está fora:
        elif (i_posicao >= 0 and k_posicao < 0):
            #Ponto de intersecção com a aresta e o segundo ponto são adicionados
            pontos_novos[novo_tamanho_poligono][0] = intersecoes_x(x1,y1,x2,y2,ix,iy,kx,ky)
            pontos_novos[novo_tamanho_poligono][1] = intersecoes_y(x1,y1,x2,y2,ix,iy,kx,ky)
            novo_tamanho_poligono = novo_tamanho_poligono +1

            pontos_novos[novo_tamanho_poligono][0] = kx
            pontos_novos[novo_tamanho_poligono][1] = ky
            novo_tamanho_poligono = novo_tamanho_poligono + 1
            print("caso 2")
        #Se apenas o ponto 2 está fora:
        elif (i_posicao<0 and k_posicao>=0):
            #Apenas o ponto de intersecção com a aresta é adicionado
            pontos_novos[novo_tamanho_poligono][0] = intersecoes_x(x1,y1,x2,y2,ix,iy,kx,ky)
            pontos_novos[novo_tamanho_poligono][1] = intersecoes_y(x1,y1,x2,y2,ix,iy,kx,ky)
            novo_tamanho_poligono = novo_tamanho_poligono +1
            print("caso 3")
        else:
            print("caso 4")

    #print(novo_tamanho_poligono)
    #Copiando novos pontos dentro do array original e mudando o número de vertices
    tamanho_poligono = novo_tamanho_poligono

    for i in range(tamanho_poligono):
        pontos_poligono[i][0] = pontos_novos[i][0]
        pontos_poligono[i][1] = pontos_novos[i][1]
    return tamanho_poligono

#Implementação do Algoritmo de Sutherland-Hodgman:
def Sutherland_Hodgman(pontos_poligono, tamanho_poligono, pontos_recorte, tamanho_recorte):
    #I e K são dois índices consecutivos:
    for i in range(tamanho_recorte):
        k = (i+1) % tamanho_recorte
        #Passa para a função os parâmetros: atual array de vertices, o tamanho do poligono e os pontos finais da linha de recorte selecionada
        tamanho_poligono = recorte_poligono(pontos_poligono, tamanho_poligono, pontos_recorte[i][0], pontos_recorte[i][1], pontos_recorte[k][0], pontos_recorte[k][1])

    #Printando os vertices do poligono recortado
    for i in range(tamanho_poligono):
        print(pontos_poligono[i][0])
        print(pontos_poligono[i][1])
        print("-")
    return pontos_poligono # [[0,0],[0,1]...[n,m]]

#print(Sutherland_Hodgman([[0,0],[0,10],[10,10],[10,0]],4,[[0,1],[0,6],[12,6],[12,0]],4))