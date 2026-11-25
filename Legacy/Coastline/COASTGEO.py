# Coastline geography in east/north world units. Streets, atlas and collisions
# read the same footprints. Block fields: x,z, half width/depth, height,
# facade family, palette index, venue ID (-1 for a landmark or ordinary block).
GLASS, BALCONY, DECO, DEPOT, COTTAGE, SILO, CABANA = range(7)
VENUE_STYLE=((DECO,0),(GLASS,1),(GLASS,2),(COTTAGE,1),
             (DEPOT,0),(DECO,1),(DECO,2),(DECO,3),
             (DEPOT,1),(DECO,0),(COTTAGE,2),(DECO,1),
             (COTTAGE,3),(DEPOT,2),(COTTAGE,0),(COTTAGE,1))
# Heights at venues allow their lit entrance signs to stay at eye level.
VENUE_HEIGHT=(5,9,13,4,5,7,6,5,5,8,4,7,5,5,3,4)
# Packed rows keep all architecture in a few hundred bytes on the handheld.
# Coordinates are offset by ten; half-width and half-depth are in quarter units.
CITY_LOTS = (
    bytes((
        4, 62, 11, 16, 15, 1, 2,  # Tideglass Avenue
        18, 61, 12, 14, 17, 0, 2,
        28, 65, 13, 14, 24, 0, 0,
        35, 57, 12, 16, 19, 1, 1,
        51, 60, 16, 20, 29, 0, 1,
        57, 68, 12, 12, 18, 1, 0,
        36, 82, 10, 14, 22, 0, 3,
        29, 79, 10, 11, 12, 1, 2,
    )) +
    bytes((
        67, 63, 13, 16, 20, 0, 0,
        57, 49, 8, 12, 12, 1, 3,
        35, 33, 12, 12, 14, 1, 0,
        51, 32, 16, 12, 18, 0, 3,
        18, 28, 12, 20, 7, 1, 3,
        27, 50, 14, 13, 11, 2, 2,
        5, 83, 10, 14, 9, 2, 1,
        67, 80, 11, 12, 10, 2, 3,
    )) +
    bytes((
        82, 64, 14, 14, 10, 2, 0,  # Coral Strand
        92, 62, 16, 12, 8, 2, 1,
        98, 54, 11, 14, 12, 1, 2,
        90, 51, 12, 12, 7, 2, 2,
        100, 32, 9, 12, 7, 2, 3,
        114, 31, 14, 13, 5, 2, 0,
        93, 18, 14, 14, 7, 2, 1,
        114, 5, 10, 9, 3, 6, 1,
    )) +
    bytes((
        99, 83, 9, 8, 3, 6, 0,
        128, 82, 11, 10, 3, 6, 2,
        19, 36, 12, 10, 4, 3, 0,  # Iron Harbor
        27, 33, 12, 12, 6, 3, 2,
        26, 20, 16, 12, 6, 3, 1,
        16, 4, 10, 9, 7, 5, 0,
        34, 18, 11, 12, 5, 3, 3,
        46, 4, 10, 8, 4, 3, 1,
    )) +
    bytes((
        126, 33, 17, 13, 5, 3, 3,
        148, 30, 8, 12, 8, 5, 1,
        125, 51, 17, 12, 5, 3, 1,
        145, 56, 8, 7, 6, 3, 0,
        67, 22, 13, 12, 4, 4, 0,  # Cane Lake and Pine Heights
        80, 25, 10, 9, 5, 5, 2,
        88, 30, 12, 11, 4, 4, 1,
        149, 6, 8, 9, 3, 6, 2,
    )) +
    bytes((
        131, 14, 8, 8, 3, 4, 2,
        129, 66, 10, 11, 4, 4, 3,
        145, 64, 10, 10, 4, 4, 1,
        163, 48, 9, 9, 3, 4, 0,
    ))
)
# Cuts through the mainland and island neck, connected to open water.
CHANNELS=((50,-10,5,54),(55,39,6,5),(107,-10,5,25),
          (112,11,11,4),(12,71,5,7),(142,24,10,20))
LAUNCH=((96,82),(128,82),(128,-14),(176,32))
BRIDGES=((50,-3.6,5,7.2),(50,28.4,5,7.2),
         (107,-3.6,5,7.2),(142,28.4,10,7.2))
# Ground patches go under the water and road layers. Color index matches atlas.
PATCHES=((-10,42,77,36,0),(-10,-10,60,35,1),(66,-10,43,85,2),
         (80,67,35,11,3),(97,-10,45,28,4),(112,47,30,31,5),
         (111,18,31,28,1),(152,24,19,20,3),(56,-10,29,32,6))
