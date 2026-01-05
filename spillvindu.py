from filleser import Filleser
from kort import Kort
from figur import Figur

import pygame

BREDDE, HOYDE = 1279, 656 # total storrelse 1279, 656

ROD = (255,0,0)
GRONN = (50,205,50)
LYS_GRONN = (60,215,60)
BLA = (11,181,255)
HVIT = (255,255,255)
GUL = (255,255,0)
GRA = (100,100,100)

FPS = 60

#---

konfig = Filleser.json("konfig")
dim = konfig["spillebrett"]["dimensjoner"]

KH = dim["kort"]["høyde"]
KB = dim["kort"]["bredde"]


class Spillvindu:

    @staticmethod
    def rotert_b_h(b,h,rotasjon):
        if rotasjon%360 in [0,180]:
            return b,h
        elif rotasjon%360 in [90,270]:
            return h,b
        else:
            raise ValueError(f"Value {rotasjon} not valid.")

    def __init__(self,spill,bakfarge = (50,205,50)):
        self._spill = spill

        pygame.font.init()
        self._brett =  pygame.display.set_mode((BREDDE, HOYDE))
        self._bakfarge = bakfarge

        self._slagplasser = []

        self._trekk_kort = []
        self._spilte_kort = []
        self._holder = None
        self._spilleforer_hand = None

        pygame.display.set_caption("⚔️ Krig (Kortspill) ⚔️")

    def trekk_kort(self,spkort):
        self._spilte_kort.append(spkort)

    def er_innenfor(self,peker,x,y,b,h):
        return all((peker[0]>=x, peker[0]<=x+b, peker[1]>=y, peker[1]<=y+h))

    def overste_holdbare(self,peker):
        for spillekort in reversed(self._trekk_kort+self._spilte_kort+self._spilleforer_hand._spkort):
            if not spillekort._holdbar:
                continue

            x,y = spillekort._gyldig_pos
            kb,kh = Spillvindu.rotert_b_h(KB,KH,spillekort._rotasjon)

            if self.er_innenfor(peker,x,y,kb,kh):
                return spillekort
        return None

    def overste_slag(self,peker):
        for slag in self._slagplasser:
            x,y = slag._posisjon
            b,h = slag._dimensjon

            if self.er_innenfor(peker,x,y,b,h):
                return slag
        return None

    def tegn_spillekort(self,spillekort):
        rotasjon = spillekort._rotasjon
        posisjon = spillekort._posisjon
        bakside = spillekort._bakside

        bilde = spillekort._kort._bilde
        if bakside:
            bilde = Kort._bilde_bakside

        self._brett.blit(pygame.transform.rotate(
            pygame.transform.scale(bilde,(KB,KH)),rotasjon),
            posisjon
        )

    def tegn_scoreboard(self):

        b = 800
        h = 400

        x = (BREDDE-b)//2
        y = (HOYDE-h)//2

        pygame.draw.rect(self._brett,GRA,pygame.Rect(x,y,b,h),2)

    def tegn_figur(self,figur):
        x = figur._x
        y = figur._y
        b = figur._b
        h = figur._h
        farge = figur._farge
        val = figur._val

        pygame.draw.rect(self._brett,farge,pygame.Rect(x,y,b,h),val)

    def tegn_boks(self,obj,farge):
        pos = obj._posisjon
        dim = obj._dimensjon
        pygame.draw.rect(self._brett,farge,pygame.Rect(*pos,*dim),1)

    def tegn_tekstboks(self,tekst,tekstfarge,font,fontstr,posisjon):
        font = pygame.font.SysFont(font, fontstr)
        tekstboks = font.render(tekst, tekstfarge, tekstfarge)
        self._brett.blit(tekstboks,posisjon)

    def animer_kort(self):

        speed = 45

        for spkort in self._spilte_kort:
            if not spkort._animeres:
                continue

            x_start, y_start = spkort._posisjon
            x_slutt, y_slutt = spkort._gyldig_pos

            dist_x = (x_slutt-x_start)
            dist_y = (y_slutt-y_start)

            if ((dist_x**2 + dist_y**2)**(1/2) > speed):
                rate = (dist_x**2 + dist_y**2)**(1/2)/speed # rate of which the distance traveled in x and y-direction has euclidian distance 1 
            
                x = x_start + dist_x/rate
                y = y_start + dist_y/rate

                spkort.sett_pos((x,y))
            
            else:
                spkort.tilbakestill_pos()
                spkort.fullfort_animasjon()


    def fyll_brett(self,figurer):
        self._brett.fill(self._bakfarge)

        for slagh in self._slagplasser:
            self.tegn_boks(slagh, LYS_GRONN)

        for deltaker in self._spill._deltakere.values():
            self.tegn_boks(deltaker._gull, LYS_GRONN)

        self.tegn_boks(self._spill._trekkbunke, LYS_GRONN)
        self.tegn_boks(self._spill._kastebunke, LYS_GRONN)

        for spillekort in self._trekk_kort:
            self.tegn_spillekort(spillekort)

        for spillekort in self._spilte_kort:
            self.tegn_spillekort(spillekort)

        for spillekort in self._spilleforer_hand._spkort: # duplikater
            self.tegn_spillekort(spillekort)

        if self._holder not in [None]+self._spilleforer_hand._spkort: # duplikat
            self.tegn_spillekort(self._holder)

        for deltaker in self._spill._deltakere.values():
            if deltaker is self._spill._spiller_i_tur:
                self.tegn_tekstboks(deltaker._spiller, GUL, "Arial", 14, deltaker._tekstboks)
                continue
            self.tegn_tekstboks(deltaker._spiller, HVIT, "Arial", 14, deltaker._tekstboks)

        for figur in figurer:
            self.tegn_figur(figur)

        if self._spill._ferdig:
            self.tegn_scoreboard()

        pygame.display.update()
        
    def spillekjoring(self):

        pygame.display.set_mode((0, 0), pygame.RESIZABLE)

        clock = pygame.time.Clock()
        running = True

        while running:

            figurer = []

            for event in pygame.event.get(): 

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    musepeker = pygame.mouse.get_pos() 
                    self._holder = self.overste_holdbare(musepeker)
                    
                    self.flytt_holdekort(musepeker)

                    
                    if self.marker_passes(musepeker):
                        self._spill._nestes_tur()

                
                if event.type == pygame.MOUSEBUTTONUP:
                    musepeker = pygame.mouse.get_pos()

                    if self._holder!=None:
                        self._holder.tilbakestill_pos() ## ikke alltid nodvendig

                        if (output := self.marker_spilles(musepeker)):
                            self._spill.spiller_kort(self._spill._spilleforer,self._holder,output[0])

                        elif self.marker_kastes(musepeker):
                            self._spill.kaster_kort(self._spill._spilleforer,self._holder)

                        elif self.marker_trekkes(musepeker):
                            self._spill.spilleforer_trekker_kort()

                        elif self.marker_innkasseres(musepeker):
                            self._spill.innkasserer_gull(self._holder,self._spill._spilleforer)

                        self._holder = None

                elif event.type == pygame.MOUSEMOTION:
                    musepeker = pygame.mouse.get_pos() 

                    self.flytt_holdekort(musepeker)
                    self.flytt_holdekort_i_spillerhand(musepeker)
                    

            if (info := self.marker()) is not None:
                figurer.append(Figur(*info))

            self.animer_kort()
            self.fyll_brett(figurer)
            clock.tick(FPS)

        pygame.quit()

    def flytt_holdekort(self,musepeker):

        if self._holder == None:
            return

        kb,kh = Spillvindu.rotert_b_h(KB,KH,self._holder._rotasjon)
        self._holder.sett_pos((musepeker[0]-kb/2, musepeker[1]-kh/2))

    def flytt_holdekort_i_spillerhand(self,musepeker):

        pekt_kort = self.overste_holdbare(musepeker)
        spillerhand = self._spilleforer_hand._spkort

        if self._holder is pekt_kort:
            return
        if self._holder not in spillerhand:
            return
        if pekt_kort not in spillerhand:
            return
    
        m,n = -1,-1
        for i,spkort in enumerate(spillerhand):
            if self._holder==spkort:
                m = i
            elif pekt_kort==spkort:
                n = i

        spillerhand[m],spillerhand[n] = spillerhand[n],spillerhand[m]

        x1,y1 = self._holder._gyldig_pos
        x2,y2 = pekt_kort._gyldig_pos

        pekt_kort.sett_pos((x1,y1))
        pekt_kort.sett_gyldig_pos((x1,y1))
        self._holder.sett_gyldig_pos((x2,y2))

    def marker(self):

        passive = (
            self.marker_spillbar,
            self.marker_trekkbar,
            self.marker_innkasserbar,
            self.marker_passes,
            self.marker_passbar,
        )

        aktive = (
            self.marker_spilles,
            self.marker_kastes,
            self.marker_trekkes,
            self.marker_innkasseres,
        )
        
        musepeker = pygame.mouse.get_pos() 

        if self._holder == None:
            for markering in passive:
                if info := markering(musepeker):
                    return (*info[1],2)
                
        else:
            for markering in aktive:
                if info := markering(musepeker):
                    return (*info[1],2)


    def marker_spillbar(self,musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None

        pekt_kort = self.overste_holdbare(musepeker)

        if pekt_kort == None:
            return None
        
        x,y = pekt_kort._posisjon
        kb,kh = Spillvindu.rotert_b_h(KB,KH,pekt_kort._rotasjon)
        
        # ytterste kort i spillehanden

        if len(self._spilleforer_hand._spkort)>0:
            if self._spilleforer_hand._spkort[-1] is pekt_kort:
                return pekt_kort,(x,y,kb,kh,BLA)

        # "innklemte" kort i spillehanden
        
        etterfolgende_kort = zip(self._spilleforer_hand._spkort[:-1],self._spilleforer_hand._spkort[1:])

        for sp1,sp2 in etterfolgende_kort:
            if pekt_kort is sp1:
                sp2_x,sp2_y = sp2._gyldig_pos
                
                if y==sp2_y:
                    b = min(kb,abs(x-sp2_x))
                    return pekt_kort,((x+kb-b,y,b,kh,BLA) if sp2_x<x else (x,y,b,kh,BLA))
                else:
                    h = min(kh,abs(sp2_y-y))
                    return pekt_kort,((x,y+kh-h,kb,h,BLA) if sp2_y<y else (x,y,kb,h,BLA))
                
    def marker_trekkbar(self,musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None

        if not self._spill.kan_trekke_kort(self._spill._spilleforer):
            return None

        pekt_kort = self.overste_holdbare(musepeker)

        if pekt_kort not in self._trekk_kort:
            return None
        
        
        vist_kort = self._trekk_kort[-1]
        
        x,y = vist_kort._posisjon
        kb,kh = Spillvindu.rotert_b_h(KB,KH,pekt_kort._rotasjon)
        
        return vist_kort,(x,y,kb,kh,BLA)
    
    def marker_passbar(self, musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None

        if len(self._trekk_kort)>0:
            return None
        
        trekkbunke = self._spill._trekkbunke
        x,y = trekkbunke._posisjon
        b,h = trekkbunke._dimensjon
        
        return trekkbunke,(x,y,b,h,BLA)
    
    def marker_innkasserbar(self,musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None

        pekt_kort = self.overste_holdbare(musepeker)
        slagh = self.overste_slag(musepeker)
        
        if None in (slagh,pekt_kort):
            return None
        if not pekt_kort._kort.er_gull():
            return None
        if not self._spill.slagh_kan_ta_gull(slagh,self._spill._spilleforer):
            return None
        
        x,y = pekt_kort._posisjon
        kb,kh = Spillvindu.rotert_b_h(KB,KH,pekt_kort._rotasjon)

        return pekt_kort,(x,y,kb,kh,BLA)
    
    def marker_spilles(self,musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None

        slagh = self.overste_slag(musepeker)
            
        if slagh == None:
            return None
        
        if not self._spill.kan_spille_kort(self._spill._spilleforer,self._holder,slagh):
            return None
        
        x,y = slagh._posisjon
        b,h = slagh._dimensjon

        return slagh,(x,y,b,h,ROD)
    
    def marker_kastes(self,musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None        
        if self._holder not in self._spilleforer_hand._spkort:
            return None
        
        kastebunke = self._spill._kastebunke
        x,y = kastebunke._posisjon
        b,h = kastebunke._dimensjon

        if not self.er_innenfor(musepeker,x,y,b,h): # markerer holdt kort over kastebunken
            return None
        
        return kastebunke,(x,y,b,h,ROD)    

    def marker_trekkes(self,musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None
        
        if not self._spill.kan_trekke_kort(self._spill._spilleforer):
            return None
        
        if self._holder not in self._trekk_kort:
            return None
        
        spillehand = self._spilleforer_hand
        x,y = spillehand._posisjon
        b,h = spillehand._dimensjon

        if not self.er_innenfor(musepeker,x,y,b,h): # markerer at kortet kan trekkes til handen
            return None

        return spillehand,(x,y,b,h,ROD)
    
    def marker_passes(self,musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None

        if len(self._trekk_kort)>0:
            return None
        
        trekkbunke = self._spill._trekkbunke
        x,y = trekkbunke._posisjon
        b,h = trekkbunke._dimensjon

        if not self.er_innenfor(musepeker,x,y,b,h):
            return None
        
        return trekkbunke,(x,y,b,h,ROD)

    def marker_innkasseres(self,musepeker):
        
        if not self._spill.er_spilleforers_tur():
            return None
        if not self._holder._kort.er_gull():
            return None
        
        slagh = self.overste_slag(self._holder._gyldig_pos)
        
        if slagh == None:
            return None
        
        gullbunke = self._spill._spilleforer._gull

        x,y = gullbunke._posisjon
        b,h = gullbunke._dimensjon

        if not self.er_innenfor(musepeker,x,y,b,h):
            return None
        if not self._spill.slagh_kan_ta_gull(slagh,self._spill._spilleforer):
            return None
        
        return gullbunke,(x,y,b,h,ROD)