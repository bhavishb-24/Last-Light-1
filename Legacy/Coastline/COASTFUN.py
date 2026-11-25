from COASTLIB import NICK, defeat, sync_search, region
from COASTLIB import (
    BLUE, COATS, COURSES, DOWN, EXIT, GOLD, INK,
    LEFT, MILK, MINT, NAMES, NICK, NIGHT, OK,
    PAINT, PINK, PURSES, RED, RIGHT, STARTS, STEEL,
    SUN, UP, VIOLET, WEATHER, alert, bond, box,
    car, center, crew, disc, earn, event_at, event_name,
    keywait, label, line, notice, pay, pick, poly,
    profile, sheet, tell, weather
)
from COASTVUE import (
    person
)

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
        if kind=='grip':
            disc(INK,160,86,27)
            disc(STEEL,160,86,17)
            disc(NIGHT,160,86,10)
        elif kind=='paint': car(160,112,112,PAINT[val],True)
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
                tell("03 / SPARE PARTS",("The old signal tube glows.","Take it to FM Tower."))
                return
        else:
            info="Need more cash: try Dispatch"

def tune(bands=(5,2,7)):
    position=1
    locks=0
    while locks<len(bands):
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

def advance_story(s,title,lines):
    s['stage']+=1
    s['pin']=-1
    tell(title,lines)

def park_at(s,n,heading):
    s['x'],s['z']=center(n)
    s['cx'],s['cz']=s['x'],s['z']
    s['angle'],s['parkangle']=heading,heading
    s['speed']=0
    s['drive']=True
    s['body'],s['fuel']=100,100

def start_race(s):
    i=0
    titles=("Lido Night Circuit","Marsh Road Sprint","Quay to Lido Run")
    limits=(45,50,63)
    while True:
        status="Medal won" if s['medals'] & (1<<i) else "First medal available"
        sheet("LIDO TIME TRIALS",(titles[i],str(len(COURSES[i]))+" gates / "+str(limits[i])+" seconds",
              "Purse: $"+str(PURSES[i]),status,"UP/DOWN selects course"),"ENTER start / CLEAR leave")
        k=keywait((UP,DOWN,OK,EXIT))
        if k==EXIT: return
        if k==OK:
            park_at(s,STARTS[i],-1.5708 if i==0 else (0 if i==1 else 1.5708))
            s['course'],s['race'],s['timer']=i,0,limits[i]
            return
        i=(i+(1 if k==DOWN else -1))%3

def fishing(s):
    # Move the bait into the strike zone, then reel with alternating taps.
    lure=pick("CAST / SELECT LURE",("Spinner","Minnow","Silver spoon"))
    if lure<0:return
    s['lure']=lure
    fish=((3,6,1,5,2,7,4,0,6)[s['fish']%9]+lure)%8
    hook=4
    tension=2
    pulled=0
    last=0
    while True:
        if pulled:
            instruction="Alternate LEFT and RIGHT."
            if tension>=4: instruction="Slack line with DOWN."
            head="FISH ON / "+str(pulled-1)+"/5"
        else:
            instruction="Line up bait with gold."
            head="TIN MARSH / FISHING"
        sheet(head,(instruction,),"ENTER hook / CLEAR leave")
        for j in range(8):
            box(GOLD if j==fish else BLUE,18+37*j,96,23,6)
        if not pulled: box(MINT,18+37*hook,111,23,4)
        else:
            label(MILK,14,137,"Tension")
            box(STEEL,106,123,170,13)
            box(PINK if tension>=4 else MINT,106,123,tension*28,13)
        k=keywait((UP,DOWN,LEFT,RIGHT,OK,EXIT))
        if k==EXIT: return
        if not pulled:
            if k==LEFT: hook=max(0,hook-1)
            if k==RIGHT: hook=min(7,hook+1)
            if k==OK and hook==fish: pulled=1
        elif k==DOWN:
            tension=max(1,tension-3)
        elif k in (LEFT,RIGHT):
            tension+=1 if k!=last else 2
            if k!=last: pulled+=1
            last=k
            if tension>=6:
                tell("LINE SNAPPED",("Use DOWN before it breaks.",))
                return
            if pulled==6:
                prize=18+fish*2
                s['fish']=min(9,s['fish']+1)
                earn(s,prize)
                tell("CATCH AND RELEASE",("Weight "+str(1+2*lure+fish%3)+" kg","Released alive / tag fee $"+str(prize)))
                return

