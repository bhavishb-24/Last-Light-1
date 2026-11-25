from EVODATA import *
from EVOVIEW import person,arrow
def map_point(x,z):
    return int(21+x*1.16),int(148-z*1.35)

def map_surface(left,top,right,bottom):
    box(INK,left,top,right-left,bottom-top)
    for i,(x,z,w,d) in enumerate(STREETS+((139,-8,10,84),)):
        a,b=map_point(x,z+d)
        u,v=map_point(x+w,z)
        a,b=max(a,left),max(b,top)
        u,v=min(u,right),min(v,bottom)
        if u>a and v>b:
            box((125,104,89) if i==len(STREETS) else ROAD,a,b,u-a,v-b)

def next_district(pin,key):
    x,z=center(pin)
    dx,dz=((1,0) if key==RIGHT else (-1,0) if key==LEFT else
           (0,1) if key==UP else (0,-1))
    choice=pin
    best=1000
    for n in range(len(NAMES)):
        u,v=center(n)
        across=abs((u-x)*dz-(v-z)*dx)
        forward=(u-x)*dx+(v-z)*dz
        cost=forward+across*3
        if forward>0 and across<=forward and cost<best:
            choice,best=n,cost
    return choice

def atlas(s):
    pin=district(s['x'],s['z'])
    while True:
        sheet("CITY ATLAS    N ^",(),"Arrows browse / ENTER pin")
        map_surface(0,44,320,165)
        for i in range(BUILDINGS):
            x,z,w,h,_,_,_,venue=building_at(i)
            a,b=map_point(x-w,z+h)
            u,v=map_point(x+w,z-h)
            box(VIOLET if venue>=0 else (70,79,88),a,b,max(1,u-a),max(1,v-b))
        for x,z,u,v in RAMPS:
            a,b=map_point(x,z)
            c,e=map_point(u,v)
            line(GOLD,a,b,c,e)
        for n in range(len(NAMES)):
            a,b=map_point(*center(n))
            disc(TRIM[n%4],a,b,3)
        n=goal(s)
        if n>=0:
            a,b=map_point(*center(n))
            disc(GOLD,a,b,6)
        a,b=map_point(s['cx'],s['cz'])
        box(PINK,a-2,b-2,5,5)
        a,b=map_point(s['x'],s['z'])
        disc(MILK,a,b,3)
        a,b=map_point(*center(pin))
        color(MINT)
        draw.draw_circle(a,b,8)
        label(MILK,10,179,NAMES[pin]+" / "+SIGNS[pin])
        k=keywait((UP,DOWN,LEFT,RIGHT,MAP,OK,EXIT))
        if k in (MAP,EXIT): return
        if k==OK:
            s['pin']=pin
            notice(s,'Pinned '+NAMES[pin])
            return
        pin=next_district(pin,k)

def shop(s,title,items):
    i=0
    info="UP/DOWN browse / ENTER buy"
    while True:
        box(NIGHT,0,0,320,210)
        box(VIOLET,0,39,320,85)
        box(INK,0,121,320,89)
        label(SUN,8,26,title)
        label(MILK,250,26,'$'+str(s['cash']))
        name,cost,kind,val=items[i]
        if kind=='paint': car(160,112,112,PAINT[val],True)
        elif kind in ('shoes','coat'): person(160,113,69,COATS[val] if kind=='coat' else COATS[s['coat']],0,True)
        else:
            box(INK,139,70,42,38)
            box(GOLD,146,55,28,35)
            box(MILK,152,60,5,14)
        label(MILK,8,144,name+'  $'+str(cost))
        label(MINT,8,169,info)
        label(MILK,8,203,"CLEAR leave")
        k=keywait((UP,DOWN,OK,EXIT))
        if k==EXIT: return
        if k in (UP,DOWN):
            i=(i+(1 if k==DOWN else -1))%len(items)
            info="UP/DOWN browse / ENTER buy"
        elif kind=='stage' and s['stage']!=2:
            info="No valve order today"
        elif s[kind]==val:
            info="Already equipped"
        elif pay(s,cost):
            s[kind]=val
            info="Fitted! CLEAR to leave"
            if kind=='stage':
                tell("THE VALVE",("The old signal tube glows.","Take it to FM Tower."))
                return
        else:
            info="Need more cash: try Dispatch"

