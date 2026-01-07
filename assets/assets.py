from PIL import Image, ImageDraw, ImageFont

DIR = "assets"
UT = "kort"

BREDDE,HOYDE = 74,112

MØRKEBLÅ = (63, 72, 204) 
BLA = (11,181,255) # hex: "#0BB5FF"
ORANSJE = (255,215,0) # hex: #FFD700
ROD = (244,69,40) # hex: "#F44528"
GRONN = (4,252,132) # hex: #04fc84

bakfarger = {"angrep": ROD, "forsvar": GRONN, "forsterkning": BLA, "gull": ORANSJE}

FNT1 = ImageFont.truetype("seguihis.ttf", size=500)
FNT2 = ImageFont.truetype("seguihis.ttf", size=250)
FNT3 = ImageFont.truetype("seguihis.ttf", size=80)
FNT4 = ImageFont.truetype("calibri.ttf", size=80)
FNT5 = ImageFont.truetype("seguihis.ttf", size=90)


oppskala = 4
nedskala = 1
def x4(x):
    return oppskala*x

def d4(x):
    return round(x*nedskala/oppskala)

def crop(img):
    return img.crop(img.split()[3].getbbox())

def fargelegg(image, rgb):
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a != 0:  # If not transparent
                pixels[x, y] = (*rgb, a)  # Preserve original alpha
    return image

def lag_tekst(tekst, font, farge):
    img = Image.new("RGBA", (1000, 1000))

    tdraw = ImageDraw.Draw(img)
    tdraw.text((20, 20), tekst, font=font, fill=farge)
    return crop(img)

def symbol_angrep():
    kort = Image.new("RGBA", (1000,1000))

    t = lag_tekst("/", FNT1, "white")
    kort.alpha_composite(t.transpose(Image.FLIP_LEFT_RIGHT).rotate(10, expand=True) )
    kort.alpha_composite(t.rotate(-10, expand=True), (40,0))

    cropped = crop(kort.crop((0, 100, 1000, 330)))
    return cropped

def symbol_forsvar():
    kort = Image.new("RGBA", (1000,1000))

    t = lag_tekst("∕", FNT1, "white")
    
    cropped = t.crop((0, 185, 1000, 1000))
    
    kort.paste(t)
    kort.paste(cropped, (0, 100))
    kort = crop(kort)

    y_trim = 12
    kort = crop(kort).crop((0,y_trim,kort.width,kort.height-y_trim))
    return kort

def symbol_forsterkning():
    kort = Image.new("RGBA", (1000,1000))

    t = lag_tekst("+", FNT1, "white")
    kort.alpha_composite(t)
    kort = crop(kort)

    return kort

SYMBOL = {
    "angrep": symbol_angrep(),
    "forsvar": symbol_forsvar(),
    "forsterkning": symbol_forsterkning()
}

def rund_hjørner(img, r):
    pixels = img.load()
    for y in range(r):
        for x in range(r):
            dist = round(((r-(y+1))**2+(r-(x+1))**2)**(1/2), 1)
            if dist > r:
                pixels[x, y] = (0,0,0,0)
                pixels[x4(BREDDE)-1-x, y] = (0,0,0,0)
                pixels[x4(BREDDE)-1-x, x4(HOYDE)-1-y] = (0,0,0,0)
                pixels[x, x4(HOYDE)-1-y] = (0,0,0,0)

def illustrer_kort(korttype, verdi):
    kort = Image.new("RGBA", (x4(BREDDE), x4(HOYDE)), bakfarger[korttype])

    if korttype != "gull":
        # midtre ikon
        ikon = SYMBOL[korttype]

        b = 30
        ikon = ikon.resize((x4(b), round(x4(b*ikon.height/ikon.width))))
        ikon.save("abc.png")
        kort.alpha_composite(ikon, ((kort.width-ikon.width)//2, (kort.height-ikon.width)//2))

        # hvite tekstfelter

        margin = 1
        høyde = 20
        r = 4

        draw = ImageDraw.Draw(kort)
        draw.rounded_rectangle(
            [(x4(margin), x4(margin)), (kort.width-x4(margin)-1, x4(margin+høyde)-1)],
            radius=x4(r),
            fill=(255, 255, 255),
        )
        draw.rounded_rectangle(
            [(x4(margin), kort.height-x4(høyde+margin)-1), (kort.width-x4(margin)-1, kort.height-x4(margin)-1)],
            radius=x4(r),
            fill=(255, 255, 255),
        )

        x_padding = 4
        tekststr = 22
        
        font = ImageFont.truetype("seguihis.ttf", size=x4(tekststr))

        verditekst = fargelegg(lag_tekst(verdi, font, bakfarger[korttype]), bakfarger[korttype])
        
        kort.alpha_composite(verditekst, (x4(margin+x_padding), x4(margin)+(x4(høyde)-verditekst.height)//2))
        kort.alpha_composite(verditekst.rotate(180, expand=True), (kort.width-x4(margin+x_padding)-verditekst.width, kort.height-x4(margin)-verditekst.height-(x4(høyde)-verditekst.height)//2))
        
        mellomrom = 6
        ikon_b = 10

        ikon = fargelegg(SYMBOL[korttype].copy(), bakfarger[korttype])
        ikon = ikon.resize((x4(ikon_b), round(x4(ikon_b*ikon.height/ikon.width))))
        
        kort.alpha_composite(ikon, (x4(margin+x_padding)+verditekst.width+x4(mellomrom), x4(margin)+(x4(høyde)-ikon.height)//2))
        kort.alpha_composite(ikon.rotate(180, expand=True), (kort.width-x4(margin+x_padding)-verditekst.width-x4(mellomrom)-ikon.width, kort.height-x4(margin)-ikon.height-(x4(høyde)-ikon.height)//2))

    # kutt hjørner
    r = 6
    rund_hjørner(kort, x4(r))

    # lagre
    kort = kort.resize((d4(kort.width), d4(kort.height)))

    if verdi == "":
        filnavn = f"{korttype}"
    else:
        filnavn = f"{korttype}_{verdi}"

    print(f" + {UT}/{filnavn}.png")
    kort.save(f"{UT}/{filnavn}.png")


def illustrer_bakside():
    kort = Image.new("RGBA", (x4(BREDDE), x4(HOYDE)), MØRKEBLÅ)

    tekststr = 80
    font = ImageFont.truetype("seguihis.ttf", size=x4(tekststr))
    t = lag_tekst("?", font, "white")

    kort.alpha_composite(t, ((kort.width-t.width)//2, (kort.height-t.height)//2))

    # rund hjørner og lagre
    r = 6
    rund_hjørner(kort, x4(r))
    
    kort = kort.resize((d4(kort.width), d4(kort.height)))

    print(f" + {UT}/bakside.png")
    kort.save(f"{UT}/bakside.png")

for korttype,verdier in zip(["forsvar", "angrep", "forsterkning"], [[8,7,6,5], [8,7,6,5], [4,3,2,1]]):
    for verdi in verdier:
        illustrer_kort(korttype, str(verdi))

illustrer_kort("gull", "")
illustrer_bakside()