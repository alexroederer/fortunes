'''
Created November 13, 2015 

Creates a Markov Chain from Text

@author: Alex Roederer
'''

#import numpy as np
import re
import collections
import random

class MarkovChain:

    occuranceProbs = collections.defaultdict(lambda: [])
    
    def __init__(self, tupleSize):
        self.tupleSize = tupleSize
    
    def learn(self, dataFile):
        #Opens provided data file
        pattern = re.compile(r"[\w']+|[.,!?;]")
        tokens = []
        #Get all the words/punctuations from file
        with open(dataFile, 'r') as dataHandle:
            for line in dataHandle: 
                tokens.extend(line.split())
                #tokens.extend(pattern.findall(line))
        #Break up into tuples; add next word to tuple's 'next words' list
        for i in range(0, len(tokens)-self.tupleSize-1):
            wordSet = tuple(tokens[i:i+self.tupleSize])
            self.occuranceProbs[wordSet].append(tokens[i+self.tupleSize]) 

    def predictNext(self, prevTuple):
        possibleNexts = self.occuranceProbs[prevTuple]
        #If there are none, return None
        if len(possibleNexts) is 0:
            return None
        else:
            #Select one at random
            nextWord = possibleNexts[random.randint(0, len(possibleNexts)-1)]
            return nextWord

    def returnRandomStart(self):
        #Returns a random 'starting' tuple from all seen tuples. 
        starts = self.occuranceProbs.keys()
        selected = random.randint(0, len(starts))
        return starts[selected]

    def generateSequence(self, start, seqLength):
        outSequence = []
        curVal = start
        for i in range(0, seqLength):
            result = self.predictNext(curVal)
            outSequence.append(result)
            newVal = list(curVal[1:])
            newVal.append(result)
            curVal = tuple(newVal)
        return outSequence

    def __str__(self):
        outputString = '------------Markov Chain Object-------------\n'
        #Add a nice printout representation of the object
        #Possibly with most likely tuples? 
        #TODO
        outputString = outputString + '' 
        return outputString

#if __name__ == "__main__":
#    print "testChain variable initiated with test MarkovChain object"
    
#    testChain = MarkovChain(1)
#    testChain.learn('./data/fortunes.txt')
