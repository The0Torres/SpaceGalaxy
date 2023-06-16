import pygame
import sys
import pygame_gui
import colores
import sqlite3
from boton_click import Boton

pygame.init()

gestor_interfaz = pygame_gui.UIManager((1250, 1000))

entrada_texto = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((280, 400), (700, 80)),
                                                    manager=gestor_interfaz,
                                                    object_id='#nombre_id')

reloj = pygame.time.Clock()

def usuario_puntuacion(pantalla, score):
    nombre_ingresado = False
    while True:
        frecuencia_ui = reloj.tick(60) / 1000

        pantalla.fill((colores.BLACK))

        poscion_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (evento.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    evento.ui_object_id == '#nombre_id' and not nombre_ingresado):
                nombre_usuario = evento.text

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
                        print("Se creó la tabla usuarios")
                    except sqlite3.OperationalError:
                        print("La tabla usuarios ya existe")

                    try:
                        conexion.execute("INSERT INTO usuarios (nombre, puntacion) VALUES (?, ?)", (nombre_usuario, score))
                        conexion.commit()
                        nombre_ingresado = True
                        print("Registro insertado correctamente")
                    except:
                        print("Error al insertar el registro")

            gestor_interfaz.process_events(evento)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_salir.verificarClick(poscion_mouse):
                    pygame.quit()
                    sys.exit()

        gestor_interfaz.update(frecuencia_ui)

        gestor_interfaz.draw_ui(pantalla)
        font = pygame.font.SysFont("cambria", 80)
        texto = font.render(f"Puntuacion: {score}", True, colores.YELLOW1)
        pantalla.blit(texto, (365, 100))
        font = pygame.font.SysFont("cambria", 60)
        if nombre_ingresado:
            texto = font.render("Nombre ingresado: {0}".format(nombre_usuario), True, colores.YELLOW1)
        else:
            texto = font.render("Ingrese su nombre de usuario", True, colores.YELLOW1)
        pantalla.blit(texto, (250, 300))

        boton_salir = Boton(None, 625, 800, "Salir")
        boton_salir.cambiarColor(poscion_mouse)
        boton_salir.actualizar()

        pygame.display.update()
