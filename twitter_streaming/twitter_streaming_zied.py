# Pour créer des data frames
from datetime import time
import pandas as pd


# Pour manipuler les données + facilement 
import numpy as np
import mysql.connector as MySQLdb
import csv
import os
import time
from tweepy import API 
from tweepy import Cursor 

# StreamListener est une classe de Tweepy qui nous permet d'écouter les tweets
from tweepy.streaming import StreamListener

# Pour nous authentifier avec nos credentials, cette classe sert de lien entre l'app Twitter et nous
from tweepy import OAuthHandler

from tweepy import Stream

# On importe les credentials
import credentials


### CONNECTION A LA BASE DE DONNEES
conn = MySQLdb.connect(user = 'root', host = 'localhost', database = 'db_twitter', charset = 'utf8mb4')

curseur = conn.cursor()

# Création d'une classe réservée à l'authentification
class TwitterAuthenticator():

    def authenticate_twitter_app(self):

        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)

        return auth

# Création d'une classe réservée à l'interaction avec le client Tiwtter

class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets


# On crée une classe de streamer 
class TwitterStreamer():
    '''
    Permet le streaming et le traitement de tweets en live
    '''

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    # Prend en paramètre un filename d'un .txt qui contiendra nos tweets streamés 
    def stream_tweets(self, feteched_tweets_filename, hash_tag_list):
        # Gère l'authentification et la connexion à l'API de streaming 
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        
        # On instancie un objet de la classe Stream, qui va nous permettre de récupérer les tweets
        stream = Stream(auth, listener)
        
        
        # On se doit de trier les tweets que l'on souhaite récupérer, on utiliser ainsi la méthode filter de la classe Stream
        # La liste track est une liste de keywords 
        stream.filter(track = hash_tag_list)
        


# Création d'une classe qui hérite de StreamListener et va nous permettre d'afficher les tweets

class TwitterListener(StreamListener):
    '''
    Un listener classique que affiche les tweets reçus
    '''
    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # Gère la récupération des données
    def on_data(self, data):
        global i
        i += 1 
        try:
            while True:
                tweet = data.split('},"geo":')[1].split(',"coordinates"')[0]
                if tweet != 'null':

                    print(tweet)
                    # On écrit les tweets dans un fichiers texte en continu
                    with open('C://wamp64//www//TWITTER//tweets json format//tweet_' + str(i) + '.json', 'a') as tf:
                        tf.write(data)
                        tf.write('\n')
                        tf.close()
                return True

        # Si ça ne marche pas, on retourne l'erreur
        except BaseException:
            print("Erreur dans on_data: %s" %str(BaseException))
        return True
    
    # méthode qui intervient lorsqu'il y a une erreur
    def on_error(self, status): 
        # L'erreur 420 correspond à la rate limit, comme ça si on a un pb on sait tout de suite s'il s'agit de la rate limit ou non         
        if status == 420:
            return False
        # on affiche la variable status, qui affichera la nature de l'erreur
        print(status)

    def on_status(self, status):
        print(status.text, file=self.output_file)


# Création d'une classe pour analyser les tweets
import json
tw = {}
class TweetAnalyzer():

    def get_infos_tweets(self, fetched_tweets_filename, tweets):
        c = 0 
        d = 0
        for tweet in tweets:
            c += 1 
            if tweet.geo:
                d += 1
                
                tw["dates"] =  str(tweet.created_at)
                tw['user_name'] = tweet.user.name               
                tw['text'] = tweet.text
                tw['latitude'] = tweet.geo['coordinates'][0]
                tw['longitude'] = tweet.geo['coordinates'][1]
                tw["place"] = tweet.place
                tw["id_place"] = tweet.place.id
                print(c, d , 'yes', tweet.geo)

                # Requête SQL (a quoter si on veut pas insérer dans la base de données)    
                sql = "INSERT INTO tweets_streaming(`created_at`, `user_name`, `text_contenu`, `latitude`, `longitude`, `place`, `id_place`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                values = (tweet.created_at, tweet.user.name, tweet.text, tweet.geo['coordinates'][0], tweet.geo['coordinates'][1], tweet.place.name,tweet.place.id)
                curseur.execute(sql,values)
	

        conn.commit()
        print('c = ', c, 'd = ', d)
        return tw




i = 0
#clients = ['googlemaps', 'weliketravel','elonmusk','sct_r']
clients = ['sct_r']
hash_tag_list = ['Annecy','Chambéry','Grenoble','Toulouse','GoogleMaps','Paris', 'Marseille', 'Ascension'
'Voiron','openstreetmap', 'geolocalization', 'géolocalisation', 'human', 'jobs', 'travel', 'innovation','Netflix']

if __name__ == "__main__":
    fetched_tweets_filename = 'tweets.csv'

    ##########    TWEET STREAM FROM HASH TAG    ##########
    
    
    twitter_streamer = TwitterStreamer()
    stream_listener = StreamListener()
    
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)


    #=====================
    


    ##########    TWEET TIMELINE STREAM    ##########
    # tweet_analyze = TweetAnalyzer()
    
    # for client in clients:
    #     twitter_client = TwitterClient(client)
    #     tweets = twitter_client.get_user_timeline_tweets(500)
    #     tw = tweet_analyze.get_infos_tweets(fetched_tweets_filename, tweets)
        
        




