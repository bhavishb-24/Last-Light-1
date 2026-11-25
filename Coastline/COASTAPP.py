from COASTLIB import (
    COATS, DOWN, EXIT, GOLD, GUNS, INK, LEFT,
    MAP, MILK, MINT, NAMES, NICK, NIGHT, OK,
    RED, REGION, REGIONS, RIGHT, SIGNS, STEEL, SUN,
    TIERS, TRIM, UP, VIOLET, alert, bond, box,
    checkpoint, crew, defeat, disc, district, door, earn,
    event_at, event_name, keywait, label, line, near, notice,
    pay, pick, profile, region, tell
)
from COASTMAP import (
    atlas, person, render
)

def scene(name):
    # Keep one optional scene resident on small MicroPython heaps.
    try:
        from gc import collect, mem_free
        from sys import modules
        if mem_free()<65000:
            for old in ('COASTTEL','COASTACT','COASTSEA'):
                if old!=name and old in modules:del modules[old]
            collect()
    except (ImportError,AttributeError):pass

def handset(s):
    scene('COASTTEL')
    from COASTTEL import phone
    phone(s)

def neighborhood(s):
    from COASTFUN import social
    n=district(s['x'],s['z'])
    x,z=door(n)
    if not near(s['x'],s['z'],x,z,7):
        s['pin']=n
        notice(s,"Meet at "+SIGNS[n]+" door")
        return
    names=("Street activities","Food and supplies","Room directory","Speak to residents",
           "Gym front desk","Animal encounter","Garage and services","Neighborhood job")
    i=pick(REGIONS[REGION[n]],names)
    h=crew(s)
    if i==0:
        scene('COASTACT')
        from COASTACT import play_sport
        play_sport(s,n)
    elif i==1:
        items=("Meal $4","Sports drink $3","Pet snack $2","Tattoo $18","Barber $7","Ammo pack $6")
        k=pick("COUNTER",items)
        if k<0: return
        if not pay(s,(4,3,2,18,7,6)[k]): notice(s,"Need more cash"); return
        if k==0:
            h['hunger']=max(0,h['hunger']-6)
            h['weight']=min(7,h['weight']+1)
            h['hp']=min(80+h['power']*3,h['hp']+18)
        elif k==1: h['stam']=min(64+4*h['cardio'],h['stam']+25)
        elif k==2: s['snack']=min(7,s['snack']+1)
        elif k==3: h['tat']=1
        elif k==4: h['style']=(h['style']+1)%3; h['hair']=1
        else: h['reserve']=min(63,h['reserve']+12)
        bond(s)
        notice(s,"Purchase complete")
    elif i==2: interior(s,n)
    elif i==3: social(s,n)
    elif i==4:
        if n in (5,10,12):
            scene('COASTACT')
            from COASTACT import gym
            gym(s)
        else: s['pin']=5; notice(s,"Gym pinned: Lantern Sq")
    elif i==5:
        k=pick("ANIMAL ENCOUNTER",("Pet the dog","Offer pet snack","Observe wildlife","Ask ranger for work"))
        if k==0: profile(s,-1); notice(s,"The dog wags its tail")
        if k==1 and s['snack']:
            s['snack']-=1
            s['pet']=1
            notice(s,"Dog joins your safehouse")
        if k==2:
            scene('COASTACT')
            from COASTACT import outing
            outing(s,11)
        if k==3:
            if n==10: s['hunt']=1; notice(s,"Paid surveys at Tin Marsh")
            else: s['pin']=10; notice(s,"Ranger at Palm Garden")
    elif i==6: garage(s,n)
    elif i==7: job(s,n)

def garage(s,n):
    k=pick("MOTOR SERVICES",("Refuel $5","Repair $12","Spray $18","Access token $25","Elite token $55","Store nearby vehicle"))
    if k<0:return
    if k in (0,1,2,5) and not near(s['x'],s['z'],s['cx'],s['cz'],15):
        notice(s,"Bring your car to the shop"); return
    if k==5:
        if n not in (0,8,12): notice(s,"Use garage at Quay/Hill/Yard"); return
        s['stored']|=1<<s['ride']
        notice(s,"Car saved to lockup"); return
    if k>=3 and n!=8: s['pin']=8; notice(s,"Tokens at Foundry"); return
    if k==2 and n not in (4,8,13): s['pin']=8; notice(s,"Spray shop pinned"); return
    if not pay(s,(5,12,18,25,55)[k]): notice(s,"Need more cash"); return
    if k==0: s['fuel']=100
    elif k==1: s['body']=100
    elif k==2:
        s['paint']=(s['paint']+1)%3
        crew(s)['zones'][region(s)]=0
        s['heat']=0
    else: s['token']=max(s['token'],k-2)
    notice(s,"Service complete")

