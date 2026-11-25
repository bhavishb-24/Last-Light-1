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


INTRO_CUTS=(3.8,5.4,7.7,9.4,11.3,13.3,15.5,17.1,20)

def intro_card(card):
    from EVOVIEW import person
    dark=(39,36,56)
    box(dark,0,0,320,210)
    if card==0:
        skyline(2)
        box(BLUE,0,84,320,95)
        for i,c in enumerate((VIOLET,STEEL,PINK,BLUE,(158,89,113),(71,105,114))):
            x=(i%3)*107+2
            y=(i//3)*83+7
            poly(c,[x+7,x+103,x+97,x],[y,y,y+78,y+78])
        palm(22,78,59,INK)
        person(151,85,81,MINT,0,False)
        car(260,68,79,GOLD,True)
        car(52,151,86,PINK,True)
        palm(199,159,63,INK)
        person(268,171,85,BLUE,0,False)
        poly(INK,[103,220,211,95],[73,73,132,132])
        label(SUN,111,96,"LAST LIGHT")
        label(MINT,111,120,"COASTLINE")
    elif card==3:
        box((27,81,59),0,21,320,155)
        for i in range(20):
            x=(17+i*71)%320
            y=39+i*37%124
            disc((54,121,65),x,y,16+i%10)
            disc((245,144,44),x+5,y+4,6+i%6)
            disc((255,213,105),x+3,y+2,2+i%3)
        poly((221,164,87),[44,278,286,37],[132,115,161,179])
        label(INK,92,152,"CORAL MARKET")
    elif card==4:
        box((46,76,42),0,21,320,155)
        disc((203,218,121),160,94,64)
        for x in (19,56,242,284):
            palm(x,176,122,NIGHT)
        for x in (104,130,185,211):
            box((143,162,83),x,67,8,94)
        box((189,200,112),94,60,130,8)
        box((83,128,72),0,162,320,16)
    elif card==5:
        box((155,206,217),0,21,320,155)
        box((85,144,173),0,122,320,54)
        disc(GOLD,160,95,59)
        disc((126,150,193),160,95,53)
        for x,direction in ((142,1),(178,-1)):
            disc(PINK,x,111,15)
            line(PINK,x,107,x+direction*12,82)
            disc(PINK,x+direction*12,79,7)
            line(INK,x+direction*13,77,x+direction*20,80)
        line(MILK,8,145,104,145)
        line(MILK,213,158,303,158)
    elif card==6:
        box((84,38,62),0,21,320,155)
        for i in range(12):
            x=i*29-8
            y=96+(i*31)%51
            box((129,57,60),x,y-38,18,55)
            box(GOLD,x+4,y-22,8,5)
        disc((241,117,56),244,66,31)
        car(124,154,137,(227,86,56),True)
        person(252,173,89,PINK,0,False)
    elif card==7:
        label(MILK,155,101,"*")
    elif card==8:
        box(STEEL,134,61,52,52)
        box(NIGHT,137,64,46,46)
        label(SUN,155,91,"W")
        label(MILK,111,140,"WAVE RADIO")

def intro():
    start=monotonic()
    previous=-1
    stars=-1
    card=0
    while True:
        if get_key(0) in (OK,EXIT):
            return
        elapsed=monotonic()-start
        if elapsed>=20:
            return
        while elapsed>=INTRO_CUTS[card]:
            card+=1
        if card!=previous:
            intro_card(card)
            previous=card
        if card==2:
            count=min(6,1+int((elapsed-5.4)*3))
            if count!=stars:
                box((39,36,56),108,79,106,28)
                for i in range(count):
                    label(MILK,111+i*17,99,"*")
                stars=count

def lead(x,y,h,coat,step,who,back=True):
    def cut(c,points):
        poly(c,[x+u*h//40 for u,v in points],[y+v*h//40 for u,v in points])
    def trim(c,u,v,w,d):
        box(c,x+u*h//40,y+v*h//40,max(1,w*h//40),max(1,d*h//40))
    swing=int(sin(step)*2)
    arm=9 if who else 7
    skin=(188,132,101) if who else (226,163,122)
    cut(ROAD,((-12,0),(10,-1),(14,2),(-15,2)))
    cut(NIGHT,((-6,-17),(0,-16),(-2,-3+swing),(-7,swing)))
    cut(STEEL,((0,-16),(6,-17),(7,-swing),(2,-3-swing)))
    trim(MILK,-8,-1+swing,5,2)
    trim(MILK,2,-1-swing,6,2)
    cut(INK,((-arm-3,-24),(-arm,-28),(7,-29),(arm+3,-24),
             (arm+2,-18),(6,-16),(-6,-16),(-arm-2,-18)))
    cut(skin,((-arm,-27),(-arm+2,-26),(-arm+1,-20),(-arm-2,-20)))
    cut(skin,((arm-2,-27),(arm,-26),(arm+2,-20),(arm-1,-20)))
    cut(coat,((-arm+2,-27),(-4,-29),(5,-28),(arm-2,-25),(5,-17),(-5,-17)))
    trim((59,47,65),-5,-18,10,1)
    trim(skin,-arm-2,-19+swing,2,3)
    trim(skin,arm,-19-swing,2,3)
    if back and not who:
        cut(NIGHT,((-4,-27),(-2,-28),(5,-18),(3,-17)))
    else:
        trim(MILK,-2,-27,4,2 if back else 8)
    cut(skin,((-4,-37),(-2,-40),(3,-39),(5,-36),(3,-32),(-2,-30)))
    cut(INK,((-5,-36),(-4,-40),(1,-41),(5,-39),(5,-36),(1,-37)))
    if not who:
        cut((64,39,43),((-4,-39),(-7,-36),(-7,-31),(-10,-27),(-5,-28),(-3,-35)))

def front_menu(show_intro=True):
    if show_intro:
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
        lead(193,190,121,(117,77,126),0,0,False)
        lead(258,190,133,(172,214,217),0,1,False)
        box(INK,0,0,133,210)
        label(SUN,8,27,"LAST LIGHT")
        label(MINT,8,48,"COASTLINE")
        for i,item in enumerate(items):
            y=72+24*i
            if i==selected:
                box(PINK,4,y-14,3,15)
            label(MILK if i==selected else STEEL,10,y,item)
        label(MINT,8,181,"INPUT V22")
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
