import pygame
import colores
import enemigos
from personaje import Personaje
from pantalla_puntuacion import usuario_puntuacion
import random
import sys



def juego(ancho_pantalla, largo_pantalla):
    pygame.init()

    pygame.mixer.init()
    audio_disparo = pygame.mixer.Sound(r"Python utn\jueguitos.py\sonidos\x wing tiro.mp3")
    tie_disparo = pygame.mixer.Sound(r"Python utn\jueguitos.py\sonidos\tie tiro.mp3")
    tie_disparo.set_volume(0.2)

    score = 0
    nivel = 1
    nivel_completado = False
    tiempo_nivel_completado = 0

    pantalla = pygame.display.set_mode((ancho_pantalla, largo_pantalla))
    pygame.display.set_caption("Space galaxy")
    reloj = pygame.time.Clock()

    imagen_espacio = pygame.image.load("Python utn\jueguitos.py\imagenes\spacefondo.png")
    imagen_espacio = pygame.transform.scale(imagen_espacio, (ancho_pantalla, largo_pantalla))

    ties = enemigos.crear_enemigos(8)

    xwing = Personaje()

    flag_correr = True
    while flag_correr:
        lista_evento = pygame.event.get()
        for evento in lista_evento:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
                    audio_disparo.play()

            if xwing.rect.left < 0:
                xwing.rect.left = 0
            elif xwing.rect.right > ancho_pantalla:
                xwing.rect.right = ancho_pantalla

            if xwing.rect.top < 0:
                xwing.rect.top = 0
            elif xwing.rect.bottom > largo_pantalla:
                xwing.rect.bottom = largo_pantalla

        reloj.tick(144)
        pantalla.blit(imagen_espacio, imagen_espacio.get_rect())

        if xwing.vivo:
            xwing.dibujar(pantalla)

        for misil in xwing.misiles:
            misil.actualizar()
            misil.dibujar(pantalla)
            
            for personaje in ties:
                if misil.rect.colliderect(personaje.rect):
                    score += 25
                    ties.remove(personaje)
                    xwing.misiles.remove(misil)
                    
                    break

        font = pygame.font.SysFont("cambria", 20)
        texto_score = font.render("SCORE: {0}".format(score), True, colores.YELLOW1)
        pantalla.blit(texto_score, (10, 10))

        for enemigo in ties:
            enemigo.actualizar_posicion(pantalla)
            enemigo.actualizar_pantalla(pantalla, xwing.rect)
            if random.random() < 0.020:
                enemigo.disparar()
                tie_disparo.play()
            for misil in enemigo.misiles:
                misil.actualizar()
                misil.dibujar(pantalla)
                if misil.rect.colliderect(xwing.rect):
                    xwing.daño()
                    enemigo.misiles.remove(misil)
                    break
    
        if not xwing.vivo:
            xwing.explotar(pantalla)
            usuario_puntuacion(pantalla,score)

        if len(ties) == 0:
            if not nivel_completado:
                nivel_completado = True
                tiempo_nivel_completado = pygame.time.get_ticks() + 1000
                
            else:
                if pygame.time.get_ticks() >= tiempo_nivel_completado:
                    nivel += 1
                    nivel_completado = False
                    ties = enemigos.crear_enemigos(8)

                    font_nivel = pygame.font.SysFont("cambria", 50)
                    texto_nivel = font_nivel.render("Nivel {0}".format(nivel), True, colores.YELLOW1)
                    texto_nivel_rect = texto_nivel.get_rect(center=(ancho_pantalla // 2, largo_pantalla // 2))
                    pantalla.blit(texto_nivel, texto_nivel_rect)
                    xwing.misiles = []

                    pygame.display.flip()
                    pygame.time.wait(2000)

        pygame.display.flip()

    pygame.quit()
