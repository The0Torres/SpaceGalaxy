"""
Pygame :: GALAXIA
Especificaciones mínimas:
1 La nave propia solo podrá moverse de izquierda a derecha o viceversa,
nunca hacia adelante o hacia atrás.
2 Las naves deben efectuar disparos, tanto la propia como las enemigas.
3 Utilizar movimientos aleatorios para las naves enemigas.
4 Al final de cada partida se deberá guardar el SCORE junto con el nombre
de usuario. En tal sentido, se deberá elaborar un ranking ordenado de
mayor a menor puntuación, mostrando su respectivo nombre y puntuación.
5 Incluir:
o Archivos.
o POO.
o Texto para ir mostrando el SCORE.
o Eventos.A
o Colisiones.
o Manejo de rectángulo.
o Temporizador.
o Imágenes.
o Audios.
o Ranking de puntuaciones
"""
import pygame
import colores
import enemigos
from personaje import Personaje
import random

ancho_pantalla = 1250
largo_pantalla = 1000

score = 0

pygame.init()

pantalla = pygame.display.set_mode((ancho_pantalla,largo_pantalla))
pygame.display.set_caption("Space galaxy")
reloj = pygame.time.Clock()

imagen_espacio = pygame.image.load("Python utn\jueguitos.py\imagenes\spacefondo.png")
imagen_espacio = pygame.transform.scale(imagen_espacio,(ancho_pantalla, largo_pantalla))

ties = enemigos.crear_enemigos(10)

#Creacion de mi personaje (constructor)
xwing = Personaje()

flag_correr = True
while flag_correr:
    lista_evento = pygame.event.get()
    for evento in lista_evento:
        if evento.type == pygame.QUIT:
            flag_correr = False

        if not xwing.vivo:
            xwing.misiles = []
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            xwing.rect.x += 20
        if keys[pygame.K_a]:
            xwing.rect.x -= 20

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == pygame.BUTTON_LEFT:
                xwing.disparar()

        if xwing.rect.left < 0:
            xwing.rect.left = 0
        elif xwing.rect.right > ancho_pantalla:
            xwing.rect.right = ancho_pantalla

        if xwing.rect.top < 0:
            xwing.rect.top = 0
        elif xwing.rect.bottom > largo_pantalla:
            xwing.rect.bottom = largo_pantalla

    reloj.tick(144)
    pantalla.blit(imagen_espacio,imagen_espacio.get_rect())

    for misil in xwing.misiles:
        misil.actualizar()
        misil.dibujar(pantalla)
        for personaje in ties:
            if misil.rect.colliderect(personaje.rect):
                score += 25
                ties.remove(personaje)
                xwing.misiles.remove(misil)
                break

    font = pygame.font.SysFont("Arial", 20)
    texto = font.render("SCORE: {0}".format(score),True, colores.YELLOW1)
    pantalla.blit(texto,(10,10))

    #dibujar mi personaje
    if xwing.vivo == True:
        xwing.dibujar(pantalla)

    for enemigo in ties:
        enemigo.actualizar_posicion(pantalla)
        enemigo.actualizar_pantalla(pantalla, xwing.rect)
        if random.random() < 0.025:  # Ajusta el valor 0.1 según la probabilidad deseada
            enemigo.disparar()
        for misil in enemigo.misiles:
            misil.actualizar()
            misil.dibujar(pantalla)
            if misil.rect.colliderect(xwing.rect):
                xwing.daño()
                enemigo.misiles.remove(misil)
                break

    if not xwing.vivo:
        pantalla.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 80)
        texto = font.render("Perdiste Burro", True, colores.YELLOW1)
        texto_rect = texto.get_rect(center=(ancho_pantalla / 2, largo_pantalla / 2))
        pantalla.blit(texto, texto_rect)
        
    pygame.display.flip()

pygame.quit