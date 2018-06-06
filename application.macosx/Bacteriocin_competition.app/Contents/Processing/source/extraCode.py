#from setup...

if mode != "bet_hedging" and mode != "bet_hedging_resistance":
        for i in range(len(occupants)):
            if occupants[i] == "empty":
                fill(0,0,255)
            else:
                fill(occupants[i].colour,75,255)
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
            ellipseMode(CORNER)
            ellipse(i*density%(width),density*int(i/(width/density)),density,density)
    # stats panel   
    fill(0,0,0,165)
    rect(0,0,1000,90)
    fill(0,0,0,195)
    rect(0,90,1000,24)
    
#modes

                            
# all strains have the possibility of being hurt by all other strains
def total_war(number_of_strains, density):
    community = []
    occupants = []
    diversity = number_of_strains
    for i in range(diversity):
        birth = 1
        death = 1/3
        sens = {}
        res = []
        for j in range (diversity):
            res.append(False)
            if i != j:
                sens[j] = int(round(random(1,4)))
            else:
                sens[j] = 1
        hu = int(map(i,0,diversity-1,30,255))
        community.append(bac.newBacteria(len(community),birth, death, sens, res, hu))
    
    for i in range(int((width/density)*(height/density))):
        chosen = floor(random(0,diversity*2))
        if chosen < diversity:
            occupants.append(bac.newBacteria(chosen, community[chosen].birth, community[chosen].death, community[chosen].sensitivities, community[chosen].resistances, community[chosen].colour))
        else:
            occupants.append("empty")
    mode = "total_war"
    return community, occupants, mode



# half producers, half sensitive
def good_v_evil(number_of_strains, density):
    community = []
    occupants = []
    diversity = number_of_strains
    for i in range(int(diversity/2)): #producers
        birth = 1
        death = random(0.32,0.36)
        sens = {}
        res = []
        for j in range (int(diversity/2)):
            res.append(False)
            if i != j:
                sens[j] = int(round(random(2,4)))
            else:
                sens[j] = 1
        
        hu = int(map(i,0,diversity/2-1,0,25))
        community.append(bac.newBacteria(len(community),birth, death, sens, res, hu))
        
    for i in range(int(diversity/2)): #sensitives
        birth = 1
        death = random(.22,.27)
        sens = {}
        res = []
        for j in range (int(diversity/2)):
            res.append(False)
            sens[j] = int(round(random(2,4)))
        hu = int(map(i,0,diversity/2-1,140,165))
        community.append(bac.newBacteria(len(community),birth, death, sens, res, hu))
    
    for i in range(int((width/density)*(height/density))):
        chosen = floor(random(0,diversity*2))
        if chosen < diversity:
            occupants.append(bac.newBacteria(chosen, community[chosen].birth, community[chosen].death, community[chosen].sensitivities, community[chosen].resistances, community[chosen].colour))
        else:
            occupants.append("empty")
    mode = "good_v_evil"
    return community, occupants, mode




# simple producer/resistant strain scenario
def resistance(density):
    community = []
    occupants = []
    
    community.append(bac.newBacteria(0, 1, 1/3, {}, [], 255)) # P: producer, slower growh rate due to production
    #community.append(bac.newBacteria(0, 1, 1/3, {}, [], 140)) # delta P: same exact strain, with toxin gene truncated.
    community.append(bac.newBacteria(0, 1, 1/4, {0:0.75}, [False], 40)) # sensitive

    for i in range(int((width/density)*(height/density))):
        chosen = floor(random(0,len(community)+1))
        if chosen < len(community):
            occupants.append(bac.newBacteria(chosen, community[chosen].birth, community[chosen].death, community[chosen].sensitivities, community[chosen].resistances, community[chosen].colour))
        else:
            occupants.append("empty")
    diversity = len(community) - 1
    mode = "resistance"
    return community, occupants, diversity, mode



# rock-paper-scissors parameters
def equilibrium(density):
    community = []
    occupants = []
    
    community.append(bac.newBacteria(0, 1, 1/3, {}, [], 255)) # P: producer, slower growh rate due to production
    #community.append(bac.newBacteria(0, 1, 10/32, {}, [], 110)) # delta P: same exact strain, with toxin genes removed. improved fitness
    community.append(bac.newBacteria(0, 1, 1/4, {0:.75}, [False], 40)) # sensitive to P: grows faster than all because no toxin production or lack of LPS, but dies more frequently as well
    for i in range(int((width/density)*(height/density))):
        chosen = floor(random(0,len(community)+1))
        if chosen < len(community):
            occupants.append(bac.newBacteria(chosen, community[chosen].birth, community[chosen].death, community[chosen].sensitivities, community[chosen].resistances, community[chosen].colour))
        else:
            occupants.append("empty")
    diversity = len(community) -1
    mode = "equilibrium"
    return community, occupants, diversity, mode




# rock-paper-scissors parameters with bet-hedging behaviors
def bet_hedging(density):
    community = []
    occupants = []
    
    community.append(bac.newBacteria(0, 1, .33, {}, [], 255)) # P: producer, slower growh rate due to production
    community.append(bac.newBacteria(0, 1, .3125, {}, [], 200)) # delta P: same exact strain, with toxin genes removed. improved fitness
    community.append(bac.newBacteria(0, 1, .25, {}, [], 200)) # sensitive to P: grows faster than all because no toxin production or lack of LPS, but dies more frequently as well
    for i in range(int((width/density)*(height/density))):
        chosen = floor(random(0,5))
        if chosen < 3:
            occupants.append(bac.newBacteria(chosen, community[chosen].birth, community[chosen].death, community[chosen].sensitivities, community[chosen].resistances, community[chosen].colour))
        else:
            occupants.append("empty")
    diversity = 3
    mode = "bet_hedging"
    return community, occupants, diversity, mode

def bet_hedging_resistance(density):
    community = []
    occupants = []
    
    community.append(bac.newBacteria(0, 1, .33, {}, [], 255)) # P: producer, slower growh rate due to production
    community.append(bac.newBacteria(0, 1.05, .33, {}, [], 200)) # delta P: same exact strain, with toxin gene truncated
    community.append(bac.newBacteria(0, 1.23, .33, {0:0.65}, [False], 200)) # sensitive to P: grows faster than all because no toxin production or lack of LPS, but dies more frequently as well
    for i in range(int((width/density)*(height/density))):
        chosen = floor(random(0,len(community)+8))
        if chosen < len(community):
            occupants.append(bac.newBacteria(chosen, community[chosen].birth, community[chosen].death, community[chosen].sensitivities, community[chosen].resistances, community[chosen].colour))
        else:
            occupants.append("empty")
    diversity = len(community)-1
    mode = "bet_hedging_resistance"
    return community, occupants, diversity, mode
