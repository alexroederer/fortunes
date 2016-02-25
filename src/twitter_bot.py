#!/usr/bin/python

import tweepy
import time
import logging
from logging.handlers import RotatingFileHandler
import datetime
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
        periodIndexes = [x for x in range(0, len(generated)) if '.' in generated[x] or '!' in x or '?' in x]
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

    #Set up logging
    logName = 'logs/' + str(datetime.datetime.now()) + '.log'
    logger = logging.getLogger("Mystic Cookie Twitter Script Logger")
    logger.setLevel(logging.DEBUG)

    #Rotating handler
    handler = RotatingFileHandler(logName, maxBytes=100000, backupCount=4)

    #Create and train markov chain
    fortuneChain = MarkovChain(1)
    chainTrainingFile = '../data/fortunes.txt'
    fortuneChain.learn(chainTrainingFile)
    lastChainUpdate = datetime.datetime.now()
    updateFrequency = 2*60*60 #in seconds
    logger.info('Markov Chain Initial Trained on '+ chainTrainingFile + ' at ' + str(lastChainUpdate))

    #Authenticate twitter account
    #Note: Only do this when ready to go live!
    auth = tweepy.OAuthHandler(secrets['CONSUMER_KEY'], secrets['CONSUMER_SECRET'])
    auth.set_access_token(secrets['ACCESS_TOKEN'], secrets['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    logger.info('Authentication Successful')

    mostRecentReply = 0
    waitTime = 1 * 60 # In Seconds
    logger.info('Wait time set to ' + str(waitTime) + ' seconds')

    #Run forever
    while True: 
        #If we're on startup, fastforward to current tweet 
        if mostRecentReply is 0:
            #Grab all mentions
            mentions = api.mentions_timeline()
            #Do not reply to these tweets (as they are old)
            if len(mentions) > 0:
                mostRecentReply = mentions[0].id
                logger.info('Fast-forwarding most recent reply to ' + str(mostRecentReply))

        #Check if we need to retrain the chain (do once per hour)
        if (datetime.datetime.now() - lastChainUpdate).total_seconds() > updateFrequency:
            #Retrain chain
            fortuneChain.learn(chainTrainingFile)
            lastChainUpdate = datetime.datetime.now()
            logger.info('Markov chain retrained at ' + str(lastChainUpdate))

        #Get tweets directed at account since last check
        mentions = api.mentions_timeline(since_id = mostRecentReply)
        mentions.reverse()
        for mention in mentions:
            #print mention.text
            #print mention.author.screen_name
            logger.info(str(mention))
            
            #Generate a fortune 
            fortune = generateFortune(fortuneChain)
            logger.info(str(fortune))

            #Send that user a reply with their fortune
            statusRet = api.update_status(status='@' + mention.author.screen_name + 
                ' ' + fortune, in_reply_to_status_id = mention.id)
            logger.info('Replied to ' + mention.author.screen_name)

        #Update most recent reply if there's something newer
        if len(mentions) > 0: 
            mostRecentReply = mentions[-1].id
            logger.info('Updating most recent reply to ' + str(mostRecentReply))
        
        #Wait for a period before looping again
        time.sleep(waitTime)
    logging.shutdown()
