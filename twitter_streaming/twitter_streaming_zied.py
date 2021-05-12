# StreamListener est une classe de Tweepy qui nous permet d'écouter les tweets
from tweepy.streaming import StreamListener

# Pour nous authentifier avec nos credentials, cette classe sert de lien entre l'app Twitter et nous
from tweepy import OAuthHandler

from tweepy import Stream

# On importe les credentials
from twitter_streaming import credentials 


# Création d'une classe qui hérite de StreamListener et va nous permettre d'afficher les tweets
class StdOutListener(StreamListener):

    def on_data(self, data):
        pass

    def on_error(self, status):
        pass




 