from COASTFUN import cues
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

SPORTS=("Pool","Mini golf","Basketball","Bowling","Target range","Scuba salvage","Kayak",
        "Airboat","Jet ski","Monster truck","Base jump","Photo safari","Wildlife survey","Bike trail","Flight school")
SPOTS=(9,10,5,4,8,15,7,14,3,13,12,10,14,1,12)
def precision(s,i):
    # Aim and power change a simulated ball path, lane throw or range shot.
    title=SPORTS[i]
    aim,power,points=0,3,0
    for turn in range(3):
        target=(turn*3+i)%7-3
        depth=2+(turn+i)%4
        while True:
            box(INK,0,0,320,210)
            box((49,104,98) if i in (0,1) else NIGHT,14,36,292,123)
            label(MILK,8,24,title+"  "+str(points)+"/3")
            tx,ty=160+target*25,141-depth*16
            if i==0:
                for x in (22,160,298):
                    disc(INK,x,43,6)
                    disc(INK,x,151,6)
                for j in range(3):disc((PINK,SUN,BLUE)[j],54+28*j,65+29*(j%2),4)
            elif i==1:
                disc((188,154,101),62,94,17)
                line(MILK,tx,ty-17,tx,ty)
                poly(PINK,[tx,tx+11,tx],[ty-17,ty-12,ty-9])
            elif i==2:
                box(MILK,tx-14,ty-15,28,12)
                box(PINK,tx-9,ty-5,18,3)
            elif i==3:
                for off in (-10,0,10):
                    box(MILK,tx+off,ty-12,4,13)
                    box(PINK,tx+off,ty-8,4,2)
            else:
                disc(MILK,tx,ty,16)
                disc(RED,tx,ty,12)
            disc(GOLD,tx,ty,10 if i!=4 else 7)
            disc(INK,tx,ty,5)
            ax,ay=160+aim*25,141-power*16
            line(MINT,160,150,ax,ay)
            disc(MILK,ax,ay,3)
            label(MILK,6,181,"L/R aim   UP/DN power")
            label(MINT,6,204,"ENTER shoot / CLEAR back")
            k=keywait((LEFT,RIGHT,UP,DOWN,OK,EXIT))
            if k==EXIT: return
            if k==LEFT: aim=max(-4,aim-1)
            if k==RIGHT: aim=min(4,aim+1)
            if k==UP: power=min(6,power+1)
            if k==DOWN: power=max(1,power-1)
            if k==OK:
                for j in range(1,6):
                    t=j/5
                    px=int(160+(ax-160)*t)
                    py=int(150+(ay-150)*t-(40*t*(1-t) if i==2 else 0))
                    disc(MILK,px,py,3)
                if aim==target and depth==power: points+=1
                break
    earn(s,points*7)
    if i==4 and points>=2: crew(s)['skill']=min(15,crew(s)['skill']+1)
    if points: bond(s)
    tell(title,("Hits "+str(points)+"/3","Prize $"+str(points*7)))

def outing(s,i):
    # Each course has its own scenery, obstacles, speed and steering.
    titles=("Wreck air","River flow","Reed channel","Buoy slalom","Crush course",
            "Canopy line","Zoo trail","Marsh tracks","Hill trail","Flight gates")
    hazards=("Rock","Log","Reeds","Buoy","Barrier","Gust","Brush","Mud","Rock","Cloud")
    modes=(0,1,1,1,2,3,4,4,2,3)
    j=i-5
    mode=modes[j]
    lane=1
    energy=6
    score=0
    for gate_no in range(7):
        safe=(gate_no*gate_no+2*j+gate_no//2)%3
        bonus=(safe+1)%3
        box(INK,0,0,320,210)
        label(MILK,7,22,titles[j]+" "+str(gate_no+1)+"/7")
        box((45,106,137) if mode<=1 else (97,131,107),12,35,296,124)
        for a in range(3):
            cx=68+a*90
            line(STEEL,cx-38,42,cx-38,155)
            if a==safe:
                disc(GOLD,cx,74,9)
                disc(MINT,cx,74,4)
            elif a==bonus: box(NIGHT,cx-9,64,18,21)
        cx=68+lane*90
        if mode==1: poly(MILK,[cx,cx+9,cx-9],[119,147,147])
        elif mode==2: car(cx,143,38,PINK,True)
        elif mode==3: poly(SUN,[cx-14,cx,cx+14,cx],[140,119,140,136])
        else: person(cx,144,23,MINT,gate_no,True)
        label(MINT,5,181,"L/R move  ENTER "+("survey" if mode==4 else "advance"))
        label(MILK,5,205,hazards[j]+" ahead / Energy "+str(energy))
        k=keywait((LEFT,RIGHT,OK,EXIT))
        if k==EXIT: return
        if k==LEFT: lane=max(0,lane-1)
        if k==RIGHT: lane=min(2,lane+1)
        if lane==safe: score+=1
        if lane==bonus: energy-=2
        if mode in (1,3) and weather(s) in (1,3) and gate_no%3==2: lane=(lane+1)%3
        if energy<=0: break
    if i==12 and not s['hunt']: tell("MARSH GUIDE",("Ask the ranger at Palm Garden","for a paid tracking contract.")); return
    amount=score*(6 if i==12 else 4)
    earn(s,amount)
    if score: bond(s)
    tell(SPORTS[i],("Score "+str(score)+"/7","Reward $"+str(amount),))

def play_sport(s,n):
    ids=[i for i in range(len(SPORTS)) if SPOTS[i]==n]
    if not ids:
        i=pick("ACTIVITY DIRECTORY",SPORTS)
        if i>=0:
            s['pin']=SPOTS[i]
            notice(s,"Pinned "+NAMES[SPOTS[i]])
        return
    k=pick("LOCAL ACTIVITIES",[SPORTS[i] for i in ids])
    if k<0: return
    i=ids[k]
    if i<5: precision(s,i)
    else: outing(s,i)

def gym(s):
    h=crew(s)
    if not h['gym']:
        if pick("FRONT DESK",("Membership $15",))<0: return
        if not pay(s,15): notice(s,"Need $15"); return
        h['gym']=1
    names=("Treadmill","Punching bag","Squats","Lat pulldown","Bench press","Deadlift")
    k=pick("GYM / "+NICK[s['who']],names)
    if k<0: return
    if h['stam']<12: tell("RECOVERY",("Eat or rest before training.",)); return
    patterns=((LEFT,RIGHT)*2,(UP,LEFT,RIGHT,DOWN),(DOWN,UP)*2,(UP,DOWN)*2,(LEFT,UP,RIGHT,UP),(DOWN,LEFT,UP,RIGHT))
    if cues(names[k],patterns[k]):
        stat=('cardio','skill','power','power','power','power')[k]
        h[stat]=min(15,h[stat]+1)
        h['stam']-=12
        h['hunger']=min(15,h['hunger']+2)
        bond(s)
        notice(s,stat+" improved")

