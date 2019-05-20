# CG-2019
### Descrição
Programa desenvolvido em Python como parte da avaliação da disciplina de Computação Gráfica, curso de CBCC-UFPA.
### Alunos:
- Ian Campos Bezerra Rêgo - 201604940043
- Lucas Gabriel de Souza - 201604940039
### Objetivos
Desenvolver um software com interface gráfica que utilize os algoritmos ministrados em aula e mostre o resultado em uma grade de pixels. Considere como pixel da sua aplicação 5x5 pixels reais.

Os algoritmos que devem ser implementados são os seguintes:

- Bresenham :+1:
- Círculos :+1:
- Curvas Bezier :+1:
- Preencimento Recursivo :+1:
- Preencimento Scanline :+1: ~~Parcial~~
- Recorte de linha :+1:
- Recorte de polígonos :+1:
- Transformações
    - Translação :+1:
    - Rotação :+1:
    - Escala :+1:
- Projeções Ortográficas :-1:
- Projeções Perspectivas :+1:

### Estrutura
O programa se divide em três arquivos distintos:
- [Algoritmos](codes/algoritmos.py)
- [Tela](codes/app.py)
- [Elementos](codes/elementos.py)

### Executando
Os arquivos do programa econtram-se em [codes](codes) e bastam estar no mesmo diretório para seu funcionamento. Além disso, para início da aplicação, deve-se executar:
```bash
$ python3 app.py
```
** `No manjaro, necessário executar: sudo pacman -S tk`
### Exemplo

![Exemplo app](exemplo_app.png)
