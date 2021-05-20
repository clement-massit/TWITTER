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

# Création d'une classe réservée à l'interaction avec le client Tiwtter

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
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)
        api = API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,compression=True)
        global i
        i += 1 
        try:
            
            tweet = json.loads(data) 
         
            if tweet["geo"] is not None:
                # print(tweet["geo"]["coordinates"][0],tweet["geo"]["coordinates"][1])
                print(get_geo_coord())
                
               

                
                # On écrit les tweets dans un fichiers texte en continu
                with open('C://wamp64//www//TWITTER//tweets json format//tweet_' + str(i) + '.json', 'a') as tf:
                    tf.write(data)
                    tf.write('\n')
                    tf.close()
            return True

        # Si ça ne marche pas, on retourne l'erreur
        except BaseException:
            print("Erreur dans on_data: %s" , BaseException)
        except KeyboardInterrupt:
            print("La recherce de Tweets via Streaming a été interrompue")
            
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

def json_modifier():
    '''
    this function will be used to open all the json files in 'tweets json format' and improves the format 
    in order to keep the main information in the same json file.
    for each 'file', we open it in order to get information then we use the 'get_infos_tweets()' function in order to 
    improve the format
    then we open the 'file' as writting method and replace the older information by the newest and then we will insert this into database
    '''
    tweet_analyze = TweetAnalyzer()
    path = "C://wamp64//www//TWITTER//tweets json format//"

    
    #list_json is the list of all json files there are in the 'tweets json format'   
    list_json = os.listdir(path)

    
    for file in list_json:
        
        try :
                
            with open(path + str(file), 'r') as json_file:
                
                data = json.load(json_file)
                
                formated_json = tweet_analyze.get_infos_tweets(data)
                
            with open(path + str(file), 'w') as f: 
                f.write(json.dumps(formated_json))
                print(" Le fichier " + file + "a bien été mis au bon format")

                
            
        except KeyError:
            print("Le fichier " + file + " est déjà au bon format")

    return True

def insert_infos_into_db():
    path = "C://wamp64//www//TWITTER//tweets json format//"
    #list_json is the list of all json files there are in the 'tweets json format'   
    list_json = os.listdir(path)    
    for file in list_json:
        with open(path + str(file), 'r') as json_file:
            tweet = json.load(json_file)
            
            # Requête SQL (a quoter si on veut pas insérer dans la base de données)    
            sql = "INSERT INTO tweets_streaming(`created_at`, `user_name`, `text_contenu`, `latitude`, `longitude`, `place`, `id_place`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            values = (tweet["dates"], tweet["user_name"], tweet["text"], tweet['latitude'], tweet['longitude'], tweet["place"]["name"],tweet["place"]["id"])
            curseur.execute(sql,values)

            # supprime les doublons
            request = "DELETE tweets_streaming FROM tweets_streaming LEFT OUTER JOIN (SELECT MIN(id) as id, text_contenu FROM tweets_streaming GROUP BY text_contenu) AS table_1 ON tweets_streaming.id = table_1.id WHERE table_1.id IS NULL"
            curseur.execute(request)
        conn.commit()
    return True

def get_geo_coord():
    ############################################################################
    # try to get the center of the cities
    ############################################################################
    auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)
    api = API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,compression=True)
   
    
    path = "C://wamp64//www//TWITTER//tweets json format//"
    #list_json is the list of all json files there are in the 'tweets json format'   
    list_json = os.listdir(path)    
    for file in list_json:
        print(file)
        with open(path + str(file), 'r') as json_file:
            data = json.load(json_file)
            print(data)
            place = api.reverse_geocode(data["latitude"],data["longitude"])[0]
        
            
# print(api.geo_id('Annecy'))
   
    

                
# print(get_geo_coord())

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







def Stream__via_hash_tag_method():
    ##########    TWEET STREAM FROM HASH TAG    ##########
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)



if __name__ == "__main__":
    '''
                PLAN
        1- Stream tweets
        2- mise en forme dans les fichiers json 
        3- insert dans la database
    '''
    Stream__via_hash_tag_method()
    # print(json_modifier())
    # print(insert_infos_into_db())
    



    


    ##########    TWEET TIMELINE STREAM    ##########
    # tweet_analyze = TweetAnalyzer()
    
    # for client in clients:
    #     twitter_client = TwitterClient(client)
    #     tweets = twitter_client.get_user_timeline_tweets(500)
    #     tw = tweet_analyze.get_infos_tweets(fetched_tweets_filename, tweets)
        
        




