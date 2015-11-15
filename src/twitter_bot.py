#!/usr/bin/python

import tweepy
import time
from markov import MarkovChain 
from secrets import secrets

def generateFortune(markovChain, seedWord=None):
    #Seed Word Functionality not currently available. 
    fortunes = []

    #Generate more fortunes while we haven't generated any, or 
    #The last one we generated was too long, or we've tried too many 
    #Times with no success
    #Essentially Prevents two-sentence fortunes
    while (len(fortunes) < 1 or len(fortunes[-1]) > 140) and len(fortunes) < 30:
        #Generate a sentence from the markov chain:
        #Generate a sequence of words
        generated = markovChain.generateSequence(markovChain.returnRandomStart(), 30)
        #Look for a complete sentence:
        periodIndexes = [x for x in range(0, len(generated)) if '.' in generated[x]]
        if len(periodIndexes) > 1 and periodIndexes[1] < len(generated)-1:
            sentence = generated[periodIndexes[0]+1:periodIndexes[1]+1]
            stringSentence = ' '.join(sentence)
            fortunes.append(stringSentence)

    outFortune = ''
    for fortune in fortunes:
        if len(outFortune + ' ' + fortune) < 140:
            if outFortune is '':
                outFortune += fortune
            else:
                outFortune += ' ' + fortune

    return outFortune

if __name__ == '__main__':

    #Create and train markov chain
    fortuneChain = MarkovChain(1)
    fortuneChain.learn('../data/fortunes.txt')

    #Authenticate twitter account
    #Note: Only do this when ready to go live!
    auth = tweepy.OAuthHandler(secrets['CONSUMER_KEY'], secrets['CONSUMER_SECRET'])
    auth.set_access_token(secrets['ACCESS_TOKEN'], secrets['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    mostRecentReply = 0
    waitTime = 5 * 60

    #Run forever
    while True:
    #if True: 

        #Bot flow: 
        #Get tweets directed at account since last check
        if mostRecentReply is 0:
            mentions = api.mentions_timeline()
        else:
            mentions = api.mentions_timeline(since_id = mostRecentReply)
        for mention in mentions:
            print mention.text
            print mention.author.screen_name
            
            #Generate a fortune 
            fortune = generateFortune(fortuneChain)

            #Send that user a reply with their fortune
            statusRet = api.update_status(status='@' + mention.author.screen_name + 
                ' ' + fortune, in_reply_to_status_id = mention.id)

        #Update most recent reply if there's something newer
        if len(mentions) > 0: 
            mostRecentReply = mentions[-1].id
        
        #Wait for a period before looping again
        time.sleep(waitTime)
#END SCRIPT
