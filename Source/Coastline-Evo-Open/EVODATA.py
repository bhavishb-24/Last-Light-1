# LAST LIGHT: DEAD AIR - TI-84 Evo
import ti_draw as draw
from ti_system import get_key
from time import monotonic
from math import sin, cos

INK=(22,22,44)
NIGHT=(43,37,68)
VIOLET=(94,70,107)
PINK=(246,98,137)
SUN=(255,214,132)
MINT=(103,230,213)
MILK=(255,239,211)
ROAD=(53,52,76)
STEEL=(98,110,132)
GOLD=(255,180,80)
BLUE=(54,145,180)
RED=(224,68,90)
NAMES=("West Quay","Glasshouse","FM Tower","Marina",
       "Kiln Yard","Lantern Sq","Arcade","Sun Pier",
       "Foundry","Velvet Club","Palms","The Lido",
       "Northgate","East Docks","Southbank","Breakwater",
       "Cypress Row","Orchard End","Sawgrass","Beacon Point")
def color(c):
    draw.set_color(c[0],c[1],c[2])

draw_bottom=210

def box(c,x,y,w,h):
    x=int(x)
    y=int(y)
    r=min(320,x+int(w))
    b=min(draw_bottom,y+int(h))
    x=max(0,x)
    y=max(0,y)
    if x<r and y<b:
        color(c)
        draw.fill_rect(x-1,y-1,r-x+1,b-y+1)

def line(c,x,y,u,v):
    color(c)
    draw.draw_line(int(x),int(y),int(u),int(v))

def poly(c,xs,ys):
    if draw_bottom<210 and max(ys)>=draw_bottom:
        edge=draw_bottom-1
        if min(ys)>edge:
            return
        xx,yy=[],[]
        px,py=xs[-1],ys[-1]
        for x,y in zip(xs,ys):
            if (py<=edge)!=(y<=edge):
                xx.append(int(px+(x-px)*(edge-py)/(y-py)))
                yy.append(edge)
            if y<=edge:
                xx.append(x)
                yy.append(y)
            px,py=x,y
        if len(xx)<3:
            return
        xs,ys=xx,yy
    color(c)
    draw.fill_poly(xs,ys)

def disc(c,x,y,r):
    if draw_bottom<210 and y+r>=draw_bottom:
        for row in range(max(0,y-r),min(draw_bottom,y+r+1)):
            half=int((r*r-(row-y)**2)**.5)
            box(c,x-half,row,2*half+1,1)
        return
    color(c)
    draw.fill_circle(x,y,r)

def label(c,x,y,s):
    if draw_bottom<210 and y>=draw_bottom:
        return
    color(c)
    draw.draw_text(x,y,s)

