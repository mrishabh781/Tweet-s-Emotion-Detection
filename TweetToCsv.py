import json
import sys
import jsonpickle
import os
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import jsonpickle
from textblob import TextBlob

#import twitter_credentials

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import tweepy


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        df['tweets'] = self.clean_tweet(tweet)
        analysis = TextBlob(df['tweets'])

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['tweets'] = np.array([self.clean_tweet(i) for i in df['tweets']])
        df['id'] = np.array([tweet.id for tweet in tweets])
        #df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        #df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        #df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

graph = {}
tweet_analyzer = TweetAnalyzer()
file = open('delhi.json', 'r')
tid = []
date = []
tweetlist=[]

tweets = jsonpickle.decode(file.read())
for i in tweets:
    df = tweet_analyzer.tweets_to_data_frame(i)

    #df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    
    tid.extend(df['id']) 
    date.extend(df['date'])
    tweetlist.extend(df['tweets'])

output = pd.DataFrame({'Id' : tid, 'date' : date, 'Tweets' : tweetlist})
output.to_csv('output.csv',index =False)

print('Done')
