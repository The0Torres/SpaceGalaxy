import pygame
from misiles import *
from colores import*

def getSuperficies(path,filas, columnas):
    lista=[]
    superficie_imagen = pygame.image.load(path)
    fotograma_ancho = int(superficie_imagen.get_width()/columnas)
    fotograma_alto = int(superficie_imagen.get_height()/filas)

    for fila in range(filas):
        for columna in range(columnas):
            x = columna * fotograma_ancho
            y = fila * fotograma_alto
            #un pedacito de la imagen del sprite
            superficie_fotograma = superficie_imagen.subsurface(x,y,fotograma_ancho, fotograma_alto)
            lista.append(superficie_fotograma)

    return lista

class Personaje:
    def __init__(self) -> None:
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
            print("¡El personaje ha explotado!")