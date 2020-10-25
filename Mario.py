# -*- coding: utf-8 -*-
import pygame, sys
import Player
import Map
import Mob
from pygame import mixer
from pygame.locals import * 

pygame.init()
pygame.font.init()

file = 'world1-music.mp3'
mixer.init()
teste = mixer.music.load(file)
mixer.music.play()

WINDOW = (800, 600) #tamanho da tela
Screen = pygame.display.set_mode(WINDOW) #inicializando a tela

Displayer_tam = (534,400)

Display = pygame.Surface(Displayer_tam) # display para aumentar a tela proporcionalmente

pygame.display.set_caption("Mario")

Clock = pygame.time.Clock() #clock para respeitar o limite de frame
#mapa
mapa = Map.Map('Map/World-1/mapa1.png', [Displayer_tam[0],Displayer_tam[1]])
game_map = mapa.map

#guardar os retangulos
tile_rects = []

#premios
moeda = 1
cogumelo = 2
flamejante = 3

#detecta a colisao do mario com os mobs
def Detect_Collision_mob(mario, all_mobs_display):
    for mob in all_mobs_display:
        if(mob.type == Mob.kopa_int):
            if(mario.mario_rect.colliderect(mob.Get_rect())):
                if(mob.death_or_win(mario) == 'death_mario'):
                    pygame.quit()
                    sys.exit() 
        if(mob.type == Mob.kopa_flyer_int):
            if(mario.mario_rect.colliderect(mob.Get_rect())):
                if(mob.death_or_win(mario) == 'death_mario'):
                    pygame.quit()
                    sys.exit()
                else:
                    mob = Mob.Kopa([mob.Get_rect().x,mob.Get_rect().y])
        if(mob.type == Mob.flor_verde_int):
            if(mario.mario_rect.colliderect(mob.Get_rect())):
                if(mob.death_or_win(mario) == 'death_mario'):
                    pygame.quit()
                    sys.exit()
        if(mob.type == Mob.dinossauro_int):
            if(mario.mario_rect.colliderect(mob.Get_rect())):
                if(mob.death_or_win(mario) == 'death_mario'):
                    pygame.quit()
                    sys.exit()
        if(mob.type == Mob.cogumelo_andante_int):
            if(mario.mario_rect.colliderect(mob.Get_rect())):
                if(mob.death_or_win(mario) == 'death_mario'):
                    pygame.quit()
                    sys.exit()
                else:
                    all_mobs_display.remove(mob)

#detecta a colisao do rect com array de rect e retorna todos os rects que foram colididos
def Detect_collision(Rect, array_rect):
    array_hit = []
    for i in array_rect:
        if(Rect.colliderect(i)):
            array_hit.append(i)
    
    return array_hit

#movimento o rect caso nao tenha colisao, senao respeita a colisao
def Move_cani(mario, array_object, all_mobs_display, mapa):
    Colision = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
    if(mario.mario_rect.x - mapa.map_current_pos_map[0] >= 160 and mario.momentum[0] > 0):
        mapa.map_current_pos_map[0] += Velocity_move
        mario.mario_rect.x += mario.momentum[0]
    else:
        mario.mario_rect.x += mario.momentum[0]
    hit_array = Detect_collision(mario.mario_rect, array_object)
    Detect_Collision_mob(mario, all_mobs_display)
    for hit in hit_array:
        if(mario.momentum[0] > 0):
            mario.mario_rect.right = hit.left
            Colision['Right'] = True
        if(mario.momentum[0] < 0):
            mario.mario_rect.left = hit.right
            Colision['Left'] = True
    mario.mario_rect.y += mario.momentum[1]
    hit_array = Detect_collision(mario.mario_rect, array_object)
    Detect_Collision_mob(mario, all_mobs_display)
    for hit in hit_array:
        if(mario.momentum[1] > 0):
            mario.mario_rect.bottom = hit.top
            Colision['Down'] = True
        if(mario.momentum[1] < 0):
            mario.mario_rect.top = hit.bottom
            Colision['Up'] = True
    return mario.mario_rect, Colision

