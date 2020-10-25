import pygame
import Mechanics
from pygame.locals import *

path = 'Sprite/Mobs_script/mobs.png'

#morte dos kopas verdes
kopa_death_tam = (15,16)
kopa_death = [(331,4),(361,4)]

#tamanho dos todos os kopas
kopa_tamanho_all = (17,24)

#kopa sprites

kopa_running_left = [(150,0),(180,0)]
kopa_running_right = [(210,0),(241,0)]

#kopa voador

kopa_flying_left = [(90,0),(120,0)]
kopa_flying_right = [(270,0),(301,0)]

#flor no indice 1 boca fechada indice 2 boca aberta

flor_verde_tam = [(17,25),(17,24)]
flor_verde = [(390,30),(420,30)]

#dinossauro vermelho

dinossauro_tam = (17,14)

dinossauro_vermelho_right = [(90,156),(120,156)]
dinossauro_vermelho_left = [(150,156),(180,156)]

dinossauro_fall_tam = (15,17)
dinossauro_fall = [(211,154),(241,154)]

#cogumelo andante marrom
cogumelo_tam = (17,17)

cogumelo_running = [(0,4),(30,4)]

cogumelo_death = [(60,8),(17,9)]

#bowser

bowser_tam = (33,33)

bowser_running_left = [(82,211),(122,211)]
bowser_running_right = [(163,211),(202,211)]

bowser_power_left = [(2,211),(42,211)]
bowser_power_right = [(243,211),(282,211)]

#poder do bowser

tam_fire = (25,9)

fire_bowser_left = [(101,253),(131,253)]
fire_bowser_right = [(161,253),(191,253)]


#tamanhos da surface
tamanho_kopa_norm = (30,45)
tamanho_kopa_death = (30,30)
tamanho_flor = (30,40)
tamanho_dinosaur = (30,30)
tamanho_cogumelo = (40,40)
tamanho_bowser = (50,50)

tamanho_poder_bowser = (20,20)

#tipos de mobs

kopa_int = 0
kopa_flyer_int = 1
flor_verde_int = 2
dinossauro_int = 3
cogumelo_andante_int = 4
bowser_int = 5

#velocidade da flor
Velocity_flor = 1

class Mob():
    def __init__(self):
        self.momentum = [0,0]

        try:
            self.sprite_sheet_mob = pygame.image.load(path)
        except:
            print("nao foi possivel carregar as texturas dos mobs")

        self.counter = 0

    def Create_sprite_list(self, lista_sprite, tam_i, tam_f):
        lista_surf = []
        for i in lista_sprite:
            Surf = pygame.Surface(tam_i)
            Surf.blit(self.sprite_sheet_mob, (0,0), (i[0],i[1],tam_i[0],tam_i[1]))
            Surf.set_colorkey((0,0,0))
            Surf = pygame.transform.scale(Surf, tam_f)
            lista_surf.append(Surf)
        return lista_surf

    def Find_one_sprite(self, pos_one, tam_i, tam_f):
        Surf = pygame.Surface(tam_i)
        Surf.blit(self.sprite_sheet_mob, (0,0),(pos_one[0],pos_one[1],tam_i[0],tam_i[1]))
        Surf.set_colorkey((0,0,0))
        Surf = pygame.transform.scale(Surf, tam_f)
        return Surf

#estados do kopa
i_am_alive = 0
kopa_is_death = 1