def job(s,n):
    # Fictional objectives resolved through abstract pattern challenges.
    from COASTFUN import cues
    if n==4 and s['vault']==0:
        if cues("NIGHT JOB / FIND THE SEAL",(UP,RIGHT,DOWN)):
            s['vault']=1
            notice(s,"Seal recovered / East Docks")
    elif n==13 and s['vault']==1:
        if cues("DOCK MANIFEST",(LEFT,UP,LEFT,RIGHT)):
            s['vault']=2
            notice(s,"Crew ready / Glasshouse")
    elif n==1 and s['vault']==2:
        if not s['pair']: notice(s,"Bring both partners"); return
        if cues("VAULT / MOSAIC",(RIGHT,DOWN,UP,LEFT,RIGHT)):
            s['vault']=3
            earn(s,200); bond(s); alert(s,3)
            notice(s,"Vault clear / $200 wallet")
    else:
        if cues("CASH RUN / MATCH SYMBOLS",(UP,LEFT,RIGHT,DOWN)):
            earn(s,25); alert(s,1); bond(s)
            notice(s,"Cash run / $25 wallet")

ROOMTYPES=("Diner","Flat","Motel","Workshop","Bar","Studio")
def interior(s,n):
    from COASTFUN import social, switch
    unit=pick("BLOCK DIRECTORY",tuple("Floor "+str(i+1) for i in range(4)))
    if unit<0:return
    wing=pick("LANDING",tuple("Door "+str(i+1) for i in range(4)))
    if wing<0:return
    addr=16*n+4*unit+wing
    home=n in (0,12) and unit==0 and wing==0
    room="Safehouse" if home else ROOMTYPES[addr%6]
    x,y=2,4
    while True:
        box(INK,0,0,320,210)
        box(TRIM[n%4],17,34,286,130)
        box((74,63,84),23,40,274,117)
        for j in range(7):
            line(VIOLET,26,45+j*16,291,45+j*16)
        fx=4+(addr%3)
        box(NIGHT,32+fx*30,59,56,30)
        box(GOLD,35+fx*30,61,50,4)
        if room in ("Diner","Bar"):
            for tx in (53,97,236):
                box((98,62,65),tx,95,28,11)
                box(SUN,tx+3,93,22,3)
                box(INK,tx+6,109,15,6)
        elif room in ("Flat","Motel","Safehouse"):
            box(VIOLET,41,56,65,27)
            box(MILK,43,57,16,16)
            box(TRIM[addr%4],65,56,41,26)
        elif room=="Workshop":
            for tx in (44,64,84):
                disc(INK,tx,75,9)
                disc(STEEL,tx,75,4)
        else:
            box(INK,39,56,48,27)
            for j in range(6):
                box(TRIM[j%4],42+j*7,63+(j*7)%11,4,5)
        box(INK,82,146,44,14)
        person(38+x*30,60+y*18,25,COATS[s['coat']],0,True)
        if home and s['pet']:
            box(GOLD,62,75,14,7); box(GOLD,70,71,6,6)
        label(MILK,7,24,room+" "+str(addr+1))
        label(SUN,6,184,"Arrows walk / ENTER counter")
        label(MILK,6,205,"CLEAR street")
        k=keywait((UP,DOWN,LEFT,RIGHT,OK,EXIT))
        if k==EXIT:return
        x=max(0,min(8,x+(k==RIGHT)-(k==LEFT)))
        y=max(0,min(5,y+(k==DOWN)-(k==UP)))
        if k!=OK:continue
        if abs(x-fx)>2 or y>2:notice(s,"Walk to the counter");continue
        if home:
            bit=1 if n==0 else 2
            if not s['homes']&bit:
                if pick("HILL LEASE",("Buy home $90",))==0 and pay(s,90): s['homes']|=bit
                else: continue
            h=crew(s)
            a=pick("AT HOME",("Checkpoint","Wardrobe","Trim hair","Call partner","Store car","Rest"))
            if a==0:checkpoint(s)
            elif a==1:
                c=pick("WARDROBE",("Blue jacket","Coral jacket","Mint jacket"))
                if c>=0 and (c==0 or c==s['coat'] or pay(s,18)): s['coat']=c
            elif a==2:h['hair']=0
            elif a==3:switch(s)
            elif a==4 and near(s['x'],s['z'],s['cx'],s['cz'],15):s['stored']|=1<<s['ride']
            elif a==5:h['hp']=80+3*h['power'];h['stam']=64+4*h['cardio'];s['clock']+=44
        elif room in ("Diner","Bar"):
            if pick(room,("House meal $4",))==0 and pay(s,4):
                h=crew(s);h['hunger']=max(0,h['hunger']-5);h['hp']=min(80+3*h['power'],h['hp']+18)
        elif room=="Workshop":garage(s,n)
        else:social(s,n)

