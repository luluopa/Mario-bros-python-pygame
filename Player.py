import pygame
import Sprite
from pygame.locals import *

max_framesprite = 3

#caminho do sprite
caminho = ['Sprite/Player_script/player.png']

#tamanho do player
tamanho_pmario_grande = (27,50)
tamanho_pmario_pequeno = (25, 28) 
tamanho_pmario_sleep = (15, 20)

tamanho_mario_grande = (16, 33)
tamanho_mario_pequeno = (17, 17) 
tamanho_mario_sleep = (16, 23)

#mario grande sprites

mario_correndo_esquerda = [(150, 52),(121, 52),(90, 52)]
mario_correndo_direita = [(239, 52), (270, 52), (299, 52)]

mario_sprint = [(60, 52), (329, 52)] # 0 e sprint da esquerda 1 sprint da dit
mario_jump = [(30, 52), (359, 52)] # 0 e jump da esquerda 1 jump da dit

mario_sleep = [(1, 52),(389, 52)] # 0 e sleep da esquerda 1 sleep da dit
mario_stand = [(180, 52), (209, 52)] # 0 e stand da esquerda 1 stand da dit

#mario pequeno

mariop_correndo_esquerda = [(89,0),(121,0),(150,0)]
mariop_correndo_direita = [(239,0),(269,0),(300,0)]

mariop_sprint = [(60,0),(331,0)]
mariop_jump = [(29,0),(359,0)]

mariop_stand = [(181,0),(211,0)]

#mario flamejante

mariof_correndo_esquerda = [(102,122),(128,122),(152,122)]
mariof_correndo_direita = [(237,122),(263,122),(287,122)]

mariof_sprint = [(52,122),(337,122)]
mariof_jump = [(27,122),(362,122)]

mariof_sleep = [(1,127),(389,127)]
mariof_stand = [(180,122),(209,122)]

mario_grande = 0
mario_pequeno = 1
mario_flamejante = 2

#posicao que o player comeca no display
init_pos = (0,-200)

#remain stand
left = 0
right = 1
empty = 2

