class Slaghandterer:

    def __init__(self,slag_id,deltaker):
        self._posisjon = (50,50)
        self._dimensjon = (50,50)

        self._forsvarer = deltaker
        self._id = slag_id
        self._slag = None

    def sett_pos(self,posisjon):
        self._posisjon = posisjon

    def sett_dim(self,dim):
        self._dimensjon = dim

    def har_sterkeste_kort(self,deltaker):
        if self._slag == None:
            return False
        return deltaker is self._slag.forelopig_vinner()

    def kan_spille_kort(self,deltaker,spillekort):

        if self._slag==None:
            return spillekort._kort.er_gull() and self._forsvarer is deltaker
        
        if spillekort._kort.er_gull():
            return False

        angrep = all((
            self._forsvarer is not deltaker,
            spillekort._kort.er_angrep() or spillekort._kort.er_forsterkning()
        ))
        forsvar = all((
            self._forsvarer is deltaker,
            spillekort._kort.er_forsvar() or spillekort._kort.er_forsterkning()
        ))

        siste = self._slag.siste_styrkekort(deltaker)
        
        if siste==None:
            return any((angrep, forsvar))
        return siste._kort._verdi>=spillekort._kort._verdi and any((angrep, forsvar))

    def sett_slag(self,slag):
        self._slag = slag