def club(s):
    sets=((LEFT,UP,RIGHT,DOWN),(RIGHT,UP,LEFT,UP,DOWN),(UP,RIGHT,DOWN,LEFT,RIGHT,UP))
    names={LEFT:"L",RIGHT:"R",UP:"U",DOWN:"D"}
    for i,pattern in enumerate(sets):
        sheet("VELVET / SOUND CHECK",("Remember the cue sequence.",'  '.join(names[k] for k in pattern)),
              "ENTER ready / CLEAR leave")
        if keywait((OK,EXIT))==EXIT: return
        for j,beat in enumerate(pattern):
            sheet("VELVET / SOUND CHECK",("Set "+str(i+1)+" of 3","Cue "+str(j+1)+" of "+str(len(pattern))),
                  "Tap the arrow / CLEAR leave")
            k=keywait((UP,DOWN,LEFT,RIGHT,EXIT))
            if k==EXIT: return
            if k!=beat:
                tell("MISSED CUE",("The band resets the set.",))
                return
    earn(s,36)
    tell("FULL HOUSE  +$36",("The room sings the hook.",))

def radio(s,cycle=True):
    if cycle: s['radio']=(s['radio']+1)%3
    station=("WAVE 84","HARBOR REPORT","VELVET LIVE")[s['radio']]
    if s['radio']==0:
        line1=("Mara: We're live till dawn." if s['stage']>=11 else
               "Mara: Save us a frequency.")
    elif s['radio']==1:
        line1="Conditions: "+WEATHER[weather(s)]
    else:
        line1="Now on: The Breakers"
    tell(station,(line1,"Roads reopen at first light." if s['stage']==12 else
          "Local news from the coast."))

def harbor(s):
    # Plot a service skiff around shoals and deliver to both beacon buoys.
    buoys=((7,1),(9,5),(1,5))
    reefs=((3,0),(3,1),(3,2),(5,3),(6,3),(7,3),(4,5),(4,6))
    x,y,leg,moves=1,5,0,34
    while moves>0:
        sheet("HARBOR / BUOY RUN",(),"Arrows helm / CLEAR dock")
        box((25,92,124),10,43,300,135)
        for j in range(7):
            line((49,108,135),14,50+18*j,305,50+18*j)
        for a,b in reefs:
            box((78,134,112),14+29*a,48+18*b,24,13)
        for i,(a,b) in enumerate(buoys):
            disc(GOLD if leg==i else STEEL,24+29*a,55+18*b,4)
        a,b=24+29*x,55+18*y
        poly(MILK,[a-8,a+8,a+6,a-6],[b-3,b-3,b+4,b+4])
        box(PINK,a-3,b-6,6,4)
        label(MILK,17,178,"Buoys "+str(min(2,leg))+"/2 / Moves "+str(moves))
        k=keywait((UP,DOWN,LEFT,RIGHT,EXIT))
        if k==EXIT: return
        u=x+(k==RIGHT)-(k==LEFT)
        v=y+(k==DOWN)-(k==UP)
        if not (0<=u<10 and 0<=v<7) or (u,v) in reefs: continue
        x,y=u,v
        moves-=1
        if (x,y)==buoys[leg]:
            leg+=1
            if leg==len(buoys):
                earn(s,55)
                tell("BEACONS ONLINE  +$55",("The channel lights come on.","The skiff is back at dock."))
                return
    tell("LOW BATTERY",("Towed back to the marina.","You can run it again.",))




def cues(title,pattern):
    arrows={UP:"U",DOWN:"D",LEFT:"L",RIGHT:"R"}
    for i,k in enumerate(pattern):
        sheet(title,("Follow the highlighted cue."," ".join(arrows[j] for j in pattern),
                    "Next: "+arrows[k]+"   "+str(i+1)+"/"+str(len(pattern))),"Arrow keys / CLEAR stop")
        if keywait((UP,DOWN,LEFT,RIGHT,EXIT))!=k: return False
    return True

def social(s,n):
    h=crew(s)
    i=pick("ON THE STREET",("Greet","Antagonize","Calm the situation","Invite on a date"))
    if i==0:
        if h['rep']>=18: tell("LOCAL",("They step back.","Someone closes a shutter."))
        else: tell("LOCAL",("Heard about "+event_name(s)+"?",NAMES[event_at(s)]+"."))
    elif i==1:
        profile(s,2)
        alert(s,1)
        notice(s,"A witness calls the patrol")
    elif i==2:
        if s['heat']>0: profile(s,-1)
        tell("LOCAL",("They step back and nod.",))
    elif i==3:
        if s['pair'] and pay(s,5): bond(s); notice(s,"Dinner together")
        else: notice(s,"Meet your partner / dinner $5")


def switch(s):
    if s['stage']<4:
        notice(s,"Restore FM to unlock switching")
        return
    i=pick("CREW / "+NICK[s['who']],("Switch lead","Meet up / tag along","Go solo","Surrender"))
    if i==0:
        crew(s)['coat']=s['coat']
        s['who']=1-s['who']
        s['coat']=crew(s)['coat']
        s['district_heat']=-1
        sync_search(s)
        notice(s,NICK[s['who']]+" takes the lead")
    elif i==1: s['pair']=1
    elif i==2: s['pair']=0
    elif i==3:
        if not s['heat']: notice(s,"No active pursuit")
        elif crew(s)['rep']>=18: notice(s,"Surrender unavailable")
        else: defeat(s,True)


