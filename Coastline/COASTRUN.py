try:
    import gc
    gc.threshold(1024)
except (ImportError,AttributeError):pass
from COASTLIB import (
    CHAPTERS, COURSES, DOWN, EXIT, GOALS, INK, LEFT,
    MAP, MILK, MINT, NAMES, OK, PURSES, RIGHT,
    SUN, TASK, TAU, TOP, UP, VENUES, alert,
    blocked, box, center, checkpoint, closest, cos, crew,
    defeat, door, draw, earn, fresh, gate, get_key,
    keywait, label, monotonic, near, notice, packed, pay,
    pick, region, roadblock, sheet, sin, sync_search,
    tell, unpack, weather
)
try:
    from gc import collect
except ImportError:
    def collect():pass
collect()
from COASTMAP import (
    atlas, render, traffic, title_key
)
collect()
from COASTAPP import (
    equipment, event_visit, handset, street_tick
)
collect()

from COASTFUN import (
    advance_story, club, fishing, harbor, park_at, radio, shop,
    social, start_race, tune
)
collect()


def venue(s,n):
    t=s['stage']
    if t==3 and n==2 and s['who']!=1:
        s['crew'][0]['coat']=s['coat']
        s['pair'],s['who'],s['coat']=1,1,s['crew'][1]['coat']
        s['district_heat']=-1
        sync_search(s)
        notice(s,"Sol takes the console")
    if t==0 and n==0:
        advance_story(s,"01 / LAST SHOW",("MARA: They sold our frequency.","At midnight they cut the feed.","My brother Ivo has their tape.","Find him at the pier booth."))
    elif t==1 and n==7:
        earn(s,30)
        advance_story(s,"02 / THE PIER TAPE",("IVO: That's my voice on it.","They hired me to reroute a","relief shipment. I kept proof.","Take $30 for a tower valve."))
    elif t==2 and n==1:
        shop(s,"GLASSHOUSE SUPPLY",(("Signal valve",20,'stage',3),))
        if s['stage']==3: s['pin']=-1
    elif t==3 and n==2:
        if tune():
            advance_story(s,"04 / DEAD AIR",("The transmitter warms up.","Then the coastal power dies.","MARA: Rook has a dock log.","Go east. Find the dock office."))
    elif t==4 and n==13:
        advance_story(s,"05 / LOW TIDE",("ROOK: That relief shipment","was sold. Ivo took our log","to the lighthouse for proof.","Find him at Breakwater."))
    elif t==5 and n==15:
        advance_story(s,"06 / THE LOGBOOK",("You find the log in a locker.","Ivo is stranded at the docks.","ROOK: The east road floods.","Foundry has storm equipment."))
    elif t==6 and n==8:
        s['grip']=1
        advance_story(s,"07 / STORM KIT",("The crew fits rain tires.","The radio works again.","Ivo is waiting at East Docks.","Take him up to Beacon Hill."))
    elif t in (7,8) and n==13:
        if s['rescue']:
            tell("IVO / KEEP MOVING",("Head north to Beacon Hill.",))
            return
        sheet("08 / THE RESCUE",("Ivo is in the passenger seat.","Drive north to Beacon Hill.","Park near LOOK and enter it.","You have 55 seconds."),"ENTER drive / CLEAR wait")
        if keywait((OK,EXIT))==OK:
            park_at(s,13,0)
            s['pin']=-1
            s['stage'],s['rescue'],s['timer']=8,True,55
    elif t==8 and n==12 and s['rescue']:
        s['rescue']=False
        earn(s,50)
        advance_story(s,"09 / HIGH GROUND",("Ivo is safe. He owns his part.","MARA: Air the original from","Arcade, or use the Velvet","dub to protect your source."))
    elif t==9 and n in (6,9):
        public=n==6
        title="10 / ORIGINAL TAPE" if public else "10 / THE VELVET DUB"
        message=("Ivo's voice stays on tape.","His name becomes public.") if public else ("The dock log names the firm.","The dub masks Ivo's voice.")
        sheet(title,message+("Take this master to FM Tower.",),"ENTER take / CLEAR leave")
        if keywait((OK,EXIT))==OK:
            s['choice']=1 if public else 2
            s['stage']=10
            s['pin']=-1
    elif t==10 and n==2:
        if tune((6,1,8)):
            advance_story(s,"11 / STORM SIGNAL",("Mara reads from the dock log.","Then the recorded deal airs.","The relief money is traced.","Mara waits at WAVE for you."))
    elif t==11 and n==0:
        public=s['choice']==1
        earn(s,180)
        advance_story(s,"ON THE RECORD" if public else "KEEP THE SIGNAL",
             (("Ivo testifies in public." if public else "Ivo gives the city the log."),
              ("The city hears his apology." if public else "He remains an unnamed source."),
              "The docks are put under audit.","WAVE reopens as a co-op.","+$180 / City stays open."))
        tell("12 / THE MORNING AFTER",("Mara hands you a studio key.","The next show starts at dawn.","CREDITS",("The two of you buy WAVE." if s['bank']>=100 and s['bond']>=6 else "WAVE opens its doors again."),("The crew lays low awhile." if crew(s)['rep']>=18 else "You stay for the first show.")))
    elif s['job']==n+1:
        earn(s,45)
        if s['pin']==n: s['pin']=-1
        s['job']=0
        s['parcel']=min(9,s['parcel']+1)
        tell("PARCEL SIGNED  +$45",("The night clerk signs for it.","Dispatch has more work."))
    elif n==5:
        shop(s,"THREAD DEPT.",(("Coral jacket",18,'coat',1),("Mint jacket",18,'coat',2),("Runners: faster walk",25,'shoes',1),("Blue jacket",0,'coat',0)))
    elif n==8:
        shop(s,"FOUNDRY CUSTOMS",(("Rose lacquer",24,'paint',1),("Gold flake",32,'paint',2),("Sea glass",0,'paint',0),("Rain tires",45,'grip',1)))
    elif n==4:
        if not s['job']:
            choices=(3,5,7,9,11,12,13,14,15)
            s['job']=1+choices[(int(s['clock'])+s['parcel'])%len(choices)]
        s['pin']=s['job']-1
        tell("NIGHT DISPATCH",("Hand this parcel to the clerk","at "+NAMES[s['job']-1]+".","Delivery pays $45."))
    elif n==11:
        if not s['rescue']: start_race(s)
    elif n==6:
        tell("PIXEL PALACE",("Needle Match pays $12.","Catch all three gold bands."))
        if tune((3,7,0)):
            earn(s,12)
            notice(s,'High score! +$12')
    elif n==3:
        sheet("MARINA / HARBOR SERVICE",("ENTER: Ferry to East Docks $5.","RIGHT: Pilot the buoy skiff.","Your coupe stays parked."),"CLEAR leave")
        k=keywait((OK,RIGHT,EXIT))
        if k==RIGHT: harbor(s)
        if k==OK:
            if pay(s,5):
                s['x'],s['z']=center(13)
                sync_search(s)
                notice(s,'East Docks landing')
            else: notice(s,'Fare is $5')
    elif n==10:
        tell("PALM GARDEN",("Six gold singles are hidden.","Check Kiln Yard, FM Tower,","the Lido and the east coast."))
    elif n==14:
        fishing(s)
    elif n==9:
        club(s)
    elif n==12:
        sheet("BEACON / SAFEHOUSE",("Rest until the sky changes.","ALPHA shows your save code."),"ENTER rest / CLEAR leave")
        if keywait((OK,EXIT))==OK:
            s['heat']=0
            crew(s)['zones'][region(s)]=0
            s['clock']+=44
            notice(s,'Rested at Beacon Hill')
    elif n==0:
        radio(s,False)
    else:
        tell(VENUES[n],(TASK[t],"2nd opens your city map."))

