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


query = ['Grenoble','ESA', 'NASA', 'Lyon', 'Netflix', 'Annecy',
 'Lyon', 'Paris', 'Chambéry', 'Voiron', 'Toulouse', 'Marseille', 'Macron']


def append_tweet_place():
	'''
	this one is for the place in order to build the polygon
	'''
	for keyword in query:
		for tweet in api.search(q = keyword, count = 200, lang='fr'):
			if tweet.geo:
				coor = api.geo_id(tweet.place.id).bounding_box.coordinates
				print(tweet.place.name)
	# 			sql = "INSERT INTO tweet_place(`place`, `lat_1`, `long_1`, `lat_2`, `long_2`, `lat_3`, `long_3`, `lat_4`, `long_4`, `lat_5`, `long_5`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	# 			values = (tweet.place.name, 
	# 				coor[0][0][1],
	# 				coor[0][0][0],
	# 				coor[0][1][1],
	# 				coor[0][1][0],
	# 				coor[0][2][1],
	# 				coor[0][2][0],
	# 				coor[0][3][1],
	# 				coor[0][3][0],
	# 				coor[0][4][1],
	# 				coor[0][4][0]
	# 				)
	# 			curseur.execute(sql,values)
	# conn.commit()
	return 'done'
print(append_tweet_place())

