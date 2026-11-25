from COASTLIB import (BLOCKS,COATS,DOWN,EXIT,LEFT,MAP,NAMES,OK,RIGHT,ROAD,SKIN,UP,
    center,district,goal,keywait,notice,road_route,sin)
from COASTGEO import CHANNELS,BRIDGES,HIGHLIGHTS,PATCHES,furniture,KEYS,COVES,LAUNCH,CAPES,DRIVES
from COASTLIB import (INK,NIGHT,STEEL,SUN,GOLD,PINK,MINT,MILK,BLUE,SIGNS,
    box,color,disc,draw,label,line,palm,poly)
from COASTGEO import GLASS,BALCONY,DECO,DEPOT,COTTAGE,SILO,CABANA

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
            ys.append(int(cam[5]+121*(cam[4]-a[1]-f*(b[1]-a[1]))))
        if b[2]>=1:
            xs.append(int(160+121*b[0]/b[2]))
            ys.append(int(cam[5]+121*(cam[4]-b[1])/b[2]))
        a=b
    if len(xs)>=3 and max(xs)>=0 and min(xs)<320 and max(ys)>=0 and min(ys)<188:
        poly(c,xs,ys)

def ground(cam,x,z,w,d,c):
    face(cam,((x,0,z),(x+w,0,z),(x+w,0,z+d),(x,0,z+d)),c)


# Street-facing and shaded materials at each facade family.
FRONTS=(((69,156,169),(85,146,180),(75,120,157),(111,152,167)),
        ((224,182,162),(208,189,166),(213,156,150),(174,180,172)),
        ((236,156,156),(158,210,187),(239,191,135),(194,175,200)),
        ((152,111,89),(111,142,146),(171,137,97),(135,111,125)),
        ((194,151,120),(144,189,166),(160,169,123),(176,142,115)),
        ((170,162,153),(146,155,164),(202,178,133),(150,160,154)),
        ((230,143,120),(126,190,178),(222,180,112),(159,172,182)))
SIDES=((43,81,112),(132,119,139),(150,126,145),(88,88,106),
       (107,113,109),(102,114,133),(124,129,139))
NIGHT_WALL=((43,75,105),(97,91,124),(116,91,120),(62,66,88),
            (69,84,92),(81,89,109),(92,96,117))
NIGHT_SIDE=((36,52,81),(73,66,96),(83,68,98),(50,50,68),
            (49,62,67),(55,65,87),(68,70,87))
TERRAIN=((142,159,154),(159,143,130),(159,181,145),(239,207,154),
         (102,151,120),(119,149,120),(159,169,112))
WATER=(45,128,156)
SHALLOW=(85,166,171)

def point(cam,x,h,z):
    u,d=uv(cam,x,z)
    if d<1:return None
    return int(160+121*u/d),int(cam[5]+121*(cam[4]-h)/d)

def wall(cam,x1,z1,x2,z2,lo,hi,c):
    face(cam,((x1,lo,z1),(x2,lo,z2),(x2,hi,z2),(x1,hi,z1)),c)

def segment(cam,x1,h1,z1,x2,h2,z2,c):
    p=point(cam,x1,h1,z1)
    q=point(cam,x2,h2,z2)
    if p and q:line(c,p[0],p[1],q[0],q[1])

def shell(cam,x,z,w,d,lo,hi,front,side,roof):
    sx=x-w if cam[0]<x else x+w
    fz=z-d if cam[1]<z else z+d
    if abs(cam[0]-x)>w:wall(cam,sx,z-d,sx,z+d,lo,hi,side)
    if abs(cam[1]-z)>d:wall(cam,x-w,fz,x+w,fz,lo,hi,front)
    if cam[4]>hi:
        face(cam,((x-w,hi,z-d),(x+w,hi,z-d),(x+w,hi,z+d),(x-w,hi,z+d)),roof)
    return sx,fz