# World props. Type 0 royal palm, 1 mangrove, 2 pine, 3 crane, 4 beach parasol,
# 5 streetlamp, 6 pier shelter, 7 water tower, 8 cypress knees, 9 bridge portal.
FURNITURE = (
    bytes((
        13, 65, 5,
        13, 55, 5,
        39, 55, 5,
        45, 68, 5,
        45, 58, 5,
        70, 68, 5,
        72, 36, 5,
        84, 45, 0,
    )) +
    bytes((
        89, 45, 0,
        96, 45, 0,
        102, 45, 0,
        109, 45, 0,
        94, 77, 0,
        100, 79, 0,
        108, 79, 0,
        115, 79, 0,
    )) +
    bytes((
        121, 78, 0,
        97, 86, 4,
        104, 85, 4,
        111, 86, 4,
        118, 85, 4,
        125, 86, 4,
        107, 87, 6,
        154, 42, 9,
    )) +
    bytes((
        160, 42, 9,
        21, 44, 3,
        130, 45, 3,
        143, 38, 3,
        149, 46, 3,
        66, 28, 7,
        85, 27, 0,
        122, 16, 1,
    )) +
    bytes((
        124, 19, 8,
        127, 23, 1,
        132, 25, 1,
        135, 21, 1,
        140, 26, 8,
        146, 23, 1,
        150, 17, 1,
        123, 6, 8,
    )) +
    bytes((
        133, 4, 1,
        126, 63, 2,
        131, 70, 2,
        142, 69, 2,
        148, 61, 2,
        145, 81, 2,
        149, 84, 2,
    ))
)
HIGHLIGHTS=("WAVE radio house","Tideglass Avenue","Beacon spire","Coral Strand",
 "Brickworks crane","Neon hotel row","Arcade marquee","Palm promenade",
 "Grain elevators","Velvet marquee","Cane water tower","Lido cabanas",
 "Pine lookout","Freight gantries","Cypress backwater","Twin-span causeway")

class CityBlocks:
    def __init__(self,centers):
        data=bytearray()
        for n,(x,z) in enumerate(centers):
            family,tint=VENUE_STYLE[n]
            data.extend(bytes((x+18,z+18,15,12,VENUE_HEIGHT[n],family,tint)))
        data.extend(CITY_LOTS)
        self.data=data

    def __len__(self):
        return len(self.data)//7

    def __getitem__(self,i):
        if i<0 or i>=len(self):raise IndexError
        j=i*7
        q=self.data
        return (q[j]-10,q[j+1]-10+(.9 if i<16 else 0),
                q[j+2]*.25,q[j+3]*.25,q[j+4],q[j+5],q[j+6],i if i<16 else -1)

    def __iter__(self):
        for i in range(len(self)):yield self[i]

    def intersects(self,x,z,r):
        q=self.data
        x+=10
        z+=10
        for j in range(0,len(q),7):
            if abs(x-q[j])<q[j+2]*.25+r:
                cz=q[j+1]+(.9 if j<112 else 0)
                if abs(z-cz)<q[j+3]*.25+r:return True
        return False

def furniture():
    for j in range(0,len(FURNITURE),3):
        yield FURNITURE[j]-10,FURNITURE[j+1]-10,FURNITURE[j+2]

def inside(x,z,rect,margin=0):
    a,b,w,d=rect
    return a-margin<=x<=a+w+margin and b-margin<=z<=b+d+margin

def water(x,z):
    land=(-10<=x<=142 and -10<=z<=78) or (142<x<=171 and 24<=z<=44)
    if not land:return not (in_patch(x,z,KEYS) or in_patch(x,z,CAPES))
    return in_patch(x,z,COVES) or any(inside(x,z,r) for r in CHANNELS)

def canal_edge(x,z,r):
    for cut in CHANNELS:
        if inside(x,z,cut,r):
            for a,b,w,d in BRIDGES:
                if a-r<=x<=a+w+r and b+r<=z<=b+d-r:
                    return False
            return True
    return False

# Convex shore polygons with bounding boxes for quick boat collision checks.
# Shallows surround the barrier keys. The two western coves open into the bay.
KEYS=((24,84,27,9,((24,86),(32,84),(43,86),(51,90),(42,93),(30,91))),
      (57,90,21,7,((57,93),(63,90),(73,90),(78,93),(69,97),(59,96))),
      (173,16,16,9,((173,22),(177,17),(185,16),(189,20),(184,25),(176,25))),
      (66,-23,21,7,((66,-20),(71,-23),(81,-22),(87,-18),(79,-16),(70,-17))))
COVES=((-10,6,13,16,((-10,6),(-1,10),(3,17),(-3,22),(-10,22))),
       (-10,39,14,10,((-10,39),(-4,40),(4,44),(-4,49),(-10,48))),
       (76,-10,16,5,((76,-10),(92,-10),(89,-6),(82,-5))))

# Mainland extensions. The shore drives use the same paths on both maps.
CAPES=((56,74,40,14,((56,75),(63,82),(72,87),(78,88),(88,84),(96,74))),
       (113,-22,15,15,((113,-7),(115,-15),(119,-22),(123,-21),(126,-15),(128,-7))),
       (-24,48,17,21,((-8,48),(-15,52),(-24,60),(-23,65),(-14,69),(-7,66))),
       (140,44,18,22,((140,44),(148,47),(157,55),(158,59),(151,60),(142,66))))
DRIVES=(((64,72),(64,75),(68,79),(76,82),(84,80),(93,77),(96,74),(96,70)),
        ((128,0),(126,-3),(125,-8),(122,-12),(120,-17)))

def in_patch(x,z,features):
    for a,b,w,d,outline in features:
        if a<=x<=a+w and b<=z<=b+d:
            inside_shape=False
            u,v=outline[-1]
            for xx,zz in outline:
                if (zz>z)!=(v>z) and x<xx+(z-zz)*(u-xx)/(v-zz):
                    inside_shape=not inside_shape
                u,v=xx,zz
            if inside_shape:return True
    return False
