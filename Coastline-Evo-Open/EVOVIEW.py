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
    pts2=[]
    for x,y,z in pts:
        u,d=uv(cam,x,z)
        pts2.append((u,y,d))
    xs=[]
    ys=[]
    a=pts2[-1]
    for b in pts2:
        if (a[2]>=1)!=(b[2]>=1):
            f=(1-a[2])/(b[2]-a[2])
            xs.append(int(160+121*(a[0]+f*(b[0]-a[0]))))
            ys.append(int(68+121*(3.4-a[1]-f*(b[1]-a[1]))))
        if b[2]>=1:
            xs.append(int(160+121*b[0]/b[2]))
            ys.append(int(68+121*(3.4-b[1])/b[2]))
        a=b
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
                sy=int(68+121*(3.4-h+1.2)/dep)
                if 0<=sx<=320-10*len(SIGNS[n]) and 18<sy<172:
                    box(INK,sx-2,sy-17,10*len(SIGNS[n])+4,16)
                    label(MILK,sx,sy,SIGNS[n])
        elif n<0:
            for y in range(2,int(h)-1,3):
                panel(l+0.6,r-0.6,y,y+0.45,STEEL)
    if h<3.4:
        face(cam,((l,h,a),(r,h,a),(r,h,f),(l,h,f)),c)

def sample(buffer):
    if buffer is not None and len(buffer)<4:
        key=get_key(0)
        if key:
            buffer.append(key)

def render(s,buffer=None):
    x,z=s['x'],s['z']
    f,c=sin(s['angle']),cos(s['angle'])
    cam=(x-6*f,z-6*c,f,c)
    night=int(s['clock']//90)%2
    box((48,49,87) if night else (102,80,130),0,0,320,35)
    box((91,77,122) if night else (202,115,143),0,35,320,33)
    sx=int(160+140*sin(1-s['angle']))
    disc(MILK if night else SUN,sx,41,10 if night else 15)
    for j in range(13 if s['detail'] else 5):
        px=(j*37-int(s['angle']%TAU*320/TAU))%352-16
        h=4+(j*17)%14
        box(NIGHT if night else VIOLET,px,68-h,12+j%5,h)
        if j%3==0: box(SUN,px+3,69-h,4,2)
    box((54,99,132),0,68,320,120)
    for j in range(3):
        box((110,151,166),j*94+14,72+j*3,32-j*4,1)
    ground(cam,-10,-10,120,88,TILE)
    sample(buffer)
    # Continuous road network and sidewalks.
    for i in range(4):
        a=i*32
        if abs(x-a)<48:
            ground(cam,a-4.5,-10,9,88,WALK)
    for i in range(3):
        a=i*32
        if abs(z-a)<48:
            ground(cam,-10,a-4.5,120,9,WALK)
    for i in range(4):
        a=i*32
        if abs(x-a)<48:
            ground(cam,a-3,-10,6,88,ASPHALT)
    for i in range(3):
        a=i*32
        if abs(z-a)<48:
            ground(cam,-10,a-3,120,6,ASPHALT)
    sample(buffer)
    # Short paint dashes mark the closest avenues.
    ix=int((x+16)//32)*32
    iz=int((z+16)//32)*32
    for off in ((-12,-4,4,12) if s['detail'] else ()):
        if -8<=iz+off<=75 and 0<=ix<=96:
            ground(cam,ix,iz+off,0.12,1.8,SUN)
        if -8<=ix+off<=105 and 0<=iz<=64:
            ground(cam,ix+off,iz,1.8,0.12,SUN)
    things=[]
    far=64 if s['detail'] else 33
    def add(bx,bz,kind,i,r):
        u,d=uv(cam,bx,bz)
        if -r<d<far and abs(u)<1.4*max(0,d)+r:
            things.append((d,kind,i,bx,bz))
    for i in range(len(BLOCKS)):
        b=BLOCKS[i]
        add(b[0],b[1],0,i,8)
    for i in range(12):
        bx,bz=door(i)
        add(bx-1.4,bz,1,i,1)
        bx,bz=center(i)
        add(bx-5,bz+4,2,i,2)
    for i in range(3):
        if not (s['records'] & (1<<i)):
            bx,bz=RECORDS[i]
            add(bx,bz,3,i,1)

    for j in range(3):
        bx,bz=center((1,5,10)[j])
        bx+=6*sin(s['clock']*0.5+j)
        add(bx,bz-4,7,j,1)
    if s['heat']>0: add(s['px'],s['pz'],8,0,2)
    add(s['cx'],s['cz'],4,0,2)
    for i,p in enumerate(traffic(s['clock'])):
        add(p[0],p[1],5,i,2)
    if s['race']>=0:
        bx,bz=center(GATES[s['race']])
        add(bx,bz,6,0,2)
    things.sort()
    for idx in range(len(things)-1,-1,-1):
        if idx%4==0: sample(buffer)
        d,k,i,bx,bz=things[idx]
        if k==0:
            building(cam,BLOCKS[i])
            continue
        if d<1.5 or (k==4 and s['drive']):
            continue
        u,d=uv(cam,bx,bz)
        px=int(160+121*u/d)
        py=int(68+411/d)
        h=max(5,int(245/d))
        if k==1:
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
        car(160,142,67,PAINT[s['paint']],True)
    else:
        person(160,137,46,COATS[s['coat']],s['stride'],True)
    box(INK,0,0,320,21)
    label(MINT,4,19,NAMES[district(x,z)])
    heading=int((s['angle']%TAU)*8/TAU+0.5)%8
    label(MILK,174,19,("N","NE","E","SE","S","SW","W","NW")[heading])
    label(SUN,253,19,'$'+str(s['cash']))
    box(INK,0,167,320,43)
    label(SUN,5,186,gps(s))
    if s['heat']>0: label(PINK,228,186,'ALERT '+str(int(s['heat'])))
    k,i=closest(s)
    hint="2nd map / ALPHA journal"
    if s['drive']: hint="ENTER park / arrows drive"
    elif k=='door': hint="ENTER "+VENUES[i]
    elif k=='disc': hint="ENTER collect record"
    elif k=='local': hint='ENTER talk to local'
    elif k=='car': hint="ENTER drive coupe"
    label(MILK,5,207,s['msg'] if s['ttl']>0 else hint)
