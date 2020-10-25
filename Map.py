#pegar a posicao do player, e vou pplotar pegando as dimensoes da camera na posicao central dentro do map
import pygame
from pygame.locals import *

pygame.init()

#palheta de cores que serve para renderizar a tela
preto = (50,50,5) #bloco_chao
cinza = (128,128,128) #premium cogumelo ou flamejante
azul = (0,0,255) #bloco_liso
ciano = (0,255,255) #nuvem_grande
limao = (0,255,0) #bloco_pedra 
red = (255,0,0) #grama_grande
cinza_cast = (143,143,143)# castelo pequeno

#sprites itens
sprite_item = ['Sprite/Itens_sprite/items.png']

#sprite map
sprite_map = ['Sprite/Itens_sprite/mapa.png']

#localizacao no sprite, posicao//tamanho x y
cogumelo = [(184, 34),(17,17)]
vida = [(214,34), (17,17)]

#localizacao no sprite do mapa, posicao//tamanho x y
bloco_pedra = [(365, 36), (17,17)]
bloco_chao = [(365, 113), (17,17)]
bloco_liso = [(365,131), (18,18)]


#ant e dep e um só
ant_premium = [(364,149), (17,17)]
dep_premium = [(365, 73), (17,17)]

nuvem_grande = [(88,187), (65,25)]
nuvem_pequena = [(154,187),(32,25)]
nuvem_media = [(38,187),(49,25)]

grama_grande = [(77,242),(65,17)]
grama_media = [(143,242),(49,17)]
grama_pequena = [(43,242),(33,17)]

castelo_pequeno = [(264,207),(81,81)]

barril_final = [(606,35),(33,33)]
barril_constituente = [(608,71),(29,17)]

#tamanhos
tamanho_castelo_pequeno = (200,200)
tamanho_blocos_chao = (25,25)
tamanho_nuvem_grande = (150,40)
tamanho_grama_grande = (150,30)


#tamanho item
tamanho_item = (20,20)

#ordem dos itens do mapa
pedra = 1
chao_bloco = 2
pedras_lisas = 3
nuvem_g = 4
grama_g = 5
cogumelo = 6
castelo = 7

#escalas
escala = (25,25)

class Item():
    def __init__(self, tam=[20,20]):
        #inicializando o momento do item do mapa
        self.momentum = [0,0]

        #criando rect padrao dos itens
        self.item_rect = pygame.Rect(0,0, tam[0], tam[1])

class Cogumelo(Item):
    def __init__(self, *args):
        #passando argumentos para o construtor da classe mae
        super().__init__(*args)

        self.sprite_cog = pygame.image.load(sprite_item[0])
        self.texture_cog = self.find_sprite()

        self.moving_right = False
        self.moving_left = True

        self.type = 2

    def find_sprite(self):
        Surf = pygame.Surface(cogumelo[1])
        Surf.blit(self.sprite_cog, (0,0), (cogumelo[0][0], cogumelo[0][1], cogumelo[1][0], cogumelo[1][1]))
        Surf.set_colorkey((0,0,0))
        return Surf

class Vida(Item):
    def __init__(self, *args):
        #passando argumentos para o construtor da classe mae
        super().__init__(*args)

        self.sprite_cog = pygame.image.load(sprite_item[0])
        self.texture_vida = self.find_sprite()
    
    def find_sprite(self):
        Surf = pygame.Surface(vida[1])
        Surf.blit(self.sprite_cog, (0,0), (vida[0][0], vida[0][1], vida[1][0], vida[1][1]))
        Surf.set_colorkey((0,0,0))
        return Surf

class Bloco_cogumelo():
    def __init__(self, pos=[0,0]):
        #charge sprite sheet
        self.sprite_sheet = pygame.image.load(sprite_item[0])

        #textura
        self.texture_ant = self.Take_sprite(ant_premium)
        self.textura_aft = self.Take_sprite(dep_premium)

        #estado
        self.state = 0

        #check estado
        self.if_touch = False

        self.rect_block = pygame.Rect(pos[0], pos[1], tamanho_item[0], tamanho_item[1])  
    
    def Take_sprite(self, ant_or_dep):
        Surf = pygame.Surface(tamanho_item)
        Surf.blit(self.sprite_sheet, (0,0), (ant_or_dep[0][0],ant_or_dep[0][1],ant_or_dep[1][0],ant_or_dep[0][0]))
        Surf.set_colorkey((0,0,0))
        Surf = pygame.transform.scale(Surf, tamanho_blocos_chao)
        return Surf

    def Get_frame(self):
        if(self.state == 0):
            return self.texture_ant
        else:
            return self.textura_aft

