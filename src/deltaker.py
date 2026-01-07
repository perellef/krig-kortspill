from .bunke import Bunke

class Deltaker:

    def __init__(self,spiller,navn):
        self._navn = navn
        self._spiller = spiller
        self.__er_ferdig = False

        self._gull = Bunke()
        self._hand = Bunke()
        self._tekstboks = (0,0)

    def antall_gull(self):
        return len(self._gull._spkort)

    def trekk_kort(self,kort):
        self._hand.legg_til(kort)

    def bruk_kort(self,kort):
        self._hand.fjern(kort)

    def legg_til_slag(self,slag_id,slag):
        self._slag[slag_id] = slag

    def fjern_slag(self,slag_id):
        self._slag[slag_id] = None

    def tekstboks_pos(self,pos):
        self._tekstboks = pos

    def sett_til_ferdig(self):
        self.__er_ferdig = True

    def er_ferdig(self):
        return self.__er_ferdig

    def __str__(self):
        return f"{self._spiller} ({self._navn})"