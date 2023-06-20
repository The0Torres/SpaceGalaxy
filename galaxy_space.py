import pygame
import sys
import os
import colores
from boton_click import Boton
import sqlite3
import enemigos
from personaje import *
import random

pygame.init()

reloj = pygame.time.Clock()

ancho_pantalla = 1250
largo_pantalla = 1000

os.environ['SDL_VIDEO_CENTERED'] = '1'

pantalla = pygame.display.set_mode((ancho_pantalla,largo_pantalla))
pygame.display.set_caption("Menu") 

fondo_menu = pygame.image.load("Python utn\jueguitos.py\imagenes\spacefondo.png")
fondo_menu = pygame.transform.scale(fondo_menu,(ancho_pantalla, largo_pantalla))

boton = pygame.image.load(r"Python utn\jueguitos.py\imagenes\boton transparente.png")
boton = pygame.transform.scale(boton, (360, 80))

def usuario_puntuacion(score):
    font = pygame.font.SysFont("Cambria", 40)
    texto_ingresado = ""
    nombre_ingresado = False
    rect_texto = pygame.Rect(275,425,140,65)
    en_poscion = False

    with sqlite3.connect("usuarios.db") as conexion:
                        try:
                            sentencia = '''CREATE TABLE IF NOT EXISTS usuarios
                                (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre TEXT,
                                puntacion INTEGER
                                )
                                '''
                            conexion.execute(sentencia)
                        except sqlite3.OperationalError:
                            print("La tabla usuarios ya existe")

    while True:
        pantalla.fill((colores.BLACK))

        poscion_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_texto.collidepoint(evento.pos):
                    en_poscion = True
                else:
                    en_poscion = False

            if evento.type == pygame.KEYDOWN:
                if en_poscion and not nombre_ingresado:  # Solo permitir entrada de texto si no se ha ingresado un nombre
                    if evento.key == pygame.K_BACKSPACE:
                        texto_ingresado = texto_ingresado[0:-1]
                    elif evento.key == pygame.K_RETURN:  # Comprobar si se presiona la tecla Enter
                        print("Nombre ingresado:", texto_ingresado)
                        with sqlite3.connect("usuarios.db") as conexion:
                            cursor = conexion.cursor()
                            cursor.execute("INSERT INTO usuarios (nombre, puntacion) VALUES (?, ?)", (texto_ingresado, score))
                            conexion.commit()
                        nombre_ingresado = True  # Establecer la bandera en True para indicar que se ha ingresado un nombre
                    else:
                        texto_ingresado += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_salir.verificarClick(poscion_mouse):
                        pygame.quit()
                        sys.exit()
                if boton_menu.verificarClick(poscion_mouse):
                        menu_galaxy()


        if en_poscion and not nombre_ingresado:
            color_actual = colores.GRAY
        else:
            color_actual = colores.GRAY10

        pygame.draw.rect(pantalla,color_actual, rect_texto)

        superficie_texto = font.render(texto_ingresado, True, colores.YELLOW1)
        pantalla.blit(superficie_texto,rect_texto)

        rect_texto.w = max(725,superficie_texto.get_width() + 10)

        font = pygame.font.SysFont("cambria", 80)
        texto = font.render(f"Juego Finalizado", True, colores.YELLOW1)
        pantalla.blit(texto, (340, 20))

        font = pygame.font.SysFont("cambria", 40)
        texto = font.render(f"Puntuacion: {score}", True, colores.YELLOW1)
        pantalla.blit(texto, (475, 200))

        font = pygame.font.SysFont("cambria", 60)
        if nombre_ingresado:
            texto = font.render("Nombre ingresado: {0}".format(texto_ingresado), True, colores.YELLOW1)
        else:
            texto = font.render("Ingrese su nombre de usuario", True, colores.YELLOW1)
        pantalla.blit(texto, (255, 325))

        boton_salir = Boton(None, 615, 850, "Salir")
        boton_menu = Boton(None , 625, 650, "Menu")

        for botones in [boton_menu , boton_salir]:
                botones.cambiarColor(poscion_mouse)
                botones.actualizar()

        pygame.display.update()

def puntuaciones():
    pygame.display.set_caption("Puntuaciones")
    
    while True:
        pantalla.blit(fondo_menu, fondo_menu.get_rect())

        poscion_mouse = pygame.mouse.get_pos()

        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        cursor.execute("SELECT nombre, puntacion FROM usuarios ORDER BY puntacion DESC LIMIT 10")
        resultados = cursor.fetchall()

        boton_menu = Boton(boton , 600, 900, "Menu")

        boton_menu.cambiarColor(poscion_mouse)
        boton_menu.actualizar()

        font_puntuaciones = pygame.font.SysFont("cambria", 100)

        mejores_score = font_puntuaciones.render("Mejores puntuaciones", True , colores.YELLOW1)
        pantalla.blit(mejores_score, (190, 100))

        font = pygame.font.SysFont("cambria", 50)
        y = 300
        posicion_juego = 1

        for nombre, puntacion in resultados:
            texto = font.render(f"{posicion_juego}. {nombre} - {puntacion}", True, colores.YELLOW1)
            pantalla.blit(texto, (440, y))
            y += 50
            posicion_juego += 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_menu.verificarClick(poscion_mouse):
                    menu_galaxy()

        pygame.display.update()

