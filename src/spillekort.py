from .filleser import Filleser

konfig = Filleser.json("konfig")
dim = konfig["spillebrett"]["dimensjoner"]

KH = dim["kort"]["høyde"]
KB = dim["kort"]["bredde"]

class Spillekort:

    def __init__(self,kort):
        self._kort = kort
        self._posisjon = (50,50)
        self._gyldig_pos = (50,50)
        self._rotasjon = 0

        self._animeres = False
        self._bakside = True
        self._holdbar = True # testverdi
        self._byttbar = True # testverdi

    def sett_pos(self,pos):
        self._posisjon = pos
    
    def sett_gyldig_pos(self,pos):
        self._gyldig_pos = pos

    def sett_rotasjon(self,rotasjon):
        self._rotasjon = rotasjon

    def tilbakestill_pos(self):
        self._posisjon = self._gyldig_pos

    def fullfort_animasjon(self):
        self._animeres = False

    def apne_kort(self):
        self._bakside = False

    def lukk_kort(self):
        self._bakside = True

    def bilde(self):
        return f"{self._kort}.png"

    def __str__(self):
        return str(self._kort).capitalize()