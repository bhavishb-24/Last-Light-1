# LAST LIGHT - an original TI-84 Evo driving game
import ti_draw as draw
from ti_system import get_key
from time import monotonic
from math import sin

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
       "Foundry","Velvet Club","Palms","The Lido")
# North, east, south, west. A dot marks the city boundary.
LINKS=(".14.",".250",".3.1","..72","058.","1694",
       ".7A5","3.B6","49..","5A.8","6B.9","7..A")
TARGETS=(7,8,2,11)
CARGO=("Film reels","Stage lights","Master tape","Aftershow kit")
ARROWS=(25,26,34,24)
BEARING=("N","E","S","W")
LENGTH=400

def neighbor(n,h):
    c=LINKS[n][h]
    if c==".":
        return -1
    return "0123456789AB".index(c)

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

def landmark(n):
    # Draw once per block. Each silhouette belongs to its destination.
    x=73 if n%2 else 238
    if n in (0,3,7,11):
        if n==7 or n==11:
            # Pier wheel: eight rim segments, gondolas and an A-frame.
            xs=[x,x+13,x+19,x+13,x,x-13,x-19,x-13]
            ys=[27,33,46,59,65,59,46,33]
            for j in range(8):
                k=(j+1)%8
                line(INK,xs[j],ys[j],xs[k],ys[k])
                line(VIOLET,x,46,xs[j],ys[j])
                box(GOLD,xs[j]-2,ys[j]+1,4,3)
            line(INK,x,46,x-9,82)
            line(INK,x,46,x+9,82)
        else:
            box(INK,x-3,43,5,39)
            poly(NIGHT,[x-16,x+27,x+26,x-16],[43,29,35,49])
            line(INK,x,42,x+24,33)
            line(INK,x+23,35,x+23,52)
            box(GOLD,x+21,52,4,3)
    elif n in (2,5,6):
        box(INK,x-15,58,30,24)
        box(NIGHT,x-11,48,22,12)
        box(INK,x-6,43,12,7)
        line(MILK,x,43,x,26)
        disc(PINK,x,25,2)
        for y in range(55,81,5):
            box(MINT,x-8,y,16,2)
    else:
        box(INK,x-21,60,42,22)
        box(NIGHT,x-12,53,25,8)
        box(PINK,x-20,63,40,2)
        box(GOLD,x-20,69,40,2)
        for j in range(3):
            box(VIOLET,x-14+j*12,74,6,8)

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

def road_x(vx,bend,a):
    # The bend is strongest at the horizon and vanishes at the car.
    depth=max(0,80-a)
    return vx+bend*depth*depth//6400