class Player():
    def __init__(self, teste):

        #posicao e momento do player
        self.momentum = [0,0]

        #stados do mario
        self.state_mario = teste
        self.sleep = False

        #menu
        self.life = 3

        #carregando os sprites do estado0
        self.state0_mario_running_right = self.Create_sprite_list(caminho[0], mario_correndo_direita, tamanho_mario_grande, 0)
        self.state0_mario_running_left = self.Create_sprite_list(caminho[0], mario_correndo_esquerda, tamanho_mario_grande, 0)
        self.state0_mario_stand = self.Create_sprite_list(caminho[0], mario_stand, tamanho_mario_grande, 0)
        self.state0_mario_jump = self.Create_sprite_list(caminho[0], mario_jump, tamanho_mario_grande, 0)
        self.state0_mario_sprint = self.Create_sprite_list(caminho[0], mario_sprint, tamanho_mario_grande, 0)
        self.state0_mario_sleep = self.Create_sprite_list(caminho[0], mario_sleep, tamanho_mario_sleep, 0)

        #carregando os sprites do estado1
        self.state1_mario_running_right = self.Create_sprite_list(caminho[0], mariop_correndo_direita, tamanho_mario_pequeno, 1)
        self.state1_mario_running_left = self.Create_sprite_list(caminho[0], mariop_correndo_esquerda, tamanho_mario_pequeno, 1)
        self.state1_mario_stand = self.Create_sprite_list(caminho[0], mariop_stand, tamanho_mario_pequeno, 1)
        self.state1_mario_jump = self.Create_sprite_list(caminho[0], mariop_jump, tamanho_mario_pequeno, 1)
        self.state1_mario_sprint = self.Create_sprite_list(caminho[0], mariop_sprint, tamanho_mario_pequeno, 1)

        #carregando os sprite do estado2
        self.state2_mario_running_right = self.Create_sprite_list(caminho[0], mariof_correndo_direita, tamanho_mario_grande, 2)
        self.state2_mario_running_left = self.Create_sprite_list(caminho[0], mariof_correndo_esquerda, tamanho_mario_grande, 2)
        self.state2_mario_stand = self.Create_sprite_list(caminho[0], mariof_stand, tamanho_mario_grande, 2)
        self.state2_mario_jump = self.Create_sprite_list(caminho[0], mariof_jump, tamanho_mario_grande, 2)
        self.state2_mario_sprint = self.Create_sprite_list(caminho[0], mariof_sprint, tamanho_mario_grande, 2)
        self.state2_mario_sleep = self.Create_sprite_list(caminho[0], mariof_sleep, tamanho_mario_sleep, 2)

        self.state0_mario_running_left.reverse()
        self.state0_mario_running_right.reverse()
        self.state1_mario_running_left.reverse()
        self.state2_mario_running_left.reverse()
        
        #rect do mario
        self.mario_rect = self.Create_rect(init_pos)

        #estado de movimento
        self.moving_right = False
        self.moving_left = False
        self.jump_fall = False
        self.remaing_stand = 0

        #estado do jogo
        self.lost = False
    
        #controle do estado
        self.state_frame = 0
        self.max_frame = max_framesprite

    def Collision_death(self):
        self.Change_state_mario()

    def Am_i_lose(self):
        return self.lost

    def Grow_up(self):
        if(self.state_mario == mario_pequeno):
            self.state_mario = mario_grande
            self.mario_rect = self.Create_rect()

    def Check_cog(self, rect_cog):
        if(self.mario_rect.colliderect(rect_cog)):
            if(self.state_mario == mario_pequeno):
                self.state_mario = 0
                self.mario_rect = self.Create_rect()
            return True
    
    def __Update_state(self):
        if(self.state_frame == self.max_frame-1):
            self.state_frame = 0
        else:
            self.state_frame += 1

    def __sleep_rect_surf(self, sprite):
        self.mario_rect = pygame.Rect(self.mario_rect.x, self.mario_rect.y, sprite.get_width(), sprite.get_height())
        if(remaing_stand == right):
            return sprite[1]
        else:
            return sprite[0]

    def __return_rect_sleep(self):
        self.mario_rect = self.Create_rect()

    def __Condict_frame(self, running_right, running_left, stand, jump, sprint, sleep=None):
        if(self.jump_fall):
            if(self.remaing_stand == right):
                return jump[1]
            else:
                return jump[0]

        if(self.moving_right):
            self.__Update_state()
            if(self.remaing_stand == left):
                return sprint[0]
            return running_right[self.state_frame]

        if(self.moving_left):
            self.__Update_state()
            if(self.remaing_stand == right):
                return sprint[1]
            return running_left[self.state_frame]

        if(not (self.moving_right or self.moving_left)):
            if(self.remaing_stand == right):
                return stand[1]
            if(self.remaing_stand == left):
                return stand[0]

        if(self.sleep):
            return self.__sleep_rect_surf(sleep)

    def Change_state_mario(self):
        if(self.state_mario == mario_grande):
            self.state_mario = mario_pequeno
            self.mario_rect = self.Create_rect([self.mario_rect.x,self.mario_rect.y])
        if(self.state_mario == mario_flamejante):
            self.state_mario = mario_pequeno
            self.mario_rect = self.Create_rect([self.mario_rect.x,self.mario_rect.y])

    def Next_frame(self):
        if(self.state_mario == mario_grande):
            return self.__Condict_frame(self.state0_mario_running_right, self.state0_mario_running_left,
            self.state0_mario_stand, self.state0_mario_jump, self.state0_mario_sprint, self.state0_mario_sleep)
        if(self.state_mario == mario_pequeno):
            return self.__Condict_frame(self.state1_mario_running_right, self.state1_mario_running_left,
            self.state1_mario_stand, self.state1_mario_jump, self.state1_mario_sprint)
        if(self.state_mario == mario_flamejante):
            return self.__Condict_frame(self.state2_mario_running_right, self.state2_mario_running_left,
            self.state2_mario_stand, self.state2_mario_jump, self.state2_mario_sprint, self.state2_mario_sleep)

    def Create_rect(self, pos):
        if(self.state_mario == mario_grande or self.state_mario == mario_flamejante):
            rect = pygame.Rect(pos[0], pos[1],tamanho_pmario_grande[0],tamanho_pmario_grande[1])
            return rect
        else:
            rect = pygame.Rect(pos[0],pos[1],tamanho_pmario_pequeno[0], tamanho_pmario_pequeno[1])
            return rect

    def __transform_scale(self, Surf, estado):
        if(self.sleep):
            return pygame.transform.scale(Surf, tamanho_pmario_sleep)
        if(estado == mario_grande or estado == mario_flamejante):
            return pygame.transform.scale(Surf, tamanho_pmario_grande)
        if(estado == mario_pequeno):
            return pygame.transform.scale(Surf, tamanho_pmario_pequeno)       

    def Create_sprite_list(self, path, player_walkn, tam, estado):
        image = pygame.image.load(path).convert_alpha()
        array = []
        for i in player_walkn:
            Surf = pygame.Surface(tam)
            Surf.blit(image, (0,0), (i[0], i[1], tam[0], tam[1]))
            Surf = self. __transform_scale(Surf, estado)
            Surf.set_colorkey((0,0,0))
            array.append(Surf)
        return array

    def Move_Left_Right(self, walk_intensity):
        self.jogador_rect.x += walk_intensity
    
    def Jump(self, jump_intensity):
        self.jogador_rect.y += jump_intensity
