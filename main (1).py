import pygame
from constantes import *
import colores
from personaje import Personaje
import json
import re

def parse_puntos(archivo:str)->list:
    i=0
    with open(archivo, "r")as archivo:
        lista_puntos = []
        todo = archivo.read()
        nombre = re.findall(r'"nombre": "([a-zA-Z0-9]+)', todo)
        tiempo = re.findall(r'"tiempo": ([0-9]+)', todo)
        puntos = re.findall(r'"puntos": ([0-9]+)', todo)

        for i in range(len(nombre)):
            dic_puntajes={}
            dic_puntajes["nombre"]=nombre[i]
            dic_puntajes["tiempo"]= tiempo[i]
            dic_puntajes["puntos"]=puntos[i]
            lista_puntos.append(dic_puntajes)
            i += 1
    return lista_puntos

pygame.init()

puntaje = parse_puntos("data_juego.json")

pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VANTANA))
pygame.display.set_caption("Mi primer bosque")
reloj = pygame.time.Clock()

imagen_bosque = pygame.image.load("bosque.jpg")
imagen_bosque = pygame.transform.scale(imagen_bosque,(ANCHO_VENTANA, ALTO_VANTANA))

imagen_jugar = pygame.image.load("jugar.jpg")
imagen_jugar = pygame.transform.scale(imagen_jugar,(ANCHO_BOTON, ALTO_BOTON))
rect_boton = imagen_jugar.get_rect()
rect_boton.y = POS_TOP_BOTON
rect_boton.x = POS_LEFT_PUNTOS

imagen_puntaje = pygame.image.load("puntajes.jpg")
imagen_puntaje = pygame.transform.scale(imagen_puntaje,(ANCHO_PUNTOS, ALTO_PUNTOS))
rect_boton_puntos = imagen_puntaje.get_rect()
rect_boton_puntos.y = POS_TOP_PUNTOS
rect_boton_puntos.x = POS_LEFT_PUNTOS


#Creacion de mi personaje (constructor)
personaje1 = Personaje()

flag_correr = True
while flag_correr:
    lista_evento = pygame.event.get()
    #fondo
    pantalla.blit(imagen_bosque,imagen_bosque.get_rect())

    if JUGANDO == 0:
        pantalla.blit(imagen_jugar, rect_boton)
        pantalla.blit(imagen_puntaje, rect_boton_puntos)
        pygame.display.flip()
        for evento in lista_evento:
            if evento.type == pygame.QUIT:
                flag_correr = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                lista_click = list(evento.pos)
                if (lista_click[0]> rect_boton[0] and lista_click[0] < (rect_boton[0]+rect_boton[2])):
                    if (lista_click[1]> rect_boton[1] and lista_click[1]< (rect_boton[1]+rect_boton[3])):
                        JUGANDO = 1
                if( lista_click[0] > rect_boton_puntos[0] and lista_click[0]< (rect_boton_puntos[0]+rect_boton_puntos[2])):
                    if( lista_click[1]> rect_boton_puntos[1] and lista_click[1]< (rect_boton_puntos[1]+rect_boton_puntos[3])):
                        JUGANDO = 2
    elif JUGANDO == 2:
        for evento in lista_evento:
            if evento.type == pygame.QUIT:
                flag_correr = False
        
        for i in range(len(puntaje)):
            font_nombre = pygame.font.SysFont("Arial", 24)
            texto_nombre = font_nombre.render(puntaje[i]["nombre"], True, colores.BLACK)
            pantalla.blit(texto_nombre,(LEFT_TEXTO, TOP_TEXTO+(i*25)))

            font_tiempo= pygame.font.SysFont("Arial", 24)
            texto_tiempo = font_tiempo.render(puntaje[i]["tiempo"], True, colores.BLACK)
            pantalla.blit(texto_tiempo,(LEFT_TEXTO*2, TOP_TEXTO+(i*25)))

            font_puntos = pygame.font.SysFont("Arial", 24)
            texto_puntos = font_puntos.render(puntaje[i]["puntos"], True, colores.BLACK)
            pantalla.blit(texto_puntos,(LEFT_TEXTO*2.5, TOP_TEXTO+(i*25)))

    elif JUGANDO == 1:
        for evento in lista_evento:
            if evento.type == pygame.QUIT:
                flag_correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    personaje1.caminarDerecha("derecha")
                if evento.key == pygame.K_LEFT:
                    personaje1.caminarIzquierda("izquierda")

        milis = reloj.tick(6) #milis guarda el tiempo que transcurrió desde la última vez que 
        #llamé a la función reloj.tick
        #actualizo los movimientos de mi personaje
        personaje1.actualizar()
        #dibujar mi personaje
        personaje1.dibujar(pantalla)

        font = pygame.font.SysFont("Arial", 30)
        tiempo = font.render("TIEMPO: {0}".format(SEGUNDOS),True,colores.WHITE)
        pantalla.blit(tiempo,(10,10))
        TIEMPO +=1
        if TIEMPO == 8:
            TIEMPO = 0
            SEGUNDOS -= 1

    pygame.display.flip()

pygame.quit

