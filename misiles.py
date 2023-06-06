class MisilArriba:
    def __init__(self, x, y, imagen):
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocidad = 10

    def actualizar(self):
        self.rect.y -= self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class MisilAbajo:
    def __init__(self, x, y, imagen):
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocidad = 5

    def actualizar(self):
        self.rect.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)