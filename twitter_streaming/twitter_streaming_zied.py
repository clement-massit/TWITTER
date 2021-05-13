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




class TwitterAuthenticator():

    def authenticate_twitter_app(self):

        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)

        return auth



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



class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()


    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):

        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()

        stream = Stream(auth, listener)

        stream.filter(track = hash_tag_list)
        



class TwitterListener(StreamListener):
    '''
    Un listener classique que affiche les tweets reçus
    '''
    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename



    def on_data(self, data):
        try:

            return True

        except BaseException:
            print("Erreur dans on_data: %s" %str(BaseException))
        return True
    

    def on_error(self, status): 
        if status == 420:
            return False
        print(status)

tw = {}

class TweetAnalyzer():

    def get_infos_tweets(self, fetched_tweets_filename, tweets):
        for tweet in tweets :
            tw["id"] = tweet.id
            if tweet.coordinates:
                tw["coordinates"] = tweet.coordinates
            else:
                tw["coordinates"] = "None"
            tw["places"] = tweet.place
            tw["dates"] = tweet.created_at
            tw["author"] = tweet.author
            
            with open(fetched_tweets_filename, 'a') as tf:
                tf.write(tw)
        print('fin')

        return tw



clients = ['googlemaps', 'BillGates']
hash_tag_list = ['annecy','Chambéry','Grenoble','Toulouse','google maps','Paris','Voiron','openstreetmap']

if __name__ == "__main__":

    
    fetched_tweets_filename = "tweets.json"
    tweets = TwitterClient.get_user_timeline_tweets(fetched_tweets_filename, 5)


    tweet_analyze = TweetAnalyzer()
    tw = tweet_analyze.get_infos_tweets(fetched_tweets_filename)







    ###### CE QUI NOUS INTERESSE #####
    #geo,coordinates, place, id_place
    #id_tweet, created_at, user_name, text
    # for client in clients:

    #     twitter_client = TwitterClient(client)
        
    #     for tweet in twitter_client.get_user_timeline_tweets(60):
            
    #         print(tweet.geo,end="")





    # Print l'ensemble des données disponible pour 1 tweet, utile notamment pour savoir quelles informations on va pouvoir extraire
    # print(dir(tweets[0]))
    # On a donc accès à tout l'ensemble de données comme si on accédait aux éléments d'une liste
    # print(tweet[0].id) # Retourne l'id du premier tweet par exemple 


    # df = tweet_analyzer.tweets_to_data_frame(tweets)

    # #print(df.head(10))


    # hash_tag_list = ['annecy','paris']
    # fetched_tweets_filename = "tweets.json"

   




# # On définit un twitter client
#    twitter_client = TwitterClient('BillGates')
#    print(twitter_client.get_user_timeline_tweets(5))


# # On définit un objet Streamer
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)



 