class Kopa(Mob):
    def __init__(self, pos, *args):
        super().__init__(*args)

        self.state = i_am_alive

        self.type = kopa_int

        #estados do kopa
        self.running_left = self.Create_sprite_list(kopa_running_left, 
        kopa_tamanho_all, tamanho_kopa_norm)
        self.running_right = self.Create_sprite_list(kopa_running_right, 
        kopa_tamanho_all, tamanho_kopa_norm)
        self.death = self.Create_sprite_list(kopa_death, 
        kopa_death_tam, tamanho_kopa_death)

        #keep state movement
        self.moving_left = False
        self.moving_right = True

        #control frame_time
        self.frame_actual = 0
        self.frame_max = 2

        self.touched_by_top = False

        self.kopa_rect = pygame.Rect(pos[0],pos[1],tamanho_kopa_norm[0],tamanho_kopa_norm[1])

    def Get_rect(self):
        return self.kopa_rect

    def death_or_win(self, mario):
        if(mario.momentum[0] > 0 or mario.momentum[0] < 0 or mario.momentum[1] < 0):
            mario.Collision_death()
            if(mario.Am_i_lose()):
                return 'death_mario'
            return 'keep_alive'
        else:
            self.touched_by_top = True
            mario.mario_rect.bottom = self.kopa_rect.top
            mario.momentum[1] = 0
            mario.momentum[1] -= 4
            return 'death_kopa'
    
    def Get_rect(self):
        return self.kopa_rect

    def Change_moving(self):
        if(self.moving_right):
            self.moving_right = False
            self.moving_left = True
        else:
            self.moving_left = False
            self.moving_right = True

    def Next_action_pos(self, tile_rect):
        if(self.moving_right):
            self.momentum[0] = Mechanics.Velocity_move
        if(self.moving_left):
            self.momentum[0] = -Mechanics.Velocity_move

        self.kopa_rect, Colision = Mechanics.Move_cani(self.kopa_rect, self.momentum, tile_rect)

        if(not Colision['Down']):
            self.momentum[1] += Mechanics.Gravity
        else:
            self.momentum[1] = 0
        
        if(Colision['Right']):
            self.Change_moving()
        if(Colision['Left']):
            self.Change_moving()

    def __update_frame(self):
        if(self.frame_actual == self.frame_max - 1):
            self.frame_actual = 0
        else:
            self.frame_actual += 1

    def Next_frame(self):
        self.__update_frame()
        if(self.touched_by_top):
            return self.death[self.frame_actual]
        if(self.moving_right):
            return self.running_right[self.frame_actual]
        if(self.moving_left):
            return self.running_left[self.frame_actual]
                
#kopa flying
class Kopa_flyer(Mob):
    def __init__(self, pos, *args):
        super().__init__(*args)

        self.state = i_am_alive

        self.type = kopa_flyer_int

        #estados do kopa
        self.flying_left = self.Create_sprite_list(kopa_flying_left, 
        kopa_tamanho_all, tamanho_kopa_norm)
        self.flying_right = self.Create_sprite_list(kopa_flying_right, 
        kopa_tamanho_all, tamanho_kopa_norm)
        self.death = self.Create_sprite_list(kopa_death, 
        kopa_death_tam, tamanho_kopa_death)

        #keep state movement
        self.moving_left = True
        self.moving_right = False

        #control frame_time
        self.frame_actual = 0
        self.frame_max = 2

        self.touched_by_top = False

        self.kopa_rect = pygame.Rect(pos[0],pos[1],tamanho_kopa_norm[0],tamanho_kopa_norm[1])

    def Get_rect(self):
        return self.kopa_rect

    def death_or_win(self, mario):
        if(mario.momentum[0] > 0 or mario.momentum[0] < 0 or mario.momentum[1] < 0):
            mario.Collision_death()
            if(mario.Am_i_lose()):
                return 'death_mario'
            return 'keep_alive'
        else:
            self.touched_by_top = True
            return 'death_kopafly'

    def Get_rect(self):
        return self.kopa_rect

    def Change_moving(self):
        if(self.moving_right):
            self.moving_right = False
            self.moving_left = True
        else:
            self.moving_left = False
            self.moving_right = True

    def Next_action_pos(self, tile_rect):
        if(self.moving_right):
            self.momentum[0] = Mechanics.Velocity_move
        if(self.moving_left):
            self.momentum[0] = -Mechanics.Velocity_move

        self.kopa_rect, Colision = Mechanics.Move_cani(self.kopa_rect, self.momentum, tile_rect)

        if(not Colision['Down']):
            self.momentum[1] += Mechanics.Gravity
        elif(not self.touched_by_top):
            self.momentum[1] -= 10
        
        if(Colision['Right']):
            self.Change_moving()
        if(Colision['Left']):
            self.Change_moving()

    def __update_frame(self):
        if(self.frame_actual == self.frame_max - 1):
            self.frame_actual = 0
        else:
            self.frame_actual += 1

    def Test_colision_player(self, rect_player):
        if(self.kopa_rect.colliderect(rect_player)):
            return True
        return False

    def Next_frame(self):
        self.__update_frame()
        if(self.touched_by_top):
            return self.death[self.frame_actual]
        if(self.moving_right):
            return self.flying_right[self.frame_actual]
        if(self.moving_left):
            return self.flying_left[self.frame_actual]