def tune(bands=(5,2,7)):
    position=1
    locks=0
    while locks<3:
        target=bands[locks]
        sheet("FM / ALIGN BAND "+str(locks+1),("Match mint to gold.",),"L/R tune / ENTER lock")
        for i in range(9):
            box(GOLD if i==target else STEEL,25+32*i,96,4,16)
        box(MINT,21+32*position,116,12,7)
        k=keywait((LEFT,RIGHT,OK,EXIT))
        if k==EXIT: return False
        if k==LEFT: position=max(0,position-1)
        if k==RIGHT: position=min(8,position+1)
        if k==OK and position==target: locks+=1
    return True


def phone(s):
    selected=0
    apps=("GPS","Taxi","Deposit","Withdraw","Scanner","Delivery")
    hints=("Pin next objective","Ride to a district $6","Move cash to savings",
           "Move savings to cash","Locate parked coupe","Bring coupe here $5")
    while True:
        phone_screen(s,apps,hints,selected)
        k=keywait((UP,DOWN,LEFT,RIGHT,OK,EXIT))
        if k==EXIT:
            return
        if k!=OK:
            selected=(selected+{UP:-3,DOWN:3,LEFT:-1,RIGHT:1}[k])%6
            continue
        if selected==0:
            s['pin']=goal(s)
            notice(s,"Objective pinned" if s['pin']>=0 else "No active objective")
        elif selected==1:
            taxi(s)
        elif selected==4:
            n=district(s['cx'],s['cz'])
            tell("VEHICLE SCANNER",(NAMES[n],"Pink marker on the city map"))
        elif selected==5:
            deliver_coupe(s)
        else:
            source,target=('cash','bank') if selected==2 else ('bank','cash')
            amount=min(s[source],999-s[target])
            s[source]-=amount
            s[target]+=amount
            notice(s,"Transferred $"+str(amount))
        return

def taxi(s):
    if s['race']>=0 or s['heat'] or s['drive']:
        notice(s,"Taxi needs a safe stop on foot")
        return
    n=district(s['x'],s['z'])
    while True:
        sheet("COASTLINE TAXI",(NAMES[n],"Fare $6"),"UP/DOWN  ENTER  CLEAR back")
        k=keywait((UP,DOWN,OK,EXIT))
        if k==EXIT:
            return
        if k==OK:
            break
        n=(n+(1 if k==DOWN else -1))%len(NAMES)
    if pay(s,6):
        s['x'],s['z']=center(n)
        s['speed']=0
        notice(s,"Arrived at "+NAMES[n])
    else:
        notice(s,"Taxi fare is $6")


def street_map(s,previous):
    x,y=map_point(s['x'],s['z'])
    if previous is None:
        box(INK,0,0,320,210)
        map_surface(0,34,320,170)
        box(NIGHT,0,171,320,39)
        label(MINT,5,206,"2nd map / DEL phone / TRACE 3D")
    elif previous[:2]!=(x,y):
        px,py=previous[:2]
        map_surface(px-1,py-1,px+2,py+2)
    status=(district(s['x'],s['z']),s['cash'],s['drive'],gps(s))
    if previous is None or previous[:2]!=(x,y) or previous[2][2]!=s['drive']:
        box(GOLD if s['drive'] else MINT,x-1,y-1,3,3)
    if previous is None or previous[2]!=status:
        box(NIGHT,0,171,320,22)
        label(MILK,5,190,(NAMES[status[0]]+" $"+str(s['cash'])+" "+status[3])[:31])
    return x,y,status

