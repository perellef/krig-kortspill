import random

class Spilleteknikker:

    #
    # Forsterk kort slik at det er like mange som lederen.
    #
    # Argumenter:
    #  prioritering     "t" -> tilfeldig, "f" -> færrest kort forsterkning, "l" -> antall poeng til krigsleder, "fl" -> blanding av "f" og "l", "fk" -> blanding av "f" og antall kort til krigsleder
    #  maks             maksimalt antall kort som brukes i en forbedring
    #
    @staticmethod
    def forsterk(spill, t="t", maks=3):

        KI_spiller = spill._spiller_i_tur
        hand = KI_spiller._hand._spkort

        slagher = []
        for spiller in spill._slagh:
            for slagh in spill._slagh[spiller].values():
                if slagh._slag == None:
                    continue
                slagher.append(slagh)

        slagher = [slagh for slagh in slagher if slagh._slag.antall_unna_sterkeste(KI_spiller)<=maks]

        if len(slagher) == 0:
            return 0
        
        prio = {
            "t": lambda _: random.random(),
            "f": lambda x: x._slag.antall_unna_sterkeste(KI_spiller),
            "l": lambda x: abs(x._slag.sterkeste_deltaker().antall_gull()-KI_spiller.antall_gull()),
            "fl": lambda x: abs(x._slag.sterkeste_deltaker().antall_gull()-KI_spiller.antall_gull()+2*x._slag.antall_unna_sterkeste(KI_spiller)),
            "fk": lambda x: x._slag.antall_unna_sterkeste(KI_spiller)+len(x._slag.sterkeste_deltaker()._hand._spkort)
        }

        slagh = max(slagher, key=prio[t])

        if (slagh._forsvarer is KI_spiller):
            fun = lambda x: (x._kort.er_forsvar() or x._kort.er_forsterkning()) and spill.kan_spille_kort(KI_spiller,x,slagh)
        else:
            fun = lambda x: (x._kort.er_angrep() or x._kort.er_forsterkning()) and spill.kan_spille_kort(KI_spiller,x,slagh)
        
        spillerkort = sorted((kort for kort in hand if fun(kort)), key = lambda x: x._kort._verdi, reverse=True)

        n = slagh._slag.antall_unna_sterkeste(KI_spiller)
        if (n > len(spillerkort)):
            return 0
        
        for spkort in spillerkort[:n]:
            spill.spiller_kort(KI_spiller, spkort, slagh, animeres=True, delay=1)
        return n

    #
    # Utplasser gullkort
    #
    # Argumenter:
    #  m             minimalt antall forsvarskort som trengs hvis ingen gullkort ligger ute
    #  n             minimalt antall forsvarskort som trengs 
    #
    @staticmethod
    def utplasser_gull_og_forsvar(spill, m=0, n=1):

        KI_spiller = spill._spiller_i_tur
        hand = KI_spiller._hand._spkort

        ledig_slagh = None
        for slagh in spill._slagh[KI_spiller].values():
            if slagh._slag is None:
                ledig_slagh = slagh
                break
        if ledig_slagh == None:
            return 0

        ingen_slag = True
        for slagh in spill._slagh[KI_spiller].values():
            if slagh._slag != None:
                ingen_slag = False
                break


        forsv_hand = [spillekort for spillekort in hand if spillekort._kort.er_forsvar() and spill.kan_spille_kort(KI_spiller,spillekort,slagh)]
        if (n > len(forsv_hand) and (m > len(forsv_hand) and not ingen_slag)):
            return 0

        i = 0
        while True:
            if i>=len(hand):
                return 0
            
            gullkort = hand[i]

            if gullkort._kort.er_gull():
                break

            i += 1
        
        spill.spiller_kort(KI_spiller, gullkort, ledig_slagh, animeres=True, delay=1)

        sort_forsv_hand = sorted(forsv_hand, key = lambda x: x._kort._verdi, reverse=True)

        for fors_kort in sort_forsv_hand[:n]:
            spill.spiller_kort(KI_spiller, fors_kort, ledig_slagh, animeres=True, delay=1)
        return n+1
    #
    # Angrip og forsvar
    #
    # Argumenter:
    #  n                antall det skal angripes/forsvares med
    #  t                "t" -> tilfeldig krig
    @staticmethod
    def angrip_forsvar(spill, n=1, t="t"):

        KI_spiller = spill._spiller_i_tur
        hand = KI_spiller._hand._spkort

        slagher = []
        for spiller in spill._slagh:
            for slagh in spill._slagh[spiller].values():
                if slagh._slag == None:
                    continue
                slagher.append(slagh)

        slagher = [slagh for slagh in slagher if slagh._slag.antall_unna_sterkeste(KI_spiller)==0]

        if len(slagher) == 0:
            return 0
        
        prio = {
            "t": lambda _: random.random(),
        }

        slagh = max(slagher, key=prio[t])

        if (slagh._forsvarer is KI_spiller):
            fun = lambda x: (x._kort.er_forsvar() or x._kort.er_forsterkning()) and spill.kan_spille_kort(KI_spiller,x,slagh)
        else:
            fun = lambda x: (x._kort.er_angrep() or x._kort.er_forsterkning()) and spill.kan_spille_kort(KI_spiller,x,slagh)
        
        spillerkort = sorted((kort for kort in hand if fun(kort)), key = lambda x: x._kort._verdi, reverse=True)

        if (n > len(spillerkort)):
            return 0
        
        for spkort in spillerkort[:n]:
            spill.spiller_kort(KI_spiller, spkort, slagh, animeres=True, delay=1)
        return n

    #
    # Kast kort
    #
    # Argumenter:
    #  t                "t" -> tilfeldig kort kastes, "f" -> dårligste forb. kort, "A" -> dårligste ang. kort -> "F" -> dårligste fors. kort
    #
    @staticmethod
    def kast_kort(spill, t="t"):

        KI_spiller = spill._spiller_i_tur
        hand = KI_spiller._hand._spkort

        n = max(len(hand)+2-spill._konfig["maks_kort"],0)
        if (n==0):
            return 0

        if t == "t":
            pri_hand = random.sample(hand, len(hand))
        else:
            er_farge = {
                "f": lambda x: x.er_forsterkning(),
                "A": lambda x: x.er_angrep(),
                "F": lambda x: x.er_forsvar()
            }[t]

            fun_forst = lambda x: x._kort._verdi if (er_farge(x._kort)) else 100 + (0 if x._kort.er_gull() else x._kort._verdi)
            pri_hand = sorted(hand, key = fun_forst)

        for spkort in pri_hand[:n]:
            spill.kaster_kort(KI_spiller, spkort, animeres=True, delay=1)
        return n