import pygame
import sys
import colores
from galaxySpace import juego
from boton_click import Boton
import sqlite3

ancho_pantalla = 1250
largo_pantalla = 1000

pygame.init()

pantalla = pygame.display.set_mode((ancho_pantalla,largo_pantalla))
pygame.display.set_caption("Menu") 

fondo_menu = pygame.image.load("Python utn\jueguitos.py\imagenes\spacefondo.png")
fondo_menu = pygame.transform.scale(fondo_menu,(ancho_pantalla, largo_pantalla))

boton = pygame.image.load(r"Python utn\jueguitos.py\imagenes\boton transparente.png")
boton = pygame.transform.scale(boton, (360, 80))

def puntuaciones():
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

def menu_galaxy(): 
    pygame.display.set_caption("Menu")

    while True:
        pantalla.blit(fondo_menu, fondo_menu.get_rect())

        poscion_mouse = pygame.mouse.get_pos()

        font = pygame.font.SysFont("cambria", 100)
        texto = font.render("Space Galaxy", True, colores.YELLOW1)

        boton_juego = Boton(boton , 625, 300, "Jugar")
        boton_score = Boton(boton , 625, 550, "Calificaciones")
        boton_salir = Boton(boton , 625, 800, "Salir")

        pantalla.blit(texto,(375,10))

        for botones in [boton_juego , boton_score , boton_salir]:
            botones.cambiarColor(poscion_mouse)
            botones.actualizar()
    
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_juego.verificarClick(poscion_mouse):
                    juego(ancho_pantalla,largo_pantalla)
                if boton_score.verificarClick(poscion_mouse):
                    puntuaciones()
                if boton_salir.verificarClick(poscion_mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

menu_galaxy()