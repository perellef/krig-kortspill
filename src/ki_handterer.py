import random

from .spillestrategier import Spillestrategier

class KI_handterer:

    def __init__(self,niva):
        self._niva = niva

    def utfor_strategi(self, spill):
        self.strategi_inkasser_gull(spill)
        return self.strategi_stridsvalg(spill)

    def strategi_inkasser_gull(self, spill):

        deltaker = spill._spiller_i_tur

        for kropp in spill._slagh.values():
            for slagh in kropp.values():

                if not spill.slagh_kan_ta_gull(slagh, deltaker):
                    continue

                p = random.random()

                # deltaker "overser" muligheten for å innkassere
                if (self._niva=="lett") and p<0.3:
                    continue
                elif (self._niva=="middels") and p<0.1:
                    continue
                elif (self._niva=="vanskelig") and p<0.005:
                    continue

                gullkort = slagh._slag._gull
                spill.innkasserer_gull(gullkort, deltaker, animeres=True, delay=2)

    def strategi_stridsvalg(self, spill):
        return Spillestrategier.normal(spill)