def interact(s):
    x,z=s['x'],s['z']
    s['speed']=0
    if s['drive']:
        for n in (4,5,13):
            u,v=door(n)
            if near(x,z,u,v,5):
                order=pick("DRIVE THROUGH",("Park and get out","Refuel $5","Meal $4"))
                if order<0:return
                if order==2:
                    if pay(s,4): crew(s)['hunger']=0;crew(s)['hp']=min(80+3*crew(s)['power'],crew(s)['hp']+12)
                    return
                if order==1:
                    if pay(s,5):s['fuel']=100
                    return
        s['drive']=False
        s['parkangle']=s['angle']
        for dx,dz in ((1.8,0),(-1.8,0),(0,1.8),(0,-1.8)):
            if not blocked(x+dx,z+dz,0.35):
                s['x'],s['z']=x+dx,z+dz
                break
        if s['race']>=0:
            s['race']=-1
            notice(s,'Trial ended / Lido to retry')
        else:
            notice(s,'Parked / on foot')
        return
    k,n=closest(s)
    if k=='car':
        s['drive']=True
        s['x'],s['z']=s['cx'],s['cz']
        s['angle']=s['parkangle']
        notice(s,'UP gas / DOWN brake or back')
    elif k=='door':
        if n!=GOALS[s['stage']] and not (s['stage']==9 and n==9) and event_visit(s):return
        venue(s,n)
        crew(s)['coat']=s['coat']
    elif k=='local':
        social(s,n)
        return
    elif k=='cache':
        h=crew(s)
        s['loot']|=1<<n
        if n==0:
            h['reserve']=min(63,h['reserve']+18)
            notice(s,"Cache / 18 reserve rounds")
        elif n==1:
            h['arms']|=2
            h['gun']=1
            h['ammo']=6
            notice(s,"Cache / revolver equipped")
        else:
            h['hp']=min(80+3*h['power'],h['hp']+32)
            h['stam']=min(64+4*h['cardio'],h['stam']+20)
            notice(s,"Cache / first aid")
    elif k=='disc':
        s['records']|=1<<n
        reward=75 if s['records']==63 else 15
        earn(s,reward)
        notice(s,'Rare single found! +$'+str(reward))
    else:
        notice(s,'Find a lit door or your coupe')

