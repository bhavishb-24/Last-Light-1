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
