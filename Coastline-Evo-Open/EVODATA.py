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
       "Northgate","East Docks","Southbank","Breakwater")
def color(c):
    draw.set_color(c[0],c[1],c[2])

def box(c,x,y,w,h):
    x=int(x)
    y=int(y)
    r=min(320,x+int(w))
    b=min(210,y+int(h))
    x=max(0,x)
    y=max(0,y)
    if x<r and y<b:
        color(c)
        draw.fill_rect(x-1,y-1,r-x+1,b-y+1)

def line(c,x,y,u,v):
    color(c)
    draw.draw_line(int(x),int(y),int(u),int(v))

def poly(c,xs,ys):
    color(c)
    draw.fill_poly(xs,ys)

def disc(c,x,y,r):
    color(c)
    draw.fill_circle(x,y,r)

def label(c,x,y,s):
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
       "NORTH","DOCK","SOUTH","POINT")
VENUES=("Mara's studio","Glasshouse Supply","FM transmitter","Marina slips",
        "City Dispatch","Thread Dept.","Pixel Palace","Pier booth",
        "Foundry Customs","Velvet Club","Palm Garden","Lido Rally",
        "Northgate overlook","East Docks office","Southbank service","Breakwater lookout")
GOALS=(0,7,1,2,6,-1,-1)
TASK=("Meet Mara at West Quay","Interview Ivo at Sun Pier","Buy a valve at Glasshouse",
      "Tune the tower transmitter","Arcade: air it / Club: dub it","City broadcast is live","Archive tape is safe")
RECORDS=((-5,38),(67,58),(91,-5))
GATES=(10,6,7,11)
SKIN=(212,145,104)
ASPHALT=(62,62,81)
WALK=(158,142,150)
TILE=(95,123,128)
TAU=6.2831853

RAMPS=((112,64,139,51),(112,32,139,32),(112,0,139,-6))

def highway(x,z):
    return abs(x-144)<=5 and -8<z<76

def road_height(x,z):
    if highway(x,z):
        return 4
    if 112<x<139:
        t=(x-112)/27
        for a,b,u,v in RAMPS:
            if abs(z-(b+(v-b)*t))<3:
                return 4*t
    return 0

def center(n):
    if n>=12:
        return ((124,64),(128,32),(124,0),(160,32))[n-12]
    return (32*(n%4),32*(2-n//4))

def door(n):
    x,z=center(n)
    return x+8,z+5

def district(x,z):
    if x>=150:
        return 15
    if x>=112:
        return 12 if z>=48 else (14 if z<16 else 13)
    col=max(0,min(3,int((x+16)//32)))
    row=max(0,min(2,int((z+16)//32)))
    return col+4*(2-row)

def near(x,z,u,v,r):
    return (x-u)*(x-u)+(z-v)*(z-v)<=r*r

# x,z half-width, half-depth, height, facade color, trim, shop index.
BLOCKS=[]
for n in range(len(NAMES)):
    x,z=door(n)
    BLOCKS.append((x,z+3.9,3.8,3,3.7+n%3, (NIGHT,VIOLET,STEEL)[n%3],TRIM[n%4],n))
for n in range(6):
    x=16+32*(n%3)
    z=16+32*(n//3)
    BLOCKS.append((x,z,4.8,4.4,7+n%4*2,NIGHT,STEEL,-1))

def blocked(x,z,r):
    if x< -10 or x>176 or z< -10 or z>78:
        return True
    for bx,bz,w,d,h,c,t,n in BLOCKS:
        if abs(x-bx)<w+r and abs(z-bz)<d+r:
            return True
    return False

def fresh():
    return dict(x=7.0,z=65.0,angle=0.0,cx=3.0,cz=64.0,
                pin=-1,detail=False,drive=False,speed=0,stage=0,cash=25,bank=0,coat=0,paint=0,
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
    return code+(".%03d%d"%(bank,bank%7) if bank else "")

def restore(code):
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
    s['bank']=bank
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

def tell(title,lines):
    sheet(title,lines,"ENTER continue")
    keywait((OK,EXIT))

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
