#!/usr/bin/env python3
"""Generate homestead pixel art sprites — EarthBound/Pokemon GBA/Terraria style."""
from PIL import Image, ImageDraw
import os

OUT = r"C:\Users\00jgv\varvarley.com\assets"
S = 4  # scale: pixels per grid cell

# ---------------------------------------------------------------------------
# PALETTE
# ---------------------------------------------------------------------------
OL  = (20,  10,  28,  255)   # universal dark outline

# Purples — Varber Shop
P1  = (52,  18,  76,  255)
P2  = (96,  46, 136,  255)
P3  = (150, 88, 196,  255)
P4  = (198,146, 232,  255)
PRD = (198, 44,  58,  255)   # barber red
PWH = (238,234, 242,  255)   # barber white
PWD = (82,  42,  14,  255)   # wood chimney
PWG = (242,192,  62,  255)   # window glow

# Blues — Univarsity
B1  = (16,  20,  58,  255)
B2  = (36,  52, 112,  255)
B3  = (66,  98, 172,  255)
B4  = (108,148, 212,  255)
BCK = (182,172, 140,  255)   # clock face cream
BWG = (238,208,  76,  255)   # warm lit window
BST = (108, 98,  88,  255)   # stone

# Greens — Varden greenhouse
VG1 = (12,  46,   8,  255)
VG2 = (28,  88,  16,  255)
VG3 = (52, 140,  32,  255)
VG4 = (88, 192,  52,  255)
VGS = (160,230, 160,  255)   # glass shimmer
VGF = (195,168,  85,  255)   # wood frame

# Greens + glass — Dealership
DK1 = (14,  46,  14,  255)
DK2 = (32,  86,  32,  255)
DK3 = (58, 138,  58,  255)
DGW = (178,234, 178,  255)   # showroom glass
DC1 = (178, 48,  48,  255)   # car 1 red
DC2 = (48,  88, 188,  255)   # car 2 blue

# Blues — Varchitect glass tower
AR1 = (14,  20,  36,  255)
AR2 = (28,  56,  98,  255)
AR3 = (52, 108, 168,  255)
AR4 = (116,182, 232,  255)   # glass highlight
ARC = (215,215, 210,  255)   # concrete

# Tans — Varcheologist
TC1 = (126, 88,  32,  255)
TC2 = (182,138,  62,  255)
TC3 = (228,188, 112,  255)
TC4 = (248,228, 172,  255)
TCE = (96,  68,  24,  255)   # earth border
TCS = (68,  48,  18,  255)   # stakes

# Environment
TRK = (78,  46,  16,  255)   # tree trunk
PDG = (20,  70,  12,  255)   # pine dark
PMG = (40, 120,  22,  255)   # pine mid
PLG = (70, 172,  38,  255)   # pine light
PTG = (96, 208,  52,  255)   # pine tip

LYD = (180,120,  18,  255)   # lantern dark
LYM = (222,162,  34,  255)   # lantern mid
LYL = (250,222,  90,  255)   # lantern bright
LPL = (92,  82,  72,  255)   # pole
LPB = (62,  54,  46,  255)   # pole base

SNW = (242,250, 255,  255)   # snow
SBL = (172,204, 228,  255)   # snow shadow

GD1 = (20,  62,  12,  255)   # grass dark
GD2 = (36, 106,  22,  255)   # grass mid
GD3 = (56, 148,  34,  255)   # grass light

PE1 = (78,  52,  20,  255)   # path dark
PE2 = (122, 86,  40,  255)   # path mid
PE3 = (168,126,  64,  255)   # path light
PST = (102, 88,  75,  255)   # path stone

# ---------------------------------------------------------------------------
# UTILS
# ---------------------------------------------------------------------------
def new(w, h):
    return Image.new('RGBA', (w*S, h*S), (0,0,0,0))

