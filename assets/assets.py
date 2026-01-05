from PIL import Image, ImageDraw, ImageFont

BREDDE,HOYDE = 675,1050 # størrelse til standardiserte Bridgekort

MARG_HVIT = 10
MARG_KANT = 10
MARG_INDRE = 100
MIDTSKILLE = 80
MELLOMSKILLE = 15
NEDRE_INNRYKK = 80
TEKST_INNRYKK = 40
SYMBOL_STORRELSE = 50

FNT1 = ImageFont.truetype("seguihis.ttf", size=500)
FNT2 = ImageFont.truetype("seguihis.ttf", size=80)
FNT3 = ImageFont.truetype("calibri.ttf", size=80)
FNT4 = ImageFont.truetype("seguihis.ttf", size=90)

GJENNOMSIKTIG = (255,255,255,0)
SVART = (0,0,0)
HVIT = (255,255,255) # hex: "#FFFFFF"

GRA_GRONN = (128,165,120)
BLA = (11,181,255) # hex: "#0BB5FF"
LYSE_ORANSJE = (255,215,153)
ORANSJE = (255,215,0) # hex: #FFD700
ROD = (244,69,40) # hex: "#F44528"
GRONN = (4,252,132) # hex: #04fc84
MORKE_GRONN = (23,174,77) # hex: #17AE4D

def bytt_farge(img,farge,ny_farge):
    data = img.getdata()
    ny_data = []
    for el in data:
        if el[:3] == farge and el[3]!=0:
            ny_data.append((*ny_farge,el[3]))
            continue
        ny_data.append(el)
    img.putdata(ny_data)

def fargelegg_stridskort(img,farge,ny_farge1,ny_farge2): # hardkodet del
    data = img.getdata()
    ny_data = []
    x = 0
    y = 0
    for el in data:
        y = (y+1)%512
        if y==0:
            x += 1

        if el[:3] == farge and el[3]>0:
            if abs(256-x)<120 and abs(256-y)<120:
                ny_data.append((*ny_farge1,el[3]))
            else:
                ny_data.append((*ny_farge2,el[3]))
            continue
        ny_data.append(el)
    img.putdata(ny_data)
            
