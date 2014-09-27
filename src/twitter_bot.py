#!/usr/bin/python

import tweepy
import time

def getSecrets(secretsFile):
    secrets = []
    with open(secretsFile) as f:
        for line in f:
            secrets.append(line.rstrip('\r\n'))
    return secrets

def generateFortune(seedWord):
    pass

if __name__ == '__main__':

    secretLocations = 'secrets.txt'
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = \
        getSecrets(secretLocations)

    #Authenticate twitter account
    #auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    #auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #api = tweepy.API(auth)

    mostRecentReply = '0'

    #Run forever
    #while True:
    if True: 
        #Gets public tweets
    #    public_tweets = api.home_timeline()
    #    for tweet in public_tweets:
    #        print tweet.text
        #Check for people tweeting at the account;
    #    mentions = api.mentions_timeline()
    #    for mention in mentions:
    #        print mention.text
    #        print mention.author.screen_name
    #    newName = mentions[-1].id
        #If there is a new at-reply
    #    if mostRecentReply != newName:
    #        mostRecentReply = newName 
        if True:
            generateFortune('frog')
            #Run fortune generator
            #Send reply tweet
        #Wait for five minutes before looping again
            time.sleep(1)


