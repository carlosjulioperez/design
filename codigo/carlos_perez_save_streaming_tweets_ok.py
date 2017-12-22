from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json
import time

import datetime

consumer_key = "C8g8wMr5PM0nofHJSXuTiiwbO"
consumer_secret = "11dI5sXdpa8HcPCXGWu9vscbxHoCfiyBTRSWg5AJDVsrOlpZiT"
access_token = "195897646-AIEBxxcB80lknX9H0CDa57ICm6P3HRJNc3tsHQWk"
access_token_secret = "Q1MbhzhEc1qDtiALJcQy6fUYkwTYGWPWQQylqBYh70FRI"

"""
	https://github.com/tweepy/tweepy/blob/master/examples/streaming.py
	https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
	https://gist.github.com/nickhargreaves/44615385daf335166980
"""

class StdOutListener(StreamListener):

    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self,limit):
        self.tweets_data = []
        self.limit = limit

    def on_data(self, data):
        tweet = json.loads(data)
        self.tweets_data.append(tweet)
        if(len(self.tweets_data)>self.limit):
            print("saving twitter data ..")
            self.save_file_csv("netflix.csv")
            self.tweets_data = []
            return False
        return True

    def on_error(self, status):
        print(status)
    
    def get_timestamp(self,created_at):
        pattern = '%a %b %d %H:%M:%S +0000 %Y'
        epoch = int(time.mktime(time.strptime(created_at, pattern)))
        return epoch

    def date_range(start,end):
        current = start
        while (end - current).days >= 0:
            yield current
            current = current + datetime.timedelta(seconds=1)
	
    def save_file_csv(self,filename):
        fd = open(filename,mode='w+')
        fd.write("id|created_at|text|created_at_timestamp|lng|lat\n")
        #GUARDAR DATOS GEOLOCALIZADOS
		#for tweet in self.tweets_data:
		
        startDate = datetime.datetime(2017, 12, 21)
        stopDate = datetime.datetime(2017, 12, 22)
		
        for tweets in tweepy.Cursor(api.search,q=query,count=100,result_type="recent",include_entities=True,since= "2017-12-21", until= "2017-12-21" ).pages():
            if 'coordinates' in tweet.keys() and tweet['coordinates'] != None:
                timestamp = self.get_timestamp(tweet['created_at'])
                line = "%s|%s|%s|%.4f|%.4f|%.4f\n"%(tweet['id_str'],tweet['created_at'],tweet['text'].encode('utf-8'),
                timestamp, tweet['coordinates']['coordinates'][0], tweet['coordinates']['coordinates'][1])
                fd.write(line)
        fd.close()

if __name__ == '__main__':
    l = StdOutListener(limit = 1)#cantidad de tweets que quiero
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['netflix'], locations=[-92.21,-5.02,-75.19,1.88])#lng sw,lat sw, lng ne,lat ne
