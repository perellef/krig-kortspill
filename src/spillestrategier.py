from .spilleteknikker import Spilleteknikker

class Spillestrategier:

    @staticmethod
    def normal(spill):
        return any((
            Spilleteknikker.forsterk(spill, t="t", maks=1),
            Spilleteknikker.forsterk(spill, t="fl", maks=3),
            Spilleteknikker.utplasser_gull_og_forsvar(spill),
            Spilleteknikker.angrip_forsvar(spill,n=3, t="t"),
            Spilleteknikker.angrip_forsvar(spill,n=1, t="t"),
            Spilleteknikker.kast_kort(spill, t="f"),
        ))