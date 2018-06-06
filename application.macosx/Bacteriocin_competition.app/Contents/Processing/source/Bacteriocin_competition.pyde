from __future__ import division
import bacteria as bac
import iterate_population as it

#UI
strain_num = "0"
strain_choosing = True
target_choosing = False
strains = []
target_lines = []
gap = 10
std_rad = 20
rad = 20

simulate = False

#simulation
density = 10
competition_range = 3
timeStep = 1
community = []
occupants = []
historyCounts = []
mode = "NA"
epoch = 0

def setup():
    #UI - NEEDED FOR SURE
    size(1000,1000)
    background(255)
    fill(0)
    noStroke()
    colorMode(HSB)

def draw():
    background(255)
    global occupants
    global historyCounts
    global rad 
    global simulate
    global epoch
    
    if simulate:
        diversity = len(community)
        counts = [0 for i in community] 
        textAlign(LEFT)
        textSize(14)
        # controls number of cycles between each rendering of the simulation
        for a in range(int((width/density)*(height/density))):
            i = floor(random(0,len(occupants)))
            neighborFreqs = it.iterate(i,competition_range,occupants,diversity,density, False)
        
            if occupants[i] == "empty":
                prob = []
                for j in range(len(neighborFreqs)):
                    resist_penalty = 0
                    if neighborFreqs[j][1] != "none of this type":
                        resist_penalty = sum(neighborFreqs[j][1].resistances)*(0.08*neighborFreqs[j][1].birth)
                        prob.append((neighborFreqs[j][1].birth*neighborFreqs[j][0]-resist_penalty)*timeStep)
                    else:
                        prob.append(0)
            
                chance = random(0,sum(prob))
                this = "empty"
                for j in range(len(prob)):
                    chance -= prob[j]
                    if chance < 0:
                        parent = neighborFreqs[j][1]
                        if mode == "equilibrium" or "bet_hedging" or "bet_hedging_resistance":
                            this = bac.newBacteria(parent.ID, parent.birth, parent.death, parent.sensitivities, parent.resistances[0:], parent.colour)
                        else:
                            this = bac.newBacteria(parent.ID, parent.birth, parent.death, parent.sensitivities, mutate(parent.resistances[0:]), parent.colour)
                        break
                occupants[i] = this
            else:
                if mode == "bet_hedging" or mode == "bet_hedging_resistance":
                    if occupants[i].colour != 200:
                        chance = random(0,1)
                        if chance < occupants[i].death: 
                            occupants = it.iterate(i, 1, occupants, diversity, density, True)           
                    else:
                        chance = random(0,1)
                        fate = occupants[i].death #these must be less than one; lower means less likely to die
                        fate *= timeStep
                        this = occupants[i]
                        if fate > chance:
                            this = "empty"
                        occupants[i] = this
                    
                else:
                    chance = random(0,1)
                    fate = occupants[i].death
                    this = occupants[i]
                    for j in occupants[i].sensitivities:
                        if occupants[i].resistances[j] == False:
                            fate += occupants[i].sensitivities[j]*neighborFreqs[j][0]
                        
                    fate *= timeStep
                    if fate > chance:
                        this = "empty"
                    occupants[i] = this
            
        
    
        
        # RENDER original simulation: 
        if mode != "bet_hedging" and mode != "bet_hedging_resistance":
            for i in range(len(occupants)):
                if occupants[i] == "empty":
                    fill(0,0,255)
                else:
                    resist_level = 255
                    highlight_resistance = 75
                    if len(occupants[i].resistances) > 0:
                        resist_level = map(sum(occupants[i].resistances), 0, len(occupants[i].resistances), 255, 75)
                        highlight_resistance = map(sum(occupants[i].resistances), 0, len(occupants[i].resistances), 75, 255)
                    fill(occupants[i].colour, 155, 255)
                    counts[occupants[i].ID] += 1
                ellipseMode(CORNER)
                ellipse(i*density%(width),density*int(i/(width/density)),density,density)
        else:
            background(255)
    
            for i in range(len(occupants)):
                if occupants[i] == "empty":
                    fill(255)
                else:
                    if occupants[i].ID == 0:
                        fill(15, map(occupants[i].colour, 0, 255, 95, 255), map(occupants[i].colour, 0, 255, 95, 255))
                    if occupants[i].ID == 1:
                        fill(140,255,255)
                    if occupants[i].ID == 2:
                        fill(40,255,255)
                    counts[occupants[i].ID] += 1
                ellipseMode(CORNER)
                ellipse(i*density%(width),density*int(i/(width/density)),density,density)
        
    
        
        epoch += 1
        #if epochs % ((width/density)*(height/density)) == 0:
        historyCounts.append(counts)

        # stats panel
        noStroke()
        fill(0,0,0,165)
        rect(0,0,1000,90)
        fill(0,0,0,195)
        rect(0,90,1000,24)
        stroke(1)
        pct_chng = []
        for i in range(1, len(historyCounts)):
            for j in range(len(historyCounts[i])):
                if mode == "bet_hedging" or mode == "bet_hedging_resistance":
                    if j == 0:
                        stroke(15, 255, 255)
                    if j == 1:
                        stroke(140,255,255)
                    if j == 2:
                        stroke(40,255,255)
                else:
                    stroke(community[j].colour, 155, 255)
                x1 = map(i-1, 0, len(historyCounts)-1, 10,990)
                x2 = map(i, 0, len(historyCounts)-1, 10,990)
                y1 = map(log(historyCounts[i-1][j]+1)/ log(10), 0, log((width/density)*(height/density))/log(10), 80, 10)
                y2 = map(log(historyCounts[i][j]+1)/ log(10), 0, log((width/density)*(height/density))/log(10), 80, 10)
                line(x1,y1,x2,y2)
                if i == len(historyCounts) -1:
                    if historyCounts[i-1][j] != 0:
                        chng = round(((historyCounts[i][j]- historyCounts[i-1][j])/historyCounts[i-1][j])*100, 2)
                        pct_chng.append(chng)
                    else:
                        pct_chng.append(-1)
        fill(255)
        
        text("epoch: " + str(epoch), 10, 105)
        pct_chng_X = 990
        textAlign(RIGHT)
        textSize(14)
        tmp = []
        if len(pct_chng) > 6: # grab top and bottom 3 changes if I can't fit them all on screen easily
            sorted = [i for i in pct_chng if i != -1]
            sorted.sort(reverse=True)
            tmp = sorted[-3:]
            tmp += sorted[:3]
            tmp2 = [i for i in tmp]
            for i in range(len(pct_chng)):
                if pct_chng[i] in tmp2:
                    tmp2.remove(pct_chng[i])
                else:
                    pct_chng[i] = "NA"
        for i in range(len(pct_chng)):
            if pct_chng[i] != "NA" and pct_chng[i] != -1:
                if mode == "bet_hedging" or mode == "bet_hedging_resistance":
                    if i == 0:
                        fill(15, 255, 255)
                    if i == 1:
                        fill(140,255,255)
                    if i == 2:
                        fill(40,255,255)
                else:
                    fill(community[i].colour, 155, 255)
                if len(tmp) > 0:
                    INDEX = tmp.index(pct_chng[i])
                    text("{}% change  ".format(pct_chng[i]), pct_chng_X - (120*INDEX), 105)
                    tmp[INDEX] = "NA"
                    
                else:
                    text("{}% change  ".format(pct_chng[i]), pct_chng_X, 105)
                    pct_chng_X -= 120
        textSize(10)
        textAlign(LEFT)
        fill(255)
        text("E X I T", 3,10)
        noStroke()
        
        
    else: #if not simulating...
        textAlign(CENTER)
    
        if strain_choosing:
            fill(140,255,255)
            textSize(16)
            text("How many strains?", 500,350)
            textSize(44)
            text(strain_num, 500,485)
            
            #draw strains
            
            if len(strains) > 0:
                proposed_rad = (900 - (gap*(len(strains)-1)))/(len(strains)*2)
                if proposed_rad < std_rad:
                    rad = proposed_rad
                else:
                    rad = std_rad
            incr = ((gap*3/2)+(3*rad))
            even_num = (len(strains)+1)%2
            sign_flip = 1
            ellipseMode(CENTER)
            for i in range(len(strains)):
                sign_flip *= -1
                fill(91)
                if even_num:
                    if i < 2:
                        ellipse(500 + (sign_flip*(gap/2+rad)), 400, rad*2, rad*2)
                    else:
                        ellipse(500 + sign_flip*incr, 400, rad*2, rad*2)
                        if sign_flip == 1:
                            incr += (gap+2*rad)
                else:
                    if i == 0:
                        ellipse(500, 400, rad*2, rad*2)
                        incr = rad*2 + gap
                    else:
                        ellipse(500 + sign_flip*incr, 400, rad*2, rad*2)
                        if sign_flip == -1:
                            incr += (gap+2*rad)
        else:
            for i in range(len(target_lines)):
                p = strains[i]
                t = target_lines[i]
                strokeWeight(1)
                stroke(191)
                if p[3]: #is a boolean value indicating if its selected currently
                    strokeWeight(2)
                    stroke(191)
                for j in range(len(t)):
                    if t[j]:
                        line(p[0],400,strains[j][0],500)
                noStroke()
                
            #draw producers and targets
            for i in range(len(strains)):
                s = strains[i]
                fill(map(s[0], strains[0][0],strains[len(strains)-1][0],60,255),255,255)
                ellipse(s[0],s[1],s[2],s[2])
                fill(map(s[0], strains[0][0],strains[len(strains)-1][0],60,255),85,255)
                ellipse(s[0],s[1]+100,s[2],s[2])
                if s[3]:
                    fill(0,0,255,200)
                    ellipse(s[0],s[1],s[2]*.75,s[2]*.75)
            fill(140,255,255)
            rect(450,800,100,40)
            fill(255)
            textSize(18)
            text("RUN",500,825)
        



