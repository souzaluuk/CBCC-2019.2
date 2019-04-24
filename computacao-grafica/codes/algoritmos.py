
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
    x2,y2 = p2

    pixels = list() # lista de pixels que será retornada
    e = m - 0.5 # primeiro valor de 'e'

    pixels.append(p1)
    while x1 < x2:
        if e >= 0:
            y1 += 1
            e -= 1
        x1 += 1
        e += m
        pixels.append((x1,y1))
    _reflexao(pixels,trocaxy,trocax,trocay)
    return pixels

print(bresenham((0,0),(5,5)))