class Flor_Verde(Mob):
    def __init__(self, pos, *args):
        super().__init__(*args)

        self.type = flor_verde_int

        self.flor_rect = pygame.Rect(pos[0],pos[1],tamanho_flor[0],tamanho_flor[1])

        self.flor_sprites = self.Create_sprite_list(flor_verde, flor_verde_tam[0], tamanho_flor)

        self.max = self.flor_rect.y - 50
        self.minimum = self.flor_rect.y + 50

        self.control_frame = 1

        self.Up_all = False
        self.Down_minimum = True

    def Get_rect(self):
        return self.flor_rect

    def death_or_win(self, mario):
        mario.Collision_death()
        if(mario.Am_i_lose()):
            return 'death_mario'
        return 'keep_alive'

    def Get_rect(self):
        return self.flor_rect

    def Next_action_pos(self, tile_rect):
        if(self.Up_all):
            self.momentum[1] = -Velocity_flor
        if(self.Down_minimum):
            self.momentum[1] = Velocity_flor

        print(self.Up_all, self.Down_minimum)

        self.flor_rect, Colision = Mechanics.Move_cani(self.flor_rect, self.momentum, tile_rect)

        self.Touched_max_height()

    def Touched_max_height(self):
        if(self.flor_rect.y == self.max):
            self.Up_all = False
            self.Down_minimum = True
        if(self.flor_rect.y == self.minimum):
            self.Up_all = True
            self.Down_minimum = False

    def Next_frame(self):
        self.control_frame += 1
        if(self.control_frame % 3 == 0):
            return self.flor_sprites[1]
        return self.flor_sprites[0]

maximo_frame = 2

class Dinosaur(Mob):
    def __init__(self, pos, *args):
        super().__init__(*args)

        self.type = dinossauro_int

        self.dinosaur_rect = pygame.Rect(pos[0],pos[1],tamanho_dinosaur[0], tamanho_dinosaur[1])

        self.running_left = self.Create_sprite_list(dinossauro_vermelho_left, dinossauro_tam, tamanho_dinosaur)
        self.running_right = self.Create_sprite_list(dinossauro_vermelho_right, dinossauro_tam, tamanho_dinosaur)

        self.fall = self.Create_sprite_list(dinossauro_fall, dinossauro_fall_tam, tamanho_dinosaur)

        self.moving_left = True
        self.moving_right = False
        self.falling = False

        #controlar os frame-time
        self.frame_actual = 0
        self.max_frame = maximo_frame

    def Get_rect(self):
        return self.dinosaur_rect

    def death_or_win(self, mario):
        mario.Collision_death()
        if(mario.Am_i_lose()):
            return 'death_mario'
        return 'keep_alive'

    def Get_rect(self):
        return self.dinosaur_rect
    
    def Change_moving(self):
        if(self.moving_right):
            self.moving_right = False
            self.moving_left = True
        else:
            self.moving_left = False
            self.moving_right = True

    def Next_action_pos(self, tile_rect):
        if(self.moving_right):
            self.momentum[0] = Mechanics.Velocity_move
        if(self.moving_left):
            self.momentum[0] = -Mechanics.Velocity_move

        self.kopa_rect, Colision = Mechanics.Move_cani(self.dinosaur_rect, self.momentum, tile_rect)

        if(not Colision['Down']):
            self.momentum[1] += Mechanics.Gravity
            self.falling = True
        else:
            self.falling = False
            self.momentum[1] = 0
        
        if(Colision['Right']):
            self.Change_moving()
        if(Colision['Left']):
            self.Change_moving()

    def __update_frame(self):
        if(self.frame_actual == self.max_frame - 1):
            self.frame_actual = 0
        else:
            self.frame_actual += 1

    def Next_frame(self):
        self.__update_frame()
        print(self.falling)
        if(self.falling):
            return self.fall[self.frame_actual]
        if(self.moving_left):
            return self.running_left[self.frame_actual]
        if(self.moving_right):
            return self.running_right[self.frame_actual]

class Cogumelo_andante(Mob):
    def __init__(self, pos, *args):
        super().__init__(*args)

        self.type = cogumelo_andante_int

        self.cogumelo_rect = pygame.Rect(pos[0],pos[1],tamanho_cogumelo[0], tamanho_cogumelo[1])

        self.running = self.Create_sprite_list(cogumelo_running, cogumelo_tam, tamanho_cogumelo)

        self.moving_left = True
        self.moving_right = False

        #controlar os frame-time
        self.frame_actual = 0
        self.max_frame = maximo_frame

    def Get_rect(self):
        return self.cogumelo_rect

    def death_or_win(self, mario):
        if(mario.momentum[0] > 0 or mario.momentum[0] < 0 or mario.momentum[1] < 0):
            mario.Collision_death()
            if(mario.Am_i_lose()):
                return 'death_mario'
            return 'keep_alive'
        else:
            return 'death_cogumelo'

    def Get_rect(self):
        return self.cogumelo_rect

    def Change_moving(self):
        if(self.moving_right):
            self.moving_right = False
            self.moving_left = True
        else:
            self.moving_left = False
            self.moving_right = True

    def Next_action_pos(self, tile_rect):
        if(self.moving_right):
            self.momentum[0] = Mechanics.Velocity_move
        if(self.moving_left):
            self.momentum[0] = -Mechanics.Velocity_move

        self.kopa_rect, Colision = Mechanics.Move_cani(self.cogumelo_rect, self.momentum, tile_rect)

        if(not Colision['Down']):
            self.momentum[1] += Mechanics.Gravity
        else:
            self.momentum[1] = 0
        
        if(Colision['Right']):
            self.Change_moving()
        if(Colision['Left']):
            self.Change_moving()

    def __update_frame(self):
        if(self.frame_actual == self.max_frame - 1):
            self.frame_actual = 0
        else:
            self.frame_actual += 1

    def Next_frame(self):
        self.__update_frame()
        return self.running[self.frame_actual]
    
