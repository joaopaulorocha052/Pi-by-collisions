
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : João Paulo P. Rocha
# Created Date: 14/08/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" 

Este projeto tem como objetivo calcular o número de colisões entre dois blocos, um de massa unitária e o outro de massa muito maior. 
O número de colisões entre os blocos deverá ser uma aproximação de Pi e quanto maior o número, maior a precisão do número calculado.

""" 
# ---------------------------------------------------------------------------
import pygame
import sympy as sp
import math as mt
# ---------------------------------------------------------------------------
from pygame.locals import *
from numpy import roots
# ---------------------------------------------------------------------------

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0, 200, 255)
RED = (230,52,39)

# Definição da classe de blocos
class Block:
    def __init__(self, mass, height, length, x ,y , speed, color) :
        self.mass = mass #massa
        self.height = height #altura
        self.length = length #comprimento
        self.x = x #posição no eixo x
        self.y = y #posição no eixo y
        self.x_speed = speed #velocidade
        self.color = color #cor
        self.mask = pygame.mask.Mask((self.length, self.height), True) #mascara

        #desenho e declaracao do rect
        self.surface = pygame.Surface((length,height))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
    #funcao que adiciona a velocidade a posicao x de um bloco, atualizando a posicao
    def speed(self):
        self.x += self.x_speed
        

pygame.init()

screen = pygame.display.set_mode((800, 600))    

#inicialização dos blocos
big_block = Block(100,46,46, 400, 280, -10, BLUE)
small_block = Block(1,26,26, 200, 300, 0, RED)
block_list = [big_block, small_block]

#calcula o offset entre dois blocos
def offset(mask1, mask2):
    return int(mask2.x - mask1.x), int(mask2.y - mask1.y)
#collisions
collisions = 0

#variaveis e funcoes da fonte
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

def show_collisions(x, y):
    count = font.render("# of collisions: " + str(collisions), True, WHITE)
    screen.blit(count, (x, y))
#loop principal
game_on = True
while game_on:
    
    i = 0
    #desenha princiapais elementos na tela, como a parede e o chão
    pygame.time.Clock().tick(60)
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (799, 326), (1, 326))
    pygame.draw.line(screen, WHITE, (1, 1), (1, 326))

    #verifica o fechamento da janela
    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_BACKSPACE:
                game_on = False
        elif event.type == QUIT:
            game_on = False
    
    #calculos principais

    #verifica se alguns dos blocos atingiu a parede, para serem refletidos
    if big_block.x < 0:
        big_block.x_speed *= -1
    if small_block.x < 0:
        collisions += 1
        small_block.x_speed *= -1
    #verifica se os blocos colidiram e realiza o calculo do momento linear e da energia cinetica, utilizando
    #os resultados para calcular as velocidades futuras de ambos os blocos
    if small_block.mask.overlap(big_block.mask, offset(small_block, big_block)):
        collisions += 1
        k1 = (big_block.mass*big_block.x_speed)+(small_block.mass*small_block.x_speed) #momento linear: m1*v1 + m2*v2 = constante
        k2 = 0.5*(big_block.mass*(big_block.x_speed**2))+0.5*(small_block.mass*(small_block.x_speed**2)) #energia cinetica: (m1*v1²)/2 + (m2*v2²)/2 = constante
        print(k1, k2)
        #funcao para resolver o sistema de equacoes nao lineares
        x,y = sp.symbols('v1,v2')
        f = sp.Eq(big_block.mass * x + small_block.mass * y, k1)
        g = sp.Eq(0.5 * (big_block.mass * (x**2)) + 0.5 * (small_block.mass * (y**2)), k2)
        roots = sp.solve([f,g], (x,y))
        print(f'roots: {roots}')
        #atualiza as velocidades dos blocos
        big_block.x_speed = roots[1][0]
        small_block.x_speed = roots[1][1]

    
        print(f"speeds: b:{big_block.x_speed} s:{small_block.x_speed}")
    #atualiza a posicao dos blocos
    big_block.speed()
    small_block.speed()
    
    big_block_x = round(big_block.x)
    small_block_x = round(small_block.x)

    # big_block_x = big_block.x
    # small_block_x = small_block.x

    #desenha ambos os blocos e o numero de colisoes na tela
    screen.blit(big_block.surface, (big_block_x, big_block.y))
    screen.blit(small_block.surface, (small_block_x, small_block.y))
    show_collisions(text_x, text_y)

    pygame.display.update()
