from .deltaker import Deltaker
from .spillvindu import Spillvindu
from .kort import Kort
from .spillekort import Spillekort
from .slaghandterer import Slaghandterer
from .slag import Slag
from .bunke import Bunke
from .oppsett import Oppsett
from .filleser import Filleser
from .ki_handterer import KI_handterer

import random
import threading
import time

konfig = Filleser.json("konfig")

class Spill:

    def __init__(self,ant_spillere,spilleforer):        
        self._konfig = konfig

        self._spillvindu = Spillvindu(self)

        self._deltakere = {}
        for spiller in self._konfig["gjeldende spillere"][f"{ant_spillere} spillere"]:
            navn = self._konfig["navn"][spiller]

            deltaker = Deltaker(spiller,navn)
            Oppsett.sett_plass_deltakerhand(deltaker)
            Oppsett.sett_plass_deltakergull(deltaker)

            self._deltakere[spiller] = deltaker
            Oppsett.sett_plass_deltakertekstboks(deltaker)
            
        # --
        self._ferdig = False
        self._passer = 0
        self._ant_spillere = ant_spillere
        self._spillekort = self._definer_spillekort(ant_spillere)
        self._spilleforer = self._deltakere[spilleforer]
        self._spiller_i_tur = self._deltakere[spilleforer]
        self._turfase = 1
        # --

        self._slagh = self._definer_slaghandterere()

        self._trekkbunke = Bunke()
        self._kastebunke = Bunke()
        Oppsett.sett_plass_bunke(self._trekkbunke,"trekk")
        Oppsett.sett_plass_bunke(self._kastebunke,"kaste")

        self._KIer = threading.Thread(target=self._KI_spillehandterer,daemon=True)

    def start_spill(self):
        spillekort = self.stokk_kort()
        
        self._trekkbunke.sett_kort(spillekort)
        self._kastebunke.sett_kort([])
        Oppsett.sett_pos_trekkbunke(self._trekkbunke)

        spvindu = self._spillvindu

        spvindu._trekk_kort = spillekort
        spvindu._spilleforer_hand = self._spilleforer._hand
        spvindu._slagplasser = [el for elem in self._slagh.values() for el in elem.values()]
        
        for deltaker in self._deltakere.values():
            for _ in range(self._konfig["start_kort"]):
                self.trekker_kort(deltaker)

        self._KIer.start()
        spvindu.spillekjoring()

    def _KI_spillehandterer(self):

        ki = KI_handterer("middels")

        waittime = 1
        while True:
            if self.alle_er_ferdig():
                break

            if self.er_spilleforers_tur():
                time.sleep(waittime)
                continue
                
            if self._spiller_i_tur.er_ferdig():
                self._nestes_tur()
                continue
            
            spilte_kort = ki.utfor_strategi(self)
            if self.kan_trekke_kort(self._spiller_i_tur):
                self.trekker_kort(self._spiller_i_tur, animeres=True)
                time.sleep(0.5)
            elif not spilte_kort:
                self._spiller_i_tur.sett_til_ferdig()
                if self.alle_er_ferdig():
                    break

            if self.kan_trekke_kort(self._spiller_i_tur):
                self.trekker_kort(self._spiller_i_tur, animeres=True)

            self._nestes_tur()
            time.sleep(waittime)

        self._ferdig = True
        self.åpne_spillerhender()

    def åpne_spillerhender(self):
        for deltaker in self._deltakere.values():
            for spkort in deltaker._hand._spkort:
                spkort.apne_kort()

    def vinnere(self):
        høyeste = 0
        vinnere = []
        for deltaker in self._deltakere.values():
            if deltaker.antall_gull() > høyeste:
                høyeste = deltaker.antall_gull()
                vinnere = [deltaker]
            elif deltaker.antall_gull() == høyeste:
                vinnere.append(deltaker)
        return vinnere

    def alle_er_ferdig(self):
        return all((deltaker.er_ferdig() for deltaker in self._deltakere.values()))

    def kan_trekke_kort(self,deltaker):
        return all((
            not self._ferdig,
            len(self._trekkbunke)>0,
            len(deltaker._hand._spkort)<self._konfig["maks_kort"],
        ))

    def trekker_kort(self, deltaker, animeres=False, delay=0):
        self._passer = 0
        spkort = self._trekkbunke.trekk_fra()

        deltaker.trekk_kort(spkort)
        if deltaker is self._spilleforer:
            spkort.apne_kort()
        spkort._animeres = animeres
        Oppsett.sett_pos_deltakerhand(deltaker)
        
        self._spillvindu.trekk_kort(spkort)

        time.sleep(delay)

    def passer(self):
        self._passer += 1
        self._nestes_tur()

    def spilleforer_trekker_kort(self):
        self.trekker_kort(self._spilleforer)
        if all((
            self._turfase in [1,2],
            len(self._spilleforer._hand._spkort)<self._konfig["maks_kort"],
        )):
            self._turfase = 3
            return
        
        self._nestes_tur()

    def kaster_kort(self, deltaker, spkort, animeres=False, delay=0):
        self._turfase = 2
        self._kastebunke.legg_til(spkort)     
        
        deltaker.bruk_kort(spkort)
        spkort.apne_kort()
        self._spillvindu._spilte_kort.remove(spkort)
        self._spillvindu._spilte_kort.append(spkort)

        spkort._animeres = animeres
        Oppsett.sett_pos_spillekort_kastebunke(self._kastebunke, spkort)
        Oppsett.sett_pos_deltakerhand(deltaker)

        time.sleep(delay)

    def _nestes_tur(self):        
        self._turfase = 1

        spillere = list(self._deltakere.values())
        for i in range(len(spillere)):
            if spillere[i] is self._spiller_i_tur:
                self._spiller_i_tur = spillere[(i+1)%len(spillere)]
                return
    
    def er_spilleforers_tur(self):
        return self._spiller_i_tur is self._spilleforer
    
    def kan_spille_kort(self,deltaker,spillekort,slagh):
        return all((
            not self._ferdig,
            spillekort in deltaker._hand._spkort,
            slagh.kan_spille_kort(deltaker,spillekort),
        ))

    def spiller_kort(self, deltaker, spillekort, slagh, animeres=False, delay=0):
        self._turfase = 2
        
        deltaker.bruk_kort(spillekort)
        self._spillvindu._spilte_kort.remove(spillekort)
        self._spillvindu._spilte_kort.append(spillekort)
        spillekort.apne_kort()

        spillekort._animeres = animeres
        if spillekort._kort.er_gull():
            slag = Slag(deltaker,spillekort)
            slagh.sett_slag(slag)
            Oppsett.sett_pos_slaggull(slagh)
        else:
            slagh._slag.legg_til_kort(deltaker, spillekort)
            Oppsett.sett_pos_slagstyrke(slagh, deltaker)

        Oppsett.sett_pos_deltakerhand(deltaker)
        
        time.sleep(delay)

    def slagh_kan_ta_gull(self,slagh,deltaker):
        return all((
            not self._ferdig,
            slagh.har_sterkeste_kort(deltaker),
            self._turfase == 1
        ))
    
    def innkasserer_gull(self, gullkort, deltaker, animeres=False, delay=0):
        gullbunke = deltaker._gull
        gullbunke.legg_til(gullkort)

        gullkort._animeres = animeres
        Oppsett.sett_pos_deltakergull(deltaker)

        self._spillvindu._spilte_kort.remove(gullkort)
        self._spillvindu._spilte_kort.append(gullkort)

        gull_slagh = None
        for spiller in self._slagh:
            for slagh in self._slagh[spiller].values():
                if slagh._slag is None:
                    continue
                if slagh._slag._gull is not gullkort:
                    continue
                gull_slagh = slagh
                break

        slag = gull_slagh._slag
        for styrke in slag._styrker.values():
            time.sleep(0.05)
            for spkort in styrke._kort:
                spkort._animeres = True
                Oppsett.sett_pos_spillekort_kastebunke(self._kastebunke, spkort)
                self._kastebunke.legg_til(spkort)

                self._spillvindu._spilte_kort.remove(spkort)
                self._spillvindu._spilte_kort.append(spkort)

        gull_slagh.sett_slag(None)

        time.sleep(delay)

    def hent_deltaker(self, spiller):
        return self._deltakere[spiller]

    def hent_slag(self, navn, slag_id):
        spiller = self._deltakere[navn]
        slag = spiller._slag[f"{slag_id}"]
        return slag

    def stokk_kort(self):
        random.shuffle(self._spillekort)
        return self._spillekort

    def _definer_spillekort(self,antall):
        
        spillekort = []

        for farge,info in konfig["kort"][f"{antall} spillere"].items():
            antall = info["antall"]
            for verdi in info["verdi"]:
                kort = Kort(farge,verdi)

                for _ in range(antall//len(info["verdi"])):
                    spillekort.append(Spillekort(kort))

        return spillekort

    def _definer_slaghandterere(self):
        slaghandterer = {}
        for deltaker in self._deltakere.values():
            slaghandterer.setdefault(deltaker,{})
            for i in range(3):

                slagh = Slaghandterer(i+1,deltaker)
                Oppsett.sett_plass_slag(slagh)

                slaghandterer[deltaker].setdefault(i+1,slagh)
        return slaghandterer