def keyPressed():
    global strain_num
    global strains
    global strain_choosing
    global target_choosing
    global target_lines
    global rad
    if strain_choosing:
        if key in [str(i) for i in range(10)]:
            if strain_num != "0" and len(strain_num) < 2:
                strain_num += key
            elif strain_num == "0":
                strain_num = key
                strains = []
            strains = [i for i in range(int(strain_num))]
        elif key == BACKSPACE:
            if len(strain_num) > 1:
                strain_num = strain_num[:-1]
                strains = strains[:-1]
            else:
                strain_num = "0"
                strains = []
        elif key == DELETE:
            strain_num = "0";
            strains = []
        elif keyCode == DOWN and int(strain_num) > 0:
            strains = strains[:-1]
            strain_num = str(int(strain_num)-1)
        elif keyCode == UP and int(strain_num) < 99:
            strains.append(str(int(strain_num)))
            strain_num = str(int(strain_num)+1)
        elif key == ENTER:
            if int(strain_num) > 1:
                strains = [i for i in range(int(strain_num))]
                strain_choosing = False
                target_choosing = True
                for i in range(len(strains)):
                    target_lines.append([False for i in range(int(strain_num))])
                proposed_rad = (900 - (gap*(len(strains)-1)))/(len(strains)*2)
                if proposed_rad < rad:
                    rad = proposed_rad
                    
                    
                incr = ((gap*3/2)+(3*rad))
                even_num = (len(strains)+1)%2
                sign_flip = 1
                for i in range(len(strains)):
                    sign_flip *= -1
                    if even_num:
                        if i < 2:
                            strains[i] = [500 + (sign_flip*(gap/2+rad)), 400, rad*2, False]
                        else:
                            strains[i] = [500 + sign_flip*incr, 400, rad*2, False]
                            if sign_flip == 1:
                                incr += (gap+2*rad)
                    else:
                        if i == 0:
                            strains[i] = [500, 400, rad*2, False]
                            incr = rad*2 + gap
                        else:
                            strains[i] = [500 + sign_flip*incr, 400, rad*2, False]
                            if sign_flip == -1:
                                incr += (gap+2*rad)
                                
                #rearrange strains to be same order as they appear on canvas
                def pos(elem):
                    return elem[0]
                strains.sort(key=pos)
                
    
    
