#configuración inicial
import pygame
from random import randint
pygame.init()
ANCHO = 1380
ALTO = 780
pantalla = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("SNAKE")

#Reloj
reloj = pygame.time.Clock()

#Sonido
pygame.mixer.init()
try:
    sonido_chocar = pygame.mixer.Sound("Desktop/python/youtube/snake/chocar.wav")
    sonido_comer = pygame.mixer.Sound("Desktop/python/youtube/snake/comer.wav")
    sonido_fin = pygame.mixer.Sound("Desktop/python/youtube/snake/fin.wav")
except:
    sonido_chocar = pygame.mixer.Sound("chocar.wav")
    sonido_comer = pygame.mixer.Sound("comer.wav")
    sonido_fin = pygame.mixer.Sound("fin.wav")

#Funciones
def añadir_comida(jugador, mapa, comida):
    x = randint(0, celdas_x - 1)
    y = randint(0, celdas_y - 1)
    if mapa[x][y] == 0 and len(comida) < (jugador["longitud"]**0.4)//1:
        comida.append({"x":x, "y": y})

def comer_comida(entidades, comida):
    for entidad in entidades:
        for elemento in comida:
            if entidad["x"] == elemento["x"] and entidad["y"] == elemento["y"]:
                entidad["longitud"] += 1
                comida.remove(elemento)
                sonido_comer.play()

def añadir_NPC(jugador, mapa, NPCs):
    x = randint(0, celdas_x - 1)
    y = randint(0, celdas_y - 1)
    if mapa[x][y] == 0 and len(NPCs) < (jugador["longitud"]**0.6)//1 - 2:
        vx, vy = [(0,1),(0,-1),(1, 0), (-1, 0)][randint(0,3)]
        NPCs.append({"x": x, "y": y, "vx": vx, "vy": vy, "longitud": 3})

def control_NPC(NPCs, mapa, comida):
    for NPC in NPCs:
        if randint(0,39) == 0:
            if randint(0,1) == 0:
                NPC["vx"] , NPC["vy"] = NPC["vy"], -1*NPC["vx"] #Girar a la izquierda
            else:
                NPC["vx"], NPC["vy"] = -1*NPC["vy"], NPC["vx"] #Girar a la derecha
        
        for elemento in comida:
            if NPC["y"] == elemento["y"] and NPC["vx"] == 0:
                if (NPC["x"] - elemento["x"]) % celdas_x < celdas_x//2:
                    NPC["vx"] = -1
                else:
                    NPC["vx"] = 1
                NPC["vy"] = 0
            elif NPC["x"] == elemento["x"] and NPC["vy"] == 0:
                if (NPC["y"] - elemento["y"])% celdas_y < celdas_y//2:
                    NPC["vy"] = -1
                else:
                    NPC["vy"] = 1
                NPC["vx"] = 0
        
        if mapa[(NPC["x"]+NPC["vx"])%celdas_x][(NPC["y"]+NPC["vy"])%celdas_y] > 0:
            if randint(0,1) == 0:
                NPC["vx"], NPC["vy"] = NPC["vy"], -1*NPC["vx"]
            else:
                NPC["vx"], NPC["vy"] = -1*NPC["vy"], NPC["vx"]
            if mapa[(NPC["x"]+NPC["vx"])%celdas_x][(NPC["y"]+NPC["vy"])%celdas_y] > 0:
                NPC["vx"], NPC["vy"] = -1*NPC["vx"], -1*NPC["vy"]

def colisiones(NPCs, mapa, comida):
    for NPC in NPCs:
        if mapa[NPC["x"]][NPC["y"]] > 0:
            comida.append({"x": (NPC["x"] - NPC["vx"])%celdas_x,  "y": (NPC["y"]- NPC["vy"])%celdas_y})
            NPCs.remove(NPC)
            sonido_chocar.play()

