from __future__ import division
import wrapping_pixels as wrap

# iterates a cell to the next point in time. neighbor_dist*2+1 = w and h of box around the pixel that should be checked

def iterate(pixel_index, neighbor_dist, occupants, diversity, density, bet_hedging):
    p = pixel_index
    neighbors = neighbor_dist
    pX = p % int(width/density) #transform 1D index to coordinates
    pY = int(p / int(width/density)) #transform 1D index to coordinates
    
    if not bet_hedging:
        neighborFreqs = count_neighbors(pX,pY, neighbors, occupants, diversity, density)
        Sum = 0
        for i in range(len(neighborFreqs)):
            Sum += neighborFreqs[i][0]
    
        neighborFreq = []
        for i in range(len(neighborFreqs)):
            neighborFreq.append((neighborFreqs[i][0] / (Sum+1),neighborFreqs[i][1]))
        return neighborFreq        
    
    
    else:
        
        for i in range(pX - neighbors, pX + neighbors + 1):
            x = wrap.wrapped_x(i,width/density)
            for j in range(pY - neighbors, pY + neighbors + 1):
                if i != pX or j != pY:
                    y = wrap.wrapped_y(j,height/density)
                    index = int(x + y * width/density)
                    if type(occupants[index]) is not str:
                        if occupants[p].ID in occupants[index].sensitivities:
                            deathrate = 0.125
                            chance = random(0,1)
                            if deathrate > chance:
                                occupants[index] = "empty"
        occupants[p] = "empty"
        return occupants
                         
    
    
def count_neighbors(pX, pY, neighbors, occ, diversity,density):
    # (with wrap-around at borders) 
    neighborCount = []
    representatives = {}
    for i in range(diversity):
        neighborCount.append(0)
        representatives[i] = []
    occupants = occ
    for i in range(pX - neighbors, pX + neighbors + 1):
        x = wrap.wrapped_x(i,width/density)
        for j in range(pY - neighbors, pY + neighbors + 1):
            if i != pX or j != pY:
                y = wrap.wrapped_y(j,height/density)
                index = int(x + y * width/density)
                if type(occupants[index]) is not str:
                    identity = occupants[index].ID
                    neighborCount[identity] += 1
                    representatives[identity].append(occupants[index])
    neighborTuples = []
    for i in range(len(neighborCount)):
        if neighborCount[i] > 0:
            neighborTuples.append((neighborCount[i], representatives[i][floor(random(0,len(representatives[i])))]))
        else:
            neighborTuples.append((0,"none of this type"))
    return neighborTuples
                    
                    
                    
                    
                    
                    
    