def Get_next_frame(mob, counter, Surf_actual):
    if(counter % (framerate/frame_quantity) == 0):
        counter = 1
        Surf = mob.Next_frame()
        return counter, Surf
    else:
        counter += 1
        return counter, Surf_actual

def Get_next_frame_mob(mob, counter, Surf_actual):
    if(mob.counter % (framerate/frame_quantity) == 0):
        mob.counter = 1
        Surf = mob.Next_frame()
        return Surf
    else:
        mob.counter +=1
        return Surf_actual

#next pos vai passar o x e o y do rect
def Next_step(lista_surf, tile_rect, all_mobs_display):
    new_frames = []
    x = 0
    for mob in all_mobs_display:
        mob.Next_action_pos(tile_rect)
        surf_actual = Get_next_frame_mob(mob, mob.counter, lista_surf[x])
        new_frames.append(surf_actual)
        x+=1
    return new_frames

def Plot_all_mobs(display, frames, all_mobs_display):
    x=0
    for surface in frames:
        display.blit(surface, (all_mobs_display[x].Get_rect().x - mapa.map_current_pos_map[0]
        ,all_mobs_display[x].Get_rect().y - mapa.map_current_pos_map[1]))
        x+=1

def Get_pressed(lista_pressed, jogador, test_cos):
    if(lista_pressed[K_RIGHT]):
        jogador.moving_right = True
        jogador.remaing_stand = Player.right
    if(lista_pressed[K_LEFT]):
        jogador.moving_left = True
        jogador.remaing_stand = Player.left
    if(lista_pressed[K_UP] and test_cos['Down']):
        jogador.jump_fall = True
        jogador.momentum[1] -= 7

#checar se perdeu

framerate = 60
frame_quantity = 10
Gravity = 0.3
Velocity_move = 3

def Main():
    #player
    jogador = Player.Player(0)
    Surface_player = pygame.Surface((15,10))
    counter = 0
    tile_pressed = []
    lista_mob = [Mob.Kopa_flyer([500,200]), Mob.Kopa([600,400]), Mob.Cogumelo_andante([700,300]), Mob.Flor_Verde([500,700]),
    Mob.Dinosaur([400,200])]
    lista_mob_surf = []
    for i in lista_mob:
        lista_mob_surf.append(i.Next_frame())
    while True:
        #atualizar
        Display.fill((146,244,255))
        Display.blit(mapa.Render_current_camera(), (0,0))
        tile_rects = mapa.tile_rect
        #mudar as posicoes
        jogador.momentum[0] = 0
        if(jogador.moving_right):
            jogador.remaing_stand = Player.right
            jogador.momentum[0] = Velocity_move
            jogador.moving_right = False
        if(jogador.moving_left):
            jogador.remaing_stand = Player.left
            jogador.momentum[0] = -Velocity_move
            jogador.moving_left = False
        jogador_rect, Colision = Move_cani(jogador, tile_rects, lista_mob, mapa)
        lista_mob_surf = Next_step(lista_mob_surf, tile_rects, lista_mob)
        if(not Colision['Down']):
            jogador.momentum[1] += Gravity
        else:
            jogador.momentum[1] = 0
            jogador.jump_fall = False
        if(Colision['Up']):
            jogador.momentum[1] = 0
        #pĺotar o player
        Display.blit(Surface_player, (jogador.mario_rect.x - mapa.map_current_pos_map[0], jogador.mario_rect.y - mapa.map_current_pos_map[1]))
        Plot_all_mobs(Display, lista_mob_surf, lista_mob)
        #checa se o usuario esta se mexendo
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #pegando entrada do usuario
        tile_pressed = pygame.key.get_pressed()
        Get_pressed(tile_pressed, jogador, Colision)

        counter, Surface_player = Get_next_frame(jogador, counter, Surface_player)

        surf = pygame.transform.scale(Display, WINDOW)# muda a escala dos objetos
        Screen.blit(surf, (0,0))
        pygame.display.update()
        Clock.tick(framerate) # mantem a taxa de atualização a 60 frames

if __name__ == "__main__":
    Main()    