class Bowser(Mob):
    def __init__(self, pos, *args):
        super().__init__(*args)

        self.type = bowser_int

        self.bowser_rect = pygame.Rect(pos[0],pos[1],tamanho_cogumelo[0], tamanho_cogumelo[1])

        self.running_left = self.Create_sprite_list(bowser_running_left, bowser_tam, tamanho_bowser)
        self.running_right = self.Create_sprite_list(bowser_running_right, bowser_tam, tamanho_bowser)

        self.power_right = self.Create_sprite_list(bowser_power_right, bowser_tam, tamanho_bowser)
        self.power_left = self.Create_sprite_list(bowser_power_left, bowser_tam, tamanho_bowser)

        self.moving_left = True
        self.moving_right = False
        self.mt_perto = False

        #controlar os frame-time
        self.frame_actual = 0
        self.max_frame = maximo_frame
    
    def Get_rect(self):
        return self.bowser_rect

    def death_or_win(self, mario):
        mario.Collision_death()
        if(mario.Am_i_lose()):
            return 'death_mario'
        return 'keep_alive'

    def Get_rect(self):
        return self.bowser_rect

    def Change_moving(self):
        if(self.moving_right):
            self.moving_right = False
            self.moving_left = True
        else:
            self.moving_left = False
            self.moving_right = True

    def Next_action_pos(self, tile_rect, player_rect):
        
        if(player_rect.x < self.bowser_rect.x):
            if(player_rect.x > self.bowser_rect.x - 50):
                self.mt_perto = True
            else:
                self.mt_perto = False
            self.moving_left = True
            self.moving_right = False
        else:
            if(player_rect.x < self.bowser_rect.x + 50):
                self.mt_perto = True
            else:
                self.mt_perto = False
            self.moving_left = False
            self.moving_right = True

        self.kopa_rect, Colision = Mechanics.Move_cani(self.bowser_rect, self.momentum, tile_rect)

        if(not Colision['Down']):
            self.momentum[1] += Mechanics.Gravity
        else:
            self.momentum[1] = 0

    def __update_frame(self):
        if(self.frame_actual == self.max_frame - 1):
            self.frame_actual = 0
        else:
            self.frame_actual += 1

    def Next_frame(self):
        self.__update_frame()
        if(self.moving_left):
            if(self.mt_perto):
                return self.power_left[self.frame_actual]
            return self.running_left[self.frame_actual]
        if(self.moving_right):
            if(self.mt_perto):
                return self.power_right[self.frame_actual]
            return self.running_right[self.frame_actual]

    def Test_colision_player(self, player_rect):
        if(self.dinosaur_rect.colliderect(player_rect)):
            return True
        return False

class power_fire(Mob):
    def __init__(self, pos, *args):
        super().__init__(*args)

        self.power_rect = pygame.Rect(pos[0],pos[1],tamanho_cogumelo[0], tamanho_cogumelo[1])

        self.power_right = self.Create_sprite_list(fire_bowser_right, tam_fire, tamanho_poder_bowser)
        self.power_left = self.Create_sprite_list(fire_bowser_right, tam_fire, tamanho_poder_bowser)

        self.moving_left = True
        self.moving_right = False

        #controlar os frame-time
        self.frame_actual = 0
        self.max_frame = maximo_frame
    
    def Get_rect(self):
        return self.power_rect

    def __update_frame(self):
        if(self.frame_actual == self.max_frame - 1):
            self.frame_actual = 0
        else:
            self.frame_actual += 1

    def Next_frame(self):
        self.__update_frame()
        if(self.moving_left):
            return self.running_left[self.frame_actual]
        if(self.moving_right):
            return self.running_right[self.frame_actual]

    def Test_colision_player(self, player_rect):
        if(self.dinosaur_rect.colliderect(player_rect)):
            return True
        return False