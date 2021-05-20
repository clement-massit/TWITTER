# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy
import mysql.connector as MySQLdb
import folium
import credentials

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)

api = tweepy.API(
    auth, wait_on_rate_limit=True, 
	wait_on_rate_limit_notify=True, 
	compression=True
    )
conn = MySQLdb.connect(
    user = 'root', 
	host = 'localhost', 
	database = 'db_twitter', 
	charset = 'utf8mb4'
    )
curseur = conn.cursor()

def check_tweets_in_city(city):
	c = 0
	#first select
	#this is tweets that we want to check if it is situated in a city
	request = 'SELECT * FROM tweets_streaming'
	curseur.execute(request)
	tweets_to_be_checked = curseur.fetchall()

	tweets_to_be_studied = []
	for tweet in tweets_to_be_checked:
		
		if tweet[6] == city:
			c += 1
		
			tweets_to_be_studied.append(tweet)
			
			
		
	return tweets_to_be_studied

			
	

# print(check_tweets_in_city('Paris'))