def px(img, x, y, c):
    W = img.width // S
    H = img.height // S
    if 0 <= x < W and 0 <= y < H and c and len(c)==4 and c[3]>0:
        ImageDraw.Draw(img).rectangle([x*S,y*S,(x+1)*S-1,(y+1)*S-1], fill=c)

def rct(img, x0,y0,x1,y1, c):
    for x in range(x0,x1+1):
        for y in range(y0,y1+1):
            px(img,x,y,c)

def border(img, x0,y0,x1,y1, bc, fc=None):
    if fc:
        rct(img,x0+1,y0+1,x1-1,y1-1,fc)
    for x in range(x0,x1+1):
        px(img,x,y0,bc); px(img,x,y1,bc)
    for y in range(y0,y1+1):
        px(img,x0,y,bc); px(img,x1,y,bc)

def hline(img,y,x0,x1,c):
    for x in range(x0,x1+1): px(img,x,y,c)

def vline(img,x,y0,y1,c):
    for y in range(y0,y1+1): px(img,x,y,c)

def save(img, name):
    p = os.path.join(OUT, name)
    img.save(p)
    print(f"  {name}  ({img.width}×{img.height})")

# ---------------------------------------------------------------------------
# PINE TREE  8×14
# ---------------------------------------------------------------------------
def make_pine():
    img = new(8,14)
    # tip (layer 1)
    px(img,3,0,PTG); px(img,4,0,PTG)
    px(img,2,1,PLG); px(img,3,1,PTG); px(img,4,1,PLG); px(img,5,1,PLG)
    hline(img,2,2,5,PMG)
    px(img,1,2,OL);  px(img,6,2,OL)
    # middle layer
    px(img,1,3,OL);  hline(img,3,2,5,PLG); px(img,6,3,OL)
    px(img,1,4,PDG); hline(img,4,2,5,PLG); px(img,6,4,PDG)
    px(img,0,5,OL);  px(img,1,5,PDG); hline(img,5,2,5,PMG); px(img,6,5,PDG); px(img,7,5,OL)
    # bottom layer
    px(img,0,6,OL);  px(img,1,6,PDG); hline(img,6,2,5,PLG); px(img,6,6,PDG); px(img,7,6,OL)
    px(img,0,7,PDG); hline(img,7,1,6,PLG); px(img,7,7,PDG)
    px(img,0,8,PDG); hline(img,8,1,6,PMG); px(img,7,8,PDG)
    px(img,0,9,OL);  hline(img,9,1,6,PDG); px(img,7,9,OL)
    # trunk
    rct(img,3,10,4,13,TRK)
    px(img,3,10,OL); px(img,4,10,OL)
    px(img,3,13,OL); px(img,4,13,OL)
    return img

# ---------------------------------------------------------------------------
# LANTERN POST  5×12
# ---------------------------------------------------------------------------
def make_lantern():
    img = new(5,12)
    # glow halo
    px(img,1,0,LYL); px(img,2,0,LYL); px(img,3,0,LYL)
    # lantern box
    border(img,1,1,3,4,OL,LYD)
    px(img,2,2,LYL); px(img,2,3,LYL)   # bright interior
    # pole
    vline(img,2,5,10,LPL)
    px(img,2,5,OL); px(img,2,11,OL)
    # base
    rct(img,1,10,3,11,LPB)
    border(img,1,10,3,11,OL)
    return img

# ---------------------------------------------------------------------------
# SNOW PATCH  14×5
# ---------------------------------------------------------------------------
def make_snow():
    img = new(14,5)
    # top bumps
    for x in [1,3,5,7,9,11]: px(img,x,0,SNW)
    for x in [2,4,6,8,10]:   px(img,x,0,SNW)
    hline(img,1,0,13,SNW)
    hline(img,2,0,13,SNW)
    hline(img,3,1,12,SBL)
    hline(img,4,2,11,SBL)
    return img