def juego():
    pygame.mixer.init()
    audio_disparo = pygame.mixer.Sound(r"Python utn\jueguitos.py\sonidos\x wing tiro.mp3")
    audio_disparo.set_volume(0.1)
    tie_disparo = pygame.mixer.Sound(r"Python utn\jueguitos.py\sonidos\tie tiro.mp3")
    tie_disparo.set_volume(0.1)

    score = 0
    nivel = 1
    i = 0
    nivel_completado = False
    tiempo_nivel_completado = 0

    pantalla = pygame.display.set_mode((ancho_pantalla, largo_pantalla))
    pygame.display.set_caption("Space galaxy")

    imagen_espacio = pygame.image.load("Python utn\jueguitos.py\imagenes\spacefondo.png")
    imagen_espacio = pygame.transform.scale(imagen_espacio, (ancho_pantalla, largo_pantalla))

    ties = enemigos.crear_enemigos(8, "tie")

    xwing = Personaje()

    

    segundos = 1  
    segundos_que_pasan = 0
    tiempo_restante = 120

    flag_correr = True
    while flag_correr:
        lista_evento = pygame.event.get()
        for evento in lista_evento:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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


        segundos_que_pasan += reloj.tick(144) / 1000 
        if segundos_que_pasan >= segundos:
            segundos_que_pasan = 0
            tiempo_restante -= 1

        reloj.tick(144)
        pantalla.blit(imagen_espacio, imagen_espacio.get_rect())

        if xwing.vivo:
            xwing.dibujar(pantalla)
        elif not xwing.vivo:
            xwing.misiles = []
            xwing.explotar(pantalla)
            if xwing.explosion_index >= len(xwing.explosion_frames):
                usuario_puntuacion(score)

        for misil in xwing.misiles:
            misil.actualizar()
            misil.dibujar(pantalla)
            
            for personaje in ties:
                if misil.rect.colliderect(personaje.rect):
                    personaje.daño()
                    xwing.misiles.remove(misil)
                    if personaje.corazones < 1:
                        score += 50
                        ties.remove(personaje)
                    
        for enemigo in ties:
            enemigo.actualizar_posicion(pantalla)
            enemigo.actualizar_pantalla(pantalla, xwing.rect)
            if random.random() < 0.02:
                enemigo.disparar()
                tie_disparo.play()
            for misil in enemigo.misiles:
                misil.actualizar()
                misil.dibujar(pantalla)
                if misil.rect.colliderect(xwing.rect):
                    xwing.daño()
                    enemigo.misiles.remove(misil)
                    break
        
        if tiempo_restante == 0:
            xwing.vivo = False

        font = pygame.font.SysFont("cambria", 20)
        texto_score = font.render("SCORE: {0}".format(score), True, colores.YELLOW1)
        pantalla.blit(texto_score, (10, 10))

        texto_temporizador = font.render(f"Tiempo: {tiempo_restante} s", True, colores.YELLOW1)
        pantalla.blit(texto_temporizador, (10,30))

    
        if len(ties) == 0:
            if not nivel_completado:
                nivel_completado = True
                tiempo_nivel_completado = pygame.time.get_ticks() + 1000            
            else:
                if pygame.time.get_ticks() >= tiempo_nivel_completado:
                    score += tiempo_restante
                    nivel += 1
                    i += 1
                    nivel_completado = False

                    if nivel == 2:
                        ties = enemigos.crear_enemigos(8, "bomber")
                    elif nivel == 3:
                        ties = enemigos.crear_enemigos(8, "defender")
                    else:
                        usuario_puntuacion(score)
                        pygame.quit()
                        sys.exit()

                    tiempo_restante = 300

                    font_nivel = pygame.font.SysFont("cambria", 50)
                    texto_nivel = font_nivel.render("Nivel {0}".format(nivel), True, colores.YELLOW1)
                    texto_nivel_rect = texto_nivel.get_rect(center=(ancho_pantalla // 2, largo_pantalla // 2))
                    pantalla.blit(texto_nivel, texto_nivel_rect)
                    xwing.misiles = []

                    pygame.display.flip()
                    pygame.time.wait(2000)

        pygame.display.flip()

    pygame.quit()

def menu_galaxy(): 
    pygame.display.set_caption("Menu")

    while True:
        pantalla.blit(fondo_menu, fondo_menu.get_rect())

        poscion_mouse = pygame.mouse.get_pos()

        font = pygame.font.SysFont("cambria", 100)
        texto = font.render("Capitan del Espacio", True, colores.YELLOW1)

        boton_juego = Boton(boton , 625, 300, "Jugar")
        boton_score = Boton(boton , 625, 550, "Calificaciones")
        boton_salir = Boton(boton , 625, 800, "Salir")

        pantalla.blit(texto,(240,10))

        for botones in [boton_juego , boton_score , boton_salir]:
            botones.cambiarColor(poscion_mouse)
            botones.actualizar()
    
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_juego.verificarClick(poscion_mouse):
                    juego()
                if boton_score.verificarClick(poscion_mouse):
                    puntuaciones()
                if boton_salir.verificarClick(poscion_mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

menu_galaxy()