def palm(x,y,h,c):
    t=x+h//7
    poly(c,[x-2,x+2,t+1,t-1],[y,y,y-h,y-h])
    b=y-h
    for side in (-1,1):
        for k in (0,1):
            w=h*(4-k)//8
            poly(c,[t,t+side*w//2,t+side*w],
                 [b+1,b-5+k*4,b+2+k*5])

def skyline(seed):
    bands=((62,57,103),(101,72,124),(153,89,136),
           (204,108,140),(244,140,139),(255,170,140))
    for i in range(6):
        box(bands[i],0,i*16,320,16)
    sx=218-(seed%4)*25
    disc(SUN,sx,43,24)
    for i in range(3):
        box(bands[(45+i*6)//16],sx-25,45+i*6,50,1+i)
    for i in range(17):
        x=i*21-5
        h=7+(i*31+seed*7)%24
        box(VIOLET,x,84-h,18,h)
    for i in range(9):
        x=(i*47+seed*19)%348-16
        h=10+(i*17+seed*5)%29
        box(NIGHT,x,84-h,15,h)
        box(NIGHT,x+4,81-h,8,4)
        for k in range(2,h-3,8):
            box((212,139,143),x+3,84-h+k,6,2)
    palm(36,84,34,INK)
    palm(279,84,24,INK)
    box(INK,0,82,320,2)

def car(x,y,w,paint,detail):
    # Normalized silhouette; y is the tire contact line.
    def shape(c,us,vs):
        poly(c,[x+i*w//64 for i in us],
               [y+i*w//64 for i in vs])
    def part(c,a,b,p,q):
        box(c,x+a*w//64,y+b*w//64,max(1,p*w//64),max(1,q*w//64))
    if w<16:
        part(INK,-21,-23,42,15)
        part(paint,-30,-14,60,12)
        part(PINK,-24,-10,12,4)
        return
    part(INK,-30,-5,60,6)
    part(INK,-25,-7,7,9)
    part(INK,19,-7,7,9)
    shape(paint,[-30,-25,-16,-10,14,22,29,30],
          [-7,-15,-18,-27,-27,-18,-14,-7])
    shape(NIGHT,[-17,-10,13,19],[-17,-25,-25,-17])
    shape(BLUE,[-14,-9,0,-5],[-18,-24,-24,-18])
    shape(paint,[-30,-22,23,30,27,-27],[-12,-16,-16,-12,-5,-5])
    if detail:
        shape((46,110,127),[-30,-18,20,30,27,-27],
              [-10,-7,-7,-10,-4,-4])
        part(MILK,-12,-26,24,1)
    part(INK,-26,-12,52,6)
    part(PINK,-24,-11,16,3)
    part(PINK,9,-11,16,3)
    if detail:
        part(MILK,-22,-11,10,1)
        part(MILK,14,-11,8,1)
        part(SUN,-4,-8,8,3)
        part(MINT,-22,-3,45,1)
        part(INK,-27,-17,54,2)

# World units: east is +x, north is +z. Districts share a continuous grid.
UP,DOWN,LEFT,RIGHT,OK,MAP,EXIT=25,34,24,26,105,21,45
PAINT=(MINT,PINK,GOLD)
COATS=(BLUE,PINK,MINT)
TRIM=(MINT,SUN,PINK,BLUE)
SIGNS=("WAVE","PARTS","FM 84","SLIP","POST","THREAD",
       "PIXEL","PIER","PAINT","VELVET","PALMS","LIDO",
       "NORTH","DOCK","SOUTH","POINT",
       "CYPRESS","ORCHARD","RANGER","BEACON")
VENUES=("Mara's studio","Glasshouse Supply","FM transmitter","Marina slips",
        "City Dispatch","Thread Dept.","Pixel Palace","Pier booth",
        "Foundry Customs","Velvet Club","Palm Garden","Lido Rally",
        "Northgate overlook","East Docks office","Southbank service","Breakwater lookout",
        "Cypress cafe","Orchard market","Sawgrass station","Beacon visitor center")
GOALS=(0,7,1,2,6,-1,-1)
TASK=("Meet Mara at West Quay","Interview Ivo at Sun Pier","Buy a valve at Glasshouse",
      "Tune the tower transmitter","Arcade: air it / Club: dub it","City broadcast is live","Archive tape is safe")
# District, objective title, counter dialogue. The opening covers 1, 2 and 7.
WIRE=(0, 4, 5, 8, 11, 14, 17, 19, 15, 13, 16, 12, 18, 10, 3, 9, 6, 0)
WIRE_NOTES="""Pick up the case at WAVE|A second tape names a relief scam.
Collect dispatch slips|These routes share a fake sender.
Ask Thread about the order|Uniforms were paid for in cash.
Match the paint at Foundry|Same paint on every missing van.
Read the Lido entry ledger|One van entered under a false plate.
Check the Southbank service bay|The plate points to a farm pickup.
Get the Orchard sales receipt|The driver paid with relief vouchers.
Read the Beacon visitor log|The van stopped below the lighthouse.
Find the Breakwater receiver|Unlock the coastal receiver.
Verify the dock manifest|Decode three bands to open the log.
Meet the witness at Cypress|The dock crew kept a backup copy.
Get the Northgate camera log|The highway camera confirms the van.
Recover the ranger's letter|Tune the ranger relay for the letter.
Collect proof from Palm Garden|Here is the survey map you need.
Get the last slip at the Marina|The manifest matches the slips.
Retrieve Velvet's backup tape|The dub will protect our witness.
Check the original at Arcade|Two copies. Same voice. Same deal.
Return the evidence to WAVE|We can air the relief case tonight.
"""

def wire_note(index):
    start=0
    for _ in range(index):
        start=WIRE_NOTES.find("\n",start)+1
    separator=WIRE_NOTES.find("|",start)
    end=WIRE_NOTES.find("\n",separator)
    return WIRE_NOTES[start:separator],WIRE_NOTES[separator+1:end]

RECORDS=((-5,38),(67,58),(91,-5))
GATES=(10,6,7,11)
SKIN=(212,145,104)
ASPHALT=(62,62,81)
WALK=(158,142,150)
TILE=(95,123,128)
TAU=6.2831853

RAMPS=((112,64,139,51),(112,32,139,32),(112,0,139,-6))
# Rectangular streets also drive the 2D atlas. World x, z, width, length.
STREETS=((-3,-10,6,88),(29,-10,6,88),(61,-10,6,88),(93,-10,6,88),
         (-10,-3,122,6),(-10,29,250,6),(-10,61,122,6),
         (185,-10,6,88),(222,19,4,53),(175,-2,48,4),(183,62,53,4))

def highway(x,z):
    return abs(x-144)<=5 and -8<z<76

def road_height(x,z):
    if highway(x,z):
        return 4
    if 149<x<174 and abs(z-32)<3:
        return (174-x)*.16
    if 112<x<139:
        t=(x-112)/27
        for a,b,u,v in RAMPS:
            if abs(z-(b+(v-b)*t))<3:
                return 4*t
    return 0

def center(n):
    if n>=12:
        return ((124,64),(128,32),(124,0),(160,32),
                (188,64),(192,32),(188,0),(224,32))[n-12]
    return (32*(n%4),32*(2-n//4))

def door(n):
    x,z=center(n)
    return x+8,z+5

def district(x,z):
    if x>=210:
        return 19
    if x>=176:
        return 16 if z>=48 else (18 if z<16 else 17)
    if x>=150:
        return 15
    if x>=112:
        return 12 if z>=48 else (14 if z<16 else 13)
    col=max(0,min(3,int((x+16)//32)))
    row=max(0,min(2,int((z+16)//32)))
    return col+4*(2-row)

def near(x,z,u,v,r):
    return (x-u)*(x-u)+(z-v)*(z-v)<=r*r

# Packed x/z, quarter-unit footprints, height and facade.
LOTS=(
    b'\x1a\x1a\x13\x12\x07\x06:\x1a\x13\x12\t\x06Z\x1a\x13\x12\x0b\x06\x1a:\x13\x12\r\x06'
    b'::\x13\x12\x07\x06Z:\x13\x12\t\x06\x05@\x08\x10\x1a\x08\x15=\x10\x14&\t'
    b'\x1eE\x0c\x08\x1a\n3A\x10\x10 \n;D\x0c\x0c$\x08D<\x0c\x10\x1c\t'
    b"\x1b'\x14\x07\x16\n5!\x10\x10\x18\x08R@\x10\x14\x14\ta;\x10\x14\x10\n"
    b'\x1b\x15\x10\x0c\x0c\n| \x0c\x0c\n\t\xb3\x17\x0c\x0c\x08\x0b\xc0@\x0c\x0c\x07\x0c'
    b'\xd5@\x10\x0c\t\r\xbf\x1c\x0e\x0c\x08\r\xd7\x1b\x10\n\x08\x0b\xe5C\x10\x10\x08\x0c'
    b'\xe3\x18\x0f\x0c\x07\x0c\xf4E\x0c\x0c\t\r'
)
FACADES=((64,113,145),(80,119,123),(132,101,129),(185,131,109),
         (148,174,149),(196,175,128))
BUILDINGS=len(NAMES)+len(LOTS)//6

def building_at(n):
    if n<len(NAMES):
        x,z=door(n)
        return (x,z+3.9,3.8,3,3.7+n%3,(NIGHT,VIOLET,STEEL)[n%3],TRIM[n%4],n)
    j=(n-len(NAMES))*6
    style=LOTS[j+5]
    c=FACADES[style-8] if style>=8 else NIGHT
    height=LOTS[j+4]*.5 if style>=8 else LOTS[j+4]
    return (LOTS[j]-10,LOTS[j+1]-10,LOTS[j+2]*.25,LOTS[j+3]*.25,height,c,
            TRIM[style%4] if style>=8 else STEEL,-1)

def blocked(x,z,r):
    if x< -10 or x>240 or z< -10 or z>78:
        return True
    for n in range(len(NAMES)):
        u,v=door(n)
        if abs(x-u)<3.8+r and abs(z-v-3.9)<3+r:
            return True
    for j in range(0,len(LOTS),6):
        if abs(x+10-LOTS[j])<LOTS[j+2]*.25+r and abs(z+10-LOTS[j+1])<LOTS[j+3]*.25+r:
            return True
    return False

def fresh():
    return dict(x=7.0,z=65.0,angle=0.0,cx=3.0,cz=64.0,
                pin=-1,detail=False,drive=False,speed=0,stage=0,cash=25,bank=0,wire=0,coat=0,paint=0,
                shoes=0,records=0,job=0,race=-1,timer=0.0,clock=0.0,
                fine=0.0,heat=0.0,px=0.0,pz=0.0,parkangle=0.0,stride=0.0,msg="",ttl=0)

def notice(s,msg):
    s['msg']=msg
    s['ttl']=2.1

def pay(s,n):
    if s['cash']<n:
        return False
    s['cash']-=n
    return True

def earn(s,n):
    s['cash']=min(999,s['cash']+n)

# Portable checkpoint, no calculator variables consumed.
def passcode(s):
    v=district(s['x'],s['z'])
    for base,key in ((7,'stage'),(1000,'cash'),(3,'coat'),(3,'paint'),(2,'shoes'),(8,'records'),(13,'job')):
        v=v*base+s[key]
    code=str(v)+str(v%7)
    bank=s['bank']
    if bank:
        code+=".%03d%d"%(bank,bank%7)
    wire=s['wire']
    return code+("/%02d%d"%(wire,wire%7) if wire else "")

def restore(code):
    wire=0
    if "/" in code:
        code,_,saved=code.partition("/")
        if len(saved)!=3 or not saved.isdigit():
            return None
        wire=int(saved[:2])
        if wire>len(WIRE) or wire%7!=int(saved[2]):
            return None
    bank=0
    if "." in code:
        code,_,saved=code.partition(".")
        if len(saved)!=4 or not saved.isdigit():
            return None
        bank=int(saved[:3])
        if bank%7!=int(saved[3]):
            return None
    if not code.isdigit() or not 2<=len(code)<=11:
        return None
    v=int(code[:-1])
    if int(code[-1])!=v%7:
        return None
    s=fresh()
    for base,key in ((13,'job'),(8,'records'),(2,'shoes'),(3,'paint'),(3,'coat'),(1000,'cash'),(7,'stage')):
        s[key]=v%base
        v//=base
    if v>=len(NAMES):
        return None
    if wire and s['stage']<5:
        return None
    s['bank'],s['wire']=bank,wire
    x,z=center(v)
    s['x'],s['z']=x+7,z+1
    s['cx'],s['cz']=x+3,z
    return s

def keywait(keys):
    while True:
        k=get_key(0)
        if k in keys:
            return k

def sheet(title,lines,footer):
    box(INK,0,0,320,210)
    box(NIGHT,0,0,320,42)
    box(PINK,8,12,3,19)
    label(SUN,18,32,title)
    for i in range(len(lines)):
        label(MILK,10,65+21*i,lines[i])
    box(NIGHT,0,183,320,27)
    label(MINT,8,204,footer)

def tell(title,lines,speaker=None):
    sheet(title,lines,"ENTER continue")
    if speaker is None:
        keywait((OK,EXIT))
        return

    hair,skin,shirt=((INK,(193,128,104),PINK),
                     (ROAD,(224,167,120),BLUE),
                     (VIOLET,(168,106,88),MINT),
                     (NIGHT,(232,176,143),VIOLET),
                     (INK,(121,79,67),GOLD),
                     (VIOLET,(185,124,102),PINK),
                     (ROAD,(207,150,111),MINT))[speaker]
    box(NIGHT,257,139,55,43)
    box(shirt,266,172,37,10)
    box(skin,274,146,21,28)
    box(hair,272,143,25,8)
    if speaker in (0,2,5):
        box(hair,270,148,5,20)
    box(INK,278,156,3,2)
    box(INK,288,156,3,2)
    start=monotonic()
    previous=-1
    while True:
        if get_key(0) in (OK,EXIT):
            return
        frame=min(6,int((monotonic()-start)*7))
        if frame!=previous:
            box(skin,281,165,8,4)
            box(hair,282,166,6,1+2*(frame%2))
            previous=frame

def closest(s):
    x,z=s['x'],s['z']
    # Doorways win if a vehicle is parked across one.
    for n in range(len(NAMES)):
        u,v=door(n)
        if near(x,z,u,v,2.8):
            return ('door',n)
    for i in range(3):
        u,v=RECORDS[i]
        if not (s['records'] & (1<<i)) and near(x,z,u,v,2.3):
            return ('disc',i)
    if near(x,z,s['cx'],s['cz'],3.2):
        return ('car',0)
    for j,n in enumerate((1,5,10)):
        u,v=center(n)
        if near(x,z,u+6*sin(s['clock']*0.5+j),v-4,2): return ('local',j)
    return ('',0)

def goal(s):
    if s['race']>=0:
        return GATES[s['race']]
    if s['job']:
        return s['job']-1
    if s['stage']>=5 and s['wire']<len(WIRE):
        return WIRE[s['wire']]
    return GOALS[s['stage']]

def gps(s):
    n=goal(s)
    pinned=s['pin']>=0 and s['race']<0
    if pinned: n=s['pin']
    if n<0:
        return 'Free roam'
    u,v=center(n) if s['race']>=0 else door(n)
    dx,dz=u-s['x'],v-s['z']
    name=NAMES[n]
    if s['race']>=0: name='Gate '+str(s['race']+1)+' '+str(int(s['timer']))+'s'
    elif pinned: name='Pin '+name
    elif s['stage']==4 and not s['job']:
        name="Arcade/Club"
    f,c=sin(s['angle']),cos(s['angle'])
    side=dx*c-dz*f
    ahead=dx*f+dz*c
    distance=int((dx*dx+dz*dz)**.5)
    direction="HERE" if distance<3 else ("TURN" if ahead<-abs(side)
               else ("R" if side>max(1,ahead*.5) else
                     ("L" if side<-max(1,ahead*.5) else "UP")))
    return name+" "+direction+" "+str(distance)


def weather(s):
    return int(s['clock']//28)%4

WEATHER=("Clear","Rain","Fog","Heat")
