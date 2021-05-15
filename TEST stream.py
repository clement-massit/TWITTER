# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy
import mysql.connector as MySQLdb
import folium 

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '1179115613966536706-43kJxODf465JpsC1LTxkpWGzoSjKv1'
ACCESS_SECRET = 'h4dMsnVMMTcNLMua8ZqYJiQYrsIMloNkRWF5JUAq0KdMt'
CONSUMER_KEY = 'quSMSDm2KMENSM8k5egwhh9Cp'
CONSUMER_SECRET = 'X5PQlJvkvBCzqyWv2azJ2u3NNAWdZxXMx3vnUbN47Kx4IhwnvE'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)



# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

conn = MySQLdb.connect(user = 'root', host = 'localhost', database = 'twitter_api', charset = 'utf8mb4')

curseur = conn.cursor()


# class StreamListener(tweepy.StreamListener()):
#     def on_status(self,status):
#         print(status.text)
#     def on_error(self, status_code):
#         if status_code == 420:
#             return False


for status in tweepy.Cursor(api.home_timeline).items(0):
    print(status._json["geo"])

#     stream_listener = StreamListener()
#     stream = tweepy.Stream(auth=api.auth, listner=stream_listener)
#     stream.filter(track=['Grenoble','ESA', 'NASA', 'Lyon', 'Netflix', 'Annecy',
#  'Lyon', 'Paris', 'Voiron', 'Toulouse', 'Marseille','Trump', 'Clinton',
#  'Macron'], languages=['fr'])

# tweet = json.loads()
# if 'text' in tweet:
#     print(tweet['id']) # This is the tweet's id
#     print(tweet['created_at']) # when the tweet posted
#     print(tweet['text']) # content of the tweet
                
#     print(tweet['user']['id']) # id of the user who posted the tweet
#     print(tweet['user']['name']) # name of the user, e.g. "Wei Xu"
#     print(tweet['user']['screen_name']) # name of the user account, e.g. "cocoweixu"