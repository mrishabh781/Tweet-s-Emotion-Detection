import json
import sys
import jsonpickle
import os

import tweepy
API_KEY = 'Your key'
API_SECRET = 'your key'
# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)



searchQuery = ('covid OR covid-19 OR covid 19 OR covid19 OR coronavirus OR CoronavirusOutbreak OR coronavirusindia OR covid19India OR StayHomeIndia OR IndiaFightsCorona')  # this is what we're searching for
maxTweets = 20000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'delhi.json' # We'll store the tweets in a text file.
date = '2020-04-1'

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None
place = '317fcc4b21a604d5' #delhi
#place = 'b850c1bfd38f30e0' # india
# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -100000
result_type1= 'mixed'
tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
list = []
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, place_id = place,lang ='en',until = date,result_type=result_type1)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId,place_id = place,lang ='en',until = date,result_type=result_type1)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),place_id = place,lang ='en',until = date,result_type=result_type1)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId,place_id = place,lang ='en',until = date,result_type=result_type1)
            if not new_tweets:
                print("No more tweets found")
                break
            #for tweet in new_tweets:
            list.append(new_tweets)

            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break
    enc = jsonpickle.encode(list)
    print(enc, file=f)

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))