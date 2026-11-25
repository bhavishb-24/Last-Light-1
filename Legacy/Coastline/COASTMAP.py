from COASTGEO import CHANNELS, BRIDGES, PATCHES, furniture, HIGHLIGHTS, KEYS, COVES, CAPES, DRIVES
from COASTVUE import (atlas, building, person, face, ground, point, prop, segment, uv,
                      TERRAIN, SHALLOW, WATER)
from COASTLIB import (
    ASPHALT, BLOCKS, BLUE, CACHES, COATS, DOWN, EXIT,
    GOLD, INK, LEFT, LOTS, MAP, MILK, MINT,
    NAMES, NIGHT, OK, PAINT, PINK, RECORDS, RED,
    RIGHT, ROAD, SIGNS, SKIN, STEEL, SUN, TAU,
    TILE, TRIM, UP, VENUES, VIOLET, WALK, WEATHER,
    box, car, center, closest, color, cos, crew,
    disc, district, door, draw, gate, get_key, goal,
    gps, keywait, label, line, local_position, lot, notice,
    palm, poly, region, road_route, roadblock, sheet, sin,
    weather
)

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
    return ((-7+(t*5)%143,1.8),(94.2,74-(t*4)%83),
            (135+(t*3)%33,30.2),(126.2,2+(t*3.4)%62))

def sample(buffer):
    if buffer is not None and len(buffer)<4:
        key=get_key(0)
        if key:
            buffer.append(key)

def scenery(s,sx,lift):
    r=region(s)
    offset=int(s['angle']*52)
    for i in range(3):
        x=(i*113-offset)%365-23
        if r==5:
            poly((66,83,104),[x-53,x+8,x+71],[77+lift,49+lift+4*i,77+lift])
            poly((83,108,102),[x+8,x+18,x+71],[49+lift+4*i,65+lift,77+lift])
        elif r==1:
            poly(MILK,[x,x,x-9],[62+lift,74+lift,74+lift])
            poly(PINK,[x+2,x+2,x+8],[65+lift,74+lift,74+lift])
            box(NIGHT,x-10,74+lift,20,2)
        elif r in (2,4):
            for j in range(3):
                poly((59,97,89),[x+j*7-5,x+j*7,x+j*7+5],[77+lift,63+lift+j*2,77+lift])
    if r==2 and s['detail']:
        x=(sx+int(s['clock']*4))%284
        line(MILK,x,43+lift,x+5,46+lift)
        line(MILK,x+5,46+lift,x+11,42+lift)
    if crew(s)['zones'][r]>=4 and s['heat']:
        x=30+(int(s['clock']*12)%228)
        box(INK,x,38,13,5)
        box(INK,x-8,37,9,2)
        line(INK,x+5,38,x+5,34)
        line(NIGHT,x-5,34,x+15,34)
        box(SUN,x+10,40,3,2)

