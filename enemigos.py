import pygame
import random
from misiles import *


class Enemigo:
    def __init__(self, x, y, ancho, alto, width=100, height=100):
        self.imagen = pygame.image.load(r"Python utn\jueguitos.py\imagenes\cazaTie.png")
        self.imagen = pygame.transform.scale(self.imagen, (ancho, alto))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
        self.velocidad_x = random.choice([4, 6])
        self.velocidad_y = random.choice([4, 6])
        self.visible = True
        self.misiles = []

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def disparar(self):
        x = self.rect.centerx
        y = self.rect.y
        imagen_misil = pygame.image.load(r"Python utn\jueguitos.py\imagenes\shotgreen.png")
        misil1 = Misil(x + 38, y + 75, imagen_misil, "abajo")
        misil2 = Misil(x - 30, y + 75, imagen_misil, "abajo")
        self.misiles.append(misil1)
        self.misiles.append(misil2)

    def actualizar_pantalla(self, pantalla, rect):
        if self.visible == True and rect.colliderect(self.rect):
            self.visible = False

        if self.visible == True:
            pantalla.blit(self.imagen, self.rect)

    def actualizar_posicion(self, pantalla):
        if self.visible == True:
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            if self.rect.left < 0 or self.rect.right > pantalla.get_width():
                self.velocidad_x *= -1
                self.rect.x += self.velocidad_x
            if self.rect.top < 0:
                self.rect.top = 0
                self.velocidad_y *= -1
            if self.rect.bottom > pantalla.get_height() / 1.5:
                self.rect.bottom = pantalla.get_height() / 1.5
                self.velocidad_y *= -1

def crear_enemigos (cantidad):
    lista_personajes = []
    for i in range(cantidad):
        lista_personajes.append(Enemigo( 0+(i* random.choice([25, 100])), 0+(i* random.choice([25, 100])), 80, 80, 75 , 50))
    return lista_personajes