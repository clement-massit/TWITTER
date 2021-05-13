# Pour créer des data frames
import pandas as pd


# Pour manipuler les données + facilement 
import numpy as np
import mysql.connector as MySQLdb

from tweepy import API 
from tweepy import Cursor 

# StreamListener est une classe de Tweepy qui nous permet d'écouter les tweets
from tweepy.streaming import StreamListener

# Pour nous authentifier avec nos credentials, cette classe sert de lien entre l'app Twitter et nous
from tweepy import OAuthHandler

from tweepy import Stream

# On importe les credentials
import credentials



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
        try:
            print(data)
            # On écrit les tweets dans un fichiers texte en continu
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
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
                
                tw["id"] = tweet.id
                tw["dates"] =  str(tweet.created_at)
                tw['user_name'] = tweet.user.name               
                tw['text'] = tweet.text
                tw['latitude'] = tweet.geo['coordinates'][0]
                tw['longitude'] = tweet.geo['coordinates'][1]
                tw["place"] = tweet.place
                tw["id_place"] = tweet.place
                print(c, d , 'yes', tweet.geo)

        # with open(fetched_tweets_filename, 'w') as tf:
        #     json.dump(tw, tf)

                # Requête SQL (a quoter si on veut pas insérer dans la base de données)    
                #sql = "INSERT INTO tweets_streaming(`id_tweet`, `created_at`, `user_name`, `text_contenu`, `latitude`, `longitude`, `place`, `id_place`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
			    #values = (tweet.created_at, tweet.user.name, tweet.full_text, tweet.geo['coordinates'][0], tweet.geo['coordinates'][1], tweet.place.name,tweet.place.id)
        print('c = ', c, 'd = ', d)
        return tw
    


clients = ['googlemaps', 'weliketravel','elonmusk','sct_r']
hash_tag_list = ['annecy','Chambéry','Grenoble','Toulouse','google maps','Paris','Voiron','openstreetmap']

if __name__ == "__main__":
    

     
    fetched_tweets_filename = 'tweets.json'

    #     twitter_streamer = TwitterStreamer()
    #     twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    
    tweet_analyze = TweetAnalyzer()

    
    for client in clients:
        twitter_client = TwitterClient(client)
        tweets = twitter_client.get_user_timeline_tweets(4000)
        tw = tweet_analyze.get_infos_tweets(fetched_tweets_filename, tweets)
        
        





    # Print l'ensemble des données disponible pour 1 tweet, utile notamment pour savoir quelles informations on va pouvoir extraire
    # print(dir(tweets[0]))
    # On a donc accès à tout l'ensemble de données comme si on accédait aux éléments d'une liste
    # print(tweet[0].id) # Retourne l'id du premier tweet par exemple 


    # df = tweet_analyzer.tweets_to_data_frame(tweets)

    # #print(df.head(10))


    # hash_tag_list = ['annecy','paris']
    # fetched_tweets_filename = "tweets.json"

   




# # On définit un twitter client
#     twitter_client = TwitterClient('BillGates')
#     print(twitter_client.get_user_timeline_tweets(5))


# # On définit un objet Streamer
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)