def building(cam,b,depth,detail,night,fog):
    x,z,w,d,h,kind,tint,n=b
    front=NIGHT_WALL[kind] if night else FRONTS[kind][tint]
    side=NIGHT_SIDE[kind] if night else SIDES[kind]
    if fog and depth>22:front,side=(143,158,165),(121,140,152)
    trim=(MINT,GOLD,PINK,MILK)[tint]
    if kind in (GLASS,BALCONY) and depth>60:front,side=(98,127,151),(82,104,135)
    sx,fz=shell(cam,x,z,w,d,0,h,front,side,front)
    if depth < -max(w,d):return
    close=detail and depth<37
    facade=abs(cam[1]-z)>d
    flank=abs(cam[0]-x)>w
    light=(255,208,130) if night else (181,221,211)
    if kind in (GLASS,BALCONY):
        if kind==GLASS and facade and depth<65:
            # The slanted reflection stays on the surface as the camera turns.
            glint=(77,111,146) if night else (123,184,193)
            face(cam,((x-w*.80,h*.21,fz),(x-w*.38,h*.20,fz),
                      (x+w*.58,h*.88,fz),(x+w*.17,h*.88,fz)),glint)
        # Stepped crowns, blades and balconies read even on the fast setting.
        crown=h*(.19 if kind==GLASS else .09)
        shell(cam,x,z,w*.64,d*.68,h,h+crown,front,side,front)
        if kind==GLASS and tint%2==1:
            segment(cam,x,h+crown,z,x,h+crown+3,z,trim)
        rows=6 if close else (3 if depth<57 else 1)
        band=light if night else ((129,195,202) if kind==GLASS else (250,222,193))
        for row in range(rows):
            y=h*(row+1)/(rows+1)
            if facade:
                if night and row%2:
                    wall(cam,x-w*.76,fz,x+w*.11,fz,y,y+.4,band)
                else:wall(cam,x-w,fz,x+w,fz,y,y+(.35 if kind==GLASS else .66),band)
            if flank and (kind==BALCONY or close):
                wall(cam,sx,z-d,sx,z+d,y,y+.30,(79,125,149) if kind==GLASS and not night else band)
        if close and kind==BALCONY and facade:
            for off in (-.7,-.1,.5):
                wall(cam,x+w*off,fz,x+w*(off+.26),fz,h*.62,h*.73,NIGHT if not night else SUN)
        if kind==GLASS and close:
            if facade:
                for off in (-.48,.22,.63):
                    segment(cam,x+w*off,1,fz,x+w*off,h,fz,side)
            if flank:segment(cam,sx,.5,z,sx,h,z,light)
    elif kind==DECO:
        shell(cam,x,z,w*.66,d*.80,h,h+.85,front,side,front)
        shell(cam,x,z,w*.23,d*.84,h+.85,h+1.65,trim,side,trim)
        if facade:
            for y in (h*.52,h*.79):
                wall(cam,x-w,fz,x+w,fz,y,y+.34,trim)
            if close:
                segment(cam,x,h*.5,fz,x,h+1,fz,MILK)
                for off in (-.62,.62):
                    p=point(cam,x+w*off,h*.69,fz)
                    if p:disc(NIGHT,p[0],p[1],max(1,min(6,int(24/max(1,depth)))))
        if flank:
            wall(cam,sx,z-d,sx,z+d,h*.79,h*.79+.34,trim)
            if close:
                for off in (-.65,-.12,.42):
                    wall(cam,sx,z+d*off,sx,z+d*(off+.30),h*.42,h*.64,side if night else (78,124,138))
    elif kind in (COTTAGE,CABANA,DEPOT):
        rise=1.65 if kind!=DEPOT else .9
        # Ridge runs along the street. Stilt huts and workshops have tin roofs.
        face(cam,((x-w-.35,h,fz),(x+w+.35,h,fz),(x+w+.35,h+rise,z),
                  (x-w-.35,h+rise,z)),(114,104,119) if kind==DEPOT else (143,106,95))
        if flank:face(cam,((sx,h,z-d),(sx,h+rise,z),(sx,h,z+d)),trim)
        if kind==DEPOT and facade:
            for off in (-.56,.35):wall(cam,x+w*off,fz,x+w*(off+.44),fz,0,h*.56,side)
        if kind==CABANA and facade:
            wall(cam,x-w*.88,fz,x+w*.88,fz,0,h*.34,side)
            wall(cam,x-w,fz,x+w,fz,h*.50,h*.64,trim)
    elif kind==SILO:
        for off in (-.57,.33):
            shell(cam,x+off*w,z,w*.27,d*.71,h,h+2.4,front,side,trim)
    if n>=0 and cam[1]<z-d and depth<43:
        wall(cam,x-.85,fz,x+.85,fz,0,2.4,INK)
        if close:
            wall(cam,x-w+.35,fz,x-1.15,fz,.55,2.25,BLUE)
            wall(cam,x+1.15,fz,x+w-.35,fz,.55,2.25,BLUE)
            wall(cam,x-w,fz,x+w,fz,2.55,2.87,trim)
        p=point(cam,x,3.12,fz)
        if p and 4<depth<22:
            xx=p[0]-5*len(SIGNS[n])
            if 1<xx<318-10*len(SIGNS[n]) and 33<p[1]<160:
                box(INK,xx-2,p[1]-16,10*len(SIGNS[n])+4,17)
                label(MILK,xx,p[1],SIGNS[n])

