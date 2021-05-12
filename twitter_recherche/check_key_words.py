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

api = tweepy.API(
    auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True
    )
conn = MySQLdb.connect(
    user = 'root', host = 'localhost', database = 'twitter_api', charset = 'utf8mb4'
    )
curseur = conn.cursor()

def check_if_in_city(city):
	#first select
	#this is tweets that we want to check if it is situated in a city
	request = 'SELECT place FROM tweet_geo'
	curseur.execute(request)
	list_tweets = curseur.fetchall()
	
	print(list_tweets)

	#second select 
	#select the place from polygon 
	sec_request = 'SELECT place FROM tweet_place'
	curseur.execute(sec_request)
	liste_places = curseur.fetchall()
	
	for tweet in list_tweets:
		if tweet[0] == city:
			print('yes bg')
		else:
			print("le tweet n'y est pas dedans connard")
			
	# for tweet in list_tweets:
	# 	if tweet[-2] == city:
	# 		return tweet

print(check_if_in_city('Paris'))