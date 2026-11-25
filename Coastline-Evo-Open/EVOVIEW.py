from EVODATA import *
def person(x,y,h,c,step,back):
    # Silhouette reads at full character scale and on distant pedestrians.
    u=max(1,h//12)
    leg=int(sin(step)*u)
    box(ROAD,x-3*u,y-u,7*u,u)
    box(NIGHT,x-2*u,y-4*u,2*u,4*u+leg)
    box(INK,x+u//2,y-4*u,2*u,4*u-leg)
    box(MILK,x-2*u,y+leg-1,2*u,2)
    box(MILK,x+u//2,y-leg-1,2*u,2)
    poly(c,[x-3*u,x+3*u,x+2*u,x-2*u],[y-8*u,y-8*u,y-3*u,y-3*u])
    box(c,x-3*u,y-8*u,u,3*u+leg)
    box(c,x+2*u,y-8*u,u,3*u-leg)
    box(SKIN,x-3*u,y-5*u+leg,u,u)
    box(SKIN,x+2*u,y-5*u-leg,u,u)
    box(SUN if back else MILK,x-2*u,y-7*u,4*u,max(1,u//2))
    if back and u>1:
        poly(NIGHT,[x-u,x+2*u,x+u,x-2*u],[y-8*u,y-5*u,y-4*u,y-7*u])
        box(GOLD,x+u,y-5*u,u,u)
    box(SKIN,x-u,y-10*u,3*u,2*u)
    box(INK,x-u,y-11*u,3*u,u if not back else 2*u)
    box((126,69,76),x-u,y-11*u,2*u,max(1,u//2))

def sidecar(x,y,w,c):
    def band(col,a,b,width,height):
        box(col,x+a*w//32,y+b*w//32,max(1,width*w//32),max(1,height*w//32))
    band(INK,-14,-2,28,3)
    band(c,-16,-6,32,5)
    band(NIGHT,-7,-10,14,5)
    band(BLUE,-6,-9,11,3)
    band(MILK,-15,-5,3,2)
    for j in (-9,9):
        disc(INK,x+j*w//32,y,max(1,w//13))
        if w>26: disc(STEEL,x+j*w//32,y,max(1,w//28))

def traffic(t):
    return ((-7+(t*5)%115,1),(95,74-(t*4)%83))

# Convert world vertices to camera space and clip against the near plane.
def uv(cam,x,z):
    dx=x-cam[0]
    dz=z-cam[1]
    return (dx*cam[3]-dz*cam[2],dx*cam[2]+dz*cam[3])

def face(cam,pts,c):
    xs=[]
    ys=[]
    ax,ay,az=pts[-1]
    au,ad=uv(cam,ax,az)
    eye=cam[4]
    for x,y,z in pts:
        u,depth=uv(cam,x,z)
        if (ad>=1)!=(depth>=1):
            fraction=(1-ad)/(depth-ad)
            xs.append(int(160+121*(au+fraction*(u-au))))
            ys.append(int(68+121*(eye-ay-fraction*(y-ay))))
        if depth>=1:
            xs.append(int(160+121*u/depth))
            ys.append(int(68+121*(eye-y)/depth))
        au,ay,ad=u,y,depth
    if len(xs)>=3 and max(xs)>=0 and min(xs)<320 and max(ys)>=0 and min(ys)<188:
        poly(c,xs,ys)

def ground(cam,x,z,w,d,c):
    face(cam,((x,0,z),(x+w,0,z),(x+w,0,z+d),(x,0,z+d)),c)

def building(cam,b):
    x,z,w,d,h,c,trim,n=b
    l,r=x-w,x+w
    a,f=z-d,z+d
    side=l if cam[0]<x else r
    if cam[0]<l or cam[0]>r:
        face(cam,((side,0,a),(side,0,f),(side,h,f),(side,h,a)),c)
    if cam[1]<a or cam[1]>f:
        front=a if cam[1]<a else f
        def panel(left,right,lo,hi,col):
            face(cam,((left,lo,front),(right,lo,front),
                      (right,hi,front),(left,hi,front)),col)
        panel(l,r,0,h,(100,76,105) if n>=0 else VIOLET)
        panel(l,r,h-0.42,h,trim)
        if n>=0 and front==a:
            panel(x-0.85,x+0.85,0,2.4,INK)
            panel(l+0.4,x-1.15,0.65,2.2,BLUE)
            panel(x+1.15,r-0.4,0.65,2.2,BLUE)
            u,dep=uv(cam,x,a)
            if 4<dep<21:
                sx=int(160+121*u/dep)-5*len(SIGNS[n])
                sy=int(68+121*(cam[4]-h+1.2)/dep)
                if 0<=sx<=320-10*len(SIGNS[n]) and 18<sy<172:
                    box(INK,sx-2,sy-17,10*len(SIGNS[n])+4,16)
                    label(MILK,sx,sy,SIGNS[n])
        elif n<0:
            for y in range(2,int(h)-1,3):
                panel(l+0.6,r-0.6,y,y+0.45,STEEL)
    if h<cam[4]:
        face(cam,((l,h,a),(r,h,a),(r,h,f),(l,h,f)),c)

def render(s):
    x,z=s['x'],s['z']
    f,c=sin(s['angle']),cos(s['angle'])
    cam=(x-6*f,z-6*c,f,c,3.4+road_height(x,z))
    detail=s['detail']
    night=int(s['clock']//90)%2
    front=weather(s)
    sky=((102,80,130),(55,73,103),(125,137,146),(158,93,96))
    haze=((202,115,143),(88,108,136),(176,181,180),(226,147,113))
    box((48,49,87) if night and front==0 else sky[front],0,0,320,35)
    box((91,77,122) if night and front==0 else haze[front],0,35,320,33)
    sx=int(160+140*sin(1-s['angle']))
    if front in (0,3): disc(MILK if night else SUN,sx,41,10 if night else 15)
    for j in range(13 if detail else 3):
        px=(j*37-int(s['angle']%TAU*320/TAU))%352-16
        h=4+(j*17)%14
        box(NIGHT if night else VIOLET,px,68-h,12+j%5,h)
        if j%3==0: box(SUN,px+3,69-h,4,2)
    box((54,99,132),0,68,320,120)
    for j in range(3 if detail else 0):
        box((110,151,166),j*94+14,72+j*3,32-j*4,1)
    ground(cam,-10,-10,186,88,TILE)
    # Continuous road network and sidewalks.
    if detail:
        for i in range(4):
            a=i*32
            if abs(x-a)<48:
                ground(cam,a-4.5,-10,9,88,WALK)
        for i in range(3):
            a=i*32
            if abs(z-a)<48:
                ground(cam,-10,a-4.5,186,9,WALK)
    for i in range(4):
        a=i*32
        if abs(x-a)<48:
            ground(cam,a-3,-10,6,88,ASPHALT)
    for i in range(3):
        a=i*32
        if abs(z-a)<48:
            ground(cam,-10,a-3,186 if i==1 else 122,6,ASPHALT)
    if x>80:
        overpass(cam,z)
    # Short paint dashes mark the closest avenues.
    ix=int((x+16)//32)*32
    iz=int((z+16)//32)*32
    for off in (-16,-8,0,8,16):
        if -8<=iz+off<=74 and 0<=ix<=96 and off:
            ground(cam,ix-.14,iz+off-.9,.28,2.6,SUN)
        if -8<=ix+off<=108 and 0<=iz<=64 and off:
            ground(cam,ix+off-.9,iz-.14,2.6,.28,SUN)
    if 0<=ix<=96 and 0<=iz<=64:
        for stripe in (-2,0,2):
            ground(cam,ix+stripe-.28,iz+3.5,.55,1.25,MILK)
    things=[]
    far=24 if front==2 else (64 if detail else 33)
    def add(bx,bz,kind,i,r):
        u,d=uv(cam,bx,bz)
        if -r<d<far and abs(u)<1.4*max(0,d)+r:
            things.append((d,kind,i,bx,bz,u))
    for i in range(len(BLOCKS)):
        b=BLOCKS[i]
        add(b[0],b[1],0,i,8)
    for i in range(len(NAMES)):
        bx,bz=door(i)
        add(bx-1.4,bz,1,i,1)
        bx,bz=center(i)
        if detail or abs(x-bx)+abs(z-bz)<24:
            add(bx-5,bz+4,2,i,2)
    for i in range(3):
        if not (s['records'] & (1<<i)):
            bx,bz=RECORDS[i]
            add(bx,bz,3,i,1)

    for j in range(3):
        bx,bz=center((1,5,10)[j])
        bx+=6*sin(s['clock']*0.5+j)
        add(bx,bz-4,7,j,1)
    if 0<=ix<=96 and 0<=iz<=64:
        add(ix+4,iz+4,9,0,1)
        add(ix-4,iz-4,9,1,1)
    if x>78:
        for i,ramp in enumerate(RAMPS):
            add(ramp[0]-4,ramp[1]+3,10,i,2)
    if s['heat']>0: add(s['px'],s['pz'],8,0,2)
    add(s['cx'],s['cz'],4,0,2)
    for i,p in enumerate(traffic(s['clock'])):
        add(p[0],p[1],5,i,2)
    if s['race']>=0:
        bx,bz=center(GATES[s['race']])
        add(bx,bz,6,0,2)
    things.sort()
    for d,k,i,bx,bz,u in reversed(things):
        if k==0:
            building(cam,BLOCKS[i])
            continue
        if d<1.5 or (k==4 and s['drive']):
            continue
        px=int(160+121*u/d)
        py=int(68+121*(cam[4]-road_height(bx,bz))/d)
        h=max(5,int(245/d))
        if k==10:
            title=("NORTHGATE","EAST DOCKS","SOUTHBANK")[i]
            if 60<px<260 and 34<py-h<166:
                box(STEEL,px-1,py-h,2,h)
                box((25,89,71),px-56,py-h-17,112,18)
                label(MILK,px-52,py-h-2,title)
                arrow(px+46,py-h-8,"UP",MILK)
        elif k==9:
            signal(px,py,h,(int(s['clock']//8)+i)%3)
        elif k==1:
            person(px,py,h,TRIM[i%4],0,False)
            if i==goal(s) or (s['stage']==4 and i==9):
                disc(GOLD,px,py-h-5,3)
        elif k==7:
            person(px,py,h,TRIM[i],s['clock']*4,False)
        elif k==8:
            car(px,py,max(5,int(330/d)),STEEL,False)
            box(PINK if int(s['clock']*5)%2 else BLUE,px-2,py-h//2,5,2)
        elif k==2:
            palm(px,py,max(6,int(500/d)),NIGHT)
        elif k==3:
            disc(GOLD,px,py-h//2,max(2,h//4))
            disc(INK,px,py-h//2,max(1,h//12))
        elif k==6:
            color(GOLD)
            draw.draw_circle(px,py-h//2,max(4,h//2))
        else:
            tint=PAINT[s['paint']] if k==4 else (PINK,GOLD)[i]
            angle=s['parkangle'] if k==4 else (1.5708 if i==0 else 0)
            if abs(sin(angle-s['angle']))>0.66:
                sidecar(px,py,max(4,int(390/d)),tint)
            else: car(px,py,int(330/d),tint,False)
    if s['drive']:
        car(160,142,67,PAINT[s['paint']],detail)
    else:
        person(160,137,46,COATS[s['coat']],s['stride'],True)
    box(INK,0,0,320,21)
    label(MINT,4,19,NAMES[district(x,z)])
    heading=int((s['angle']%TAU)*8/TAU+0.5)%8
    label(MILK,174,19,("N","NE","E","SE","S","SW","W","NW")[heading])
    label(MILK,211,19,WEATHER[front])
    label(SUN,273,19,'$'+str(s['cash']))
    box(INK,0,167,320,43)
    route=gps(s)
    parts=route.split()
    if len(parts)>2:
        arrow(216,178,parts[-2],SUN)
        route=" ".join(parts[:-2])[:17]+" "+parts[-1]
    label(SUN,5,186,route)
    if s['heat']>0: label(PINK,228,186,'ALERT '+str(int(s['heat'])))
    k,i=closest(s)
    hint="2nd map / ALPHA journal"
    if s['drive']: hint="ENTER park / arrows drive"
    elif k=='door':
        hint="ENTER "+VENUES[i]
        if i==7 and s['stage']!=1: hint="ENTER fish at Sun Pier"
        if i==0 and s['stage']>0: hint="ENTER safehouse / rest"
        if i==9 and s['stage']!=4: hint="ENTER play pool"
        if i==10: hint="ENTER gym / mini golf"
    elif k=='disc': hint="ENTER collect record"
    elif k=='local': hint='ENTER talk to local'
    elif k=='car': hint="ENTER drive coupe"
    label(MILK,5,207,s['msg'] if s['ttl']>0 else hint)


def overpass(cam,z):
    face(cam,((139,0,-8),(139,0,76),(139,4,76),(139,4,-8)),STEEL)
    face(cam,((139,4,-8),(149,4,-8),(149,4,76),(139,4,76)),ASPHALT)
    face(cam,((143.85,4.03,-8),(144.15,4.03,-8),
              (144.15,4.03,76),(143.85,4.03,76)),SUN)
    for edge in (139.55,148.25):
        face(cam,((edge,4.03,-8),(edge+.2,4.03,-8),
                  (edge+.2,4.03,76),(edge,4.03,76)),MILK)
    for a,b,u,v in RAMPS:
        if abs(z-b)<48:
            face(cam,((a,0,b-3),(u,4,v-3),(u,4,v+3),(a,0,b+3)),ASPHALT)
            face(cam,((a,.03,b),(u,4.03,v),(u,4.03,v+.28),(a,.03,b+.28)),SUN)

def signal(x,y,h,phase):
    width=max(2,h//4)
    lamp=max(1,h//12)
    box(STEEL,x-1,y-h,2,h)
    box(INK,x-width,y-h-3*lamp,2*width,6*lamp)
    box((RED,SUN,MINT)[phase],x-lamp,y-h+(phase*2-3)*lamp,2*lamp,lamp)


def arrow(x,y,direction,c):
    if direction=="HERE":
        disc(c,x,y,3)
        return
    dx,dy=(1,0) if direction=="R" else ((-1,0) if direction=="L" else
          ((0,1) if direction=="TURN" else (0,-1)))
    poly(c,[x+6*dx,x-4*dx-4*dy,x-4*dx+4*dy],
           [y+6*dy,y-4*dy+4*dx,y-4*dy-4*dx])
