from EVODATA import *


def fishing(s):
    target=int(s['clock']*3)%7
    bait=3
    pulls=0
    tension=0
    last=0
    hooked=False
    while True:
        title="FISH ON / %d of 5"%pulls if hooked else "SUN PIER / FISHING"
        hint="Alternate LEFT and RIGHT" if hooked else "Line up bait with gold"
        footer="DOWN slack / CLEAR leave" if hooked else "ENTER hook / CLEAR leave"
        sheet(title,(hint,),footer)
        if hooked:
            label(MILK,12,113,"Tension %d / 6"%tension)
            box(PINK if tension>=4 else MINT,12,125,35*tension,8)
        else:
            for i in range(7):
                box(GOLD if i==target else BLUE,12+43*i,100,32,7)
            box(MINT,12+43*bait,112,32,5)
        key=keywait((LEFT,RIGHT,DOWN,OK,EXIT))
        if key==EXIT:
            return
        if not hooked:
            if key==OK:
                hooked=bait==target
            if key in (LEFT,RIGHT):
                bait=max(0,min(6,bait+(1 if key==RIGHT else -1)))
        elif key==DOWN:
            tension=max(0,tension-3)
        elif key in (LEFT,RIGHT):
            tension+=2 if key==last else 1
            if key!=last:
                pulls+=1
            last=key
            if tension>=6:
                tell("LINE SNAPPED",("Press DOWN to give it slack.",))
                return
            if pulls==5:
                earn(s,18)
                tell("CATCH AND RELEASE",("Fish released / Tag fee $18",))
                return


def pool(s):
    aim=3
    score=0
    for target in (1,5,2):
        while True:
            sheet("VELVET CLUB / POOL",("Line up with the gold pocket.",
                  "Sunk %d / 3"%score),"LEFT/RIGHT aim / ENTER shoot")
            for i in range(7):
                box(GOLD if i==target else STEEL,16+42*i,122,27,5)
            box(MINT,16+42*aim,137,27,5)
            key=keywait((LEFT,RIGHT,OK,EXIT))
            if key==EXIT:
                return
            if key==OK:
                if aim==target:
                    score+=1
                break
            aim=max(0,min(6,aim+(1 if key==RIGHT else -1)))
    prize=score*6
    earn(s,prize)
    tell("POOL RESULTS",("Sunk %d / 3"%score,"Prize $"+str(prize)))


def palm_garden(s):
    sheet("PALM GARDEN",("UP gym workout", "RIGHT play mini golf",
          "DOWN clues for lost records"),"CLEAR leave")
    k=keywait((UP,RIGHT,DOWN,EXIT))
    if k==UP:
        gym(s)
    elif k==RIGHT:
        golf(s)
    elif k==DOWN:
        tell("LOST RECORDS",("West of Kiln Yard.","South of FM Tower.",
                             "Southwest of the Lido."))

def gym(s):
    for i,move in enumerate((LEFT,RIGHT,LEFT,RIGHT,LEFT,RIGHT)):
        sheet("PALM GARDEN / GYM",("Cycle %d / 6"%(i+1),
              "Pedal "+("LEFT" if move==LEFT else "RIGHT")),"CLEAR leave")
        k=keywait((LEFT,RIGHT,EXIT))
        if k==EXIT:
            return
        if k!=move:
            notice(s,"Workout stopped / Try again")
            return
    s['fit']=s['clock']+30
    notice(s,"Cardio boost / Faster walking")

def golf(s):
    power=3
    sunk=0
    for distance in (2,5,4):
        while True:
            sheet("PALM GARDEN / MINI GOLF",("Hole %d / 3"%(1+sunk),
                  "Match power to cup distance."),"LEFT/RIGHT power / ENTER putt")
            for i in range(7):
                box(GOLD if i==distance else STEEL,15+42*i,119,30,6)
            box(MINT,15+42*power,133,30,6)
            k=keywait((LEFT,RIGHT,OK,EXIT))
            if k==EXIT:
                return
            if k==OK:
                if power!=distance:
                    tell("MISSED PUTT",("Try the course again anytime.",))
                    return
                sunk+=1
                break
            power=max(0,min(6,power+(1 if k==RIGHT else -1)))
    earn(s,15)
    tell("THREE HOLES CLEARED",("Course prize $15",))


def marina(s):
    sheet("MARINA / TRANSPORT",("UP pilot a harbor skiff",
          "RIGHT fly a floatplane","ENTER ferry to West Quay $5"),
          "CLEAR leave")
    key=keywait((UP,RIGHT,OK,EXIT))
    if key==OK:
        if pay(s,5):
            s['x'],s['z']=center(0)
            notice(s,'West Quay landing')
        else:
            notice(s,'Fare is $5')
    elif key in (UP,RIGHT):
        coastal_trip(s,key==RIGHT)

def coastal_trip(s,plane):
    x,y=1,3
    altitude=1
    cargo=False
    while True:
        heading="FLOATPLANE / BAY" if plane else "SKIFF / BAY"
        status="Altitude "+str(altitude) if plane else "Avoid the shoals"
        sheet(heading,(status,), "ARROWS move / ENTER dock")
        box(BLUE,15,75,290,95)
        for col in (3,4,5):
            box(GOLD,17+36*col,119,32,20)
        box(MINT,269,77,30,17)
        if not cargo:
            disc(SUN,251,129,4)
        px,py=35+36*x,85+22*y
        if plane:
            line(MILK,px-9,py,px+9,py)
            line(MILK,px,py-6,px,py+6)
        else:
            box(MILK,px-6,py-4,13,8)
        label(MILK,10,181,"2nd altitude / CLEAR return" if plane else
              ("Log aboard / Head to dock" if cargo else "Gold buoy: recover dock log"))
        k=keywait((UP,DOWN,LEFT,RIGHT,MAP,OK,EXIT))
        if k==EXIT:
            return
        if k==MAP and plane:
            altitude=1-altitude
        if k==OK and (x,y)==(7,0):
            if plane and altitude:
                continue
            s['x'],s['z']=center(7)
            if cargo:
                earn(s,20)
            notice(s,"Pier landing / Log +$20" if cargo else "Sun Pier landing")
            return
        u=max(0,min(7,x+(k==RIGHT)-(k==LEFT)))
        v=max(0,min(3,y+(k==DOWN)-(k==UP)))
        if not (v==2 and 3<=u<=5 and (not plane or not altitude)):
            x,y=u,v
        if (x,y)==(6,2):
            cargo=True