def ribbon(c,vx,bend,width):
    depths=(0,12,30,54,82,104)
    xs=[]
    ys=[]
    for a in depths:
        xs.append(road_x(vx,bend,a)-1-a*width//100)
        ys.append(84+a)
    for j in range(5,-1,-1):
        a=depths[j]
        xs.append(road_x(vx,bend,a)+1+a*width//100)
        ys.append(84+a)
    poly(c,xs,ys)

def terrain(kind,pos,lane,bend):
    # Keep the skyline in display memory. Only repaint below it.
    vx=160-int(lane*10)
    land=((64,138,153),(106,83,102),(64,127,116))[kind]
    box(land,0,84,320,104)
    if kind==0:
        poly((76,116,132),[0,82,126,102,40,0],[86,84,85,88,90,94])
        for i in range(3):
            box((143,182,179),12+i*105,92+i*8,53-i*8,2)
    ribbon(STEEL,vx,bend,278)
    ribbon(ROAD,vx,bend,255)
    for i in range(5):
        z=18+i*32-(pos%32)
        if z<12:
            continue
        a=1280//z
        b=1280//(z+10)
        near=road_x(vx,bend,a)
        far=road_x(vx,bend,b)
        for side in (-1,1):
            x=near+side*a*4//5
            u=far+side*b*4//5
            line(MILK,x,84+a,u,84+b)
        # Raised curbs with repeating coral blocks.
        for side in (-1,1):
            poly(PINK,[near+side*a*255//100,near+side*a*277//100,
                       far+side*b*277//100,far+side*b*255//100],
                      [84+a,84+a,84+b,84+b])
    if pos>320:
        depth=LENGTH-pos+16
        a=1280//depth
        b=1280//(depth+4)
        near=road_x(vx,bend,a)
        far=road_x(vx,bend,b)
        for k in range(-3,4):
            poly(MILK,[near+(k*8-2)*a//13,near+(k*8+2)*a//13,
                       far+(k*8+2)*b//13,far+(k*8-2)*b//13],
                      [84+a,84+a,84+b,84+b])
    for i in range(3,-1,-1):
        z=17+i*50-(pos%50)
        if z<16:
            continue
        a=1280//z
        side=1 if (i+pos//50)%2 else -1
        x=road_x(vx,bend,a)+side*a*3
        y=84+a
        if -20<x<340:
            if kind==2:
                palm(x,y,max(8,a*3//4),NIGHT)
            elif kind==1:
                w=max(4,a//2)
                box(NIGHT,x-w//2,y-a*2//3,w,a*2//3)
                box(GOLD,x-w//2,y-a//2,w,2)
                box(VIOLET,x-w//2,y-a//3,w,2)
            else:
                line(MILK,x,y,x,y-a//2)
                line(INK,x,y-a//2,x-side*a//4,y-a//2)
                box(SUN,x-side*a//4-1,y-a//2,4,2)
    return vx

def mapxy(n):
    return (35+(n%4)*83,60+(n//4)*39)

def chart(node,goal,dest,progress,choosing,job):
    box(INK,0,0,320,210)
    box(NIGHT,0,32,320,130)
    for n in range(12):
        x,y=mapxy(n)
        for h in (1,2):
            m=neighbor(n,h)
            if m>=0:
                u,v=mapxy(m)
                box(STEEL,x-1,y-1,u-x+3,v-y+3)
    # Route guidance is a shortest path; all streets are two-way.
    if goal>=0:
        n=dest if dest>=0 else node
        dist=[99]*12
        dist[goal]=0
        queue=[goal]
        for m in queue:
            for h in range(4):
                q=neighbor(m,h)
                if q>=0 and dist[q]==99:
                    dist[q]=dist[m]+1
                    queue.append(q)
        while n!=goal:
            for h in range(4):
                m=neighbor(n,h)
                if m>=0 and dist[m]<dist[n]:
                    x,y=mapxy(n)
                    u,v=mapxy(m)
                    line(MINT,x,y,u,v)
                    n=m
                    break
    for n in range(12):
        x,y=mapxy(n)
        disc(INK,x,y,5)
        disc(STEEL,x,y,2)
    if goal>=0:
        x,y=mapxy(goal)
        poly(GOLD,[x,x+7,x,x-7],[y-8,y,y+8,y])
    x,y=mapxy(node)
    if dest>=0:
        u,v=mapxy(dest)
        x+=int((u-x)*progress/LENGTH)
        y+=int((v-y)*progress/LENGTH)
    disc(MILK,x,y,4)
    label(MINT,8,23,NAMES[node])
    label(MILK,240,23,"NORTH ^")
    if goal>=0:
        label(SUN,8,51,str(job+1)+"/4  "+CARGO[job])
    label(GOLD,8,181,("TO "+NAMES[goal]) if goal>=0 else "FREE DRIVE")
    if choosing:
        ways=""
        for h in range(4):
            if neighbor(node,h)>=0:
                ways+=BEARING[h]+" "
        label(MILK,8,205,"Arrow to drive: "+ways)
    else:
        label(MILK,8,205,"ENTER resume")

def street_kind(a,b):
    if a%4==3 or b%4==3:
        return 0
    if min(a,b)>=8 or max(a,b)==10:
        return 2
    return 1

def traffic_for(a,b):
    seed=a*13+b*7
    return [[80+i*68,(seed+i*2)%3-1,3+i%3] for i in range(4)]

def advance(cars,old,new,lane,dt):
    hit=False
    for t in cars:
        before=t[0]-old
        t[0]+=t[2]*dt
        if before>0 and t[0]<=new and abs(lane-t[1])<0.55:
            hit=True
    return hit

def frame(node,dest,kind,pos,lane,speed,cars,damage,head):
    bend=int(52*sin(pos*0.013)*(1 if (node+dest)%3 else -1))
    vx=terrain(kind,int(pos),lane,bend)
    for i in range(len(cars)-1,-1,-1):
        gap=cars[i][0]-pos
        if -2<gap<170:
            a=int(1280/(16+gap))
            x=road_x(vx,bend,a)+cars[i][1]*a*8//5
            car(x,84+a,max(5,a*3//4),(BLUE,GOLD,PINK,STEEL)[i],False)
    car(vx+int(lane*128),164,67,RED if damage else MINT,True)
    box(NIGHT,0,185,320,3)
    box(MINT,0,185,int(pos*320/LENGTH),3)
    box(INK,0,188,320,22)
    label(MINT,4,207,BEARING[head]+" "+NAMES[dest])
    if damage:
        label(PINK,208,207,"BUMP!")
    else:
        label(MILK,201,207,str(int(speed*2))+" KM/H")

def menu():
    skyline(1)
    landmark(7)
    terrain(0,23,0,-38)
    car(201,178,118,MINT,True)
    box(INK,8,14,119,41)
    label(SUN,17,35,"LAST LIGHT")
    box(PINK,18,43,87,3)
    box(INK,0,185,320,25)
    label(MILK,8,205,"ENTER shift    2nd free drive")

def card(title,a,b):
    box(INK,8,88,304,92)
    box(PINK,8,88,4,92)
    label(SUN,21,111,title)
    label(MILK,21,137,a)
    label(MINT,21,166,b)

def wait_for(keys):
    while True:
        k=get_key(0)
        if k==45 or k in keys:
            return k

def run():
    draw.clear()
    menu()
    k=wait_for((105,21))
    if k==45:
        return
    job=0 if k==105 else len(TARGETS)
    score=0
    bumps=0
    node=0
    card("LEFT/RIGHT lane   UP/DN gas","2nd map / CLEAR quit","ENTER to start")
    if wait_for((105,))==45:
        return
    while True:
        goal=TARGETS[job] if job<len(TARGETS) else -1
        if goal==node:
            earned=max(40,100-10*bumps)
            score+=earned
            card("DELIVERED  +$"+str(earned),CARGO[job]+" at "+NAMES[node],
                 "ENTER to collect")
            if wait_for((105,))==45:
                return
            job+=1
            bumps=0
            if job==len(TARGETS):
                card("SHIFT COMPLETE","Four drops / $"+str(score),"ENTER for free drive")
                if wait_for((105,))==45:
                    return
            continue
        chart(node,goal,-1,0,True,job)
        dest=-1
        while dest<0:
            k=wait_for(ARROWS)
            if k==45:
                return
            head=ARROWS.index(k)
            dest=neighbor(node,head)
        kind=street_kind(node,dest)
        skyline(node+head)
        landmark(dest)
        cars=traffic_for(node,dest)
        speed=24
        pos=0
        lane=0
        target=0
        damage=0
        last=monotonic()
        while pos<LENGTH:
            frame(node,dest,kind,pos,lane,speed,cars,damage,head)
            # Poll between frames. Bound catch-up on slower devices.
            while True:
                k=get_key(0)
                if k==45:
                    return
                if k==21:
                    chart(node,goal,dest,pos,False,job)
                    if wait_for((105,))==45:
                        return
                    skyline(node+head)
                    landmark(dest)
                    last=monotonic()
                    break
                if k==24:
                    target=max(-1,target-1)
                if k==26:
                    target=min(1,target+1)
                if k==25:
                    speed=min(48,speed+8)
                if k==34:
                    speed=max(8,speed-8)
                now=monotonic()
                if now-last>=0.09:
                    break
            now=monotonic()
            dt=min(0.22,max(0,now-last))
            last=now
            lane+=max(-4*dt,min(4*dt,target-lane))
            new=pos+speed*dt
            damage=max(0,damage-dt)
            if advance(cars,pos,new,lane,dt):
                speed=12
                damage=1
                bumps+=1
            pos=new
        node=dest

run()