def prop(kind,px,py,scale,night):
    # Billboards stay anchored to the ground. Their width is in world units.
    unit=max(1,scale)
    def loc(a):return int(a*unit)
    def stroke(c,x,y,u,v):
        line(c,px+loc(x),py-loc(y),px+loc(u),py-loc(v))
    def panel(c,x,y,w,h):
        box(c,px+loc(x),py-loc(y),max(1,loc(w)),max(1,loc(h)))
    if kind==0:
        palm(px,py,loc(5.4),(42,83,81))
    elif kind==1:
        for a in (-1.1,0,1.1):stroke((80,75,68),a,0,0,2.3)
        for a,y in ((-.85,2.5),(.75,2.7),(0,3.2)):
            disc((48,91,77),px+loc(a),py-loc(y),max(2,loc(1.13)))
        disc((89,133,96),px-loc(.35),py-loc(3.55),max(1,loc(.65)))
    elif kind==2:
        panel((103,83,74),-.2,1.6,.4,1.6)
        for y in (1,2.5):
            poly((56,97,88),[px-loc(1.45),px,px+loc(1.45)],
                 [py-loc(y),py-loc(y+3),py-loc(y)])
    elif kind==3:
        for a in (-1.8,1.8):stroke(INK,a,0,a,7)
        stroke(GOLD,-2,6.7,5,8)
        stroke(GOLD,-2,7.5,5,8)
        stroke(INK,4.5,7.9,4.5,4.2)
        panel((205,108,88),3.5,4.5,2.1,1)
        stroke(STEEL,-1.8,1,1.8,5.5)
    elif kind==4 or kind==6:
        width=1.45 if kind==4 else 3
        h=2.25 if kind==4 else 3.7
        for a in ((0,) if kind==4 else (-2.5,2.5)):stroke(INK,a,0,a,h)
        poly(PINK if kind==4 else MINT,[px-loc(width),px,px+loc(width)],
             [py-loc(h),py-loc(h+.8),py-loc(h)])
        if kind==6:
            panel((166,120,90),-3,1,6,.6)
            stroke(MILK,-2.5,2,2.5,2)
        else:
            stroke(MILK,-width,h,0,h+.8)
            panel((127,109,87),.6,.30,1.5,.24)
    elif kind==5:
        stroke(STEEL,0,0,0,4.8)
        stroke(STEEL,0,4.8,.9,4.8)
        panel(SUN if night else MILK,.58,4.8,.7,.25)
    elif kind==7:
        for a in (-1,1):stroke(INK,a*1.5,0,a*.9,5)
        panel((116,172,161),-1.6,7,3.2,2.7)
        poly(SUN,[px-loc(1.8),px,px+loc(1.8)],[py-loc(7),py-loc(8),py-loc(7)])
    else:
        for a in (-1,.3,1.25):stroke((102,107,76),a,0,a+.2,1.2)

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

# Five rows of navigational lettering, three bits per row.
CHART_ALPHA=" ABEFGKLNORSTUY"
CHART_GLYPH=(0, 11245, 27566, 31143, 31140, 14699, 23469, 18727, 24573, 11114, 27565, 14478, 29842, 23407, 23186)

def chart(x,y,word):
    for c in word:
        bits=CHART_GLYPH[CHART_ALPHA.index(c)]
        for row in range(5):
            for col in range(3):
                if bits&(1<<(14-row*3-col)):
                    box((156,202,201),x+col,y+row,1,1)
        x+=4

