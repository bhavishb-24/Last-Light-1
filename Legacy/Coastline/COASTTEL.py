from COASTFUN import cues, radio, switch
from COASTLIB import (
    BLUE, CARS, COATS, DOWN, EXIT, FRONT, INK,
    LEFT, LOTS, MILK, MINT, NAMES, NICK, NIGHT,
    OK, PRICE, REGIONS, RIGHT, SKIN, STEEL, SUN,
    TASK, UP, VIOLET, WEATHER, alert, box, center,
    checkpoint, crew, defeat, district, door, earn, event_at,
    event_name, keywait, label, line, lot, near, notice,
    pay, pick, poly, region, sheet, sync_search, tell,
    weather
)
from COASTMAP import (
    person, render
)

def scan(s):
    i=lot(s)
    if i<0:
        n=min(range(len(LOTS)),key=lambda j:(center(LOTS[j])[0]-s['x'])**2+(center(LOTS[j])[1]-s['z'])**2)
        s['pin']=LOTS[n]
        tell("CAR SCANNER",("Closest lot: "+NAMES[LOTS[n]],"Stand beside its parked car.","Lots sit NW of intersections."))
        return
    tier=(0,1,1,2,2,0,1,0)[i]
    alarm=i in (1,2,3,4)
    gps=i in (3,4)
    items=("Try arcade lock","Register $"+str(PRICE[i]))
    sheet(CARS[i]+" / SCAN",("Street value $"+str(PRICE[i]*5),"Lock tier "+str(tier),
          "Alarm "+("ON" if alarm else "OFF")+" / GPS "+("ON" if gps else "OFF"),
          "Registration $"+str(PRICE[i])),"ENTER options / CLEAR back")
    if keywait((OK,EXIT))==EXIT: return
    k=pick("VEHICLE",items)
    if k<0: return
    if k==1:
        if not s['owned']&(1<<i) and not pay(s,PRICE[i]):
            notice(s,"Not enough cash")
            return
        s['owned']|=1<<i
    else:
        if tier>s['token']:
            notice(s,"Get access token at Foundry")
            return
        if tier and not cues("ARCADE LOCK",(LEFT,UP,RIGHT)[:tier+1]): return
        if alarm or gps: alert(s,2 if gps else 1)
    s['ride'],s['drive'],s['fuel'],s['body']=i,True,80,100
    s['cx'],s['cz']=s['x'],s['z']
    notice(s,CARS[i]+" ready")

def deliver(s):
    cars=[j for j in range(8) if (s['owned']|s['stored'])&(1<<j)]
    i=pick("GARAGE DELIVERY",[CARS[j] for j in cars]+["Premium pass $60"])
    if i<0: return
    if i==len(cars):
        if s['premium'] or pay(s,60): s['premium']=1
        else: notice(s,"Need $60")
    elif s['premium'] or pay(s,4):
        if s['drive']: s['drive']=False
        s['speed']=0
        s['ride']=cars[i]
        s['cx'],s['cz']=s['x'],s['z']
        s['body'],s['fuel']=100,80
        notice(s,"Delivered / ENTER to drive")
    else: notice(s,"Delivery fee is $4")

def photo(s):
    while True:
        render(s)
        if s['blur']:
            for x in (0,269):
                for j in range(0,140,8):
                    box(STEEL,x,22+j,11*s['blur'],3)
        if s['selfie']: person(157,161,106,COATS[s['coat']],0,False)
        for x in (60,240):
            line(MILK,x,67,x+14,67)
            line(MILK,x,67,x,80)
        box(INK,0,169,320,41)
        label(MILK,5,187,"UP selfie / DOWN aperture")
        label(MINT,5,206,"ENTER post / CLEAR close")
        k=keywait((UP,DOWN,OK,EXIT))
        if k==EXIT: return
        if k==UP: s['selfie']=1-s['selfie']
        if k==DOWN: s['blur']=(s['blur']+1)%3
        if k==OK:
            s['lastpic']=district(s['x'],s['z'])
            s['photo']=min(31,s['photo']+1)
            notice(s,"Posted to your local feed")
            return

