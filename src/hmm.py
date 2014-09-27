'''
Created December 10, 2013

A file for running a learning HMMs from data

@author: Alex Roederer
'''

import numpy as np

class HMM:
    
    numStates = 3
    numObsSymbs = 3
    
    sensorMat = None
    transiMat = None
    
    def __init__(self, numStates, numObsSymbs):
        self.numStates = numStates
        self.numObsSymbs = numObsSymbs
        self.transiMat = np.zeros((numStates, numStates))
        self.sensorMat = np.zeros((numStates, numObsSymbs))
    
    def learnHMM(self, data):
        pass
    
    def predictStates(self, data):
        pass

if __name__ == "__main__":
    print "UNIMPLEMENTED"
