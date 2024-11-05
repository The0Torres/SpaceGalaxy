import pygame
import random
from misiles import *


class Enemigo:
    def __init__(self, x, y, ancho, alto, width=100, height=100):
        self.imagen = pygame.image.load(r"imagenes\cazaTie.png")
        self.imagen = pygame.transform.scale(self.imagen, (ancho, alto))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
        self.velocidad_x = random.choice([4, 5])
        self.velocidad_y = random.choice([4, 5])
        self.visible = True
        self.misiles = []
        self.vivo = True
        self.corazones = 1

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def disparar(self):
        x = self.rect.centerx
        y = self.rect.y
        imagen_misil = pygame.image.load(r"imagenes\shotgreen.png")
        misil1 = Misil(x + 38, y + 75, imagen_misil, "abajo")
        misil2 = Misil(x - 30, y + 75, imagen_misil, "abajo")
        self.misiles.append(misil1)
        self.misiles.append(misil2)
    
    def daño(self):
        self.corazones -= 1
        if self.corazones < 1:
            self.vivo = False

    def actualizar_pantalla(self, pantalla, rect):
        if self.vivo== True:
            pantalla.blit(self.imagen, self.rect)

    def actualizar_posicion(self, pantalla):
        if self.visible == True:
            #Movimiento del enemigo
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            #Evita que se vaya fuera de pantalla
            if self.rect.left < 0 or self.rect.right > pantalla.get_width():
                self.velocidad_x *= -1
                self.rect.x += self.velocidad_x
            if self.rect.top < 0:
                self.rect.top = 0
                self.velocidad_y *= -1
            if self.rect.bottom > pantalla.get_height() / 1.5:
                self.rect.bottom = pantalla.get_height() / 1.5
                self.velocidad_y *= -1

class Bomber(Enemigo):
    def __init__(self, x, y, ancho, alto, width=100, height=100):
        super().__init__(x, y, ancho, alto, width, height)
        self.imagen = pygame.image.load(r"imagenes\tie bomber.png")
        self.imagen = pygame.transform.scale(self.imagen, (ancho, alto))
        #Enemigo con mas vida pero mas lento
        self.velocidad_x = random.choice([2, 3])
        self.velocidad_y = random.choice([2, 3])
        self.corazones = 4

    def disparar(self):
        x = self.rect.centerx
        y = self.rect.y
        imagen_misil = pygame.image.load(r"imagenes\shotgreen.png")
        #Solo tiene un misil
        misil = Misil(x + 5, y + 75, imagen_misil, "abajo")
        self.misiles.append(misil)

class Defender(Enemigo):
    def __init__(self, x, y, ancho, alto, width=100, height=100):
        super().__init__(x, y, ancho, alto, width, height)
        self.imagen = pygame.image.load(r"imagenes\tie defender.png")
        self.imagen = pygame.transform.scale(self.imagen, (ancho, alto))
        #Enemigo mas rapido y con mas vida
        self.velocidad_x = random.choice([6, 7])
        self.velocidad_y = random.choice([6, 7])
        self.corazones = 3

    def disparar(self):
        x = self.rect.centerx
        y = self.rect.y
        imagen_misil = pygame.image.load(r"imagenes\shotgreen.png")
        #Tiene 3 misiles
        misil1 = Misil(x + 20, y + 75, imagen_misil, "abajo")
        misil2 = Misil(x - 20, y + 75, imagen_misil, "abajo")
        misil3 = Misil(x, y + 65, imagen_misil, "abajo")
        self.misiles.append(misil1)
        self.misiles.append(misil2)
        self.misiles.append(misil3)

def crear_enemigos (cantidad,modelo):
    lista_personajes = []
    for i in range(cantidad):
        #Segun el modelo que se pase se crea un enemeigo u otro
        if modelo == "defender":
            lista_personajes.append(Defender( 0+(i* random.choice([25, 100])), 0+(i* random.choice([25, 100])), 80, 80, 75 , 50))
        elif modelo == "bomber":
            lista_personajes.append(Bomber( 0+(i* random.choice([25, 100])), 0+(i* random.choice([25, 100])), 80, 80, 75 , 50))
        elif modelo == "tie":
            lista_personajes.append(Enemigo( 0+(i* random.choice([25, 100])), 0+(i* random.choice([25, 100])), 80, 80, 75 , 50))
    return lista_personajes