for verdier,kategori,farge in zip([["5"],["1","2","3","4"],["6","7","8","9"],["6","7","8","9"]],["vitalitet","forsterkning","angrep","forsvar"],[ORANSJE,BLA,ROD,GRONN]):
    
    for verdi in verdier:

        img = Image.new(mode="RGBA",size=(BREDDE,HOYDE),color=GJENNOMSIKTIG)
        tegn = ImageDraw.Draw(img)

        # tegner den avrundede kortbakgrunnen

        tegn.rounded_rectangle((0,0,BREDDE,HOYDE), fill=HVIT, radius=27) # hvit
        tegn.rounded_rectangle((MARG_HVIT,MARG_HVIT,BREDDE-MARG_HVIT,HOYDE-MARG_HVIT), fill=farge, radius=15) # bak.farge

        if kategori == "vitalitet":
            tegn.rounded_rectangle((MARG_KANT+MARG_HVIT,MARG_INDRE+MARG_HVIT,BREDDE-MARG_HVIT-MARG_KANT,HOYDE-MARG_INDRE-MARG_KANT), fill=HVIT, radius=5, outline=GRA_GRONN, width=40) # bak.farge

        # tegner tittel og enten kortverdi eller symbol foran

        
        if kategori != "vitalitet":
            _,_,b1,h1 = tegn.textbbox(xy=(0,0),text=kategori.capitalize(),font=FNT2,anchor="lt")
            _,_,b2,h2 = tegn.textbbox(xy=(0,0),text=verdi,font=FNT1,anchor="lt")
            tegn.text(((BREDDE-b1)//2, (HOYDE-h1-MIDTSKILLE-h2-NEDRE_INNRYKK)//2),text=kategori.capitalize(),font=FNT2,fill=HVIT,anchor="lt")
            tegn.text(((BREDDE-b2)//2, (HOYDE+h1+MIDTSKILLE-h2-NEDRE_INNRYKK)//2),text=verdi,font=FNT1,fill="white",anchor="lt")

        else:
            # tegner tittel og kortsymbol
            
            _,_,b1,h1 = tegn.textbbox(xy=(0,0),text=kategori.upper(),font=FNT4,anchor="lt")
            _,_,b2,h2 = tegn.textbbox(xy=(0,0),text=verdi,font=FNT1,anchor="lt")
            tegn.text(((BREDDE-b1)//2, (HOYDE-h1-h2-NEDRE_INNRYKK)//2),text=kategori.upper(),font=FNT4,fill=GRA_GRONN,anchor="lt")
            
            symbol_img = Image.open(f'Symbol_{kategori}.png').convert('RGBA') # henter symbol
            fargelegg_stridskort(symbol_img,SVART,ORANSJE,MORKE_GRONN)

            symbol_img = symbol_img.resize((h2,h2)) # eksperimentell verdi
            img.paste(symbol_img, ((BREDDE-h2)//2, (HOYDE+h1+2*MIDTSKILLE-h2-NEDRE_INNRYKK)//2), symbol_img)

        # tegner bokser nederst og øverst

        tegn.rounded_rectangle((MARG_HVIT+MARG_KANT,MARG_HVIT+MARG_KANT,BREDDE-MARG_HVIT-MARG_KANT,MARG_INDRE), fill = 'white', radius=5)
        tegn.rounded_rectangle((MARG_HVIT+MARG_KANT,HOYDE-MARG_INDRE, BREDDE-MARG_HVIT-MARG_KANT,HOYDE-MARG_HVIT-MARG_KANT), fill = 'white', radius=5)

        # tegner kortverdi øverst

        _,_,b,h = tegn.textbbox(xy=(0,0),text=verdi,font=FNT3,anchor="lt")
        
        bredde = TEKST_INNRYKK
        hoyde = MARG_HVIT+MARG_KANT+(MARG_INDRE-MARG_HVIT-MARG_KANT-h)//2
        
        tegn.text((bredde,hoyde),text=verdi,font=FNT3,fill=farge,anchor="lt")
        tegn.rectangle((bredde+1,hoyde+h+6,bredde+b-2,hoyde+h+8),fill=farge) # understrekning, eksperimentelle verdier

        # tegner symbol øverst

        if kategori == "vitalitet":
            symbol_img = Image.new(mode="RGBA",size=(SYMBOL_STORRELSE,SYMBOL_STORRELSE),color=GJENNOMSIKTIG)
        else:
            symbol_img = Image.open(f'Symbol_{kategori}.png').convert('RGBA') # henter symbol    
            bytt_farge(symbol_img,SVART,farge)
            symbol_img = symbol_img.resize((SYMBOL_STORRELSE,SYMBOL_STORRELSE))    

        hoyde = MARG_HVIT+MARG_KANT+(MARG_INDRE-MARG_KANT-SYMBOL_STORRELSE)//2
        img.paste(symbol_img, (bredde+b+MELLOMSKILLE,hoyde), symbol_img)

        # tegner kortverdi og symbol oppned nederst

        img_hoyde = max(h,SYMBOL_STORRELSE)
        oppned_img=Image.new('RGBA', (b+MELLOMSKILLE+SYMBOL_STORRELSE,img_hoyde), color="white")
        d = ImageDraw.Draw(oppned_img)

        d.text((0,(img_hoyde-h)//2),text=verdi,font=FNT3,fill=farge,anchor="lt")
        oppned_img.paste(symbol_img, (b+MELLOMSKILLE,(img_hoyde-SYMBOL_STORRELSE)//2), symbol_img)
        
        w = oppned_img.rotate(180)

        hoyde = HOYDE-MARG_INDRE+(MARG_INDRE-MARG_KANT-MARG_HVIT-h)//2
        bredde = BREDDE-TEKST_INNRYKK-b
        img.paste(w, (bredde-MELLOMSKILLE-SYMBOL_STORRELSE,hoyde))
        tegn.rectangle((bredde+1,hoyde-6,bredde+b-2,hoyde-8),fill=farge) # understrekning, eksperimentelle verdier

        img.save(f"{kategori}_{verdi}.png")