def tick(s,k,dt):
    driving=s['drive']
    wet=weather(s) in (1,3)
    limit=(14 if not wet or s['grip'] else 10) if driving else (6 if s['shoes'] else 4)
    turning=0.18 if driving and wet and not s['grip'] else 0.23
    if driving:
        limit=min(limit+(TOP[s['ride']]-14),TOP[s['ride']])
        if s['body']<30:limit*=0.55
        if s['fuel']<=0:limit=0
    elif s['stance']==1 and crew(s)['stam']>=1:limit+=3
    elif s['stance']==2:limit*=0.5
    if k==LEFT: s['angle']=(s['angle']-turning)%TAU
    if k==RIGHT: s['angle']=(s['angle']+turning)%TAU
    if k==UP: s['speed']=min(limit,max(0,s['speed'])+(3 if driving else limit))
    if k==DOWN:
        s['speed']=0 if s['speed']>0 else -limit*0.4
    s['speed']=min(limit,s['speed'])
    d=s['speed']*dt
    x,z=s['x'],s['z']
    r=0.85 if driving else 0.35
    u=x+sin(s['angle'])*d
    v=z+cos(s['angle'])*d
    if not blocked(u,z,r): s['x']=u
    if not blocked(s['x'],v,r): s['z']=v
    if d and x==s['x'] and z==s['z']: s['speed']=0
    traveled=abs(x-s['x'])+abs(z-s['z'])
    if driving and abs(d)>0.5 and traveled<0.05 and not s['fine']:
        s['body']=max(0,s['body']-int(abs(d)*3))
        s['fine']=1
        if s['body']<=0:
            defeat(s,False)
            return
    sync_search(s)
    street_tick(s,dt,traveled)
    s['stride']+=abs(d)*2
    s['clock']+=dt
    if s['pin']>=0 and s['pin']!=s['job']-1:
        u,v=door(s['pin'])
        if near(s['x'],s['z'],u,v,2.7): s['pin']=-1
    s['ttl']=max(0,s['ttl']-dt)
    s['fine']=max(0,s['fine']-dt)
    if driving:
        s['cx'],s['cz']=s['x'],s['z']
        if s['speed']>6 and not s['fine']:
            for u,v in traffic(s['clock']):
                if near(s['x'],s['z'],u,v,1.5):
                    if s['race']<0:alert(s,1)
                    s['body']=max(0,s['body']-12)
                    if not s['body']:defeat(s,False);return
                    s['cash']=max(0,s['cash']-5)
                    s['speed']=0
                    s['fine']=3
                    notice(s,'Traffic contact / $5 repair')
                    break
    barrier=roadblock(s)
    if driving and barrier and not s['fine'] and abs(s['speed'])>4:
        if near(s['x'],s['z'],barrier[0],barrier[1],1.6):
            s['body']=max(0,s['body']-15)
            s['fine'],s['speed']=4,0
            if not s['body']:defeat(s,False);return
            notice(s,"Roadblock / car damaged")
    if s['heat']>0:
        s['heat']=max(0,s['heat']-dt)
        stars=crew(s)['zones'][region(s)]
        if near(s['x'],s['z'],s['px'],s['pz'],15):
            s['lastx'],s['lastz']=s['x'],s['z']
        dx=s['lastx']-s['px']
        dz=s['lastz']-s['pz']
        pace=dt*(3+stars+crew(s)['rep']//6)/max(1,abs(dx),abs(dz))
        u=s['px']+dx*pace
        v=s['pz']+dz*pace
        if not blocked(u,s['pz'],0.6): s['px']=u
        if not blocked(s['px'],v,0.6): s['pz']=v
        if near(s['x'],s['z'],s['px'],s['pz'],1.9):
            defeat(s,True)
        elif not s['heat']:
            crew(s)['zones'][region(s)]=0
            notice(s,'Search called off')
    if s['rescue']:
        s['timer']-=dt
        if s['timer']<=0:
            s['rescue']=False
            s['stage']=7
            park_at(s,13,0)
            s['drive']=False
            s['x'],s['z']=door(13)
            notice(s,'Rescue retry at the dock')
    if s['race']>=0:
        s['timer']-=dt
        u,v=center(gate(s))
        if s['timer']<=0:
            s['race']=-1
            notice(s,'Time up / retry at Lido')
        elif driving and near(s['x'],s['z'],u,v,3.4):
            s['race']+=1
            if s['race']==len(COURSES[s['course']]):
                s['race']=-1
                s['medals']|=1<<s['course']
                prize=PURSES[s['course']]
                earn(s,prize)
                notice(s,'Circuit complete! +$'+str(prize))
            else: notice(s,'Gate cleared!')

def journal(s):
    count=sum((s['records']>>i)&1 for i in range(6))
    medals=sum((s['medals']>>i)&1 for i in range(3))
    stage=s['stage']
    title=CHAPTERS[stage] if stage<12 else ("ON THE RECORD" if s['choice']==1 else "KEEP THE SIGNAL")
    if stage<12:
        chapter=(0,1,1,2,2,3,3,4,4,5,5,5)[stage]
        title=("PROLOGUE" if chapter==0 else "CH "+str(chapter))+" / "+title
    page=0
    while True:
        mode="Full" if s['detail'] else "Fast"
        if page==0:
            target="Retry at East Docks" if stage==8 and not s['rescue'] else TASK[stage]
            lines=(target,("Parcel: "+NAMES[s['job']-1]) if s['job'] else "Parcels: Visit Kiln Yard",
                   "DEL: show full checkpoint","2nd graphics: "+mode,"RIGHT: activity tracker")
        else:
            lines=("Records "+str(count)+"/6   Medals "+str(medals)+"/3",
                   "Fish released: "+str(s['fish'])+("+" if s['fish']==9 else ""),"Parcels delivered: "+str(s['parcel']),
                   "Road tires: "+("Rain" if s['grip'] else "Standard"),"LEFT: story and checkpoint")
        sheet(title if page==0 else "CITY ACTIVITIES",lines,"ENTER back / CLEAR quit")
        k=keywait((OK,EXIT,MAP,LEFT,RIGHT,23))
        if k==23:checkpoint(s);continue
        if k in (OK,EXIT): return k!=EXIT
        if k==MAP: s['detail']=not s['detail']
        if k==RIGHT: page=1
        if k==LEFT: page=0

def play():
    k=title_key()
    if k==EXIT: return
    if k==MAP:
        while True:
            print("Enter checkpoint or 0 to exit")
            code=input().strip()
            if code=="0": return
            if len(code)==20:
                for line_no in range(3):
                    print("Next checkpoint row")
                    code+=input().strip()
            s=unpack(code)
            if s is not None: break
            print("Check the digits and retry.")
        draw.clear()
    else:
        s=fresh()
        tell("PROLOGUE / WEST QUAY",("Lena and Sol ran cash jobs.","Now WAVE needs their help.","Walk to the WAVE door ahead.","UP starts / DOWN stops.","LEFT and RIGHT turn you."))
    tell("STREET CONTROLS",("ENTER: talk, shop, car, park","2nd: map / DEL: phone","MODE: actions / rooms / crew","ALPHA: journal, DEL for save","TRACE skyline / CLEAR x2 quit"))
    buffer=[]
    slowframes=0
    autotune=True
    while True:
        start=monotonic()
        render(s,buffer)
        if autotune and s['detail']:
            slowframes=slowframes+1 if monotonic()-start>.30 else 0
            if slowframes>=3:
                s['detail']=False
                autotune=False
                notice(s,"Fast detail / journal to change")
        k=buffer.pop(0) if buffer else get_key(0)
        while not k and monotonic()-start<0.075:
            k=get_key(0)
        if k in (EXIT,31):
            buffer=[]
            before=s['detail']
            if not journal(s): return
            if before!=s['detail']:autotune=False
            continue
        if k==14:
            buffer=[]
            s['lookup']=not s.get('lookup',False)
            notice(s,"Skyline view" if s['lookup'] else "Street view")
            continue
        if k==MAP:
            buffer=[]
            atlas(s)
            continue
        if k==22:
            buffer=[]
            equipment(s)
            continue
        if k==23:
            buffer=[]
            handset(s)
            continue
        if k==OK:
            buffer=[]
            interact(s)
            continue
        tick(s,k,min(0.22,max(0.035,monotonic()-start)))

play()
