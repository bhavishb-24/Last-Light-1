# LAST LIGHT / COASTLINE - TI-84 Evo
from COASTGEO import CityBlocks, canal_edge, CAPES, COVES, in_patch
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
       "Beacon Hill","East Docks","Tin Marsh","Breakwater")
_pen=None

def color(c):
    global _pen
    if c!=_pen:
        draw.set_color(c[0],c[1],c[2])
        _pen=c

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
    draw.draw_text(x,y,s[:(320-x)//10])

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
       "LOOK","DOCK","BAIT","LIGHT")
VENUES=("Mara's studio","Glasshouse Supply","FM transmitter","Marina slips",
        "City Dispatch","Thread Dept.","Pixel Palace","Pier booth",
        "Foundry Customs","Velvet Club","Palm Garden","Lido Rally",
        "Hill safehouse","Dock office","Marsh bait shack","Lighthouse")
GOALS=(0,7,1,2,13,15,8,13,12,6,2,0,-1)
TASK=("Meet Mara at West Quay","Interview Ivo at Sun Pier","Buy a valve at Glasshouse",
      "Tune the tower transmitter","Meet Rook at East Docks","Find Ivo at Breakwater",
      "Visit Foundry Customs","Return to the dock office","Take Ivo to Beacon Hill",
      "Pick Arcade or Velvet","Air the tape from FM Tower","Meet Mara at the studio",
      "Story complete / free roam")
CHAPTERS=("LAST SHOW","THE PIER TAPE","SPARE PARTS","DEAD AIR","LOW TIDE",
          "THE LOGBOOK","STORM KIT","THE RESCUE","HIGH GROUND","TWO TAPES",
          "STORM SIGNAL","THE MORNING AFTER")
CACHES=((-3,33),(92,61),(125,-4))
RECORDS=((-5,38),(67,58),(91,-5),(130,71),(118,8),(155,27))
COURSES=((10,6,7,11),(14,13,15,13,14),(1,5,9,10,11))
STARTS=(11,14,0)
PURSES=(70,110,90)
WEATHER=("CLEAR","RAIN","FOG","STORM","HEAT")
FRONT=(0,1,4,2,3,1)
# Keep the original 12 door coordinates for earlier checkpoint codes.
EXTRA=((128,64),(128,32),(128,0),(160,32))

SKIN=(212,145,104)
ASPHALT=(62,62,81)
WALK=(158,142,150)
TILE=(95,123,128)
TAU=6.2831853

def center(n):
    if n>=12: return EXTRA[n-12]
    return (32*(n%4),32*(2-n//4))

def door(n):
    x,z=center(n)
    return x+8,z+5

def district(x,z):
    row=max(0,min(2,int((z+16)//32)))
    if x>=144 and 16<=z<48: return 15
    if x>=112: return 14-row
    col=max(0,min(3,int((x+16)//32)))
    return col+4*(2-row)

def near(x,z,u,v,r):
    return (x-u)*(x-u)+(z-v)*(z-v)<=r*r

BLOCKS=CityBlocks(tuple(center(i) for i in range(len(NAMES))))

def blocked(x,z,r):
    if x< -10 or x>171 or z< -10 or z>78 or (x>142 and (z<24 or z>44)):
        return not in_patch(x,z,CAPES)
    if canal_edge(x,z,r):return True
    if (x<5 or z< -4) and abs(x)>3.6-r and in_patch(x,z,COVES):return True
    return BLOCKS.intersects(x,z,r)

def fresh():
    return city_state(dict(x=7.0,z=65.0,angle=0.0,cx=3.0,cz=64.0,
                pin=-1,detail=True,drive=False,speed=0,stage=0,cash=25,coat=0,paint=0,
                shoes=0,records=0,job=0,race=-1,course=0,
                choice=0,grip=0,medals=0,fish=0,parcel=0,radio=2,rescue=False,timer=0.0,clock=0.0,
                fine=0.0,heat=0.0,px=0.0,pz=0.0,parkangle=0.0,stride=0.0,msg="",ttl=0))

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

# Fixed-width decimal chunks keep arithmetic small on the calculator.
def passcode(s):
    a=(district(s['x'],s['z'])*13+s['stage'])*1000+s['cash']
    b=s['coat']
    for base,key in ((3,'paint'),(2,'shoes'),(64,'records'),(17,'job')):
        b=b*base+s[key]
    c=s['choice']
    for base,key in ((2,'grip'),(8,'medals'),(10,'fish'),(10,'parcel')):
        c=c*base+s[key]
    body='8%06d%05d%04d'%(a,b,c)
    return body+str(sum(int(ch) for ch in body)%10)

def restore(code):
    if not code.isdigit(): return None
    s=fresh()
    if len(code)==17 and code[0]=='8':
        if sum(int(ch) for ch in code[:-1])%10!=int(code[-1]): return None
        a,b,c=int(code[1:7]),int(code[7:12]),int(code[12:16])
        v=a//13000
        if v>=len(NAMES) or b>=19584 or c>=4800: return None
        s['stage'],s['cash']=(a//1000)%13,a%1000
        for base,key in ((17,'job'),(64,'records'),(2,'shoes'),(3,'paint'),(3,'coat')):
            s[key],b=b%base,b//base
        for base,key in ((10,'parcel'),(10,'fish'),(8,'medals'),(2,'grip'),(3,'choice')):
            s[key],c=c%base,c//base
        if (s['stage']>=10)!=(s['choice']!=0): return None
    elif 2<=len(code)<=11:
        v=int(code[:-1])
        if int(code[-1])!=v%7: return None
        for base,key in ((13,'job'),(8,'records'),(2,'shoes'),(3,'paint'),(3,'coat'),(1000,'cash'),(7,'stage')):
            s[key],v=v%base,v//base
        if v>=12: return None
        if s['stage']>=5: s['stage']=4
    else:
        return None
    if s['stage']==8: s['stage']=7
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
    for i in range(len(RECORDS)):
        u,v=RECORDS[i]
        if not (s['records'] & (1<<i)) and near(x,z,u,v,2.3):
            return ('disc',i)
    for j,(u,v) in enumerate(CACHES):
        if not s['loot']&(1<<j) and near(x,z,u,v,2):return ('cache',j)
    if near(x,z,s['cx'],s['cz'],3.2):
        return ('car',0)
    for j in range(3):
        u,v=local_position(s,j)
        if near(x,z,u,v,2): return ('local',j)
    return ('',0)

def local_position(s,j):
    night=int(s['clock']//90)%2
    n=((1,5,10),(6,9,13))[night][j]
    x,z=center(n)
    span=3 if weather(s) in (1,3,4) else 6
    return x+span*sin(s['clock']*.5+j),z-4

def road_route(s,n):
    a=district(s['x'],s['z'])
    if a==n and s['race']<0:
        return [door(n)]
    x,z=center(a)
    tx,tz=center(n)
    corners=[]
    if a==15 and n!=15:
        corners.append((128,32))
        x,z=128,32
    if n==15 and a!=15:
        corners.append((x,32))
        corners.append((128,32))
    elif z!=tz:
        corners.append((x,tz))
    corners.append((tx,tz))
    if s['race']<0:
        corners.append(door(n))
    return corners

def roadblock(s):
    if s['heat'] and crew(s)['zones'][region(s)]>=3:
        x,z=center(district(s['x'],s['z']))
        return x,z+2
    return None

def weather(s):
    if s['rescue']: return 3
    return FRONT[int(s['clock']//44)%len(FRONT)]

def gate(s):
    return COURSES[s['course']][s['race']]

def goal(s):
    if s['race']>=0: return gate(s)
    if s['rescue']: return 12
    if s['pin']>=0: return s['pin']
    if s['job'] and GOALS[s['stage']]<0: return s['job']-1
    return GOALS[s['stage']]

def gps(s):
    n=goal(s)
    if n<0: return 'Free roam'
    u,v=center(n) if s['race']>=0 else door(n)
    if s['drive']:
        for wx,wz in road_route(s,n):
            if not near(s['x'],s['z'],wx,wz,4):
                u,v=wx,wz
                break
    dx,dz=u-s['x'],v-s['z']
    if s['race']>=0: name='Gate '+str(s['race']+1)+' '+str(int(s['timer']))+'s'
    elif s['rescue']: name='Shelter '+str(int(s['timer']))+'s'
    elif s['pin']>=0: name='Pin '+NAMES[n]
    elif s['stage']==9: name='Arcade/Club'
    else: name=NAMES[n]
    heading=('N' if dz>3 else 'S' if dz< -3 else '')+('E' if dx>3 else 'W' if dx< -3 else '')
    return name+' '+heading

NICK=("Lena","Sol")
TIERS=("Professional","Hardened","Violent","Psycho","Irredeemable")
REGIONS=("Neon Bay","Tern Keys","Sedge River","Iron Harbor","Cane Lake","Pine Heights")
REGION=(0,0,0,1,3,0,0,1,3,0,4,1,5,3,2,1)
CARS=("Compact","Muscle","Sport","Luxury","Super","Pickup","Trail ATV","Motorbike")
LOTS=(1,5,7,9,11,4,12,14)
TOP=(11,16,19,15,22,12,13,17)
PRICE=(24,65,95,120,180,55,48,38)
GUNS=("Sidearm","Revolver","Burst","Scatter","Carbine","Longshot","Thrown")
PEOPLE=(('hp',7,80),('stam',7,64),('focus',5,8),('power',4,0),('cardio',4,0),
        ('skill',4,0),('rep',5,0),('gym',1,0),('hair',2,1),('style',2,0),
        ('hunger',4,0),('weight',3,3),('tat',1,0),('arms',7,1),('gun',3,0),
        ('ammo',6,6),('reserve',6,18),('coat',2,0))
SHARED=(('who',1,0),('pair',1,0),('bond',5,0),('bank',12,0),('owned',8,1),
        ('stored',8,0),('ride',3,0),('fuel',7,100),('body',7,100),('premium',1,0),
        ('token',2,0),('tags',6,0),('pet',2,0),('snack',3,0),('homes',2,1),
        ('photo',5,0),('lastpic',4,0),('selfie',1,0),('blur',2,0),('vault',2,0),
        ('lure',2,0),('hunt',1,0),('event',5,0),('salvage',1,0),('loot',3,0))
ABC="0123456789ABCDEFGHJKMNPQRSTVWXYZ"

def crew(s):
    return s['crew'][s['who']]

def region(s):
    return REGION[district(s['x'],s['z'])]

def pick(title,items,foot="ENTER select / CLEAR back",start=0):
    i=start
    while True:
        first=i//5*5
        lines=[("> " if j==i else "  ")+items[j] for j in range(first,min(first+5,len(items)))]
        sheet(title,lines,foot)
        k=keywait((UP,DOWN,OK,EXIT))
        if k==EXIT: return -1
        if k==OK: return i
        i=(i+(1 if k==DOWN else -1))%len(items)

def sync_search(s):
    r=region(s)
    if s['district_heat']==r:
        return
    s['district_heat']=r
    s['heat']=0
    if crew(s)['zones'][r]:
        alert(s,0)

def city_state(s):
    for key,bits,v in SHARED: s[key]=v
    s['crew']=[]
    for i in range(2):
        h={}
        for key,bits,v in PEOPLE: h[key]=v
        h['coat']=i
        h['zones']=[0]*6
        s['crew'].append(h)
    s['district_heat']=-1
    s['rest']=0
    s['slow']=0
    s['stance']=0
    s['jump']=0
    s['lastx'],s['lastz']=s['x'],s['z']
    s['craft'],s['depth']=0,0
    s['distance']=0
    return s

def packed(s):
    crew(s)['coat']=s['coat']
    fields=[(s[k],bits) for k,bits,_ in SHARED]
    for h in s['crew']:
        fields.extend([(h[k],bits) for k,bits,_ in PEOPLE])
        fields.extend([(v,3) for v in h['zones']])
    carry=0
    bits=0
    result=''
    for v,n in fields:
        carry+=int(v)<<bits
        bits+=n
        while bits>=5:
            result+=ABC[carry%32]
            carry//=32
            bits-=5
    if bits: result+=ABC[carry]
    body=passcode(s)+result
    return body+ABC[sum((i+1)*ord(c) for i,c in enumerate(body))%31]

def unpack(code):
    code=code.strip().upper()
    if len(code)<=17:
        s=restore(code)
        if s: crew(s)['coat']=s['coat']
        return s
    if len(code)!=74 or any(c not in ABC for c in code) or ABC[sum((i+1)*ord(c) for i,c in enumerate(code[:-1]))%31]!=code[-1]: return None
    s=restore(code[:17])
    if s is None: return None
    index=17
    bits=0
    carry=0
    for obj,fields in [(s,SHARED)]+[(h,PEOPLE+tuple((j,3,0) for j in range(6))) for h in s['crew']]:
        for k,n,_ in fields:
            while bits<n:
                carry+=ABC.index(code[index])<<bits
                index+=1
                bits+=5
            value=carry%(1<<n)
            if isinstance(k,int): obj['zones'][k]=min(5,value)
            else: obj[k]=value
            carry//=1<<n
            bits-=n
    if any(h['gun']>=7 or h['coat']>2 for h in s['crew']) or s['blur']>2 or s['lure']>2: return None
    s['coat']=crew(s)['coat']
    if crew(s)['zones'][region(s)]: alert(s,0)
    return s

def checkpoint(s):
    code=packed(s)
    lines=tuple(code[i:i+20] for i in range(0,len(code),20))
    tell("CHECKPOINT / COPY ALL ROWS",lines+("Load rows in order at title.",))

def bond(s):
    if s['pair']: s['bond']=min(31,s['bond']+1)

def profile(s,change):
    h=crew(s)
    if h['rep']<24: h['rep']=max(0,min(24,h['rep']+change))
    notice(s,TIERS[min(4,h['rep']//6)]+" / conduct "+str(h['rep']))

def alert(s,level):
    h=crew(s)
    r=region(s)
    s['district_heat']=r
    h['zones'][r]=min(5,h['zones'][r]+level)
    s['lastx'],s['lastz']=s['x'],s['z']
    if s['heat']<=0:
        s['px'],s['pz']=s['x']-8,s['z']-7
    s['heat']=12+3*h['zones'][r]+h['rep']//3

def defeat(s,busted):
    p=crew(s)
    s['cash']=max(0,s['cash']-(35 if busted else 25))
    p['hp'],p['stam']=80,64
    p['zones']=[0]*6
    s['heat'],s['race'],s['speed'],s['drive']=0,-1,0,False
    if s['rescue']: s['stage'],s['rescue']=7,False
    s['x'],s['z']=center(4 if busted else 5)
    s['district_heat']=-1
    notice(s,"BUSTED / cash fine" if busted else "WASTED / clinic fee")


def lot(s):
    for i,n in enumerate(LOTS):
        x,z=center(n)
        if near(x-3,z+3,s['x'],s['z'],4.0): return i
    return -1


def event_at(s):
    return (7,13,9,12,3,14)[int(s['clock']//75)%6]

def event_name(s):
    return ("Pier regatta","Dock swap meet","Velvet open mic","Hill dog show","Harbor parade","Marsh bird count")[int(s['clock']//75)%6]

