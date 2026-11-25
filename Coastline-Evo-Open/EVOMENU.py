from EVODATA import *
from EVOVIEW import *
def atlas(s):
    pin=district(s['x'],s['z'])
    while True:
        sheet("CITY ATLAS    N ^",(),"Arrows browse / ENTER pin")
        def dotpos(x,z):
            return (int(39+x*2.36),int(141-z*1.20))
        for i in range(4):
            a,b=dotpos(i*32,64)
            line(STEEL,a,b,a,141)
        for i in range(3):
            a,b=dotpos(0,i*32)
            line(STEEL,a,b,265,b)
        for n in range(12):
            a,b=dotpos(*center(n))
            disc(TRIM[n%4],a,b,3)
        n=goal(s)
        if n>=0:
            a,b=dotpos(*center(n))
            disc(GOLD,a,b,6)
        a,b=dotpos(s['cx'],s['cz'])
        box(PINK,a-2,b-2,5,5)
        a,b=dotpos(s['x'],s['z'])
        disc(MILK,a,b,3)
        a,b=dotpos(*center(pin))
        color(MINT)
        draw.draw_circle(a,b,8)
        label(MILK,10,179,NAMES[pin]+" / "+SIGNS[pin])
        k=keywait((UP,DOWN,LEFT,RIGHT,MAP,OK,EXIT))
        if k in (MAP,EXIT): return
        if k==OK:
            s['pin']=pin
            notice(s,'Pinned '+NAMES[pin])
            return
        if k==LEFT and pin%4: pin-=1
        if k==RIGHT and pin%4<3: pin+=1
        if k==UP and pin>=4: pin-=4
        if k==DOWN and pin<8: pin+=4

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

def tune():
    position=1
    locks=0
    while locks<3:
        target=(5,2,7)[locks]
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
    apps=("Pin next objective","Taxi to district $6","Deposit cash","Withdraw cash","Locate parked coupe","Deliver coupe $5")
    while True:
        lines=[("> " if i==selected else "  ")+name for i,name in enumerate(apps)]
        sheet("PHONE $%d / BANK $%d"%(s['cash'],s['bank']),lines,"UP/DOWN  ENTER  CLEAR back")
        k=keywait((UP,DOWN,OK,EXIT))
        if k==EXIT:
            return
        if k in (UP,DOWN):
            selected=(selected+(1 if k==DOWN else -1))%len(apps)
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
    x=int(30+s['x']*2.4)
    y=int(148-s['z']*1.45)
    if previous is None:
        box(INK,0,0,320,210)
        for n in range(len(NAMES)):
            px=(30,106,183,260)[n%4]
            py=(55,101,148)[n//4]
            box(ROAD,px-3,py-3,7,7)
            if n%4<3:
                box(ROAD,px,py-3,(76,77,77)[n%4],7)
            if n<8:
                box(ROAD,px-3,py,7,(46,47)[n//4])
        box(NIGHT,0,171,320,39)
        label(MINT,5,206,"2nd map / DEL phone / TRACE 3D")
    elif previous[:2]!=(x,y):
        px,py=previous[:2]
        box(INK,px-1,py-1,3,3)
        for a in range(px-1,px+2):
            for b in range(py-1,py+2):
                if (27<=a<=263 and min(abs(b-55),abs(b-101),abs(b-148))<=3) or (52<=b<=151 and min(abs(a-30),abs(a-106),abs(a-183),abs(a-260))<=3):
                    box(ROAD,a,b,1,1)
    status=(district(s['x'],s['z']),s['cash'],s['drive'],gps(s))
    if previous is None or previous[:2]!=(x,y) or previous[2][2]!=s['drive']:
        box(GOLD if s['drive'] else MINT,x-1,y-1,3,3)
    if previous is None or previous[2]!=status:
        box(NIGHT,0,171,320,22)
        label(MILK,5,190,NAMES[status[0]]+" $"+str(s['cash'])+" "+status[3])
    return x,y,status


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
          "RIGHT change jacket", "DOWN show checkpoint", "ENTER WAVE radio"),
          "CLEAR leave")
    key=keywait((UP,RIGHT,DOWN,OK,EXIT))
    if key==UP:
        s['heat']=0
        s['clock']+=28
        notice(s,"Rested / Patrol alert cleared")
    elif key==RIGHT:
        # The starter jacket is free. Other jackets remain sold at Thread.
        s['coat']=0
        notice(s,"Wearing starter jacket")
    elif key==DOWN:
        tell("SAFEHOUSE CHECKPOINT",(passcode(s),"Load with 2nd at the title."))
    elif key==OK:
        radio_bulletin(s)
