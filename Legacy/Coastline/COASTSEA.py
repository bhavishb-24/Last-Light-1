from COASTLIB import (
    BLUE, DOWN, EXIT, GOLD, INK, LEFT, MAP,
    MILK, NAMES, NIGHT, OK, PINK, REGIONS, RIGHT,
    SKIN, STEEL, SUN, TAU, UP, bond, box,
    color, cos, disc, door, draw, earn, get_key,
    label, line, monotonic, near, notice, pick, poly,
    region, sin, sync_search, tell, weather
)
from COASTMAP import (
    render
)

from COASTGEO import water

# Coastal travel uses the same landmarks and coordinates as the street map.

PORTS=(3,12,14,15)
from COASTGEO import LAUNCH
CRAFT=("Harbor skiff","Floatplane","Jet ski","Airboat","Swim and dive")
WRECK=(153,10)

def in_water(x,z):
    if not (-27<=x<=192 and -24<=z<=99):
        return False
    return water(x,z)


def seaview(s):
    kind=s['craft']
    w=weather(s)
    if kind==5 and s['depth']:
        box((27,88,110),0,21,320,144)
        for j in range(8):
            x=(j*47+int(s['x']*3))%320
            y=35+(j*29+int(s['clock']*4))%116
            if j%2:disc((81,157,163),x,y,2)
            else:poly((105,181,163),[x,x+8,x+14,x+14,x+8],[y,y-3,y-6,y+5,y+3])
        if near(s['x'],s['z'],WRECK[0],WRECK[1],9):
            poly(NIGHT,[87,204,181,101],[111,108,136,140])
            line(STEEL,143,110,139,76)
            box(GOLD,134,110,13,8)
    elif kind==2:
        poly(MILK,[106,146,156,164,175,214,214,169,161,153,106],
             [132,116,94,94,116,132,136,129,143,129,136])
        box(BLUE,156,104,9,13)
        box(PINK,154,136,14,3)
    elif kind==5:
        disc(SKIN,160,133,5)
        line(SKIN,151,133,142,127)
        line(SKIN,168,133,179,137)
    else:
        bob=int((2 if w in (1,3) else 1)*sin(s['clock']*4))
        y=135+bob
        poly(MILK,[127,152,168,193,182,140],[y-1,y-20,y-20,y-1,y+6,y+6])
        poly((52,136,151),[131,153,168,189,180,142],[y-2,y-17,y-17,y-2,y+2,y+2])
        box(NIGHT,149,y-13,23,10)
        disc(SKIN,160,y-12,4)
        if kind==4:
            color(INK)
            draw.draw_circle(161,y-9,11)
            line(INK,154,y-16,168,y-2)
        if s['speed']>0:
            line(MILK,138,y+7,127,y+15)
            line(MILK,182,y+7,193,y+15)
    box(INK,0,165,320,45)

def voyage(s,n):
    if s['rescue'] or s['race']>=0:
        notice(s,"Finish the timed run first")
        return
    if n not in PORTS:
        s['pin']=3
        notice(s,"Marina slip pinned")
        return
    u,v=door(n)
    if not near(s['x'],s['z'],u,v,7):
        s['pin']=n
        notice(s,"Visit the lit shore office")
        return
    idx=pick("COASTAL TRANSPORT",CRAFT)
    if idx<0:return
    kind=idx+1
    pick_to=pick("PIN A LANDING",tuple(NAMES[i] for i in PORTS))
    if pick_to<0:return
    start=PORTS.index(n)
    s['craft'],s['depth']=kind,0
    s['alt']=9
    s['drive'],s['speed']=False,0
    s['x'],s['z']=LAUNCH[start]
    target=LAUNCH[pick_to]
    s['angle']=(0,0,3.14159,1.5708)[start]
    air=20
    found=False
    finish=n
    buffer=[]
    tell(CRAFT[idx],("UP throttle / DOWN stop","LEFT and RIGHT steer","ENTER dock near a landing","2nd dive or surface" if kind==5 else ("2nd change altitude" if kind==2 else "2nd view ports and heading"),"CLEAR calls a tow home"))
    while True:
        begin=monotonic()
        render(s,buffer)
        seaview(s)
        dx,dz=target[0]-s['x'],target[1]-s['z']
        heading=('N' if dz>3 else 'S' if dz< -3 else '')+('E' if dx>3 else 'W' if dx< -3 else '')
        label(SUN,5,184,NAMES[PORTS[pick_to]]+' '+heading+' '+str(int((dx*dx+dz*dz)**.5))+'m')
        label(MILK,5,206,('Air '+str(int(air))+' / ENTER search' if s['depth'] else ('2nd altitude '+str(s['alt'])+'m / ENTER dock' if kind==2 else 'ENTER dock / 2nd info / CLEAR')))
        key=buffer.pop(0) if buffer else get_key(0)
        while not key and monotonic()-begin<.075:
            key=get_key(0)
        dt=min(.24,max(.035,monotonic()-begin))
        if key==EXIT:break
        if key==MAP:
            if kind==5:
                s['depth']=1-s['depth']
                if not s['depth']:air=20
            elif kind==2:
                s['alt']=9 if s['alt']==23 else s['alt']+7
            else:
                tell("NAVIGATION",(REGIONS[region(s)],"Marina / Hill: north shore","Marsh: south shore","Breakwater: east shore","Steer toward the marked port."))
            continue
        if key==OK:
            if s['depth'] and near(s['x'],s['z'],WRECK[0],WRECK[1],9):
                if not s['salvage']:
                    s['salvage']=1
                    found=True
                    tell("SUNKEN CUTTER",("A brass bell lies inside.","Recover it for the museum.","+$80 when you reach shore."))
            else:
                for i,(x,z) in enumerate(LAUNCH):
                    if near(s['x'],s['z'],x,z,7):
                        finish=PORTS[i]
                        break
                else:
                    tell("SHORE RADIO",("Reach a landing to go ashore.","CLEAR to tow to home port."))
                    continue
                break
        if key in (LEFT,RIGHT):
            s['angle']=(s['angle']+(.22 if key==RIGHT else -.22))%TAU
        if key==UP:s['speed']=min((13,24,18,15,5)[idx],s['speed']+4)
        if key==DOWN:s['speed']=0
        wet=weather(s) in (1,3)
        drift=.9*sin(s['clock']*.5) if wet and s['speed'] else 0
        x=s['x']+(sin(s['angle'])*s['speed']+drift)*dt
        z=s['z']+cos(s['angle'])*s['speed']*dt
        if kind==2:
            s['x'],s['z']=min(192,max(-27,x)),min(99,max(-24,z))
        else:
            if in_water(x,s['z']):s['x']=x
            if in_water(s['x'],z):s['z']=z
        s['clock']+=dt
        if s['depth']:
            air-=dt
            if air<=0:s['depth']=0;air=20
    s['craft'],s['depth'],s['speed']=0,0,0
    s['x'],s['z']=door(finish)
    sync_search(s)
    if found:earn(s,80)
    if finish!=n:bond(s)
    notice(s,("Bell delivered / $80" if found else "Ashore / "+NAMES[finish]))
