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
    apps=("Pin next objective","Taxi to district $6","Deposit cash","Withdraw cash")
    while True:
        lines=["Cash $%d  Bank $%d"%(s['cash'],s['bank'])]
        lines.extend(("> " if i==selected else "  ")+name for i,name in enumerate(apps))
        sheet("COASTLINE PHONE",lines,"UP/DOWN  ENTER  CLEAR back")
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