#Variables
tamaño = 15
celdas_x = ANCHO//tamaño
celdas_y = ALTO//tamaño
mapa = [[0 for i in range(celdas_y)] for j in range(celdas_x)]
jugador = {"x": celdas_x//2, "y": celdas_y//2, "vx": 1, "vy": 0 , "longitud": 5}
comida = []
NPCs = []

#Bucle Principal
while True:
    #Botón de cerrar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    #Entrada del teclado
    teclado = pygame.key.get_pressed()

    if teclado[pygame.K_w] and jugador["vy"] == 0:
        jugador["vx"] = 0
        jugador["vy"] = -1
    elif teclado[pygame.K_s] and jugador["vy"] == 0:
        jugador["vx"] = 0
        jugador["vy"] = 1
    elif teclado[pygame.K_a] and jugador["vx"] == 0:
        jugador["vx"] = -1
        jugador["vy"] = 0
    elif teclado[pygame.K_d] and jugador["vx"] == 0:
        jugador["vx"] = 1
        jugador["vy"] = 0

    control_NPC(NPCs, mapa, comida)

    #Reglas del juego
    for entidad in [jugador] + NPCs:
        entidad["x"] += entidad["vx"]
        entidad["y"] += entidad["vy"]
        entidad["x"] %= celdas_x
        entidad["y"] %= celdas_y

    añadir_comida(jugador, mapa, comida)
    comer_comida([jugador] + NPCs, comida)
    añadir_NPC(jugador, mapa, NPCs)
    colisiones(NPCs, mapa, comida)

    if mapa[jugador["x"]][jugador["y"]] > 0:
        sonido_fin.play()
        fin_x = celdas_x // 8 - 5
        fin_y = celdas_y // 8 - 2
        for x in range(celdas_x//4):
            for y in range(celdas_y//4):
                #Boton de cerrar
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                
                if (x,y) not in [(0 + fin_x , 0 + fin_y),(0 + fin_x , 1 + fin_y),(0 + fin_x , 2 + fin_y),
                                 (0 + fin_x , 3 + fin_y),(0 + fin_x , 4 + fin_y),(1 + fin_x , 0 + fin_y),
                                 (2 + fin_x , 0 + fin_y),(1 + fin_x , 2 + fin_y),(2 + fin_x , 2 + fin_y),
                                 (4 + fin_x , 0 + fin_y),(4 + fin_x , 2 + fin_y),(4 + fin_x , 3 + fin_y),
                                 (4 + fin_x , 4 + fin_y),(6 + fin_x , 0 + fin_y),(6 + fin_x , 1 + fin_y),
                                 (6 + fin_x , 2 + fin_y),(6 + fin_x , 3 + fin_y),(6 + fin_x , 4 + fin_y),
                                 (7 + fin_x , 1 + fin_y),(8 + fin_x , 2 + fin_y),(9 + fin_x , 3 + fin_y),
                                 (9 + fin_x , 0 + fin_y),(9 + fin_x , 1 + fin_y),(9 + fin_x , 2 + fin_y),
                                 (9 + fin_x , 4 + fin_y)]:

                    pygame.draw.rect(pantalla, (0,0,0), (x*tamaño*4, y*tamaño*4, tamaño*4, tamaño*4))
                    reloj.tick(200)
                    pygame.display.flip()

        mapa = [[0 for i in range(celdas_y)] for j in range(celdas_x)]
        jugador = {"x": celdas_x//2, "y": celdas_y//2, "vx": 1, "vy": 0, "longitud": 5}
        comida = []
        NPCs = []
        reloj.tick(1)

    for x in range(celdas_x):
        for y in range(celdas_y):
            if mapa[x][y] > 0:
                mapa[x][y] -= 1

    for entidad in [jugador] + NPCs:
        mapa[entidad["x"]][entidad["y"]] = entidad["longitud"]

    #Sección Gráfica
    pantalla.fill((255,255,255)) #color de fondo

    for x in range(celdas_x):
        for y in range(celdas_y):
            if mapa[x][y] > 0:
                pygame.draw.rect(pantalla, (0,0,0), (x*tamaño, y*tamaño, tamaño, tamaño))
    
    pygame.draw.rect(pantalla, (0,0,255), (jugador["x"]*tamaño, jugador["y"]*tamaño, tamaño, tamaño))

    for NPC in NPCs:
        pygame.draw.rect(pantalla, (0,255,0), (NPC["x"]*tamaño, NPC["y"]*tamaño, tamaño, tamaño))

    for elemento in comida:
        pygame.draw.rect(pantalla, (255,0,0), (elemento["x"]*tamaño, elemento["y"]*tamaño, tamaño, tamaño))

    pygame.display.flip()
    reloj.tick(5+ (jugador["longitud"]**0.5)//1)