# ---------------------------------------------------------------------------
# VARBER SHOP  20×26
# ---------------------------------------------------------------------------
def make_varber():
    img = new(20,26)
    # chimney (x=5-7, y=0-2)
    border(img,5,0,7,2,OL,PWD)
    # gabled roof: peak y=3 at x=9-10, spreads 1px per row
    for dy in range(8):
        y = 3+dy
        x0 = 9-dy; x1 = 10+dy
        if x0 < 0: x0=0
        if x1 > 19: x1=19
        shade = P4 if dy<2 else (P3 if dy<5 else P2)
        hline(img,y,x0,x1,shade)
        px(img,x0,y,OL); px(img,x1,y,OL)
    hline(img,11,0,19,OL)  # eave line
    # body
    rct(img,0,12,19,25,P1)
    rct(img,1,12,18,24,P2)
    border(img,0,12,19,25,OL)
    # left window
    border(img,2,13,6,17,OL,PWG)
    hline(img,15,2,6,OL); vline(img,4,13,17,OL)
    # right window
    border(img,13,13,17,17,OL,PWG)
    hline(img,15,13,17,OL); vline(img,15,13,17,OL)
    # door (arched)
    rct(img,8,18,11,25,OL)
    rct(img,9,19,10,24,P1)
    px(img,8,18,P3); px(img,11,18,P3)  # arch shoulders
    # barber pole (right of body, x=18-19 — actually use x=18)
    for y in range(12,25):
        stripe = (y % 3)
        c = PRD if stripe==0 else (PWH if stripe==1 else P3)
        px(img,18,y,c)
    vline(img,18,12,25,OL) # side outline covers pole
    # sign band
    rct(img,2,12,17,12,P4)
    return img

# ---------------------------------------------------------------------------
# THE UNIVARSITY  22×30
# ---------------------------------------------------------------------------
def make_univarsity():
    img = new(22,30)
    # tower (x=8-13, y=0-9)
    border(img,8,0,13,9,OL,B1)
    rct(img,9,1,12,8,B2)
    # battlements
    px(img,8,0,B2);px(img,10,0,B2);px(img,12,0,B2)
    # clock face
    border(img,9,2,12,6,B4,BCK)
    # clock hands
    px(img,10,3,OL); px(img,11,4,OL); px(img,10,4,OL)
    # tower window below clock
    border(img,10,7,11,8,OL,BWG)
    # main roof (gabled, spans full width)
    for dy in range(6):
        y = 10+dy
        x0 = 8-dy; x1 = 13+dy
        if x0<0: x0=0
        if x1>21: x1=21
        shade = B4 if dy<2 else (B3 if dy<4 else B2)
        hline(img,y,x0,x1,shade)
        px(img,x0,y,OL); px(img,x1,y,OL)
    hline(img,16,0,21,OL)
    # body
    rct(img,0,17,21,29,B1)
    rct(img,1,17,20,28,B2)
    border(img,0,17,21,29,OL)
    # left arched window
    border(img,2,18,6,23,OL,BWG)
    hline(img,21,2,6,OL); vline(img,4,18,23,OL)
    px(img,2,18,B3);px(img,6,18,B3)  # arch
    # right arched window
    border(img,15,18,19,23,OL,BWG)
    hline(img,21,15,19,OL); vline(img,17,18,23,OL)
    px(img,15,18,B3);px(img,19,18,B3)
    # door
    border(img,9,22,12,29,OL,B1)
    px(img,9,22,B3);px(img,12,22,B3)
    # stone texture (scattered dots)
    for x,y in [(3,28),(7,26),(14,25),(18,27)]:
        px(img,x,y,BST)
    return img