def enter_room(s,n):
    # Position is local to the room. Leaving returns to the same street door.
    col,row=3,3
    accent=TRIM[n%4]
    country=n>=16
    while True:
        box(NIGHT,0,0,320,210)
        box((125,106,94) if country else VIOLET,0,29,320,67)
        box((122,110,92) if country else STEEL,0,96,320,87)
        label(SUN,8,22,VENUES[n])
        box(ROAD,91,83,138,19)
        box(accent,91,81,138,4)
        person(158,84,34,accent,0,False)
        for x in (15,252):
            box(INK,x,47,52,37)
            for j in range(3):
                box(accent,x+5,51+j*10,42-j*4,3)
        for v in range(107,180,18):
            line(ROAD,0,v,319,v)
        box(PINK,138,169,44,4)
        person(65+32*col,104+21*row,34,COATS[s['coat']],col,True)
        label(MILK,7,205,"ENTER counter / CLEAR exit" if row==0 else "ARROWS walk / CLEAR exit")
        k=keywait((UP,DOWN,LEFT,RIGHT,OK,EXIT))
        if k==EXIT:
            return False
        if k==OK and row==0:
            return True
        if k==UP: row=max(0,row-1)
        if k==DOWN: row=min(3,row+1)
        if k==LEFT: col=max(0,col-1)
        if k==RIGHT: col=min(6,col+1)

def deliver_coupe(s):
    if s['drive'] or s['race']>=0 or s['heat']:
        notice(s,"Delivery needs a safe stop")
        return
    x,z=s['x'],s['z']
    for dx,dz in ((2.7,0),(-2.7,0),(0,2.7),(0,-2.7)):
        u,v=x+dx,z+dz
        if blocked(u,v,0.85):
            continue
        if pay(s,5):
            s['cx'],s['cz']=u,v
            s['parkangle']=s['angle']
            s['speed']=0
            notice(s,"Coupe delivered nearby")
        else:
            notice(s,"Delivery costs $5")
        return
    notice(s,"No space to deliver here")


def radio_bulletin(s):
    if s['heat']:
        bulletin="Patrols active in your area."
    elif goal(s)>=0:
        bulletin="Crew heading to "+NAMES[goal(s)]
    else:
        bulletin="Sun Pier fishing is open."
    tell("WAVE / LOCAL RADIO",(bulletin,"Now: "+WEATHER[weather(s)],
                              "Next: "+WEATHER[(weather(s)+1)%4]))


def safehouse(s):
    sheet("WEST QUAY / SAFEHOUSE",("UP rest and advance weather",
          "RIGHT change jacket", "DOWN show checkpoint", "ENTER WAVE radio",
          "LEFT switch Lena / Sol"),
          "CLEAR leave")
    key=keywait((UP,RIGHT,DOWN,LEFT,OK,EXIT))
    if key==UP:
        s['heat']=0
        s['clock']+=28
        notice(s,"Rested / Patrol alert cleared")
    elif key==LEFT:
        active=1-s.get('who',0)
        s['who']=active
        s['coat']=2 if active else 0
        s['speed']=0
        notice(s,"Now playing "+("Sol" if active else "Lena"))
    elif key==RIGHT:
        # The starter jacket is free. Other jackets remain sold at Thread.
        s['coat']=0
        notice(s,"Wearing starter jacket")
    elif key==DOWN:
        tell("SAFEHOUSE CHECKPOINT",(passcode(s),"Load with 2nd at the title."))
    elif key==OK:
        radio_bulletin(s)


def phone_screen(s,apps,hints,selected):
    box(INK,0,0,320,210)
    box(STEEL,36,3,248,204)
    box(NIGHT,40,7,240,196)
    label(MINT,48,28,"COASTLINE")
    label(MILK,48,46,"Cash $%d  Bank $%d"%(s['cash'],s['bank']))
    for i,name in enumerate(apps):
        x,y=48+77*(i%3),54+54*(i//3)
        c=(MINT,GOLD,BLUE,PINK,STEEL,SUN)[i]
        box(MILK if i==selected else ROAD,x,y,70,49)
        box(c,x+24,y+3,22,22)
        if i in (0,2,3):
            arrow(x+35,y+14,("UP","","TURN","UP")[i],INK)
        elif i==4:
            disc(INK,x+35,y+14,6)
            disc(c,x+35,y+14,3)
        else:
            box(INK,x+28,y+12,14,7)
            box(INK,x+31,y+8,8,5)
            disc(INK,x+30,y+20,2)
            disc(INK,x+40,y+20,2)
        label(INK if i==selected else MILK,x+4,y+43,name)
    label(MINT,48,179,hints[selected])
    label(MILK,48,198,"ENTER open / CLEAR back")
