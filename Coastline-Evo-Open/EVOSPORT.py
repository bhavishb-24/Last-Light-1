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


def intro_card(card):
    from EVOVIEW import person
    box(INK,0,0,320,210)
    if card in (0,2,3):
        skyline(card+2)
        box((44,91,112),0,84,320,86)
        if card==0:
            for x in (0,108,222):
                box((118,83,115) if x==108 else (63,77,112),x,90,104,84)
            person(51,171,82,MINT,0,False)
            person(265,171,78,BLUE,0,False)
            car(155,159,91,PINK,True)
        elif card==2:
            for x in (22,84,222,278):
                palm(x,167,90-x%20,NIGHT)
            disc(SUN,160,110,33)
            car(162,168,136,MINT,True)
        else:
            box((30,66,88),0,101,320,70)
            for x in (18,73,244,287):
                line(STEEL,x,128,x,171)
            line(MILK,0,128,319,128)
            person(134,176,99,MINT,0,False)
            person(190,176,105,BLUE,0,False)
        box(NIGHT,5,5,152,40)
        label(SUN,11,22,"LAST LIGHT")
        label(MINT,11,40,"COASTLINE")
    elif card==4:
        box(VIOLET,107,57,106,66)
        box(NIGHT,111,61,98,58)
        label(SUN,119,88,"WAVE RADIO")
        label(MINT,132,109,"84 FM")
    box(INK,0,175,320,35)
    label(MILK,8,207,"ENTER skip")

def intro():
    start=monotonic()
    previous=-1
    pulse=-1
    while True:
        if get_key(0) in (OK,EXIT):
            return
        elapsed=monotonic()-start
        if elapsed>=20:
            return
        card=0 if elapsed<4 else (1 if elapsed<8 else
             (2 if elapsed<12 else (3 if elapsed<16 else 4)))
        if card!=previous:
            intro_card(card)
            previous=card
        step=int(elapsed*4)
        if step==pulse:
            continue
        pulse=step
        if card==1:
            box(INK,89,80,142,25)
            for star in range(1+(step-16)//3):
                label(SUN if star%2 else MILK,98+21*star,98,"*")
        box(MINT,8,182,3*(step+1),3)

def front_menu():
    from EVOVIEW import person
    intro()
    settings=[False,1,True]
    items=("New story","Load save","Settings","Quit")
    selected=0
    while True:
        skyline(7)
        box((51,91,121),0,84,320,53)
        for x in (149,194,242,287):
            box((123,146,174),x,100+x%9,23,2)
        box(VIOLET,0,133,320,77)
        box(STEEL,132,138,188,3)
        for x in (147,219,291):
            box(STEEL,x,138,3,59)
        person(193,190,121,MINT,0,False)
        person(258,190,133,BLUE,0,False)
        box(INK,0,0,133,210)
        label(SUN,8,27,"LAST LIGHT")
        label(MINT,8,48,"COASTLINE")
        for i,item in enumerate(items):
            y=72+24*i
            if i==selected:
                box(PINK,4,y-14,3,15)
            label(MILK if i==selected else STEEL,10,y,item)
        label(MINT,8,181,"INPUT V15")
        label(MILK,8,202,"ENTER select")
        key=keywait((UP,DOWN,OK,MAP,EXIT))
        if key==EXIT or (key==OK and selected==3):
            return EXIT,settings
        if key==MAP or (key==OK and selected==1):
            return MAP,settings
        if key==OK:
            if selected==0:
                return OK,settings
            menu_settings(settings)
        else:
            selected=(selected+(1 if key==DOWN else -1))%4

def menu_settings(settings):
    row=0
    while True:
        labels=("Graphics  "+("Full" if settings[0] else "Fast"),
                "Turning   "+("Fine","Normal","Sharp")[settings[1]],
                "View      "+("3D" if settings[2] else "Top-down"))
        lines=tuple(("> " if i==row else "  ")+item
                    for i,item in enumerate(labels))
        sheet("SETTINGS",lines,"ARROWS change / CLEAR back")
        key=keywait((UP,DOWN,LEFT,RIGHT,OK,EXIT))
        if key==EXIT:
            return
        if key in (UP,DOWN):
            row=(row+(1 if key==DOWN else -1))%3
        elif row==1:
            settings[1]=(settings[1]+(-1 if key==LEFT else 1))%3
        else:
            settings[row]=not settings[row]
