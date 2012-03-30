'''
Created on Mar 29, 2012

@author: satshabad
'''
import random
import copy
from termcolor import colored
import copy


def quality(chromo, qualityMap):
    '''
    Returns the quality of the chromosome based on the quality map
    '''
    sugar = chromo[0]
    flour = chromo[1]
    return qualityMap[sugar][flour]

def mutate_chromo(chromo):
    '''
    Returns the mutated chromosome by incrementing or decrementing one of it's genes at random
    '''
    chromo = list(chromo)
    geneToMutate = random.randint(0, len(chromo) - 1)
    mutatePlus = random.randint(0, 1);
    if mutatePlus:
        chromo[geneToMutate] = (chromo[geneToMutate] + 1) % 8
    else:
        chromo[geneToMutate] = (chromo[geneToMutate] - 1) % 8
    return tuple(chromo)

def best_of_population(population, qualMap):
    '''
    Returns the best chromosome of the population based on the given quality map
    '''
    best = population[0]
    for chromo in population:
        if quality(chromo, qualMap) > quality(best, qualMap):
            best = chromo
    return best

def pick_random_by_standard_method(population, qualMap):
    '''
    Returns the index of a random element, chosen by the standard method. If list is empty, returns None
    '''
    
    if not population:
        return None
    
    sumOfQual = 0
    for chromo in population:
        sumOfQual += quality(chromo, qualMap)
        
    # create a list with the form [(<prob>, (<sugar>, <flour>)),(<prob>, (<sugar>, <flour>))]
    # where prob is the probability that the chromo will be picked at random using Standard Method
    probList = [(quality(chromo, qualMap) / float(sumOfQual), chromo) for chromo in population]
    
    # randomly pick a chromo weighted by probability. i.e. if prob is .25 that chromo will be picked 25% of the time
    # does this by picking random number between 0 and 1. Then starts to total the sorted probs. 
    # When the total is above the random number, that chromo is picked.
    probList.sort(reverse=True)
    r = random.random()
    s = 0
    for chromoProb in probList:
        s += chromoProb[0]
        if s >= r:
            return chromoProb[1]

def mate_chromo(chromo, population, qualMap):
    '''
    Returns a list of offspring produced by mating the given chromosome with a "randomly chosen" mate
    '''
    copyOfPop = copy.deepcopy(population)
    copyOfPop.remove(chromo)
    mate = pick_random_by_standard_method(copyOfPop, qualMap)
    offspring1 = chromo[:len(chromo)/2] + mate[:len(mate)/2]
    offspring2 = mate[:len(mate)/2] + chromo[len(chromo)/2:]
    return [offspring1,offspring2]

def cull_population(pop, sizeToReturn, qualMap):
    '''
    Returns a population of size sizeToReturn which contains the best of the passed 
    population and the rest pick at "random" weighted by fitness
    '''
    newPop = []
    
    # get the best from this generation
    newPop.append(best_of_population(pop, qualMap))
    pop.remove(best_of_population(pop, qualMap))
    
    # pick up to sizeToReturn-1 number of "random" chromosomes based on their fitness (probability)
    for i in range(sizeToReturn - 1):
        chromo = pick_random_by_standard_method(pop, qualMap)
        if chromo == None:
            break
        newPop.append(chromo)
        pop.remove(chromo)
    return newPop
    
def printPop(pop, qualMap):
    '''
    Prints the population onto the given map. The population is colored red.
    '''
    printableQualMap = copy.deepcopy(qualMap)
    for chromo in pop:
        sugar = chromo[0]
        flour = chromo[1]
        printableQualMap[sugar][flour] = 'c' + str(printableQualMap[sugar][flour])
    for row in printableQualMap:
        for num in row:
            if type(num) == type(1):
                print num,
            else:
                print colored(num[1], 'red'),
        print ''

if __name__ == '__main__':
    moatMountainMap = [[1, 2, 3, 4, 5, 4, 3, 2, 1],
                       [2, 0, 0, 0, 0, 0, 0, 0, 2],
                       [3, 0, 0, 0, 0, 0, 0, 0, 3],
                       [4, 0, 0, 7, 8, 7, 0, 0, 4],
                       [5, 0, 0, 8, 9, 8, 0, 0, 5],
                       [4, 0, 0, 7, 8, 7, 0, 0, 4],
                       [3, 0, 0, 0, 0, 0, 0, 0, 3],
                       [2, 0, 0, 0, 0, 0, 0, 0, 2],
                       [1, 2, 3, 4, 5, 4, 3, 2, 1]]
    
    bumpMountainMap = [[1, 2, 3, 4, 5, 4, 3, 2, 1],
                       [2, 3, 4, 5, 6, 5, 4, 3, 2],
                       [3, 4, 5, 6, 7, 6, 5, 4, 3],
                       [4, 5, 6, 7, 8, 7, 6, 5, 4],
                       [5, 6, 7, 8, 9, 8, 7, 6, 5],
                       [4, 5, 6, 7, 8, 7, 6, 5, 4],
                       [3, 4, 5, 6, 7, 6, 5, 4, 3],
                       [2, 3, 4, 5, 6, 5, 4, 3, 2],
                       [1, 2, 3, 4, 5, 4, 3, 2, 1]]
    map = moatMountainMap
    
    population = [(0, 0)]
    count = 0
    while quality(best_of_population(population,  map),  map) < 9:
        
        # mate all of the existing chromosomes with each other
        matedChromos = []
        if not len(population) < 2:
            for chromo in population:
                matedChromos.extend(mate_chromo(chromo, population, map))
        
        
        # mutate all of the existing chromosomes
        mutatedChromos = []
        for chromo in population:
            mutatedChromos.append(mutate_chromo(chromo))
            
        # get rid of the duplicate chromosomes, throw mutated, and offspring ones in with old ones
        population = list(set(mutatedChromos + population + matedChromos))
        
        # cut down the population 
        population = cull_population(population, 4,  map)
        
        count += 1
        printPop(population,  map)
        print "-----------------"
    print count

    
    
    
    
    
    
    
    
    
