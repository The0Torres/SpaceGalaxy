import pygame
from misiles import *
from colores import*

import pygame

def getSuperficies(path, filas, columnas):
    lista = []
    superficie_imagen = pygame.image.load(path)
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
        self.imagen = pygame.image.load(r"Python utn\jueguitos.py\imagenes\xwing.png")
        self.rect = self.imagen.get_rect()
        self.rect.y = 900
        self.rect.x = 560
        self.rect.width = 85
        self.rect.height = 60
        self.misiles = []
        self.vivo = True
        self.corazones = 5
        self.explosion_frames = getSuperficies(r"Python utn\jueguitos.py\imagenes\pngwing.com.png", 6, 8)
        self.explosion_index = 0

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def disparar(self):
        x = self.rect.centerx
        y = self.rect.y
        imagen_misil = pygame.image.load(r"Python utn\jueguitos.py\imagenes\shot.png")
        misil1 = MisilArriba(x + 38, y, imagen_misil)
        misil2 = MisilArriba(x - 38, y, imagen_misil)
        self.misiles.append(misil1)
        self.misiles.append(misil2)

    def daño(self):
        self.corazones -= 1
        if self.corazones == 0:
            self.vivo = False

    def explotar(self, pantalla):
        if self.explosion_index < len(self.explosion_frames):
            explosion_frame = self.explosion_frames[self.explosion_index]
            explosion_rect = explosion_frame.get_rect(center=self.rect.center)
            pantalla.blit(explosion_frame, explosion_rect)
            self.explosion_index += 1
        
