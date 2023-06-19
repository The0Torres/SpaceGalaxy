class Misil:
    def __init__(self, x, y, imagen, direccion):
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.direccion = direccion
        if self.direccion == "arriba":
            self.velocidad = 10
        elif self.direccion == "abajo":
            self.velocidad = 5

    def actualizar(self):
        if self.direccion == "arriba":
            self.rect.y -= self.velocidad
        elif self.direccion == "abajo":
            self.rect.y += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
