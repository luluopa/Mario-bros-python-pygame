import pygame
from pygame.locals import *

framerate = 60
frame_quantity = 10
Gravity = 0.2
Velocity_move = 1

#detecta a colisao do rect com array de rect e retorna todos os rects que foram colididos
def Detect_collision(Rect, array_rect):
    array_hit = []
    for i in array_rect:
        if(Rect.colliderect(i)):
            array_hit.append(i)
    
    return array_hit

#movimento o rect caso nao tenha colisao, senao respeita a colisao
def Move_cani(Rect, momentum, array_object):
    Colision = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
    Rect.x += momentum[0]
    hit_array = Detect_collision(Rect, array_object)
    for hit in hit_array:
        if(momentum[0] > 0):
            Rect.right = hit.left
            Colision['Right'] = True
        if(momentum[0] < 0):
            Rect.left = hit.right
            Colision['Left'] = True
    Rect.y += momentum[1]
    hit_array = Detect_collision(Rect, array_object)
    for hit in hit_array:
        if(momentum[1] > 0):
            Rect.bottom = hit.top
            Colision['Down'] = True
        if(momentum[1] < 0):
            Rect.top = hit.bottom
            Colision['Up'] = True
    return Rect, Colision