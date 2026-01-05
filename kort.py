
import pygame

class Kort:

    _bilde_bakside = pygame.image.load("assets/bakside.png")

    def __init__(self,farge,verdi):
        self._farge = farge
        self._verdi = verdi

        bildepng = f"assets/{verdi}_{farge}.png"
        if (verdi==None):
            bildepng = f"assets/{farge}.png" 

        self._bilde = pygame.image.load(bildepng)

    def er_gull(self):
        return self._farge=="gull"
    
    def er_forsterkning(self):
        return self._farge=="forsterkning"
    
    def er_angrep(self):
        return self._farge=="angrep"
    
    def er_forsvar(self):
        return self._farge=="forsvar"

    def __str__(self):
        if self.er_gull():
            return self._farge
        return self._farge + str(self._verdi)