def mousePressed():
    global target_lines
    global strain_choosing
    global target_choosing
    global strains
    global strain_num
    global community
    global occupants
    global historyCounts
    global simulate
    global epoch
    if target_choosing:
        if 380 < mouseY < 520:
            for i in range(len(strains)):
                s = strains[i]
                if s[0]-s[2]/2 < mouseX < s[0]+s[2]/2: #b/c target/producers share x coordinates, this check both groups at once.
                    if s[1]-s[2]/2 < mouseY < s[1]+s[2]/2:
                        for r in range(len(strains)):
                            st = strains[r]
                            if st == s:
                                st[3] = not st[3]
                            else:
                                st[3] = False
                        
                    elif (s[1]+100)-s[2]/2 < mouseY < (s[1]+100)+s[2]/2:
                        for a in range(len(strains)):
                            if strains[a][3]: 
                                target_lines[a][i] = not target_lines[a][i]
                                
        if 800 < mouseY < 840 and 450 < mouseX < 550: #RUN was pressed
            for i in range(len(strains)):
                sensitive = {}
                for j in range(len(target_lines[i])):
                    if target_lines[j][i]: #if strain j is sensitive to strain i
                        sensitive[j] = random(0.7,0.77)
        
                resistnt = [False for strain in strains]
                life = 1.23
                death = .33
                if sum(target_lines[i]) > 0:
                    life = 1
                hu = map(strains[i][0], strains[0][0],strains[len(strains)-1][0],60,255)
                community.append(bac.newBacteria(len(community), life, death, sensitive, resistnt, hu))
            for i in range(int((width/density)*(height/density))):
                chosen = floor(random(0,len(community)*1.5))
                if chosen < len(community):
                    occupants.append(bac.newBacteria(chosen, community[chosen].birth, community[chosen].death, community[chosen].sensitivities, community[chosen].resistances, community[chosen].colour))
                else:
                    occupants.append("empty")
            simulate = True
        if simulate:
            if mouseY < 20 and mouseX < 40: 
                strain_num = "0"
                strains = []
                target_lines = []
                simulate = False
                strain_choosing = True
                target_choosing = False
                historyCounts = []
                occupants = []
                community = []
                epoch = 0
                
            


    
def mutate(resist):
    # 1 in 6 million chance to either gain or lose the resistance state for each bacteriocin
    for i in resist:
        chance = random(0,1)
        if chance < 0.0001:
            resist[i] = not resist[i]
    return resist
            
            
            
