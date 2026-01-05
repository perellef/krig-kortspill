
class Slagstyrke:

    def __init__(self):
        self._kort = []

    def legg_til(self, kort):
        self._kort.append(kort)
        
    def styrke(self):
        return len(self._kort)

    def siste(self):
        return self._kort[-1]

    def __str__(self):
        return ' '.join(str(kort) for kort in self._kort)