import gc
if hasattr(gc,"threshold"):
    gc.threshold(4096)
gc.collect()
def boot_clip():
    # Play before loading the city renderer so frame imports have room.
    try:
        import EVFSPLAY
        played=EVFSPLAY.play()
    except (ImportError,MemoryError):
        return False
    finally:
        from sys import modules
        if 'EVFSPLAY' in modules:
            del modules['EVFSPLAY']
    return played

clip_played=boot_clip()
gc.collect()
from EVOVIEW import render,traffic
gc.collect()
from EVODATA import *
gc.collect()
def venue(s,n):
    from EVOMENU import shop,tune,safehouse
    t=s['stage']
    if s['job']==n+1:
        earn(s,45)
        s['job']=0
        tell("PARCEL SIGNED  +$45",("The night clerk signs for it.","Dispatch has more work."))
        return
    if n==0 and t==0:
        tell("MARA / DEAD AIR",("They sold our frequency.","Ivo has a recording of it.","Find the PIER sign at Sun Pier.","Park and use the PIER counter."),0)
        s['stage']=1
    elif n==7 and t==1:
        tell("IVO / THE PIER TAPE",("Mara's brother signed the deal.","Take $30 for a signal valve.","Go to PARTS in Glasshouse.","Buy the valve for $20."),1)
        s['stage']=2
        earn(s,30)
    elif n==2 and t==3:
        if tune():
            s['stage']=4
            tell("MARA / OPEN CHANNEL",("That's my brother's voice.","PIXEL airs the original tape.","VELVET disguises his voice.","Visit one door to choose."),0)
    elif t==4 and n in (6,9):
        public=n==6
        s['stage']=5 if public else 6
        earn(s,90)
        tell("ON THE RECORD" if public else "THE VELVET DUB",
             ("Every radio hears the deal." if public else "A filtered voice hits the air.",
              "Mara lets the tape roll." if public else "Her brother stays anonymous.",
              "The station stays on air.","+$90 / City stays open."))
    elif t>=5 and s['wire']<len(WIRE) and n==WIRE[s['wire']]:
        follow_wire(s,n)
    elif n==0:
        safehouse(s)
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
    elif n==7:
        from EVOSPORT import fishing
        fishing(s)
    elif n==9:
        from EVOSPORT import pool
        pool(s)
    elif n==10:
        from EVOSPORT import palm_garden
        palm_garden(s)
    elif n>=12:
        tell(VENUES[n],("Coast Expressway access",
             "Follow the gold merge lines."))
    else:
        chatter=("The signal is yours now.","Try the shelves at Parts.","Bring me the signal valve.","Last ferry leaves at dusk.",
                 "Dispatch needs a rider.","The new jackets just arrived.","The machines still take coins.","I kept a copy of that reel.",
                 "Fresh paint dries fast.","This room has good acoustics.","The palms hide old records.","Listen for the starting bell.")
        tell(VENUES[n],(chatter[n],TASK[t]))

def follow_wire(s,n):
    index=s['wire']
    line_text=wire_note(index)[1]
    next_stop=WIRE[index+1] if index+1<len(WIRE) else -1
    if n in (15,13,18,19):
        from EVOMENU import tune
        landmark={15:"Breakwater relay",13:"East Docks antenna",
                  18:"Sawgrass field station",19:"Beacon Point tower"}[n]
        tell(landmark,(line_text,"Match all three bands."))
        bands=(8,0,6) if n==15 else (7,1,8) if n==13 else (6,0,7) if n==18 else (8,2,7)
        if not tune(bands):
            return
    s['wire']=index+1
    s['pin']=-1
    earn(s,8 if next_stop>=0 else 150)
    if next_stop>=0:
        tell("THE RELIEF TAPE",(line_text,"Next: "+NAMES[next_stop],
                              "Use the "+SIGNS[next_stop]+" counter."),0)
        notice(s,"Evidence filed / $8")
    else:
        tell("THE RELIEF TAPE / COMPLETE",("Mara airs the evidence in full.",
             "The stolen relief fund is traced.","Campaign complete / Bonus $150."),0)
        notice(s,"Campaign complete")

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
        from EVOMENU import enter_room
        if enter_room(s,n):
            venue(s,n)
    elif k=='local':
        lines=(("Ivo kept every pier show.","Look for the gold dot."),("The Foundry does gold flake.","Dispatch pays for the paint."),("Start the rally at the Lido.","Gold hoops mark each gate."))
        tell(("ANA / TECH","KIT / RUNNER","RED / DRIVER")[n],lines[n],n+2)
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
    if driving and highway(s['x'],s['z']):
        limit=19
    if not driving and s.get("fit",0)>s['clock']:
        limit+=2
    if k in (LEFT,RIGHT):
        turn=(0.20,0.39,0.58)[s.get('turn',1)]
        s['angle']=(s['angle']+(turn if k==RIGHT else -turn))%TAU
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

