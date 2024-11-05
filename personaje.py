import pygame
from misiles import *
from colores import*

import pygame

def getSuperficies(path, filas, columnas,tamano=None):
    #Toma cuantas imagenes hay en un sprite
    lista = []
    superficie_imagen = pygame.image.load(path)
    if tamano == "chico":
        superficie_imagen = pygame.transform.scale(superficie_imagen,(200,50))
    fotograma_ancho = int(superficie_imagen.get_width() / columnas)
    fotograma_alto = int(superficie_imagen.get_height() / filas)

    for fila in range(filas):
        for columna in range(columnas):
            x = columna * fotograma_ancho
            y = fila * fotograma_alto
            superficie_fotograma = superficie_imagen.subsurface(x, y, fotograma_ancho, fotograma_alto)
            lista.append(superficie_fotograma)

    return lista

class Personaje:
    def __init__(self):
        self.score = 0
        self.imagen = pygame.image.load(r"imagenes\xwing.png")
        self.rect = self.imagen.get_rect()
        self.rect.y = 900
        self.rect.x = 560
        self.rect.width = 85
        self.rect.height = 60
        self.misiles = []
        self.vivo = True
        self.corazones = 5
        self.explosion_frames = getSuperficies(r"imagenes\pngwing.com.png", 6, 8)
        self.explosion_indice = 0
        self.frames_daño = getSuperficies(r"imagenes\spritesheet.png", 1, 6, tamano="chico")
        self.indice_daño = 0

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
        frame_daño = self.frames_daño[self.indice_daño]
        pantalla.blit(frame_daño, (1200,10))

    def disparar(self):
        x = self.rect.centerx
        y = self.rect.y
        imagen_misil = pygame.image.load(r"imagenes\shot.png")
        #Posicion de los misiles
        misil1 = Misil(x + 38, y, imagen_misil, "arriba")
        misil2 = Misil(x - 38, y, imagen_misil, "arriba")
        #Los agrega a la listas
        self.misiles.append(misil1)
        self.misiles.append(misil2)

    def daño(self):
        self.corazones -= 1
        if self.corazones < 1:
            self.vivo = False
        else:
            #Se mueve un frame del sprite cuando le haccen daño
            self.indice_daño = (self.indice_daño + 1) % len(self.frames_daño)

    def explotar(self, pantalla):
        if self.explosion_indice < len(self.explosion_frames):
            explosion_frame = self.explosion_frames[self.explosion_indice]
            #Toma la posicon del personaje
            explosion_rect = explosion_frame.get_rect(center=self.rect.center)
            pantalla.blit(explosion_frame, explosion_rect)
            #Avanza un frame hasta que termine el sprite
            self.explosion_indice += 1
        