class Map():
    def __init__(self, path_mapa, tam_camera):
        try:
            self.path = str(path_mapa)
        except:
            print("entrada de valores invalidos")

        #tipos de blocos no mapa
        self.pedra = limao
        self.chao_bloco = preto
        self.pedras_lisas = azul
        self.nuvem_g = ciano
        self.grama_g = red
        self.cogumelo = cinza
        self.castelo = cinza_cast

        #carregar texturas
        self.sprites = pygame.image.load(sprite_map[0])

        #carregando as pedras
        self.chao_bloco_surf = self.Take_sprite(bloco_chao[0], bloco_chao[1], tamanho_blocos_chao)
        self.pedras_lisas_surf = self.Take_sprite(bloco_liso[0], bloco_liso[1], tamanho_blocos_chao)
        self.pedra_norm = self.Take_sprite(bloco_pedra[0], bloco_pedra[1], tamanho_blocos_chao)

        #carregando outras coisas
        self.nuvem_grande = self.Take_sprite(nuvem_grande[0], nuvem_grande[1], tamanho_nuvem_grande)
        self.grama_grande = self.Take_sprite(grama_grande[0], grama_grande[1], tamanho_grama_grande)
        self.Cheange_colorKey(self.grama_grande, (0,0,0))
        self.Cheange_colorKey(self.nuvem_grande, (0,0,0))

        self.castelo_teste = self.Take_sprite(castelo_pequeno[0], castelo_pequeno[1], tamanho_castelo_pequeno)

        self.tile_rect = []

        #carregando o mapa e a camera do jogador
        self.image_map = pygame.image.load(self.path)
        self.map = []
        self.Construir_mapa()
        self.map_surf = self.Create_map_surf()
        self.map_current_pos_map = [0,680]
        self.map_current_tam = tam_camera

    def Cheange_colorKey(self, surf, color):
            surf.set_colorkey(color)

    def Take_sprite(self, pos, tam, scale):
        Surf = pygame.Surface(tam)
        Surf.blit(self.sprites, (0,0), (pos[0],pos[1],tam[0],tam[1]))
        Surf = pygame.transform.scale(Surf, scale)
        return Surf

    #constroi apenas grass
    def Construir_mapa(self):
        qtd_pixel = self.image_map.get_rect().size
        matriz = []; lista = []
        Surf = pygame.Surface((qtd_pixel))
        Surf.blit(self.image_map, (0,0))
        for i in range(qtd_pixel[1]):
            for j in range(qtd_pixel[0]):
                try_color = Surf.get_at((j,i))
                if(self.pedra == try_color):
                    lista.append(pedra)
                elif(self.chao_bloco == try_color):
                    lista.append(chao_bloco)
                elif(self.pedras_lisas == try_color):
                    lista.append(pedras_lisas)
                elif(self.nuvem_g == try_color):
                    lista.append(nuvem_g)
                elif(self.grama_g == try_color):
                    lista.append(grama_g)
                elif(self.cogumelo == try_color):
                    lista.append(cogumelo)
                elif(self.castelo == try_color):
                    lista.append(castelo)
                else:
                    lista.append(0)
            matriz.append(lista)
            lista = []

        self.map = matriz

    def Create_map_surf(self):
        tupla_pos = self.image_map.get_rect().size
        list_tam_transformed = [tupla_pos[0] * escala[0], tupla_pos[1] * escala[1]]
        Surf = pygame.Surface((list_tam_transformed[0], list_tam_transformed[1]))
        Surf.fill((34, 216, 215))

        y = 0
        for pos_y in range(tupla_pos[1]):
            x = 0 
            for pos_x in range(tupla_pos[0]):
                if(self.map[pos_y][pos_x] == pedra):
                    Surf.blit(self.pedra_norm, (x * escala[0], y * escala[1]))
                    self.tile_rect.append(pygame.Rect(x * escala[0], y * escala[1], tamanho_blocos_chao[0], tamanho_blocos_chao[1]))

                if(self.map[pos_y][pos_x] == chao_bloco):
                    Surf.blit(self.chao_bloco_surf, (x * escala[0], y * escala[1]))
                    self.tile_rect.append(pygame.Rect(x * escala[0], y * escala[1], tamanho_blocos_chao[0], tamanho_blocos_chao[1]))

                if(self.map[pos_y][pos_x] == pedras_lisas):
                    Surf.blit(self.pedras_lisas_surf, (x * escala[0], y * escala[1]))
                    self.tile_rect.append(pygame.Rect(x * escala[0], y * escala[1], tamanho_blocos_chao[0], tamanho_blocos_chao[1]))

                if(self.map[pos_y][pos_x] == nuvem_g):
                    Surf.blit(self.nuvem_grande, (x * escala[0], y * escala[1]))

                if(self.map[pos_y][pos_x] == grama_g):
                    Surf.blit(self.grama_grande, (x * escala[0], y * escala[1]))

                if(self.map[pos_y][pos_x] == castelo):
                    Surf.blit(self.castelo_teste, (x * escala[0], y * escala[1]))
                x+=1
            y+=1

        return Surf

#pedra = 1 chao_bloco = 2 pedras_lisas = 3 nuvem_g = 4 grama_g = 5 cogumelo = 6 castelo = 7
    def Render_current_camera(self):

        Surf = pygame.Surface((self.map_current_tam[0], self.map_current_tam[1]))
        Surf.fill((146,244,255))

        Surf.blit(self.map_surf, (0,0), (self.map_current_pos_map[0], self.map_current_pos_map[1],
        self.map_current_tam[0], self.map_current_tam[1]))

        return Surf