STORY_HELP=("Enter WAVE at West Quay.",
            "Put the car in park at PIER.",
            "PARTS sells the valve for $20.",
            "Enter FM 84 and tune 3 bands.",
            "PIXEL: original / VELVET: dub.",
            "Explore the city or take a job.",
            "Explore the city or take a job.")

def journal(s):
    ending=("AIRWAVES","ARCHIVE")
    title=ending[s['stage']-5] if s['stage']>=5 else "DEAD AIR / STORY"
    job=NAMES[s['job']-1] if s['job'] else "Visit Kiln Yard"
    count=sum((s['records']>>i)&1 for i in range(3))
    objective,help_line=TASK[s['stage']],STORY_HELP[s['stage']]
    if s['stage']>=5 and s['wire']<len(WIRE):
        n=WIRE[s['wire']]
        objective=wire_note(s['wire'])[0]
        title="RELIEF TAPE %02d / %02d"%(s['wire']+1,len(WIRE))
        help_line="Counter at "+SIGNS[n]+" / "+NAMES[n]
    elif s['stage']>=5:
        title="CAMPAIGN COMPLETE"
    while True:
        mode="Full" if s['detail'] else "Fast"
        turn=("Fine","Normal","Sharp")[s.get("turn",1)]
        sheet(title,(objective,help_line,"Parcel: "+job,"Records "+str(count)+"/3 | 2nd "+mode,
                     "Checkpoint: "+passcode(s),"RIGHT turning: "+turn),
                     "ENTER back / CLEAR quit")
        k=keywait((OK,EXIT,MAP,RIGHT))
        if k==RIGHT:
            s['turn']=(s.get('turn',1)+1)%3
        elif k==MAP:
            s['detail']=not s['detail']
        else:
            return k!=EXIT


def play():
    from EVOSPORT import front_menu
    k,settings=front_menu(not clip_played)
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
        tell("WEST QUAY / DUSK",("Mara's station goes silent","at midnight. Her studio is","the WAVE door ahead.","Enter the WAVE door.","Walk UP to the counter."))
    tell("STREET CONTROLS",("ENTER: talk, shop, car, park","2nd: map and district pins","ALPHA: journal / checkpoint","CLEAR: journal and quit","DEL: phone and taxi"))
    s["detail"],s["turn"],perspective=settings
    previous=None
    cockpit=False
    controls=(UP,DOWN,LEFT,RIGHT,OK,MAP,EXIT,31,23,14)
    while get_key(0)==OK:
        pass
    while True:
        if perspective:
            previous=render(s,cockpit,previous)
        else:
            from EVOMENU import street_map
            previous=street_map(s,previous)
        k=keywait(controls)
        while get_key(0)==k:
            pass
        if k==14:
            if perspective and s['drive'] and not cockpit:
                cockpit=True
            else:
                perspective=not perspective
                cockpit=False
            previous=None
        elif k in (EXIT,31):
            if not journal(s): return
            previous=None
        elif k==23:
            from EVOMENU import phone
            phone(s)
            previous=None
        elif k==MAP:
            from EVOMENU import atlas
            atlas(s)
            previous=None
        elif k==OK:
            interact(s)
            if not s['drive']:
                cockpit=False
            previous=None
        else:
            # Advance once per key so movement stays matched to the picture.
            tick(s,k,0.18)
            if k in (UP,DOWN) and s['speed']:
                tick(s,0,0.18)

play()
