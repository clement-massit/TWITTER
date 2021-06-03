from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
import nltk
import re
import mysql.connector 
from check_tweets_in_cities import check_tweets_in_city

data = """@@@@ [ https://Wikipédia est le le le un projet wiki d’encyclopédie 
collective en ligne, universelle, multilingue et fonctionnant sur le 
principe du wiki. Aimez-vous l'encyclopédie wikipedia ?"""

conn = mysql.connector.connect(user = 'root', host = 'localhost', database = 'db_twitter', charset = 'utf8mb4')
curseur = conn.cursor()

sql = 'SELECT `text_contenu`FROM tweets_streaming'


curseur.execute(sql)
myresult = curseur.fetchall()



tokenizer = nltk.RegexpTokenizer(r'\w+')


dataFrame = tokenizer.tokenize(data)


stop_words = set(stopwords.words('french'))
stop_words.add('[')
stop_words.add('@')
stop_words.add(',')
stop_words.add('https')
stop_words.add(':')
stop_words.add('.')
stop_words.add('’')
stop_words.add('#')
stop_words.add('in')
stop_words.add('a')
stop_words.add('..')
stop_words.add('?')
stop_words.add('the')

word_token = word_tokenize(data)
filtre_stopfr =  lambda textes: [token for token in textes if token.lower() not in stop_words]



def list_word_most_common(city):
    liste_tweets = check_tweets_in_city(city)
    caractere = ""
    liste_common_words = []
    for tweets in liste_tweets:
        caractere += tweets[3]

    txt = filtre_stopfr(word_tokenize(caractere, language='english'))
    
    fd = nltk.FreqDist(txt) 
    most_common = fd.most_common()  

    for i in range(0, 11):
        liste_common_words.append(most_common[i][0])
    
    return liste_common_words       
print(list_word_most_common('Paris'))    

# for text in myresult:
  

#     # print(filtre_stopfr(word_tokenize(text[0], language='french')))

#     txt = filtre_stopfr(word_tokenize(text[0], language='french'))

#     fd = nltk.FreqDist(txt) 
#     print(fd.most_common())
