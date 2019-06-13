#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

import json

#Variables that contains the user credentials to access Twitter API
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""



#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    account = 'realDonaldTrump'
    api = API(auth)
    new_tweets = api.user_timeline(screen_name=account,count=500)
    oldest_id = new_tweets[-1].id-1
    tweets = []

    json_results = [ x._json for x in new_tweets]

    while len(new_tweets) > 1 :
        oldest_id = new_tweets[-1].id - 1
        print "Getting next round of tweets after %s" % (oldest_id)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=account, count=200, max_id=oldest_id)

        json_results.extend([ x._json for x in new_tweets])

        print "%s tweets downloaded from @%s" %(len(json_results),account)


    json_set = json.dumps(json_results)
    with open('data_repo/data1.txt', 'w') as outfile:
        json.dump(json_results, outfile)
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])