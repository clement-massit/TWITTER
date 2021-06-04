# Pour créer des data frames
from datetime import time
from mysql.connector import catch23
import pandas as pd


# Pour manipuler les données + facilement 
import numpy as np
import mysql.connector as MySQLdb

import os
import sys
import requests
try:
    import json
except ImportError:
    import simplejson as json

from tweepy import API, api 
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

# Création d'une classe réservée à l'interaction avec le client Twitter

class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.api = API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

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

    
    def stream_tweets(self, location):
        # Gère l'authentification et la connexion à l'API de streaming 
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        
        # On instancie un objet de la classe Stream, qui va nous permettre de récupérer les tweets
        stream = Stream(auth, listener)
        
        stream.filter(locations=location,languages=["fr"])
        


# Création d'une classe qui hérite de StreamListener et va nous permettre d'afficher les tweets

class TwitterListener(StreamListener):
    '''
    Un listener classique que affiche les tweets reçus
    '''
    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # Gère la réception des données
    def on_data(self, data):
        '''
        Cette fonciton s'execute à la réception d'un tweet
        '''
        
        try:
            coor = {}     
            tweet = json.loads(data) 
            coor["coordinates"] = tweet["place"]["bounding_box"]["coordinates"]

            if tweet["geo"] is not None:
                print(
                    tweet["created_at"], '\n',
                    tweet["user"]["name"], '\n',
                    tweet["text"], '\n',
                    tweet["geo"]["coordinates"][0],'\n', 
                    tweet["geo"]["coordinates"][1], '\n',
                    tweet["place"]["name"],'\n',
                    tweet["place"]["id"]
                    )
                #on insère dans la base de données les infos liées a nos tweets
                sql = "INSERT INTO tweets_streaming(`created_at`, `user_name`, `text_contenu`, `latitude`, `longitude`, `place`, `id_place`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                values = (
                    tweet["created_at"],
                    tweet["user"]["name"], 
                    tweet["text"], 
                    tweet["geo"]["coordinates"][0], 
                    tweet["geo"]["coordinates"][1], 
                    tweet["place"]["name"],
                    tweet["place"]["id"]
                    )
                curseur.execute(sql,values)             
               

               #On insère dans la base de donné les infos liées aux polygon
                sql_polygon = "INSERT INTO polygon(`id_place`,`place`, `lat_1`, `long_1`, `lat_2`, `long_2`, `lat_3`, `long_3`, `lat_4`, `long_4`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values_polygon = (
                    tweet["place"]["id"],
                    tweet["place"]["name"], 
                    coor["coordinates"][0][0][1],
                    coor["coordinates"][0][0][0],
                    coor["coordinates"][0][1][1],
                    coor["coordinates"][0][1][0],
                    coor["coordinates"][0][2][1],
                    coor["coordinates"][0][2][0],
                    coor["coordinates"][0][3][1],
                    coor["coordinates"][0][3][0])
                curseur.execute(sql_polygon,values_polygon)    

                conn.commit()
              
                

            return True

        # Si ça ne marche pas, on retourne l'erreur

        except KeyboardInterrupt or BaseException:
            print("La recherce de Tweets via Streaming a été interrompue")
           
        # except BaseException:
        #     print("Erreur dans on_data: %s" , BaseException)
        
            
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
class TweetAnalyzer():

    def get_infos_tweets(self, tweets):
        tw = {}
       
        
        tw["dates"] =  tweets["created_at"]
        tw['user_name'] = tweets["user"]["name"]              
        tw['text'] = tweets["text"]
        tw['latitude'] = tweets["geo"]['coordinates'][0]
        tw['longitude'] = tweets["geo"]['coordinates'][1]
        tw["place"] = tweets["place"]
        tw["id_place"] = tweets["place"]["id"]
        

        
        return tw

def delete_doublons_polygon():
    request = "DELETE polygon FROM polygon LEFT OUTER JOIN (SELECT MIN(id) as id, id_place FROM polygon GROUP BY id_place) AS table_1 ON polygon.id = table_1.id WHERE table_1.id IS NULL"
    curseur.execute(request)
    conn.commit()
    return True 

def delete_doublons_tweets():
    request = "DELETE tweets_streaming FROM tweets_streaming LEFT OUTER JOIN (SELECT MIN(id) as id, text_contenu FROM tweets_streaming GROUP BY text_contenu) AS table_1 ON tweets_streaming.id = table_1.id WHERE table_1.id IS NULL"
    curseur.execute(request)
    conn.commit()  
    return True       


i = 0
fetched_tweets_filename = 'tweets'
clients = ['googlemaps', 'weliketravel','elonmusk','sct_r']


hash_tag_list2 = ['Annecy','Chambéry','Grenoble','Toulouse',
'GoogleMaps','Paris', 'Marseille', 'Ascension',
'Voiron','openstreetmap', 'geolocalization', 'géolocalisation', 
'human', 'travel', 'innovation','Netflix']

hash_tag_list = ['France','Polytech','Ocean','Ville','Ecole',
'Ingenieur','Annecy','Voyage','openstreetmap', 'NASA','doge',
'Grenoble','Paris','Lyon','ia','adwords','RGPD',
'CNIL','Cookie','Instagram','GoogleMaps']



France = [-4.67, 42, 8, 51.1485061713]
Grenoble = [5.6250000,45.1345864,5.8090210,45.2425030]
Paris = [2.1052551, 48.7525672, 2.6106262, 48.9576789]

def Stream__via_hash_tag_method():
    ##########    TWEET STREAM FROM HASH TAG    ##########
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(France)



if __name__ == "__main__":
    print(delete_doublons_polygon())
    Stream__via_hash_tag_method()
   
    



    


    ##########    TWEET TIMELINE STREAM    ##########
    # tweet_analyze = TweetAnalyzer()
    
    # for client in clients:
    #     twitter_client = TwitterClient(client)
    #     tweets = twitter_client.get_user_timeline_tweets(500)
    #     tw = tweet_analyze.get_infos_tweets(fetched_tweets_filename, tweets)
        
        




