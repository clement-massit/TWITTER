import json
import os

import tweepy
import credentials
import mysql.connector as MySQLdb

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(
    auth, 
    wait_on_rate_limit=True, 
    wait_on_rate_limit_notify=True, 
    compression=True)

conn = MySQLdb.connect(
    user = 'root', 
    host = 'localhost', 
    database = 'db_twitter', 
    charset = 'utf8mb4')
curseur = conn.cursor()

#########################################################

path = "C://wamp64//www//TWITTER//tweets json format//"

def get_polygon(path):
    #list_json is the list of all json files there are in the 'tweets json format'   
    list_json = os.listdir(path)
    
    for file in list_json:
        coor = {}
        with open(path + str(file), 'r') as json_file:  
            data = json.load(json_file)
            coor["coordinates"] = data["place"]["bounding_box"]["coordinates"]
            
        sql = "INSERT INTO polygon(`id_place`,`place`, `lat_1`, `long_1`, `lat_2`, `long_2`, `lat_3`, `long_3`, `lat_4`, `long_4`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data["id_place"],
            data["place"]["name"], 
            coor["coordinates"][0][0][1],
            coor["coordinates"][0][0][0],
            coor["coordinates"][0][1][1],
            coor["coordinates"][0][1][0],
            coor["coordinates"][0][2][1],
            coor["coordinates"][0][2][0],
            coor["coordinates"][0][3][1],
            coor["coordinates"][0][3][0])
        curseur.execute(sql,values)

        # supprime les doublons
        request = "DELETE polygon FROM polygon LEFT OUTER JOIN (SELECT MIN(id) as id, id_place FROM polygon GROUP BY id_place) AS table_1 ON polygon.id = table_1.id WHERE table_1.id IS NULL"
        curseur.execute(request)
        conn.commit()
    return True

print(get_polygon(path))