def equipment(s):
    from COASTFUN import switch
    h=crew(s)
    k=pick("STREET ACTIONS",("Arcade aim","Loadout","Walk / sprint / crouch","Jump or vault",
        "Request partner","Surrender or profile","Work / interiors","Map and activities","Coastal transport"))
    if k==0: encounter(s)
    elif k==1:
        a=pick("LOADOUT",tuple(("* " if h['arms']&(1<<i) else "$15 ")+name for i,name in enumerate(GUNS)))
        if a>=0:
            if not h['arms']&(1<<a):
                if not pay(s,15):notice(s,"Need $15");return
                h['arms']|=1<<a
            h['gun']=a
            notice(s,GUNS[a]+" equipped")
    elif k==2:
        a=pick("MOVEMENT",("Walk","Sprint","Crouch"))
        if a>=0:s['stance']=a
    elif k==3 and not s['drive'] and crew(s)['stam']>3:
        s['jump']=0.7
        crew(s)['stam']-=3
    elif k==4:switch(s)
    elif k==5:
        tell("CRIMINAL PROFILE",(NICK[s['who']],TIERS[min(4,h['rep']//6)],
             "Health "+str(int(h['hp']))+" / Focus "+str(h['focus']),"Bond "+str(1+min(3,s['bond']//6))+"/4",
             "Fracture warning" if 20<=h['rep']<24 else ""))
        switch(s)
    elif k==6:neighborhood(s)
    elif k==7:atlas(s)
    elif k==8:
        scene('COASTSEA')
        from COASTSEA import voyage
        voyage(s,district(s['x'],s['z']))

def encounter(s):
    h=crew(s)
    # Arcade encounter with a moving target and independent magazine.
    threat=s['heat']>0
    phase=0
    aim=0
    hits=0
    cover=False
    while True:
        target=(phase%7)-3
        render(s)
        box(INK,0,0,320,25)
        box(INK,0,158,320,52)
        person(160+25*target,137,49,RED if threat else GOLD,phase,False)
        if cover:box(STEEL,0,120,120,42)
        line(MINT,151+25*aim,106,169+25*aim,106)
        line(MINT,160+25*aim,98,160+25*aim,115)
        label(MILK,5,23,GUNS[h['gun']]+" "+str(h['ammo'])+"/"+str(h['reserve']))
        label(SUN,5,177,"L/R aim  UP lock  DOWN cover")
        label(MILK,5,204,"ENTER fire / 2nd options")
        k=keywait((LEFT,RIGHT,UP,DOWN,OK,MAP,EXIT))
        if k==EXIT:return
        if k==LEFT:aim=max(-3,aim-1)
        if k==RIGHT:aim=min(3,aim+1)
        if k==UP:aim=target
        if k==DOWN:cover=not cover
        if k==MAP:
            q=pick("ENCOUNTER",("Reload","Spend focus","Disengage peacefully","Nonlethal takedown"))
            if q==0:
                count=min(max(0,6-h['ammo']),h['reserve']);h['ammo']+=count;h['reserve']-=count
            if q==1 and h['focus']>=3:
                h['focus']-=3
                s['slow']=max(1,4+h['skill']//2-h['rep']//6)
            if q==2:profile(s,-1);return
            if q==3 and (cover or s['stance']==2):
                profile(s,-1)
                if h['rep']<12:h['focus']=min(31,h['focus']+2)
                return
        if k==OK and h['ammo']:
            h['ammo']-=1
            if aim==target:
                hits+=2 if h['gun'] in (3,5) else 1
                h['focus']=min(31,h['focus']+1)
            if not threat:profile(s,3);alert(s,2);threat=True
            if hits>=2:
                notice(s,"Encounter over");return
            aim=max(-3,min(3,aim+(1 if h['gun'] in (1,3,5) else 0)))
        if k in (OK,DOWN,MAP):
            if threat and not cover:h['hp']=max(0,h['hp']-8)
            if h['hp']<=0:defeat(s,False);return
            if s['slow']>0:s['slow']-=1
            else:phase+=1

def event_visit(s):
    n=event_at(s)
    u,v=door(n)
    if not near(s['x'],s['z'],u,v,5):return False
    serial=int(s['clock']//75)%30+1
    if s['event']==serial:return False
    if pick(event_name(s),("Join live event","Continue to venue"))==0:
        s['event']=serial
        s['photo']=min(31,s['photo']+1)
        s['lastpic']=n
        earn(s,12);bond(s)
        tell("LIVE POST",("Shared from "+NAMES[n],"+$12 local tip"))
        return True
    return False

def street_tick(s,dt,distance):
    h=crew(s)
    old=int(s['rest']//15)
    s['rest']+=dt
    if int(s['rest']//15)!=old:
        h['hunger']=min(15,h['hunger']+1)
        if h['hunger']==15:h['weight']=max(0,h['weight']-1)
        if old%5==4:h['hair']=min(3,h['hair']+1)
        h['stam']=min(64+4*h['cardio'],h['stam']+6)
    if s['drive']:
        s['fuel']=max(0,s['fuel']-distance*.05)
        if not s['fuel'] and s['speed']:
            s['speed']=0;notice(s,"Empty tank / call delivery")
    elif s['stance']==1:
        h['stam']=max(0,h['stam']-distance*.25)
        if not h['stam']:s['stance']=0
    if s['pair']:
        s['distance']+=distance
        if s['distance']>=90:s['distance']-=90;bond(s)
    s['jump']=max(0,s['jump']-dt)

