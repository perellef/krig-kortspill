from filleser import Filleser

import math

konfig = Filleser.json("konfig")
dim = konfig["spillebrett"]["dimensjoner"]

KH = dim["kort"]["høyde"]
KB = dim["kort"]["bredde"]
LM = dim["margin"]["liten"]
MM = dim["margin"]["medium"]
SM = dim["margin"]["stor"]
EM = dim["margin"]["ekstra"]
HTM = dim["margin"]["horisontal-tekst"]
VTM = dim["margin"]["vertikal-tekst"]

# i.   HOYDE = 656 = bar + 8*KL + 4*lm (liten margin) + 4*mm (medium margin)
# ii.  BREDDE = 1279 = 9*KB + 6*KL + 10*lm (liten margin) + 4*mm (medium margin) + 2*sm (stor margin)
# iii. hoyde = 656 = bar + 7*KL + 3*KB + 6*lm (liten margin) + 2*mm (medium margin)

bunke_bredde = KB
bunke_hoyde = KH        
hand_bredde = 4*KB
hand_hoyde = KH
slag_bredde = 2*KH+KB+2*LM
slag_hoyde = 3*KH+2*LM

posisjoner = {}

posisjoner["trekkbunke"] = ((2*KH+4*KB+SM+HTM+MM+5*LM+1e-4)//1, (3.7*KH+VTM+MM+2*LM+1e-4)//1, bunke_hoyde, bunke_bredde)
posisjoner["kastebunke"] = ((5*KH+5*KB+SM+HTM+MM+5*LM+1e-4)//1, (3.7*KH+VTM+MM+2*LM+1e-4)//1, bunke_hoyde, bunke_bredde)

posisjoner.setdefault("sør", {})
posisjoner["sør"].setdefault("hånd", ((6.7*KH+1.5*KB+HTM+SM+MM+5*LM+1e-4-hand_bredde/2)//1, (6.7*KH+KB+2*VTM+2*MM+4*LM+1e-4)//1, hand_bredde, hand_hoyde))
posisjoner["sør"].setdefault("gull", ((3.7*KH+KB+HTM+SM+MM+4*LM+1e-4)//1, (7.2*KH+0.5*KB+2*VTM+2*MM+4*LM+1e-4)//1, (1.5*bunke_hoyde+1e-4)//1, bunke_bredde))
posisjoner["sør"].setdefault("slag 1", ((3.7*KH+SM+HTM+2*LM+1e-4)//1, (3.7*KH+KB+VTM+2*MM+2*LM+1e-4)//1, slag_bredde, slag_hoyde))
posisjoner["sør"].setdefault("slag 2", ((5.7*KH+KB+HTM+SM+MM+4*LM+1e-4)//1, (3.7*KH+KB+VTM+2*MM+2*LM+1e-4)//1, slag_bredde, slag_hoyde))
posisjoner["sør"].setdefault("slag 3", ((7.7*KH+2*KB+HTM+SM+2*MM+6*LM+1e-4)//1, (3.7*KH+KB+VTM+2*MM+2*LM+1e-4)//1, slag_bredde, slag_hoyde))
posisjoner["sør"].setdefault("tekstboks", ((6.7*KH+1.5*KB+HTM+SM+MM+5*LM+1e-4-hand_bredde/2)//1, (6.7*KH+KB+VTM+2*MM+4*LM+1e-4)//1, hand_bredde, VTM))

posisjoner.setdefault("nord", {})
posisjoner["nord"].setdefault("hånd", ((6.7*KH+1.5*KB+HTM+SM+MM+5*LM+1e-4-hand_bredde/2)//1, (-0.3*KH+1e-4)//1, hand_bredde, hand_hoyde))
posisjoner["nord"].setdefault("gull", ((8.7*KH+KB+HTM+SM+MM+4*LM+1e-4)//1, 0.2*KH-0.5*KB, (1.5*bunke_hoyde+1e-4)//1, bunke_bredde))
posisjoner["nord"].setdefault("slag 1", ((7.7*KH+2*KB+HTM+SM+2*MM+6*LM+1e-4)//1, (0.7*KH+VTM+1e-4)//1, slag_bredde, slag_hoyde))
posisjoner["nord"].setdefault("slag 2", ((5.7*KH+KB+HTM+SM+MM+4*LM+1e-4)//1, (0.7*KH+VTM+1e-4)//1, slag_bredde, slag_hoyde))
posisjoner["nord"].setdefault("slag 3", ((3.7*KH+SM+HTM+2*LM+1e-4)//1, (0.7*KH+VTM+1e-4)//1, slag_bredde, slag_hoyde))
posisjoner["nord"].setdefault("tekstboks", ((6.7*KH+1.5*KB+HTM+SM+MM+5*LM+1e-4-hand_bredde/2)//1, (0.7*KH)//1, hand_bredde, VTM))

posisjoner.setdefault("vest", {})
posisjoner["vest"].setdefault("hånd", ((-0.3*KH+1e-4)//1, (2*KH+KB+EM+MM+2*LM+1e-4)//1, hand_hoyde, hand_bredde))
posisjoner["vest"].setdefault("gull", (0.2*KH-0.5*KB, (KB+EM+MM+2*LM+1e-4)//1, bunke_bredde, (1.5*bunke_hoyde+1e-4)//1))
posisjoner["vest"].setdefault("slag 1", ((0.7*KH+HTM+1e-4)//1, (EM+1e-4)//1, slag_hoyde, slag_bredde))
posisjoner["vest"].setdefault("slag 2", ((0.7*KH+HTM+1e-4)//1, (2*KH+KB+EM+MM+2*LM+1e-4)//1, slag_hoyde, slag_bredde))
posisjoner["vest"].setdefault("slag 3", ((0.7*KH+HTM+1e-4)//1, (4*KH+2*KB+EM+2*MM+4*LM+1e-4)//1, slag_hoyde, slag_bredde))    
posisjoner["vest"].setdefault("tekstboks", ((0.7*KH)//1, (2*KH+KB+EM+MM+2*LM+1e-4)//1, HTM, hand_bredde))    

posisjoner.setdefault("øst", {})
posisjoner["øst"].setdefault("hånd", ((12.7*KH+3*KB+2*HTM+2*SM+2*MM+10*LM+1e-4)//1, (2*KH+KB+EM+MM+2*LM+1e-4)//1, hand_hoyde, hand_bredde))
posisjoner["øst"].setdefault("gull", ((13.2*KH+2.5*KB+2*HTM+2*SM+2*MM+10*LM+1e-4)//1, (KB+EM+MM+2*LM+1e-4)//1, bunke_bredde, (1.5*bunke_hoyde+1e-4)//1))
posisjoner["øst"].setdefault("slag 1", ((9.7*KH+3*KB+HTM+2*SM+2*MM+8*LM+1e-4)//1, (4*KH+2*KB+EM+2*MM+4*LM+1e-4)//1, slag_hoyde, slag_bredde))
posisjoner["øst"].setdefault("slag 2", ((9.7*KH+3*KB+HTM+2*SM+2*MM+8*LM+1e-4)//1, (2*KH+KB+EM+MM+2*LM+1e-4)//1, slag_hoyde, slag_bredde))
posisjoner["øst"].setdefault("slag 3", ((9.7*KH+3*KB+HTM+2*SM+2*MM+8*LM+1e-4)//1, EM, slag_hoyde, slag_bredde))
posisjoner["øst"].setdefault("tekstboks", ((12.7*KH+3*KB+HTM+2*SM+2*MM+10*LM+1e-4)//1, (2*KH+KB+EM+MM+2*LM+1e-4)//1, HTM, hand_bredde))    

rotasjonspunkt = {}
rotasjonspunkt.setdefault("horisontal", {})
rotasjonspunkt["horisontal"].setdefault(0, (0,0))
rotasjonspunkt["horisontal"].setdefault(90, (5/4*KH+1/4*KB+LM, 7/4*KH-1/4*KB+LM))
rotasjonspunkt["horisontal"].setdefault(180, (KH+1/2*KB+LM, 3/2*KH+LM))
rotasjonspunkt["horisontal"].setdefault(270, (3/4*KH+3/4*KB+LM, 7/4*KH-1/4*KB+LM))
rotasjonspunkt.setdefault("vertikal", {})
rotasjonspunkt["vertikal"].setdefault(0, (0,0))
rotasjonspunkt["vertikal"].setdefault(90, (5/4*KH+1/4*KB+LM, 3/4*KH+3/4*KB+LM))
rotasjonspunkt["vertikal"].setdefault(180, (3/2*KH+LM, KH+1/2*KB+LM))
rotasjonspunkt["vertikal"].setdefault(270, (7/4*KH-1/4*KB+LM, 3/4*KH+3/4*KB+LM))

class Oppsett:

    @staticmethod
    def sett_plass_slag(slaghandterer):
        spiller = slaghandterer._forsvarer._spiller
        slag_id = slaghandterer._id

        pos_x,pos_y,dim_b,dim_h = posisjoner[spiller][f"slag {slag_id}"]

        slaghandterer.sett_pos((pos_x,pos_y))
        slaghandterer.sett_dim((dim_b,dim_h))

    @staticmethod
    def sett_plass_bunke(bunke,type):

        x,y,b,h = posisjoner[f"{type}bunke"]

        bunke.sett_pos((x,y))
        bunke.sett_dim((b,h))

    @staticmethod
    def sett_plass_deltakerhand(deltaker):
        spiller = deltaker._spiller
        hand = deltaker._hand

        x,y,b,h = posisjoner[spiller]["hånd"]

        hand.sett_pos((x,y))
        hand.sett_dim((b,h))

    @staticmethod
    def sett_plass_deltakergull(deltaker):
        gull = deltaker._gull
        spiller = deltaker._spiller
        
        x,y,b,h = posisjoner[spiller]["gull"]

        gull.sett_pos((x,y))
        gull.sett_dim((b,h))

    @staticmethod
    def sett_plass_deltakertekstboks(deltaker):
        spiller = deltaker._spiller
        
        x,y,b,h = posisjoner[spiller]["tekstboks"]

        deltaker.tekstboks_pos((x,y,b,h))

    @staticmethod
    def sett_pos_slaggull(slagh):

        x,y = slagh._posisjon
        b,h = slagh._dimensjon
        spkort = slagh._slag._gull
        forsvarer = slagh._forsvarer

        rotasjon = Oppsett.rotasjonsgrad(forsvarer._spiller)
        kb,kh = Oppsett.rotert_b_h(KB,KH,rotasjon)

        S_x,S_y = Oppsett.sentrum(x,y,b,h)

        x = S_x - kb/2
        y = S_y - kh/2

        spkort.sett_rotasjon(rotasjon)
        spkort.sett_gyldig_pos((x,y))

        if not spkort._animeres:
            spkort.sett_pos((x,y))

    @staticmethod
    def sett_pos_slagstyrke(slagh,spiller):

        x,y = slagh._posisjon
        _,h = slagh._dimensjon
        forsvarer = slagh._forsvarer._spiller
        slag = slagh._slag

        styrke = slag._styrker[spiller]
        styrkekort = styrke._kort

        if len(styrkekort) == 0:
            raise ValueError(f"Value 0 not valid.")

        maksbredde = KH+KB+LM
        kortdist = 20
        while True:
            bredde = KB + len(styrkekort)*kortdist
            if bredde<maksbredde:
                break

            if kortdist == 0:
                raise ValueError(f"Value 0 not valid.")
            kortdist -= 1

        rotasjon = Oppsett.rotasjonsgrad(spiller._spiller)

        if forsvarer in ["sør","nord"]:
            kortstilling = "horisontal"            
            sorstyrke_x = x+KH+LM
            sorstyrke_y = y+h-KH

        elif forsvarer in ["øst","vest"]:
            kortstilling = "vertikal"    
            sorstyrke_x = x+KH+LM+(KH-KB)/2
            sorstyrke_y = y+h-KH

        else:
            raise ValueError(f"Value {spiller} not valid.")

        rotp_x,rotp_y = rotasjonspunkt[kortstilling][rotasjon]
        rot_punkt = (x+rotp_x, y+rotp_y)

        for i,spillekort in enumerate(styrkekort):

            sorkort_x = sorstyrke_x + i*kortdist

            kort_x, kort_y = Oppsett.roter_objekt(sorkort_x,sorstyrke_y,KB,KH,rot_punkt,rotasjon,spillekort)
                       
            spillekort.sett_rotasjon(rotasjon)
            spillekort.sett_gyldig_pos((kort_x,kort_y))
            
            if not spillekort._animeres:
                spillekort.sett_pos((kort_x,kort_y))

    @staticmethod
    def sett_pos_trekkbunke(trekkbunke):
        x,y = trekkbunke._posisjon

        for i,spillekort in enumerate(trekkbunke._spkort):
            spillekort.sett_gyldig_pos((x-i//8,y))
            spillekort.sett_rotasjon(90)

            spillekort.sett_pos((x-i//8,y))
            

    @staticmethod
    def sett_pos_spillekort_kastebunke(kastebunke,spkort):
        x,y = kastebunke._posisjon

        antall = len(kastebunke)
        
        kort_x = x-(antall-1)//8

        spkort.sett_rotasjon(90)
        spkort.sett_gyldig_pos((kort_x,y))

        if not spkort._animeres:
            spkort.sett_pos((kort_x,y))

    @staticmethod
    def sett_pos_deltakerhand(deltaker):
        spiller = deltaker._spiller

        hand = deltaker._hand
        kort = hand._spkort

        if spiller in ["nord","øst"]:
            kort = list(reversed(kort))

        x,y = hand._posisjon
        
        rotasjon = Oppsett.rotasjonsgrad(spiller)
        b,h = Oppsett.rotert_b_h(*hand._dimensjon,rotasjon)

        maksbredde = b
        kortdist = 40
        while True:
            bredde = KB + (len(kort)-1)*kortdist
            if bredde<maksbredde:
                break

            if kortdist == 0:
                raise ValueError(f"Value 0 not valid.")
            kortdist -= 1

        if spiller in ["sør","nord"]:

            hand_x = x+(b-bredde)/2
            for i,spillekort in enumerate(kort):
                kort_x = hand_x + i*kortdist
                
                spillekort.sett_rotasjon(rotasjon)
                spillekort.sett_gyldig_pos((kort_x,y))

                if not spillekort._animeres:
                    spillekort.sett_pos((kort_x,y))

        elif spiller in ["øst","vest"]:

            hand_y = y+(b-bredde)/2
            for i,spillekort in enumerate(kort):

                kort_y = hand_y + i*kortdist
                
                spillekort.sett_rotasjon(rotasjon)
                spillekort.sett_gyldig_pos((x,kort_y))

                if not spillekort._animeres:
                    spillekort.sett_pos((x,kort_y))
        else:
            raise ValueError(f"Value {spiller} not valid.")
        
    @staticmethod
    def sett_pos_deltakergull(deltaker):
        spiller = deltaker._spiller

        gullbunke = deltaker._gull
        kort = gullbunke._spkort

        x,y = gullbunke._posisjon
        
        rotasjon = Oppsett.rotasjonsgrad(spiller)
        b,h = Oppsett.rotert_b_h(*gullbunke._dimensjon,rotasjon)

        maksbredde = b
        kortdist = 10
        while True:
            bredde = KB + (len(kort)-1)*kortdist
            if bredde<maksbredde:
                break

            if kortdist == 0:
                raise ValueError(f"Value 0 not valid.")
            kortdist -= 1

        if spiller in ["sør","nord"]:

            hand_x = x+(b-bredde)/2
            for i,spillekort in enumerate(kort):
                kort_x = hand_x + i*kortdist
                
                spillekort.sett_gyldig_pos((kort_x,y))
                spillekort.sett_rotasjon(270+rotasjon)

                if not spillekort._animeres:
                    spillekort.sett_pos((kort_x,y))

        elif spiller in ["øst","vest"]:

            hand_y = y+(b-bredde)/2
            for i,spillekort in enumerate(kort):

                kort_y = hand_y + i*kortdist
                
                spillekort.sett_gyldig_pos((x,kort_y))
                spillekort.sett_rotasjon(270+rotasjon)

                if not spillekort._animeres:
                    spillekort.sett_pos((x,kort_y))
        else:
            raise ValueError(f"Value {spiller} not valid.")

    @staticmethod
    def rotasjonsgrad(spiller):
        for rotasjon,plass in enumerate(["sør","vest","nord","øst"]):
            if spiller==plass:
                return 90*rotasjon
        raise ValueError(f"Value {spiller} not valid.")

    @staticmethod
    def rotasjonsdiff(spiller1,spiller2):
        for rotasjon,plass in enumerate(["sør","vest","nord","øst"]):
            if plass == spiller1:
                i1 = rotasjon
            elif plass == spiller2:
                i2 = rotasjon
        return ((i2-i1) % 4)*90

    @staticmethod
    def sentrum(x,y,b,h):
        return x+b/2, y + h/2

    @staticmethod
    def rotert_b_h(b,h,rotasjon):
        if rotasjon%360 in [0,180]:
            return b,h
        elif rotasjon%360 in [90,270]:
            return h,b
        else:
            raise ValueError(f"Value {rotasjon} not valid.")

    @staticmethod
    def roter_objekt(x,y,b,h,rot_punkt,grader,kort):

        rotpunkt_x,rotpunkt_y = rot_punkt
        v = math.radians(grader)

        senter_x, senter_y = Oppsett.sentrum(x,y,b,h)

        urot_x = senter_x - rotpunkt_x
        urot_y = senter_y - rotpunkt_y

        rotert_x = math.cos(v)*urot_x-math.sin(v)*urot_y
        rotert_y = math.sin(v)*urot_x+math.cos(v)*urot_y

        nytt_senter_x = rotert_x + rotpunkt_x
        nytt_senter_y = rotert_y + rotpunkt_y

        b,h = Oppsett.rotert_b_h(b,h,grader)

        hjorne_x = nytt_senter_x - b/2
        hjorne_y = nytt_senter_y - h/2

        return hjorne_x,hjorne_y