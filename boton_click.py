import pygame
import colores


pygame.init()
pantalla = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Boton")
fuente_principal = pygame.font.SysFont("cambria", 60)

class Boton():
	def __init__(self, imagen, x_pos, y_pos, texto_boton):
		self.imagen = imagen
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.texto = texto_boton
		self.texto_renderizado = fuente_principal.render(str(self.texto), True, colores.YELLOW4)
		if self.imagen is None:
			#Si no hay imagen de boton se vuelve un boton el texto
			self.imagen = self.texto_renderizado
		self.rect = self.imagen.get_rect(center=(self.x_pos, self.y_pos))
		self.rect_texto = self.texto_renderizado.get_rect(center=(self.x_pos, self.y_pos))

	def actualizar(self):
		if self.imagen is not None:
			pantalla.blit(self.imagen, self.rect)
		pantalla.blit(self.texto_renderizado, self.rect_texto)

	def cambiarColor(self, posicion):
		#Cambia de color el boton si esta en posicion para clickearlo
		if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.bottom):
			self.texto_renderizado = fuente_principal.render(str(self.texto), True, colores.YELLOW1)
		else:
			self.texto_renderizado = fuente_principal.render(str(self.texto), True, colores.YELLOW4)

	def verificarClick(self, posicion):
		if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False