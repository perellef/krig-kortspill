from spilleteknikker import Spilleteknikker

class Spillestrategier:

    @staticmethod
    def normal(spill):

        # sjekker om ingen handlinger er utført
        if not any((
            Spilleteknikker.forsterk(spill, t="t", maks=1),
            Spilleteknikker.forsterk(spill, t="fl", maks=3),
            Spilleteknikker.utplasser_gull_og_forsvar(spill),
            Spilleteknikker.angrip_forsvar(spill,n=3, t="t"),
            Spilleteknikker.angrip_forsvar(spill,n=1, t="t"),
            Spilleteknikker.kast_kort(spill, t="f"),
        )):
            # sjekker om deltakeren ikke har mulighet til å trekke
            if any((
                len(spill._trekkbunke._spkort)==0,
                len(spill._spiller_i_tur._hand._spkort)>=spill._konfig["maks_kort"],
            )):
                spill.passer()