def atlas(s):
    pin=district(s['x'],s['z'])
    zoom=False
    while True:
        if zoom:
            scale=3.65
            cx,cz=center(pin)
        else:
            scale=1.50
            cx,cz=86,35
        def pos(x,z):
            return int(160+(x-cx)*scale),int((102 if zoom else 96)-(z-cz)*scale*.77)
        def land(a,b,w,h,paint):
            left,top=pos(a,b+h)
            right,bottom=pos(a+w,b)
            box(paint,left,top,max(1,right-left),max(1,bottom-top))
        def marker(n,col,r):
            a,b=pos(*center(n))
            if -r<a<320+r and 20-r<b<169+r:disc(col,a,b,r)
        box((33,73,94),0,0,320,210)
        def outline(points,c):
            xy=[pos(x,z) for x,z in points]
            poly(c,[q[0] for q in xy],[q[1] for q in xy])
        land(-14,-14,160,96,(55,114,130))
        land(139,20,36,28,(55,114,130))
        land(-10,-10,152,88,(118,143,133))
        land(142,24,29,20,TERRAIN[3])
        for j,(_,_,_,_,points) in enumerate(CAPES):
            outline(points,TERRAIN[(3,4,0,5)[j]])
        for a,b,w,h,i in PATCHES:land(a,b,w,h,TERRAIN[i])
        for a,b,w,h,points in COVES:outline(points,(53,111,127))
        for a,b,w,h,points in KEYS:
            cx1,cz1=a+w*.5,b+h*.5
            outline([(cx1+(u-cx1)*1.3,cz1+(v-cz1)*1.5) for u,v in points],(55,114,130))
            outline(points,(223,198,145))
            outline([(cx1+(u-cx1)*.73,cz1+(v-cz1)*.64) for u,v in points],(103,143,113))
        for a,b,w,h in CHANNELS:land(a,b,w,h,(51,104,121))
        for a,b,w,h in BRIDGES:land(a,b,w,h,MILK)
        for i in range(5):land(i*32-2,-10,4,88,(69,80,94))
        for i in range(3):land(-10,i*32-2,181 if i==1 else 152,4,(69,80,94))
        for j,path in enumerate(DRIVES):
            u,v=pos(*path[0])
            for px,pz in path[1:]:
                a,b=pos(px,pz)
                line((90,88,92) if j==0 else (160,136,98),u,v,a,b)
                u,v=a,b
        land(78,70.3,39,1.4,(163,105,83))
        land(95,70.3,3,7.7,(163,105,83))
        inks=((50,92,114),(120,106,123),(180,104,121),(106,93,101),
              (91,109,99),(121,115,100),(172,119,102))
        for x,z,w,h,height,kind,tint,n in BLOCKS:
            land(x-w,z-h,2*w,2*h,inks[kind])
            if height>=14:land(x-w,z+h-.8,2*w,.8,(211,232,206))
        for x,z,kind in furniture():
            if kind in (0,1,2) and zoom:
                a,b=pos(x,z)
                if 0<a<320 and 21<b<169:disc((57,99,86),a,b,2)
        if not zoom:
            chart(49,28,"TERN KEYS")
            chart(3,114,"GULF")
            chart(257,147,"OUTER BAY")
        for u,v in LAUNCH:
            a,b=pos(u,v)
            if 2<a<317 and 28<b<161:
                line(MILK,a,b-2,a,b+2)
                line(MILK,a-2,b,a,b+2)
                line(MILK,a,b+2,a+2,b)
        target=goal(s)
        if target>=0:
            a,b=pos(s['x'],s['z'])
            for x,z in road_route(s,target):
                h,j=pos(x,z)
                line(GOLD,a,b,h,j)
                a,b=h,j
        for i in range(len(NAMES)):marker(i,INK,3 if zoom else 2)
        if target>=0:marker(target,GOLD,4)
        if s['stage']==9:marker(9,GOLD,4)
        a,b=pos(s['cx'],s['cz'])
        box(PINK,a-2,b-2,5,5)
        a,b=pos(s['x'],s['z'])
        if -3<a<323 and 18<b<175:
            disc(INK,a,b,4)
            disc(MILK,a,b,2)
        a,b=pos(*center(pin))
        color(MINT)
        draw.draw_circle(a,b,8)
        box(INK,0,0,320,24)
        label(MINT,5,21,"COASTLINE")
        label(MILK,114,21,"DISTRICT" if zoom else "REGION")
        label(SUN,266,21,"N ^")
        box(INK,0,166,320,44)
        label(MILK,5,185,NAMES[pin]+" / "+HIGHLIGHTS[pin])
        label(MINT,5,207,"DEL zoom  ENTER pin  CLR back")
        k=keywait((UP,DOWN,LEFT,RIGHT,MAP,OK,EXIT,23))
        if k in (MAP,EXIT):return
        if k==23:zoom=not zoom
        elif k==OK:
            s['pin']=pin
            notice(s,'Pinned '+NAMES[pin])
            return
        else:
            x,z=center(pin)
            x+=32*((k==RIGHT)-(k==LEFT))
            z+=32*((k==UP)-(k==DOWN))
            for i in range(len(NAMES)):
                if center(i)==(x,z):pin=i;break