def phone(s):
    # Raise the handset from the avatar's hand, then draw its app screen.
    for top in (115,81,44):
        poly(SKIN,[173,185,226,210],[138,144,top+52,top+47])
        box(INK,196,top,45,63)
        box(BLUE,200,top+4,37,49)
    apps=("Scan vehicle","Bank wallet","Deliver vehicle","Call taxi","Messages / crew",
          "Camera / selfie","City feed / live","Scan street art","Forecast","Fitness","Police radio","Checkpoint","Switch radio station")
    pos=0
    while True:
        render(s)
        poly(SKIN,[198,222,282,251],[147,127,168,205])
        box(INK,82,15,171,183)
        box(NIGHT,86,20,163,171)
        box(VIOLET,86,22,163,34)
        label(SUN,95,45,NICK[s['who']]+" / PHONE")
        for j in range(4):
            idx=pos//4*4+j
            if idx>=len(apps):break
            y=79+j*22
            if idx==pos: box((48,98,112),89,y-16,156,21)
            label(MILK,94,y,apps[idx][:15])
        label(MINT,94,183,"ENTER / CLEAR")
        k=keywait((UP,DOWN,OK,EXIT))
        if k==EXIT:return
        if k in (UP,DOWN):
            pos=(pos+(1 if k==DOWN else -1))%len(apps)
            continue
        if pos==0: scan(s); return
        if pos==1:
            i=pick("SAVINGS $"+str(s['bank']),("Deposit wallet $"+str(s['cash']),"Withdraw up to $50"))
            if i==0:
                amount=min(s['cash'],4095-s['bank'])
                s['cash']-=amount
                s['bank']+=amount
            elif i==1:
                amount=min(50,s['bank'],999-s['cash'])
                s['bank']-=amount
                earn(s,amount)
        elif pos==2: deliver(s); return
        elif pos==3:
            i=pick("CITY CAB / $6",NAMES)
            if i>=0 and not s['rescue'] and s['race']<0 and pay(s,6):
                tell("CAB / DRIVER",(("Fog near the piers today." if weather(s)==2 else "My sister works at WAVE."),
                     "You: Keep the radio on.","Arriving at "+NAMES[i]+"."))
                s['drive'],s['speed']=False,0
                s['x'],s['z']=center(i)
                sync_search(s)
                return
            if i>=0: tell("CAB",("Need $6 and no active race","or rescue.",))
        elif pos==4:
            tell("INBOX / MARA",(TASK[s['stage']],))
            switch(s)
        elif pos==5: photo(s); return
        elif pos==6:
            n=event_at(s)
            post=NAMES[s['lastpic']] if s['photo'] else "No photos yet"
            sheet("CITY FEED",("LIVE: "+event_name(s),NAMES[n],"Your latest: "+post,"Posts: "+str(s['photo'])),
                  "ENTER pin event / CLEAR back")
            if keywait((OK,EXIT))==OK: s['pin']=n; return
        elif pos==7:
            n=region(s)
            u,v=door(district(s['x'],s['z']))
            if near(s['x'],s['z'],u,v,6) and not s['tags']&(1<<n):
                s['tags']|=1<<n
                earn(s,14)
                tell("MURAL ARCHIVE",(REGIONS[n],"First scan +$14",))
            else: tell("AR LENS",("One mural per region.","Scan near a storefront.",))
        elif pos==8:
            w=weather(s)
            nxt=FRONT[(int(s['clock']//44)+1)%len(FRONT)]
            tell("WEATHER WIRE",("Now: "+WEATHER[w],"Next front: "+WEATHER[nxt],"Rain tires help on wet roads."))
        elif pos==9: status(s)
        elif pos==10: tell("DISPATCH",(REGIONS[region(s)],"Local stars: "+str(crew(s)['zones'][region(s)]),))
        elif pos==11: checkpoint(s)
        else: radio(s)

def status(s):
    h=crew(s)
    tell(NICK[s['who']]+" / FITNESS",("Health "+str(int(h['hp']))+"  Energy "+str(int(h['stam'])),
         "Power "+str(h['power'])+"  Cardio "+str(h['cardio']), "Focus "+str(h['focus'])+"  Skill "+str(h['skill']),
         "Hunger "+str(h['hunger'])+"  Weight "+str(h['weight']),"Workout: "+("ready" if h['stam']>=12 else "rest or eat")))