def render(s,buffer=None):
    x,z=s['x'],s['z']
    f,c=sin(s['angle']),cos(s['angle'])
    back=17 if s['craft']==2 else 6
    lift=31 if s.get('lookup') and not s['craft'] else 0
    horizon=77+lift
    altitude=s.get('alt',10) if s['craft']==2 else (1.6 if lift else 3.0)
    cam=(x-back*f,z-back*c,f,c,altitude,horizon)
    night=int(s['clock']//90)%2
    w=weather(s)
    sky=((102,80,130),(56,73,110),(117,126,147),(38,49,77),(146,90,101))[w]
    low=((206,104,138),(101,119,152),(164,174,183),(66,86,119),(240,162,109))[w]
    if w==0 and night: sky,low=(32,35,75),(102,73,127)
    elif w==0 and 18<s['clock']%180<72:
        sky,low=(57,134,184),(173,212,215)
    if w==3 and s['clock']%9<0.16: low=(177,188,213)
    band_h=horizon//4
    for j in range(4):
        tint=tuple((sky[i]*(3-j)+low[i]*j)//3 for i in range(3))
        box(tint,0,j*band_h,320,band_h+3)
    sx=int(160+140*sin(1-s['angle']))
    if w in (0,4):
        disc(MILK if night else SUN,sx,41+lift,10 if night else 15)
        if night and s['detail']:
            for j in range(8):
                box((154,164,197),(j*81+sx)%320,24+(j*13)%26,2,1)
        elif not night:
            for j in range(3):
                box(low,sx-16,43+lift+j*4,32,1+j//2)
    elif w!=2:
        for j in range(4):
            box(sky,(j*91+sx)%350-22,37+j%2*6,64,4)
    scenery(s,sx,lift)
    ocean=(35,73,101) if night else (WATER if w!=2 else (123,150,162))
    box(ocean,0,horizon,320,110)
    for j in range(3):
        box(SHALLOW if not night else STEEL,j*94+14,horizon+3+j*3,32-j*4,1)
    ground(cam,-10,-10,152,88,TILE if w!=2 else (124,144,152))
    ground(cam,142,24,29,20,TERRAIN[3])
    for j,(a,b,width,length,outline) in enumerate(CAPES):
        if abs(x-a-width/2)+abs(z-b-length/2)<78:
            face(cam,tuple((u,0,v) for u,v in outline),TERRAIN[(3,4,0,5)[j]] if not night else (80,101,105))
    for a,b,width,length,land in PATCHES:
        if abs(x-a-width*.5)<width*.5+42 and abs(z-b-length*.5)<length*.5+42:
            ground(cam,a,b,width,length,TERRAIN[land] if not night else (80,101,105))
    for a,b,width,length,outline in COVES:
        face(cam,tuple((u,0,v) for u,v in outline),ocean)
    for a,b,width,length,outline in KEYS:
        if abs(x-a-width/2)+abs(z-b-length/2)>98:continue
        face(cam,tuple((u,0,v) for u,v in outline),(221,201,151))
        cx,cz=a+width/2,b+length/2
        face(cam,tuple((cx+(u-cx)*.77,.08,cz+(v-cz)*.66) for u,v in outline),(109,151,113))
    for a,b,width,length in CHANNELS:
        ground(cam,a,b,width,length,ocean)
    # The promenade follows the north strand. A public pier projects over the sand.
    if 46<x<143 and z>35:
        ground(cam,78,70.3,39,1.4,(169,127,96))
        ground(cam,95,70.3,3,7.7,(190,148,111))
    for a,b,width,length in BRIDGES:
        ground(cam,a,b,width,length,WALK)
    road=ASPHALT if not w else ((76,88,113) if w!=2 else (102,116,128))
    sample(buffer)
    # Continuous road network and sidewalks.
    for i in range(5):
        a=i*32
        if abs(x-a)<48:
            ground(cam,a-4.5,-10,9,88,WALK)
    for i in range(3):
        a=i*32
        if abs(z-a)<48:
            ground(cam,-10,a-4.5,152,9,WALK)
    for i in range(5):
        a=i*32
        if abs(x-a)<48:
            ground(cam,a-3,-10,6,88,road)
    for i in range(3):
        a=i*32
        if abs(z-a)<48:
            ground(cam,-10,a-3,181 if i==1 else 152,6,road)
    sample(buffer)
    for j,path in enumerate(DRIVES):
        if abs(x-path[0][0])+abs(z-path[0][1])>48:continue
        px,pz=path[0]
        for x2,z2 in path[1:]:
            dx,dz=x2-px,z2-pz
            scale=(1.5 if j==0 else 1)/max(1,(dx*dx+dz*dz)**.5)
            ax,az=dz*scale,-dx*scale
            face(cam,((px-ax,0,pz-az),(px+ax,0,pz+az),
                      (x2+ax,0,z2+az),(x2-ax,0,z2-az)),road if j==0 else (165,139,100))
            px,pz=x2,z2
    # Short paint dashes mark the closest avenues.
    ix=int((x+16)//32)*32
    iz=int((z+16)//32)*32
    for off in ((-12,-4,4,12) if s['detail'] else ()):
        if -8<=iz+off<=75 and 0<=ix<=128:
            ground(cam,ix,iz+off,0.12,1.8,SUN)
        if -8<=ix+off<=(168 if iz==32 else 139) and 0<=iz<=64:
            ground(cam,ix+off,iz,1.8,0.12,SUN)
    if s['detail'] and ix in (0,32,64,96) and iz in (32,64):
        for stripe in (-2,-.7,.7,2):
            ground(cam,ix+stripe-.22,iz+4.9,.44,1.35,(210,205,185))
    things=[]
    far=28 if w==2 else (62 if s['detail'] else 33)
    def add(bx,bz,kind,i,r):
        u,d=uv(cam,bx,bz)
        if -r<d<far and abs(u)<1.4*max(0,d)+r:
            things.append((d,kind,i,bx,bz))
    for i,b in enumerate(BLOCKS):
        bx,bz,bw,bd,height,family,tint,venue=b
        u,dep=uv(cam,bx,bz)
        reach=(119 if s['detail'] else 94) if height>=14 and w!=2 else far
        radius=bw+bd
        if -radius<dep<reach and abs(u)<1.4*max(0,dep)+radius:
            things.append((dep,0,i,bx,bz))
    for a,b,width,length,outline in KEYS:
        add(a+width*.35,b+length*.52,14,0,3)
        add(a+width*.61,b+length*.55,14,1,3)
    for bx,bz,kind in furniture():
        if kind in (3,6,7,9) or (s['detail'] and abs(x-bx)+abs(z-bz)<44):
            add(bx,bz,14,kind,4)
    add(160,38,9,0,6)
    add(122,67,9,1,5)
    if s['detail']:
        for i in range(5):
            add(117+i*4,8+(i*7)%19,10,i,2)
    for i in range(len(NAMES)):
        bx,bz=door(i)
        add(bx-1.4,bz,1,i,1)
        bx,bz=center(i)
        add(bx-5,bz+4,2,i,2)
    for i,n in enumerate(LOTS):
        bx,bz=center(n)
        if abs(x-bx)<30 and abs(z-bz)<30 and not (s['drive'] and s['ride']==i):
            add(bx-3,bz+3,11,i,2)
    for j,(bx,bz) in enumerate(CACHES):
        if not s['loot']&(1<<j):add(bx,bz,13,j,1)
    for i in range(len(RECORDS)):
        if not (s['records'] & (1<<i)):
            bx,bz=RECORDS[i]
            add(bx,bz,3,i,1)
        
    for j in range(3):
        bx,bz=local_position(s,j)
        add(bx,bz,7,j,1)
    barrier=roadblock(s)
    if barrier: add(barrier[0],barrier[1],12,0,2)
    if s['heat']>0: add(s['px'],s['pz'],8,0,2)
    add(s['cx'],s['cz'],4,0,2)
    for i,p in enumerate(traffic(s['clock'])):
        add(p[0],p[1],5,i,2)
    if s['race']>=0:
        bx,bz=center(gate(s))
        add(bx,bz,6,0,2)
    things.sort()
    for idx in range(len(things)-1,-1,-1):
        if idx%4==0: sample(buffer)
        d,k,i,bx,bz=things[idx]
        if k==0:
            building(cam,BLOCKS[i],d,s['detail'],night,w==2)
            continue
        if d<1.5 or (k==4 and s['drive']):
            continue
        u,d=uv(cam,bx,bz)
        px=int(160+121*u/d)
        py=int(horizon+121*altitude/d)
        h=max(5,int(245/d))
        if k==14:
            if i==9:
                for zz in (28.4,35.6):
                    segment(cam,bx,0,zz,bx,5.1,zz,MILK)
                segment(cam,bx,5.1,28.4,bx,5.1,35.6,MINT)
                segment(cam,bx,4.1,28.4,bx,5.1,30.2,STEEL)
                segment(cam,bx,4.1,35.6,bx,5.1,33.8,STEEL)
            else:prop(i,px,py,121/d,night)
        elif k==1:
            person(px,py,h,TRIM[i%4],0,False)
            if i==goal(s) or (s['stage']==9 and i in (6,9)):
                disc(GOLD,px,py-h-5,3)
        elif k==7:
            person(px,py,max(4,h*(8+i)//9),TRIM[i],s['clock']*4,False)
        elif k==9:
            if i==0:
                height=int(1120/d)
                width=max(2,h//3)
                poly(MILK,[px-width,px+width,px+width//2,px-width//2],
                     [py,py,py-height,py-height])
                box(RED,px-width,py-height+height//3,width*2,2)
                box(NIGHT,px-width-1,py-height-4,width*2+2,5)
                box(SUN,px-width,py-height,width*2,3)
            else:
                height=max(3,int(850/d))
                line(NIGHT,px,py,px-2,py-height)
                line(NIGHT,px+4,py,px+2,py-height)
                line(PINK,px-2,py-height,px+2,py-height)
                disc(SUN,px,py-height-3,2)
        elif k==13:
            size=max(3,int(88/d))
            box(NIGHT,px-size,py-size,2*size,size)
            box(MINT,px-size,py-size,2*size,2)
            box(SUN,px,py-size,2,size)
        elif k==12:
            width=max(4,int(315/d))
            box(INK,px-width//2,py-4,width,4)
            for j in range(3):
                box(SUN,px-width//2+j*width//3,py-5,max(1,width//6),3)
        elif k==11:
            sidecar(px,py,max(5,int(330/d)),TRIM[i%4])
        elif k==10:
            for j in (-1,0,1):
                line((100,141,103),px,py,px+j*max(2,h//4),py-h//3)
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
            tint=PAINT[s['paint']] if k==4 else (PINK,GOLD,STEEL,BLUE)[i]
            angle=s['parkangle'] if k==4 else (1.5708 if i in (0,2) else 0)
            if abs(sin(angle-s['angle']))>0.66:
                sidecar(px,py,max(4,int(390/d)),tint)
            else: car(px,py,int(330/d),tint,False)
    if s['drive']:
        ride=s['ride']
        tint=PAINT[s['paint']]
        if ride in (6,7):
            width=20 if ride==6 else 9
            box(INK,160-width,130,7,12)
            box(INK,153+width,130,7,12)
            person(160,138,34,COATS[s['coat']],0,True)
            box(tint,150,126,20,8)
            box(RED,156,130,8,3)
        else:
            car(160,142,60 if ride==0 else 75,tint,True)
            if ride in (2,4): box(INK,131,126,58,3)
            if ride==5:
                box(tint,140,109,40,12)
                box(BLUE,145,111,30,7)
        if s['body']<40:
            for j in (0,1,2):
                disc(STEEL,174+j*2,110-j*4-(int(s['clock']*4)%3),2+j)
        if s['rescue']: box(SUN,164,119,5,3)
    elif not s['craft']:
        person(160,137-int(s['jump']*9),34 if s['stance']==2 else 44+crew(s)['weight']//2,COATS[s['coat']],s['stride'],True)
    h=crew(s)
    if not s['drive'] and not s['craft']:
        if h['tat']: box(PINK,150,117,2,3)
        if h['hair']: box(INK if h['style']==0 else VIOLET,157,104-int(s['jump']*9),8,2+h['hair'])
    if s['pair'] and not s['drive'] and not s['craft']: person(133,136,38,COATS[s['crew'][1-s['who']]['coat']],s['stride'],True)
    if w in (1,3):
        step=int(s['clock']*68)
        rain=(118,146,173) if w==1 else (133,159,193)
        for j in range(16 if s['detail'] else 8):
            px=(j*71-step)%320
            py=(j*31+2*step)%137+24
            line(rain,px,py,max(0,px-4),py+7)
    if s.get("panorama"):return
    box(INK,0,0,320,21)
    label(MINT,4,19,NAMES[district(x,z)])
    heading=int((s['angle']%TAU)*8/TAU+0.5)%8
    label(MILK,143,19,("N","NE","E","SE","S","SW","W","NW")[heading])
    label((175,188,208),178,19,WEATHER[w])
    label(SUN,253,19,'$'+str(s['cash']))
    box(INK,0,167,320,43)
    label(SUN,5,186,gps(s))
    stars=crew(s)['zones'][region(s)]
    if stars: label(PINK,260,186,'*'*stars)
    health=crew(s)['hp']
    box(INK,4,24,43,10)
    box(RED,6,26,max(1,39*health//(80+3*crew(s)['power'])),2)
    box(MINT,6,30,max(1,39*crew(s)['focus']//31),2)
    if s['drive']:
        box(INK,4,36,43,7)
        box(GOLD,6,38,max(1,int(s['fuel']*0.39)),2)
    # Corner radar: north up, white player, gold waypoint.
    box(INK,280,24,38,32)
    box(STEEL,282,39,34,1)
    box(STEEL,299,26,1,27)
    dest=goal(s)
    if dest>=0:
        ux,uz=door(dest)
        disc(GOLD,299+int(max(-16,min(16,(ux-x)*0.25))),39-int(max(-12,min(12,(uz-z)*0.25))),2)
    disc(MILK,299,39,2)
    k,i=closest(s)
    hint="DEL phone / MODE actions"
    if s['drive']: hint="ENTER park / "+str(int(abs(s['speed'])*4))+" km/h"
    elif lot(s)>=0: hint='DEL scan / MODE actions'
    elif k=='door': hint="ENTER "+VENUES[i]
    elif k=='cache': hint='ENTER open street cache'
    elif k=='disc': hint="ENTER collect record"
    elif k=='local': hint='ENTER talk to local'
    elif k=='car': hint="ENTER drive coupe"
    label(MILK,5,207,s['msg'] if s['ttl']>0 else hint)


def title_key():
    from COASTLIB import fresh
    scene=fresh()
    scene.update(x=63,z=27,angle=-.66,clock=12,craft=6,panorama=True)
    draw.clear()
    render(scene)
    box(INK,0,104,320,106)
    box(PINK,8,116,3,18)
    label(SUN,17,135,"LAST LIGHT / COASTLINE")
    label(MILK,12,161,"ENTER new story")
    label(MINT,12,183,"2nd load checkpoint")
    label(MILK,12,205,"CLEAR quit")
    return keywait((OK,MAP,EXIT))
