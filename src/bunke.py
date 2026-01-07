
class Bunke:

    def __init__(self):
        self._posisjon = (50,50)
        self._dimensjon = (50,50)

        self._spkort = []

    def legg_til(self,spkort):
        self._spkort.append(spkort)

    def fjern(self,spkort):
        self._spkort.remove(spkort)

    def trekk_fra(self):
        return self._spkort.pop()

    def sett_kort(self,spkort_liste):
        self._spkort = spkort_liste

    def sett_pos(self,posisjon):
        self._posisjon = posisjon

    def er_tom(self):
        return len(self._spkort) == 0

    def ikke_er_tom(self):
        return len(self._spkort) > 0

    def sett_dim(self,dim):
        self._dimensjon = dim

    def __len__(self):
        return len(self._spkort)