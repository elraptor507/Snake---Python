#CONFIGURACION ESTANDAR
import pygame
from random import randint
import numpy as np
pygame.init()
ANCHO = 1380
ALTO = 780
pantalla = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("SNAKE/CLASS")
reloj = pygame.time.Clock()
pygame.mixer.init()

class Mapa:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.celdas_x = ANCHO//self.tamaño
        self.celdas_y = ALTO//self.tamaño
        self.casillas = [[0 for i in range(self.celdas_y)] for j in range(self.celdas_x)]
        self.jugador = Entidad(self.celdas_x//2, self.celdas_y//2, 1, 0 , 5)
        self.comida = []
        self.NPCs = []

    def añadir_comida(self):
        x = randint(0, self.celdas_x - 1)
        y = randint(0, self.celdas_y - 1)
        if self.casillas[x][y] == 0 and len(self.comida) < (self.jugador.longitud**0.4)//1:
            self.comida.append(Comida(x,y, randint(1,3)))

    def añadir_NPC(self):
        x = randint(0, self.celdas_x - 1)
        y = randint(0, self.celdas_y - 1)
        if self.casillas[x][y] == 0 and len(self.NPCs) < (self.jugador.longitud**0.6)//1 - 2:
            vx, vy = [(0,1),(0,-1),(1, 0), (-1, 0)][randint(0,3)]
            self.NPCs.append(Entidad(x,y,vx,vy,3))

    def colision(self):
        for NPC in self.NPCs:
            if self.casillas[NPC.x][NPC.y] > 0:
                self.comida.append(Comida((NPC.x - NPC.vx) % self.celdas_x, (NPC.y - NPC.vy) % self.celdas_y , NPC.longitud//2))
                self.NPCs.remove(NPC)
        if self.casillas[self.jugador.x][self.jugador.y] > 0:
            self.__init__(self.tamaño)

    def control(self, teclado):
        self.jugador.controlar(teclado)
        for NPC in self.NPCs:
            if randint(0,39) == 0:
                if randint(0,1) == 0:
                    NPC.vx, NPC.vy = NPC.vy, -1*NPC.vx #Girar a la izquierda
                else:
                    NPC.vx, NPC.vy = -1*NPC.vy, NPC.vx #Girar a la derecha
            
            for elemento in self.comida:
                if NPC.y == elemento.y and NPC.vx == 0:
                    if (NPC.x - elemento.x) % self.celdas_x < self.celdas_x//2:
                        NPC.vx = -1
                    else:
                        NPC.vx = 1
                    NPC.vy = 0
                elif NPC.x == elemento.x and NPC.vy == 0:
                    if (NPC.y - elemento.y)% self.celdas_y < self.celdas_y//2:
                        NPC.vy = -1
                    else:
                        NPC.vy = 1
                    NPC.vx = 0
            
            if self.casillas[(NPC.x + NPC.vx) % self.celdas_x][(NPC.y + NPC.vy) % self.celdas_y] > 0:
                if randint(0,1) == 0:
                    NPC.vx, NPC.vy = NPC.vy, -1*NPC.vx
                else:
                    NPC.vx, NPC.vy = -1*NPC.vy, NPC.vx
                if self.casillas[(NPC.x + NPC.vx) % self.celdas_x][(NPC.y + NPC.vy) % self.celdas_y] > 0:
                    NPC.vx, NPC.vy = -1*NPC.vx, -1*NPC.vy

    def reglas(self):
        for entidad in [self.jugador]+self.NPCs: #MOVIMIENTO DE LAS ENTIDADES
            entidad.mover()
            entidad.modular(self.celdas_x, self.celdas_y)

        self.añadir_comida() #AÑADIR COMIDA
        [entidad.comer(self.comida) for entidad in [self.jugador]+self.NPCs] #COMER COMIDA
        self.añadir_NPC() #AÑADIR NPC
        self.colision() #COLISIONES

         
        for x in range(self.celdas_x): #RESTAR MAPA
            for y in range(self.celdas_y):
                if self.casillas[x][y] > 0:
                    self.casillas[x][y] -= 1

        for entidad in [self.jugador] + self.NPCs: #SUMAR MAPA
            self.casillas[entidad.x][entidad.y] = entidad.longitud

    def mostrar(self):
        pantalla.fill((255,255,255)) #color de fondo

        for x in range(self.celdas_x):
            for y in range(self.celdas_y):
                if self.casillas[x][y] > 0:
                    pygame.draw.rect(pantalla, (0,0,0), (x*self.tamaño, y*self.tamaño, self.tamaño, self.tamaño)) #Cuerpo de jugador y NPCs

        pygame.draw.rect(pantalla, (0,0,255), (self.jugador.x*self.tamaño, self.jugador.y*self.tamaño, self.tamaño, self.tamaño)) #Jugador

        for NPC in self.NPCs:
            pygame.draw.rect(pantalla, (0,255,0), (NPC.x*self.tamaño, NPC.y*self.tamaño, self.tamaño, self.tamaño)) #NPCs

        for elemento in self.comida:
            pygame.draw.rect(pantalla, (255,0,0), (elemento.x*self.tamaño, elemento.y*self.tamaño, self.tamaño, self.tamaño)) #Comida

class Comida:
    def __init__(self, x, y, cantidad):
        self.x = x
        self.y = y
        self.cantidad = cantidad

class Entidad:
    def __init__(self, x, y, vx, vy, longitud):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.longitud = longitud

    def mover(self):
        self.x += self.vx
        self.y += self.vy

    def modular(self, x, y):
        self.x %= x
        self.y %= y

    def controlar(self, teclado):
        if teclado[pygame.K_w] and self.vy == 0:
            self.vx = 0
            self.vy = -1
        elif teclado[pygame.K_s] and self.vy == 0:
            self.vx = 0
            self.vy = 1
        elif teclado[pygame.K_a] and self.vx == 0:
            self.vx = -1
            self.vy = 0
        elif teclado[pygame.K_d] and self.vx == 0:
            self.vx = 1
            self.vy = 0

    def comer(self, comida):
        for elemento in comida:
            if self.x == elemento.x and self.y == elemento.y:
                self.longitud += elemento.cantidad
                comida.remove(elemento)

mapa = Mapa(15)
#Bucle Principal
while True:
    #Botón de cerrar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    #Control
    mapa.control(pygame.key.get_pressed())

    #Reglas
    mapa.reglas()

    #Sección Gráfica
    mapa.mostrar()

    pygame.display.flip()
    reloj.tick(8)