from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
import nltk
import re
import mysql.connector 
from check_tweets_in_cities import get_tweets_in_city



conn = mysql.connector.connect(user = 'root', host = 'localhost', database = 'db_twitter', charset = 'utf8mb4')
curseur = conn.cursor()

sql = 'SELECT `text_contenu`FROM tweets_streaming'


curseur.execute(sql)
myresult = curseur.fetchall()



# tokenizer = nltk.RegexpTokenizer(r'\w+')


# dataFrame = tokenizer.tokenize(data)


stop_words = set(stopwords.words('french'))
stop_words.add('[')
stop_words.add('@')
stop_words.add(',')
stop_words.add('https')
stop_words.add(':')
stop_words.add('.')
stop_words.add('’')
stop_words.add('#')
stop_words.add('-')
stop_words.add('a')
stop_words.add('..')
stop_words.add('?')
stop_words.add('!')
stop_words.add('(')
stop_words.add(')')
stop_words.add(']')
stop_words.add(';')
stop_words.add('&')

filtre_stopfr =  lambda textes: [token for token in textes if token.lower() not in stop_words]



def list_word_most_common(city):
    liste_tweets = get_tweets_in_city(city)
    caractere = ""
    liste_common_words = []
    if len(liste_tweets) != 0:
        
        for tweets in liste_tweets:
            
            caractere += tweets[3][:-23]

        txt = filtre_stopfr(word_tokenize(caractere, language='french'))
        
        fd = nltk.FreqDist(txt) 
        most_common = fd.most_common()  
        
        for mot in most_common:
            liste_common_words.append(mot[0])
        if len(liste_common_words) < 10:
            return liste_common_words
        else:
            return liste_common_words[0:10]
        
    return liste_common_words   

# print(list_word_most_common('Paris'))