# ---------------------------------------------------------------------------
# THE VARDEN  20×24  (greenhouse)
# ---------------------------------------------------------------------------
def make_varden():
    img = new(20,24)
    # A-frame glass roof
    for dy in range(8):
        y = 0+dy
        x0 = 9-dy; x1 = 10+dy
        if x0<0: x0=0
        if x1>19: x1=19
        # alternate glass panels
        for x in range(x0+1,x1):
            c = VGS if (x+y)%3==0 else VG2
            px(img,x,y,c)
        px(img,x0,y,OL); px(img,x1,y,OL)
    hline(img,8,0,19,OL)
    # body (wood frame + glass walls)
    border(img,0,9,19,23,OL,VG1)
    rct(img,1,9,18,22,VG1)
    # glass windows (large greenhouse panes)
    border(img,1,9,9,19,VGF,VGS)
    border(img,10,9,18,19,VGF,VGS)
    # plants visible through glass
    for x,y in [(3,12),(3,15),(5,11),(7,14),(12,13),(14,11),(16,15)]:
        px(img,x,y,VG4)
        px(img,x,y-1,VG3)
    # door
    border(img,8,19,11,23,OL,VGF)
    px(img,8,19,VG3);px(img,11,19,VG3)
    # frame wood trim
    hline(img,9,0,19,VGF)
    hline(img,23,0,19,VGF)
    return img

# ---------------------------------------------------------------------------
# VAR DEALERSHIP  22×22
# ---------------------------------------------------------------------------
def make_dealership():
    img = new(22,22)
    # flat roof with sign band
    rct(img,0,0,21,4,DK1)
    border(img,0,0,21,4,OL)
    rct(img,1,1,20,3,DK3)
    # sign lettering dots (pixel "CAR" suggestion)
    for x in [3,5,7,9,11,13,15,17]: px(img,x,2,DK1)
    # main body
    rct(img,0,5,21,21,DK1)
    border(img,0,5,21,21,OL)
    # big showroom window (left 2/3)
    border(img,1,6,14,15,OL,DGW)
    # window pane dividers
    vline(img,5,6,15,OL); vline(img,9,6,15,OL)
    # car 1 (red, left bay x=2-4, y=9-13)
    rct(img,2,10,4,13,DC1)
    border(img,2,10,4,13,OL)
    px(img,2,12,OL);px(img,4,12,OL)  # wheels
    rct(img,2,9,4,10,DC1)
    # car 2 (blue, mid bay x=6-8)
    rct(img,6,10,8,13,DC2)
    border(img,6,10,8,13,OL)
    px(img,6,12,OL);px(img,8,12,OL)
    rct(img,6,9,8,10,DC2)
    # office window (right)
    border(img,16,6,20,11,OL,DGW)
    hline(img,8,16,20,OL)
    # door
    border(img,16,15,19,21,OL,DK2)
    px(img,16,15,DK3);px(img,19,15,DK3)
    # forecourt dividers
    vline(img,15,5,21,OL)
    # lot stripes on forecourt (decorative)
    for y in [17,19]: hline(img,y,1,14,DK2)
    return img

# ---------------------------------------------------------------------------
# VARCHITECT  18×28  (glass tower)
# ---------------------------------------------------------------------------
def make_varchitect():
    img = new(18,28)
    # antenna/spire
    vline(img,8,0,3,OL); vline(img,9,0,3,OL)
    px(img,8,0,AR4); px(img,9,0,AR4)
    # roof (flat, geometric)
    rct(img,2,4,15,6,AR1)
    border(img,2,4,15,6,OL)
    rct(img,3,5,14,5,AR3)
    # main tower body
    border(img,2,7,15,27,OL,AR1)
    rct(img,3,8,14,26,AR2)
    # glass window grid (3 cols × 5 rows)
    for col in range(3):
        x0 = 3 + col*4
        for row in range(5):
            y0 = 9 + row*3
            border(img,x0,y0,x0+2,y0+1,OL,AR4)
            # reflection highlight
            px(img,x0+1,y0,ARC)
    # entrance (ground floor)
    border(img,5,23,12,27,OL,AR3)
    rct(img,6,24,11,26,AR4)
    hline(img,24,5,12,OL)
    # corner accent lines
    vline(img,2,7,27,AR3)
    vline(img,15,7,27,AR3)
    return img

