'''
wordsToNumbers.py
Created December 10, 2013

Creates a word to number mapping from a series of text files.  

@author: Alex Roederer
'''
import numpy as np
import os

def createWordTransitionCountMatrix(fileLocation, wordToNumbDict, matrixToExtend=None):
    """
    Creates a transition probability matrix for bigrams
    """
    numObs = np.max(wordToNumbDict.values()) + 1 
    if matrixToExtend is None:
        transMat = np.zeros((numObs, numObs))
    else:
        transMat = matrixToExtend
    with open(fileLocation, 'r') as fileH:
        prevNum = None
        for line in fileH:
            for word in line.split():
                currNum = wordToNumbDict[word]
                #print prevNum, currNum
                if prevNum is not None:
                    transMat[prevNum][currNum] += 1.0
                prevNum = currNum
    return transMat

def createWordCountDict(fileLocation, dictToExtend=None):
    """
    Creates a dict that maps to counts of words
    @param file: The text file to pull words from
    @param dictToExtend: Optional previously created dict to extend
    @return: a dict that maps from a word to a count of that word's frequency 
    """
    if dictToExtend is None:
        dictToExtend = {}
    with open(fileLocation, 'r') as fileH:
        for line in fileH:
            #Split on whitespace
            for word in line.split():
                if word not in dictToExtend:
                    dictToExtend[word] = 1.0
                else:
                    dictToExtend[word] += 1.0
    return dictToExtend

def createWordToNumberDict(fileLocation, dictToExtend=None):
    """
    Creates the word to number dictionary
    @param file: The text file to pull words from
    @param dictToExtend: Optional previously created dict to extend
    @return: a dict that maps from a word to a number for each word in the file. 
    """
    
    #Get current largest value in dictionary
    if not dictToExtend:
        dictToExtend = {}
        currentMax = -1
    else:
        try:
            currentMax = np.max(dictToExtend.values())
        except ValueError:
            print "Unable to get largest value in provided dict; dict is malformed"
            return None
    
    #Run through the file
    with open(fileLocation, 'r') as fileH: 
        for line in fileH:
            #Split on whitespace
            for word in line.split():
                if word not in dictToExtend:
                    currentMax += 1
                    dictToExtend[word] = currentMax
    return dictToExtend

if __name__ == "__main__":
    print "Begin testing sequence"
    
    numMap = None
    files = "../../data/"
    for fileName in os.listdir(files):
        numMap = createWordToNumberDict(files + fileName, dictToExtend=numMap)
    
    transMat = None
    for fileName in os.listdir(files):
        transMat = createWordTransitionCountMatrix(files + fileName, numMap, matrixToExtend=transMat)
    listVal = transMat.tolist()