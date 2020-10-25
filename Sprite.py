import pygame
from pygame.locals import *


#biblioteca feita em pygame para lidar com sprites feita por lucas lima
#é necessario inicializar a screen antes de usa - la
class Sprite():
    def __init__(self, path_image):
        try:
            self.path = str(path_image)
        except:
            print("entrada invalida de textura")

        self.sprite_sheet = pygame.image.load(self.path)

    def Charge_sprite(self, x, y, tam_x, tam_y):
        #cria uma superficia do tamanho do sprite
        Surf = pygame.Surface((tam_x, tam_y))
        #plota a parte do spritesheet do sprite pedido na superficie
        Surf.blit(self.sprite_sheet, (0,0), (x, y, tam_x, tam_y))

        #retorno do sprite na superficie
        return Surf

#so funciona se o sprite sheet estiver enfileirado de forma que
#cada posicao de um sprite seja a posicao do anterior com incremento
#do tamanho do sprite, e tem que ser organizado de forma matriz
def Create_arraysprite(sprite, x, y, tam_x, tam_y, final_x, final_y):
    array_sprite = []#declarando lista de sprite
    qtd_y = (final_y - y) / tam_y 
    qtd_x = (final_x - x) / tam_x
    #usando for para acessar cada sprite
    y_t = y
    for i in range(qtd_y):
        x_t = x
        for j in range(qtd_x):
            array_sprite.append(Charge_sprite(i, j, tam_x, tam_y))
            x_t += tam_x
        y_t += tam_y
        
    return array_sprite


        
        

