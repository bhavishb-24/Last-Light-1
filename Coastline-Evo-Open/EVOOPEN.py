from EVODATA import *
from EVOVIEW import *
from EVOMENU import *
def venue(s,n):
    t=s['stage']
    if s['job']==n+1:
        earn(s,45)
        s['job']=0
        tell("PARCEL SIGNED  +$45",("The night clerk signs for it.","Dispatch has more work."))
        return
    if n==0 and t==0:
        tell("MARA / DEAD AIR",("They sold our frequency.","Tonight is our last show.","Ivo taped the deal at the","pier. Ask him for the reel."))
        s['stage']=1
    elif n==7 and t==1:
        tell("IVO / THE PIER TAPE",("You hear a second voice:","Mara's brother signed it.","The tower needs a $20 valve.","Take $30. Get us on air."))
        s['stage']=2
        earn(s,30)
    elif n==2 and t==3:
        if tune():
            s['stage']=4
            tell("MARA / OPEN CHANNEL",("That's my brother's voice.","Arcade will air it uncut.","Velvet can mask his voice.","Your tape. Your call."))
    elif t==4 and n in (6,9):
        public=n==6
        s['stage']=5 if public else 6
        earn(s,90)
        tell("ON THE RECORD" if public else "THE VELVET DUB",
             ("Every radio hears the deal." if public else "A filtered voice hits the air.",
              "Mara lets the tape roll." if public else "Her brother stays anonymous.",
              "The station stays on air.","+$90 / City stays open."))
    elif n==1:
        shop(s,"GLASSHOUSE SUPPLY",(("Signal valve",20,'stage',3),))
    elif n==5:
        shop(s,"THREAD DEPT.",(("Coral jacket",18,'coat',1),("Mint jacket",18,'coat',2),("Runners: faster walk",25,'shoes',1),("Blue jacket",0,'coat',0)))
    elif n==8:
        shop(s,"FOUNDRY CUSTOMS",(("Rose lacquer",24,'paint',1),("Gold flake",32,'paint',2),("Sea glass",0,'paint',0)))
    elif n==4:
        if not s['job']:
            choices=(3,5,7,9,11)
            target=choices[int(s['clock']+s['cash'])%5]
            s['job']=target+1
        tell("NIGHT DISPATCH",("Hand this parcel to the clerk","at "+NAMES[s['job']-1]+".","Delivery pays $45."))
    elif n==11:
        sheet("LIDO / NIGHT CIRCUIT",("Pass four gold checkpoints.","Palms > Arcade > Pier > Lido","The entry grid has your car.","Purse: $70. Limit: 45s."),"ENTER race / CLEAR leave")
        if keywait((OK,EXIT))==OK:
            s['x'],s['z']=center(11)
            s['cx'],s['cz']=s['x'],s['z']
            s['drive']=True
            s['angle']=-1.5708
            s['speed']=0
            s['race']=0
            s['timer']=45
    elif n==6:
        tell("PIXEL PALACE",("Needle Match pays $12.","Catch all three gold bands."))
        if tune():
            earn(s,12)
            notice(s,'High score! +$12')
    elif n==3:
        sheet("MARINA / WATER TAXI",("Ferry to West Quay: $5.","Your coupe stays parked."),"ENTER sail / CLEAR leave")
        if keywait((OK,EXIT))==OK:
            if pay(s,5):
                s['x'],s['z']=center(0)
                notice(s,'West Quay landing')
            else: notice(s,'Fare is $5')
    elif n==10:
        tell("PALM GARDEN",("Three gold singles are lost.","One west of Kiln Yard.","One south of FM Tower.","One southwest of the Lido."))
    else:
        chatter=("The signal is yours now.","Try the shelves at Parts.","Bring me the signal valve.","Last ferry leaves at dusk.",
                 "Dispatch needs a rider.","The new jackets just arrived.","The machines still take coins.","I kept a copy of that reel.",
                 "Fresh paint dries fast.","This room has good acoustics.","The palms hide old records.","Listen for the starting bell.")
        tell(VENUES[n],(chatter[n],TASK[t]))

def interact(s):
    x,z=s['x'],s['z']
    s['speed']=0
    if s['drive']:
        s['drive']=False
        s['parkangle']=s['angle']
        for dx,dz in ((1.8,0),(-1.8,0),(0,1.8),(0,-1.8)):
            if not blocked(x+dx,z+dz,0.35):
                s['x'],s['z']=x+dx,z+dz
                break
        notice(s,'Parked / on foot')
        return
    k,n=closest(s)
    if k=='car':
        s['drive']=True
        s['x'],s['z']=s['cx'],s['cz']
        s['angle']=s['parkangle']
        notice(s,'UP gas / DOWN brake or back')
    elif k=='door':
        venue(s,n)
    elif k=='local':
        lines=(("Ivo kept every pier show.","Look for the gold dot."),("The Foundry does gold flake.","Dispatch pays for the paint."),("Start the rally at the Lido.","Gold hoops mark each gate."))
        tell(("ANA / TECH","KIT / RUNNER","RED / DRIVER")[n],lines[n])
    elif k=='disc':
        s['records']|=1<<n
        reward=50 if s['records']==7 else 15
        earn(s,reward)
        notice(s,'Rare single found! +$'+str(reward))
    else:
        notice(s,'Find a lit door or your coupe')

