from slagstyrke import Slagstyrke

class Slag:
    
    def __init__(self,forsvarer,gull_spkort):
        self._gull = gull_spkort
        self._forsvarer = forsvarer
        self._styrker = {}

    def legg_til_kort(self,deltaker,spillekort):
        if deltaker not in self._styrker:
            self._styrker[deltaker] = Slagstyrke()
        self._styrker[deltaker].legg_til(spillekort)

    def sterkeste_deltaker(self):

        if len(self._styrker)==0:
            return self._forsvarer
        elif len(self._styrker)==1:
            return list(self._styrker.keys())[0]

        styrker = list(sorted(self._styrker.items(), key=lambda x:x[1].styrke(), reverse=True))

        beste, nest_beste = styrker[:2]
        if beste[1] == nest_beste[1]:
            return self._forsvarer
        return beste[0]
    
    def forelopig_vinner(self):
        antall = []
        for i,styrke in self._styrker.items():
            antall.append(len(styrke._kort))

        if len(antall)==0:
            return None

        if (antall.count(max(antall)) == 1):
            return self.sterkeste_deltaker()
        return None

    def antall_unna_sterkeste(self, deltaker):
        sterkeste = self.sterkeste_deltaker()
        if sterkeste not in self._styrker:
            return 0
        if deltaker not in self._styrker:
            return len(self._styrker[sterkeste]._kort)
        return len(self._styrker[sterkeste]._kort) - len(self._styrker[deltaker]._kort)

    def siste_styrkekort(self,deltaker):
        if deltaker not in self._styrker:
            return None
        return self._styrker[deltaker].siste()

    def __str__(self):
        return f'slag: {", ".join(f"{deltaker._spiller}: {slagstyrke}" for deltaker,slagstyrke in self._styrker.items())}'
