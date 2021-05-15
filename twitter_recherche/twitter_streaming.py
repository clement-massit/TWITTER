# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy
import mysql.connector as MySQLdb 

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



'''
for tweet in api.search(q = 'IA', count = 200, lang='fr', tweet_mode = 'extended'):
	
	try:
		sql = "INSERT INTO `tweet`(`id_tweet`, `date`, `text`, `user_id`, `user_name`) VALUES(%s, %s, %s, %s, %s)"
		values = (tweet.id, tweet.created_at, tweet.full_text, tweet.user.id, tweet.user.name)
		curseur.execute(sql, values)
	except:
		print('yes')

conn.commit()'''

query = ['Grenoble','ESA', 'NASA', 'Lyon', 'Netflix', 'Annecy',
 'Lyon', 'Paris', 'Voiron', 'Toulouse', 'Marseille','Trump', 'Clinton',
 'Macron']



for keyword in query:

	# for tweet in api.search(q = keyword, count = 200, lang = 'fr', tweet_mode = 'extended').items(500):
	for tweet in tweepy.Cursor(api.search, q = keyword, lang = 'fr').items(100):
		if tweet.geo:
			print(tweet.geo['coordinates'][0], tweet.geo['coordinates'][1], tweet.place.name)
			
# 			for coor in tweet.place.bounding_box.coordinates[0]:
# 				print(coor)

# 			sql = "INSERT INTO tweet_geo(`date`, `user_name`, `text`, `latitude`, `longitude`, `place`, `id_place`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
# 			values = (tweet.created_at, tweet.user.name, tweet.full_text, tweet.geo['coordinates'][0], tweet.geo['coordinates'][1], tweet.place.name,tweet.place.id)
# 			curseur.execute(sql,values)
	

# conn.commit()



        