def tick(s,k,dt):
    driving=s['drive']
    limit=14 if driving else (6 if s['shoes'] else 4)
    if k==LEFT: s['angle']=(s['angle']-0.23)%TAU
    if k==RIGHT: s['angle']=(s['angle']+0.23)%TAU
    if k==UP: s['speed']=min(limit,max(0,s['speed'])+(3 if driving else limit))
    if k==DOWN:
        s['speed']=0 if s['speed']>0 else -limit*0.4
    d=s['speed']*dt
    x,z=s['x'],s['z']
    r=0.85 if driving else 0.35
    u=x+sin(s['angle'])*d
    v=z+cos(s['angle'])*d
    if not blocked(u,z,r): s['x']=u
    if not blocked(s['x'],v,r): s['z']=v
    if d and x==s['x'] and z==s['z']: s['speed']=0
    s['stride']+=abs(d)*2
    s['clock']+=dt
    if s['pin']>=0:
        u,v=door(s['pin'])
        if near(s['x'],s['z'],u,v,2.7): s['pin']=-1
    s['ttl']=max(0,s['ttl']-dt)
    s['fine']=max(0,s['fine']-dt)
    if driving:
        s['cx'],s['cz']=s['x'],s['z']
        if s['speed']>6 and not s['fine']:
            for u,v in traffic(s['clock']):
                if near(s['x'],s['z'],u,v,1.5):
                    if s['heat']<=0:
                        for dx,dz in ((-10,0),(10,0),(0,-10),(0,10)):
                            if not blocked(s['x']+dx,s['z']+dz,0.7):
                                s['px'],s['pz']=s['x']+dx,s['z']+dz
                                s['heat']=14
                                break
                    s['cash']=max(0,s['cash']-5)
                    s['speed']=0
                    s['fine']=3
                    notice(s,'Traffic alert / $5 repair')
                    break
    if s['heat']>0:
        s['heat']=max(0,s['heat']-dt)
        dx=s['x']-s['px']
        dz=s['z']-s['pz']
        pace=dt*5/max(1,abs(dx),abs(dz))
        u=s['px']+dx*pace
        v=s['pz']+dz*pace
        if not blocked(u,s['pz'],0.6): s['px']=u
        if not blocked(s['px'],v,0.6): s['pz']=v
        if near(s['x'],s['z'],s['px'],s['pz'],1.9):
            s['heat']=0
            s['cash']=max(0,s['cash']-10)
            notice(s,'Patrol ticket / $10')
        elif not s['heat']: notice(s,'Patrol alert cleared')
    if s['race']>=0:
        s['timer']-=dt
        u,v=center(GATES[s['race']])
        if s['timer']<=0:
            s['race']=-1
            notice(s,'Time up / retry at Lido')
        elif driving and near(s['x'],s['z'],u,v,3.4):
            s['race']+=1
            if s['race']==4:
                s['race']=-1
                earn(s,70)
                notice(s,'Circuit complete! +$70')
            else: notice(s,'Gate cleared!')

def journal(s):
    ending=("AIRWAVES","ARCHIVE")
    title=ending[s['stage']-5] if s['stage']>=5 else "DEAD AIR / STORY"
    job=NAMES[s['job']-1] if s['job'] else "Visit Kiln Yard"
    count=sum((s['records']>>i)&1 for i in range(3))
    while True:
        mode="Full" if s['detail'] else "Fast"
        sheet(title,(TASK[s['stage']],"Parcel: "+job,"Rare singles: "+str(count)+"/3",
                     "Checkpoint: "+passcode(s),"2nd graphics: "+mode),
                     "ENTER back / CLEAR quit")
        k=keywait((OK,EXIT,MAP))
        if k!=MAP: return k!=EXIT
        s['detail']=not s['detail']


def play():
    draw.clear()
    skyline(7)
    box(INK,0,84,320,126)
    label(SUN,12,110,"LAST LIGHT / DEAD AIR")
    label(MILK,12,139,"ENTER new story")
    label(MINT,12,164,"2nd load checkpoint")
    label(MILK,12,196,"CLEAR quit")
    k=keywait((OK,MAP,EXIT))
    if k==EXIT: return
    s=fresh()
    if k==MAP:
        while True:
            print("Enter checkpoint or 0 to exit")
            code=input()
            if code=="0": return
            s=restore(code)
            if s is not None: break
            print("Check the digits and retry.")
        draw.clear()
    else:
        tell("WEST QUAY / DUSK",("Mara's station goes silent","at midnight. Her studio is","the WAVE door ahead.","UP starts / DOWN stops.","LEFT and RIGHT turn you."))
    tell("STREET CONTROLS",("ENTER: talk, shop, car, park","2nd: map and district pins","ALPHA: journal / checkpoint","CLEAR: journal and quit","Pink map dot: parked coupe."))
    buffer=[]
    next_frame=0
    while True:
        start=monotonic()
        if start>=next_frame:
            render(s,buffer)
            # Keep polling and advancing the simulation between idle redraws.
            next_frame=start+(0.15 if s['speed'] or s['heat'] else 0.5)
        k=buffer.pop(0) if buffer else get_key(0)
        while not k and monotonic()-start<0.075:
            k=get_key(0)
        if k:
            next_frame=0
        if k in (EXIT,31):
            buffer=[]
            if not journal(s): return
            continue
        if k==MAP:
            buffer=[]
            atlas(s)
            continue
        if k==OK:
            buffer=[]
            interact(s)
            continue
        tick(s,k,min(0.22,max(0.035,monotonic()-start)))

play()