# ---------------------------------------------------------------------------
# VARCHEOLOGIST  22×20  (tent + dig)
# ---------------------------------------------------------------------------
def make_varcheologist():
    img = new(22,20)
    # tent: A-frame (left half of image, x=0-12)
    for dy in range(7):
        y = 0+dy
        x0 = 6-dy; x1 = 6+dy+1
        if x0<0: x0=0
        shade = TC4 if dy<2 else (TC3 if dy<5 else TC2)
        hline(img,y,x0,x1,shade)
        px(img,x0,y,OL); px(img,x1,y,OL)
    # tent base (sides)
    hline(img,7,0,13,OL)
    rct(img,0,8,13,14,TC2)
    border(img,0,8,13,14,OL)
    # tent opening (dark door)
    border(img,4,8,9,14,OL,TC1)
    # tent rope stakes
    px(img,0,7,TCS); px(img,13,7,TCS)
    px(img,0,8,TCS); px(img,13,8,TCS)
    # dig site (right half, x=14-21)
    rct(img,14,5,21,14,TCE)   # pit edge / soil border
    border(img,14,5,21,14,OL)
    rct(img,15,6,20,13,TC1)   # pit interior dark
    # rope/grid lines in pit
    hline(img,9,15,20,TCE); vline(img,17,6,13,TCE)
    # artifacts in pit
    px(img,15,8,TC4); px(img,19,11,TC4)
    # stakes with rope at corners
    for sx in [14,21]:
        for sy in [5,14]:
            px(img,sx,sy,TCS)
    # ground labels
    hline(img,15,0,21,OL)
    rct(img,0,15,21,19,TC3)
    border(img,0,15,21,19,OL)
    # dirt texture on ground
    for x,y in [(2,16),(5,17),(8,16),(11,18),(15,16),(18,17)]:
        px(img,x,y,TC1)
    return img

# ---------------------------------------------------------------------------
# GRASS TILE  16×16
# ---------------------------------------------------------------------------
def make_grass():
    img = new(16,16)
    rct(img,0,0,15,15,GD2)
    # scattered lighter/darker patches
    for x,y in [(1,1),(4,3),(7,1),(10,4),(13,2),(2,7),(6,9),(9,6),(14,8),(3,12),(11,13),(8,14)]:
        px(img,x,y,GD3)
    for x,y in [(0,5),(3,8),(7,11),(12,6),(15,3),(5,14),(14,12)]:
        px(img,x,y,GD1)
    return img

# ---------------------------------------------------------------------------
# DIRT PATH TILE  16×16
# ---------------------------------------------------------------------------
def make_path():
    img = new(16,16)
    rct(img,0,0,15,15,PE2)
    # cobblestone pattern
    stones = [
        (0,0,3,3), (4,0,7,3), (8,0,11,3), (12,0,15,3),
        (0,4,3,7), (4,4,7,7), (8,4,11,7), (12,4,15,7),
        (0,8,3,11),(4,8,7,11),(8,8,11,11),(12,8,15,11),
        (0,12,3,15),(4,12,7,15),(8,12,11,15),(12,12,15,15),
    ]
    for (x0,y0,x1,y1) in stones:
        rct(img,x0+1,y0+1,x1-1,y1-1,PE3)
        border(img,x0,y0,x1,y1,PE1)
    return img

# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------
print("Generating homestead sprites...")
sprites = {
    "hs-pine.png":          make_pine(),
    "hs-lantern.png":       make_lantern(),
    "hs-snow.png":          make_snow(),
    "hs-varber.png":        make_varber(),
    "hs-univarsity.png":    make_univarsity(),
    "hs-varden.png":        make_varden(),
    "hs-dealership.png":    make_dealership(),
    "hs-varchitect.png":    make_varchitect(),
    "hs-varcheologist.png": make_varcheologist(),
    "hs-grass.png":         make_grass(),
    "hs-path.png":          make_path(),
}
for name, img in sprites.items():
    save(img, name)
print("Done.")
